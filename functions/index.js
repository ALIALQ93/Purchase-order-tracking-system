const { onDocumentCreated } = require("firebase-functions/v2/firestore");
const { setGlobalOptions } = require("firebase-functions/v2");
const admin = require("firebase-admin");
const nodemailer = require("nodemailer");

setGlobalOptions({ region: "us-central1" });
admin.initializeApp();

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const APP_URL = "https://alialq93.github.io/Purchase-order-tracking-system/";

function normalizeEmail(value) {
  return String(value || "").trim().toLowerCase();
}

function isEmail(value) {
  return EMAIL_RE.test(value) && !/[\r\n]/.test(value);
}

function profileIsAdmin(data) {
  const sections = Array.isArray(data?.visibleSections) ? data.visibleSections : [];
  if (sections.map((x) => String(x || "").trim()).includes("admin")) return true;
  const roles = [data?.role, ...(Array.isArray(data?.roles) ? data.roles : [])].map((x) =>
    String(x || "").trim()
  );
  return roles.includes("admin");
}

function allowlistFromSettings(data) {
  const raw = Array.isArray(data?.passwordResetRecipients) ? data.passwordResetRecipients : [];
  const seen = new Set();
  const out = [];
  raw.forEach((item) => {
    const email = normalizeEmail(item);
    if (!isEmail(email) || seen.has(email)) return;
    seen.add(email);
    out.push(email);
  });
  return out;
}

function smtpConfig() {
  const host = String(process.env.SMTP_HOST || "").trim();
  const user = String(process.env.SMTP_USER || "").trim();
  const pass = String(process.env.SMTP_PASS || "");
  const from = String(process.env.SMTP_FROM || user).trim();
  const port = Number(process.env.SMTP_PORT || "587");
  return { host, user, pass, from, port };
}

async function markJob(ref, fields) {
  await ref.update({
    ...fields,
    finishedAt: admin.firestore.FieldValue.serverTimestamp(),
  });
}

exports.onPasswordResetJob = onDocumentCreated("passwordResetJobs/{jobId}", async (event) => {
  const snap = event.data;
  if (!snap) return;
  const jobRef = snap.ref;
  const job = snap.data() || {};
  if (job.status && job.status !== "pending") return;

  const callerUid = String(event.authId || "").trim();
  const targetUid = String(job.targetUid || "").trim();
  const recipientEmail = normalizeEmail(job.recipientEmail);

  const fail = (errorCode) => markJob(jobRef, { status: "error", errorCode });

  if (!callerUid) return fail("not-signed-in");
  if (!/^[A-Za-z0-9_-]{6,128}$/.test(targetUid)) return fail("bad-target");
  if (!isEmail(recipientEmail)) return fail("bad-recipient");

  const db = admin.firestore();
  const callerSnap = await db.doc(`userProfiles/${callerUid}`).get();
  if (!callerSnap.exists || !profileIsAdmin(callerSnap.data())) return fail("not-admin");

  const settingsSnap = await db.doc("appConfig/generalSettings").get();
  const allowlist = allowlistFromSettings(settingsSnap.exists ? settingsSnap.data() : {});
  if (!allowlist.includes(recipientEmail)) return fail("recipient-not-allowed");

  let target;
  try {
    target = await admin.auth().getUser(targetUid);
  } catch (err) {
    if (err?.code === "auth/user-not-found") return fail("user-not-found");
    console.error("getUser failed", err?.code || err?.message || err);
    return fail("user-lookup-failed");
  }
  const targetEmail = normalizeEmail(target.email);
  if (!isEmail(targetEmail)) return fail("user-has-no-email");

  const profileSnap = await db.doc(`userProfiles/${targetUid}`).get();
  const displayName = String(profileSnap.exists ? profileSnap.data()?.displayName || "" : "").trim();

  let link;
  try {
    link = await admin.auth().generatePasswordResetLink(target.email, {
      url: APP_URL,
      handleCodeInApp: false,
    });
  } catch (err) {
    console.error("generatePasswordResetLink failed", err?.code || err?.message || err);
    return fail("link-failed");
  }

  const mail = smtpConfig();
  if (!mail.host || !mail.user || !mail.pass || !mail.from || !Number.isFinite(mail.port)) {
    return fail("smtp-not-configured");
  }

  const subject = "رابط تغيير كلمة المرور — نظام تتبع أوامر الشراء";
  const text = [
    "طلب المشرف رابط تغيير كلمة المرور للحساب التالي:",
    "",
    `الاسم: ${displayName || "—"}`,
    `بريد الدخول: ${target.email}`,
    "",
    "افتح الرابط، عيّن كلمة المرور الجديدة، ثم بلّغ المستخدم بها.",
    "الرابط صالح لمدة محدودة ويعمل مرة واحدة.",
    "",
    link,
  ].join("\n");

  try {
    const transporter = nodemailer.createTransport({
      host: mail.host,
      port: mail.port,
      secure: mail.port === 465,
      auth: { user: mail.user, pass: mail.pass },
    });
    await transporter.sendMail({
      from: mail.from,
      to: recipientEmail,
      subject,
      text,
    });
  } catch (err) {
    console.error("password reset mail failed", err?.message || err);
    return fail("email-send-failed");
  }

  await db.collection("passwordResetRequests").add({
    requestedBy: callerUid,
    targetUid,
    targetEmail,
    targetName: displayName || null,
    recipientEmail,
    createdAt: admin.firestore.FieldValue.serverTimestamp(),
  });
  await markJob(jobRef, { status: "sent", errorCode: null });
});

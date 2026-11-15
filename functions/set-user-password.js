const fs = require("fs");
const path = require("path");
const readline = require("readline");
const admin = require("firebase-admin");

const keyPath = path.join(__dirname, "service-account.json");
const login = String(process.argv[2] || "").trim();

if (!fs.existsSync(keyPath)) {
  console.error("ضع ملف مفتاح الخدمة هنا أولاً:");
  console.error(keyPath);
  console.error("من Firebase Console: Project settings → Service accounts → Generate new private key");
  process.exit(1);
}
if (!login) {
  console.error('الاستخدام: node set-user-password.js "user@email"');
  process.exit(1);
}

admin.initializeApp({
  credential: admin.credential.cert(JSON.parse(fs.readFileSync(keyPath, "utf8"))),
});

function ask(question) {
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
  return new Promise((resolve) => {
    rl.question(question, (answer) => {
      rl.close();
      resolve(String(answer || ""));
    });
  });
}

async function main() {
  const user = login.includes("@")
    ? await admin.auth().getUserByEmail(login)
    : await admin.auth().getUser(login);
  const password = await ask("كلمة المرور الجديدة (6 أحرف على الأقل): ");
  const confirm = await ask("تأكيد كلمة المرور: ");
  if (password.length < 6) {
    console.error("كلمة المرور أقصر من 6 أحرف.");
    process.exit(1);
  }
  if (password !== confirm) {
    console.error("التأكيد لا يطابق كلمة المرور.");
    process.exit(1);
  }
  await admin.auth().updateUser(user.uid, { password });
  console.log("تم تغيير كلمة المرور.");
  console.log("الحساب:", user.email || user.uid);
}

main()
  .then(() => process.exit(0))
  .catch((err) => {
    const code = err?.code || "";
    if (code === "auth/user-not-found") console.error("الحساب غير موجود في Firebase Authentication.");
    else console.error(err?.message || err);
    process.exit(1);
  });

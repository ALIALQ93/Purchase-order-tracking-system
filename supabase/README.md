# إيصالات مصروفات المندوب (معزول عن الأرشيف)

## الإعداد مرة واحدة

1. في مشروع Supabase (نفس مشروع الأرشيف أو مشروع مستقل):
   - افتح **SQL Editor**
   - نفّذ ملف `po_expense_receipts.sql`
2. من Firebase التطبيق → **الإدارة → إعدادات النظام**:
   - الصق **Project URL**
   - الصق **anon public key** (Settings → API)
   - احفظ

## ماذا يُنشأ؟

| العنصر | الاسم |
|--------|--------|
| Bucket | `po-receipts` |
| جدول | `public.po_expense_receipts` |

لا يمسّ `archive_cards` ولا `card_attachments`.

## ملاحظة أمان

الرفع يتم من واجهة Firebase بعد تسجيل الدخول. سياسات Supabase لـ `po-receipts` مفتوحة لـ `anon` ضمن هذا الـ bucket/الجدول فقط — وليست لجداول الأرشيف.

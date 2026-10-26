-- =========================================================
-- إيصالات مصروفات المندوبين — معزول عن أرشيف الشركة
-- نفّذ في: Supabase → SQL Editor
-- =========================================================

-- 1) Bucket للملفات (عام للقراءة بروابط UUID؛ الرفع عبر anon محدود بالحجم/النوع)
INSERT INTO storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
VALUES (
  'po-receipts',
  'po-receipts',
  true,
  2097152, -- 2 MB
  ARRAY['image/jpeg', 'image/png', 'image/webp']::text[]
)
ON CONFLICT (id) DO UPDATE
SET
  public = EXCLUDED.public,
  file_size_limit = EXCLUDED.file_size_limit,
  allowed_mime_types = EXCLUDED.allowed_mime_types;

-- 2) جدول بيانات المرفق (منفصل عن archive_cards / card_attachments)
CREATE TABLE IF NOT EXISTS public.po_expense_receipts (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  expense_id text NOT NULL,
  storage_path text NOT NULL,
  file_name text,
  content_type text,
  size_bytes bigint,
  uploaded_by_uid text,
  uploaded_by_email text,
  created_at timestamptz NOT NULL DEFAULT now(),
  CONSTRAINT po_expense_receipts_storage_path_key UNIQUE (storage_path)
);

CREATE INDEX IF NOT EXISTS idx_po_expense_receipts_expense_id
  ON public.po_expense_receipts (expense_id);

CREATE INDEX IF NOT EXISTS idx_po_expense_receipts_created_at
  ON public.po_expense_receipts (created_at DESC);

COMMENT ON TABLE public.po_expense_receipts IS
  'إيصالات مصروف نظام تتبع أوامر الشراء — معزول عن أرشيف الشركة';

-- 3) RLS على الجدول
-- ملاحظة: المصادقة الأساسية من Firebase؛ الواجهة لا ترفع إلا لمستخدم مسجّل.
-- anon مسموح لهذا الجدول/الـ bucket فقط (ليست لجداول الأرشيف).
ALTER TABLE public.po_expense_receipts ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS po_expense_receipts_select ON public.po_expense_receipts;
DROP POLICY IF EXISTS po_expense_receipts_insert ON public.po_expense_receipts;
DROP POLICY IF EXISTS po_expense_receipts_update ON public.po_expense_receipts;
DROP POLICY IF EXISTS po_expense_receipts_delete ON public.po_expense_receipts;

CREATE POLICY po_expense_receipts_select
  ON public.po_expense_receipts FOR SELECT
  TO anon, authenticated
  USING (true);

CREATE POLICY po_expense_receipts_insert
  ON public.po_expense_receipts FOR INSERT
  TO anon, authenticated
  WITH CHECK (true);

CREATE POLICY po_expense_receipts_update
  ON public.po_expense_receipts FOR UPDATE
  TO anon, authenticated
  USING (true)
  WITH CHECK (true);

CREATE POLICY po_expense_receipts_delete
  ON public.po_expense_receipts FOR DELETE
  TO anon, authenticated
  USING (true);

-- 4) سياسات Storage لـ bucket po-receipts فقط
DROP POLICY IF EXISTS po_receipts_storage_select ON storage.objects;
DROP POLICY IF EXISTS po_receipts_storage_insert ON storage.objects;
DROP POLICY IF EXISTS po_receipts_storage_update ON storage.objects;
DROP POLICY IF EXISTS po_receipts_storage_delete ON storage.objects;

CREATE POLICY po_receipts_storage_select
  ON storage.objects FOR SELECT
  TO anon, authenticated
  USING (bucket_id = 'po-receipts');

CREATE POLICY po_receipts_storage_insert
  ON storage.objects FOR INSERT
  TO anon, authenticated
  WITH CHECK (
    bucket_id = 'po-receipts'
    AND (storage.foldername(name))[1] IS NOT NULL
    AND coalesce(octet_length(name), 0) < 500
  );

CREATE POLICY po_receipts_storage_update
  ON storage.objects FOR UPDATE
  TO anon, authenticated
  USING (bucket_id = 'po-receipts')
  WITH CHECK (bucket_id = 'po-receipts');

CREATE POLICY po_receipts_storage_delete
  ON storage.objects FOR DELETE
  TO anon, authenticated
  USING (bucket_id = 'po-receipts');

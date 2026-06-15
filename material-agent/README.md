# Material linking agent (Phase A)

Clusters similar material names from purchase-order line exports and compares unit prices per group.

## Run with Docker

```bash
cd material-agent
docker compose up --build
```

Service: `http://localhost:8080`

Health check: `GET /api/v1/health`

## API

### Analyze JSON lines (from the app report)

`POST /api/v1/analyze/lines`

```json
{
  "similarity_threshold": 85,
  "lines": [
    {
      "item": "اسمنت",
      "unit": "BAG",
      "qty": 100,
      "price": 8500,
      "currency": "IQD",
      "ref": "PO-001",
      "project": "Project A",
      "requestDate": "2025-03-01"
    }
  ]
}
```

### Analyze uploaded CSV

`POST /api/v1/analyze/csv?similarity_threshold=85`

Form field: `file` — export from **تقرير المواد** or **تصدير بنود CSV**.

## Deploy for GitHub Pages (HTTPS) — Render (free)

Use when the app runs at `https://alialq93.github.io/Purchase-order-tracking-system/`.

**Blueprint requires a paid Render plan.** Use **Web Service** instead (free tier):

1. [Render](https://render.com) → sign in with GitHub.
2. **New +** → **Web Service** (not Blueprint).
3. Connect repo `alialq93/Purchase-order-tracking-system`.
4. Settings:
   - **Name:** `po-material-agent`
   - **Branch:** `main`
   - **Root Directory:** `material-agent`
   - **Runtime:** **Docker**
   - **Instance Type:** **Free**
5. **Create Web Service** → wait until **Live**.
6. Copy URL, e.g. `https://po-material-agent.onrender.com`.
7. Test: `https://YOUR-URL.onrender.com/api/v1/health`
8. In the app → **التقارير** → **ربط المواد المتشابهة** → paste HTTPS URL.
9. Run **تقرير المواد وأسعارها** → **تحليل البنود الحالية**.

**Note:** Free services sleep after ~15 min idle; first request may take ~30s.

## App integration

1. Open **التقارير** → run **تقرير المواد وأسعارها** (or purchasing report + line export).
2. In **ربط المواد المتشابهة**, set agent URL (`https://…onrender.com` for Pages, or `http://localhost:8080` locally).
3. Review unified material groups and price spread.

Optional: upload the exported CSV instead via curl:

```bash
curl -F "file=@purchasing_lines_2025-01-01_2025-06-01.csv" "http://localhost:8080/api/v1/analyze/csv"
```

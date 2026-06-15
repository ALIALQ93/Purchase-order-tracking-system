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

## Deploy for GitHub Pages (HTTPS) — Render

Use this when the app runs at `https://alialq93.github.io/Purchase-order-tracking-system/`.

1. Push this repo to GitHub (must include `material-agent/` and updated `index.html`).
2. Sign in at [Render](https://render.com) → **New** → **Blueprint**.
3. Connect repo `alialq93/Purchase-order-tracking-system` → apply `render.yaml`.
4. Wait for deploy; copy the service URL, e.g. `https://po-material-agent.onrender.com`.
5. Open the app → **التقارير** → **ربط المواد المتشابهة** → paste that URL (HTTPS, no trailing slash).
6. Run **تقرير المواد وأسعارها**, then **تحليل البنود الحالية**.

Health check: `https://YOUR-SERVICE.onrender.com/api/v1/health`

**Note:** Free Render services sleep after ~15 min idle; first request may take ~30s to wake.

## App integration

1. Open **التقارير** → run **تقرير المواد وأسعارها** (or purchasing report + line export).
2. In **ربط المواد المتشابهة**, set agent URL (`https://…onrender.com` for Pages, or `http://localhost:8080` locally).
3. Review unified material groups and price spread.

Optional: upload the exported CSV instead via curl:

```bash
curl -F "file=@purchasing_lines_2025-01-01_2025-06-01.csv" "http://localhost:8080/api/v1/analyze/csv"
```

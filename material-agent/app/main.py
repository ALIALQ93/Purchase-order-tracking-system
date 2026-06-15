"""Material linking agent — FastAPI service for Phase A report analysis."""

from __future__ import annotations

import os
from typing import Any

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from .cluster import LineIn, cluster_material_lines, clusters_to_report
from .csv_parser import parse_csv_text

DEFAULT_THRESHOLD = int(os.getenv("SIMILARITY_THRESHOLD", "85"))

app = FastAPI(
    title="PO Material Linking Agent",
    description="Clusters similar material names from purchase order line exports.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnalyzeLinesRequest(BaseModel):
    lines: list[dict[str, Any]] = Field(default_factory=list)
    similarity_threshold: int = Field(default=DEFAULT_THRESHOLD, ge=50, le=100)


def _analyze(lines: list[LineIn], threshold: int) -> dict[str, Any]:
    parsed = [ln for ln in lines if ln.item.strip()]
    if not parsed:
        raise HTTPException(status_code=400, detail="No line items with material names found.")
    clusters = cluster_material_lines(parsed, similarity_threshold=threshold)
    return clusters_to_report(
        clusters,
        similarity_threshold=threshold,
        input_line_count=len(lines),
    )


@app.get("/health")
@app.get("/api/v1/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "material-agent"}


@app.post("/api/v1/analyze/lines")
def analyze_lines(body: AnalyzeLinesRequest) -> dict[str, Any]:
    lines = [LineIn.from_dict(row) for row in body.lines]
    return _analyze(lines, body.similarity_threshold)


@app.post("/api/v1/analyze/csv")
async def analyze_csv(
    file: UploadFile = File(...),
    similarity_threshold: int = DEFAULT_THRESHOLD,
) -> dict[str, Any]:
    raw = await file.read()
    for encoding in ("utf-8-sig", "utf-8", "cp1256", "latin-1"):
        try:
            text = raw.decode(encoding)
            break
        except UnicodeDecodeError:
            text = None
    if text is None:
        raise HTTPException(status_code=400, detail="Could not decode CSV file.")

    lines = parse_csv_text(text)
    if not lines:
        raise HTTPException(status_code=400, detail="No material rows found in CSV.")
    return _analyze(lines, max(50, min(100, similarity_threshold)))

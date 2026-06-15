"""Parse CSV exports from the purchase-order tracking app."""

from __future__ import annotations

import csv
import io
from typing import Any

from .cluster import LineIn

_ITEM_KEYS = {"item", "material", "description", "poLineDescCol", "po line desc", "المادة", "الوصف", "بند"}
_UNIT_KEYS = {"unit", "poLineUnitCol", "po line unit", "الوحدة"}
_QTY_KEYS = {"qty", "quantity", "poLineQtyCol", "po line qty", "الكمية"}
_PRICE_KEYS = {"price", "accUnitPriceCol", "unit price", "سعر الوحدة", "السعر"}
_CURRENCY_KEYS = {"currency", "reportBaseCurrencyLabel", "العملة"}
_REF_KEYS = {"ref", "poreference", "colPoReference", "المرجع", "مرجع"}
_PROJECT_KEYS = {"project", "colProject", "المشروع"}
_DATE_KEYS = {"requestdate", "colRequestDate", "تاريخ الطلب", "تاريخ"}
_COMPANY_KEYS = {"company", "reportCompanyLabel", "الشركة"}
_LINE_NO_KEYS = {"lineno", "line#", "line no", "رقم البند"}


def _norm_header(h: str) -> str:
    return "".join(ch for ch in h.strip().lower() if ch.isalnum() or ch.isspace()).strip()


def _map_headers(row: list[str]) -> dict[str, int]:
    mapping: dict[str, int] = {}
    for i, raw in enumerate(row):
        key = _norm_header(raw)
        if not key:
            continue
        compact = key.replace(" ", "")
        checks = [
            (_ITEM_KEYS, "item"),
            (_UNIT_KEYS, "unit"),
            (_QTY_KEYS, "qty"),
            (_PRICE_KEYS, "price"),
            (_CURRENCY_KEYS, "currency"),
            (_REF_KEYS, "ref"),
            (_PROJECT_KEYS, "project"),
            (_DATE_KEYS, "request_date"),
            (_COMPANY_KEYS, "company"),
            (_LINE_NO_KEYS, "line_no"),
        ]
        for keys, field in checks:
            if key in keys or compact in keys:
                mapping.setdefault(field, i)
    return mapping


def _cell(row: list[str], idx: int | None) -> str:
    if idx is None or idx >= len(row):
        return ""
    return (row[idx] or "").strip()


def parse_csv_text(text: str) -> list[LineIn]:
    # Strip UTF-8 BOM
    if text.startswith("\ufeff"):
        text = text[1:]

    reader = csv.reader(io.StringIO(text))
    rows = list(reader)
    if not rows:
        return []

    header = rows[0]
    col = _map_headers(header)

    # Fallback: materials/lines export column positions when headers are localized
    # ref, date, company, project, region, workflow, rep, [requestType], lineNo, item, unit, qty, ...
    if "item" not in col:
        if len(header) >= 14:
            col.setdefault("ref", 0)
            col.setdefault("request_date", 1)
            col.setdefault("company", 2)
            col.setdefault("project", 3)
            col.setdefault("line_no", 7 if len(header) >= 15 else 6)
            col.setdefault("item", 8 if len(header) >= 15 else 7)
            col.setdefault("unit", 9 if len(header) >= 15 else 8)
            col.setdefault("qty", 10 if len(header) >= 15 else 9)
            col.setdefault("price", 11 if len(header) >= 15 else 10)
            col.setdefault("currency", 12 if len(header) >= 15 else 11)
        elif len(header) >= 10:
            col.setdefault("item", 7)
            col.setdefault("unit", 8)
            col.setdefault("qty", 9)

    lines: list[LineIn] = []
    for row in rows[1:]:
        if not row or not any(cell.strip() for cell in row):
            continue
        item = _cell(row, col.get("item"))
        if not item:
            continue
        qty_raw = _cell(row, col.get("qty"))
        price_raw = _cell(row, col.get("price"))
        line_no_raw = _cell(row, col.get("line_no"))
        lines.append(
            LineIn(
                item=item,
                unit=_cell(row, col.get("unit")),
                qty=float(qty_raw.replace(",", "")) if qty_raw else 0.0,
                price=float(price_raw.replace(",", "")) if price_raw else 0.0,
                currency=_cell(row, col.get("currency")) or "IQD",
                ref=_cell(row, col.get("ref")),
                project=_cell(row, col.get("project")),
                request_date=_cell(row, col.get("request_date")),
                company=_cell(row, col.get("company")),
                line_no=int(line_no_raw) if line_no_raw.isdigit() else None,
            )
        )
    return lines


def lines_to_dicts(lines: list[LineIn]) -> list[dict[str, Any]]:
    return [
        {
            "item": ln.item,
            "unit": ln.unit,
            "qty": ln.qty,
            "price": ln.price,
            "currency": ln.currency,
            "ref": ln.ref,
            "project": ln.project,
            "requestDate": ln.request_date,
            "company": ln.company,
            "lineNo": ln.line_no,
        }
        for ln in lines
    ]

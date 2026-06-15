"""Cluster similar material line items and compute per-unit price stats."""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass, field
from typing import Any

from rapidfuzz import fuzz

from .normalize import normalize_material_text, normalize_unit


@dataclass
class LineIn:
    item: str
    unit: str = ""
    qty: float = 0.0
    price: float = 0.0
    currency: str = "IQD"
    ref: str = ""
    project: str = ""
    request_date: str = ""
    company: str = ""
    line_no: int | None = None

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> LineIn:
        return cls(
            item=str(d.get("item") or "").strip(),
            unit=str(d.get("unit") or "").strip(),
            qty=float(d.get("qty") or 0),
            price=float(d.get("price") or 0),
            currency=(str(d.get("currency") or "IQD").strip() or "IQD").upper(),
            ref=str(d.get("ref") or "").strip(),
            project=str(d.get("project") or "").strip(),
            request_date=str(d.get("requestDate") or d.get("request_date") or "").strip(),
            company=str(d.get("company") or "").strip(),
            line_no=int(d["lineNo"]) if d.get("lineNo") not in (None, "") else None,
        )


@dataclass
class Cluster:
    cluster_id: str
    canonical_name: str
    normalized_key: str
    aliases: Counter[str] = field(default_factory=Counter)
    lines: list[LineIn] = field(default_factory=list)

    def similarity_to(self, norm_text: str) -> int:
        if not self.normalized_key or not norm_text:
            return 0
        if self.normalized_key == norm_text:
            return 100
        return int(
            fuzz.token_set_ratio(self.normalized_key, norm_text)
        )


def _pick_canonical_name(alias_counter: Counter[str]) -> str:
    if not alias_counter:
        return ""
    return alias_counter.most_common(1)[0][0]


def cluster_material_lines(
    lines: list[LineIn],
    *,
    similarity_threshold: int = 85,
) -> list[Cluster]:
    usable = [ln for ln in lines if ln.item.strip()]
    if not usable:
        return []

    threshold = max(50, min(100, int(similarity_threshold)))
    clusters: list[Cluster] = []

    for ln in usable:
        norm_item = normalize_material_text(ln.item)
        if not norm_item:
            continue

        best: Cluster | None = None
        best_score = -1
        for cl in clusters:
            score = cl.similarity_to(norm_item)
            if score >= threshold and score > best_score:
                best = cl
                best_score = score

        if best is None:
            cid = f"c{len(clusters) + 1}"
            best = Cluster(
                cluster_id=cid,
                canonical_name=ln.item.strip(),
                normalized_key=norm_item,
            )
            clusters.append(best)

        best.lines.append(ln)
        best.aliases[ln.item.strip()] += 1
        best.canonical_name = _pick_canonical_name(best.aliases)

    clusters.sort(
        key=lambda c: (-len(c.lines), c.canonical_name.lower()),
    )
    return clusters


def _price_stats(prices: list[float]) -> dict[str, float | int | None]:
    if not prices:
        return {
            "priced_line_count": 0,
            "min_price": None,
            "max_price": None,
            "avg_price": None,
            "price_spread_pct": None,
        }
    mn = min(prices)
    mx = max(prices)
    avg = sum(prices) / len(prices)
    spread = None
    if mn > 0 and mx > mn:
        spread = round(((mx - mn) / mn) * 100, 1)
    return {
        "priced_line_count": len(prices),
        "min_price": round(mn, 4),
        "max_price": round(mx, 4),
        "avg_price": round(avg, 4),
        "price_spread_pct": spread,
    }


def clusters_to_report(
    clusters: list[Cluster],
    *,
    similarity_threshold: int,
    input_line_count: int,
) -> dict[str, Any]:
    raw_items = set()
    for cl in clusters:
        for ln in cl.lines:
            if ln.item.strip():
                raw_items.add(ln.item.strip().lower())

    out_clusters: list[dict[str, Any]] = []
    for cl in clusters:
        unit_groups: dict[str, list[LineIn]] = defaultdict(list)
        for ln in cl.lines:
            unit_groups[normalize_unit(ln.unit)].append(ln)

        units_out: list[dict[str, Any]] = []
        for unit_key, unit_lines in sorted(
            unit_groups.items(),
            key=lambda kv: (-len(kv[1]), kv[0]),
        ):
            by_currency: dict[str, list[float]] = defaultdict(list)
            for ln in unit_lines:
                if ln.price > 0:
                    by_currency[ln.currency].append(ln.price)

            currency_stats = []
            for cur, prices in sorted(by_currency.items()):
                currency_stats.append({"currency": cur, **_price_stats(prices)})

            units_out.append(
                {
                    "unit": unit_key,
                    "display_unit": unit_lines[0].unit or unit_key,
                    "line_count": len(unit_lines),
                    "currency_stats": currency_stats,
                }
            )

        alias_list = [
            {"text": text, "count": count}
            for text, count in cl.aliases.most_common()
        ]

        sample = []
        for ln in cl.lines[:8]:
            sample.append(
                {
                    "item": ln.item,
                    "unit": ln.unit,
                    "qty": ln.qty,
                    "price": ln.price,
                    "currency": ln.currency,
                    "ref": ln.ref,
                    "project": ln.project,
                    "requestDate": ln.request_date,
                }
            )

        out_clusters.append(
            {
                "id": cl.cluster_id,
                "canonical_name": cl.canonical_name,
                "normalized_name": cl.normalized_key,
                "line_count": len(cl.lines),
                "alias_count": len(cl.aliases),
                "aliases": alias_list,
                "units": units_out,
                "sample_lines": sample,
            }
        )

    return {
        "summary": {
            "input_lines": input_line_count,
            "lines_with_item": sum(len(c.lines) for c in clusters),
            "unique_raw_items": len(raw_items),
            "clusters": len(clusters),
            "similarity_threshold": similarity_threshold,
        },
        "clusters": out_clusters,
    }

"""地图工具骨架。

设计原则（详见根 README 第 11/12 章）：
- 每个工具一个纯函数，输入输出严格 dict / pydantic。
- 把 *写操作* 与 *读操作* 分两组，写操作必须 HITL。
- 接真实 API 时只改本文件 + 加 .env 配置。
"""
from __future__ import annotations

import math
import os
from dataclasses import dataclass
from typing import Any

import httpx

AMAP_KEY = os.getenv("AMAP_KEY")  # 高德 API key，可选


# =============== 通用 ===============

def haversine_m(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    R = 6371000
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lng2 - lng1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


# =============== 读 操作 ===============

def geocode(address: str) -> dict[str, Any]:
    """地址 → (lat, lng)。优先调高德，无 key 时用 mock。"""
    if AMAP_KEY:
        r = httpx.get(
            "https://restapi.amap.com/v3/geocode/geo",
            params={"address": address, "key": AMAP_KEY},
            timeout=5,
        ).json()
        if r.get("geocodes"):
            lng, lat = map(float, r["geocodes"][0]["location"].split(","))
            return {"address": address, "lat": lat, "lng": lng, "source": "amap"}
        return {"error": "no result", "raw": r}
    mock = {
        "中关村": (39.9805, 116.3163),
        "望京": (40.0035, 116.4709),
        "三里屯": (39.9367, 116.4570),
        "故宫": (39.9163, 116.3972),
    }
    for k, (lat, lng) in mock.items():
        if k in address:
            return {"address": address, "lat": lat, "lng": lng, "source": "mock"}
    return {"error": f"无匹配: {address}"}


def poi_search(keyword: str, near: dict, radius_m: int = 2000) -> dict[str, Any]:
    if AMAP_KEY:
        r = httpx.get(
            "https://restapi.amap.com/v3/place/around",
            params={
                "keywords": keyword,
                "location": f"{near['lng']},{near['lat']}",
                "radius": radius_m,
                "key": AMAP_KEY,
            },
            timeout=5,
        ).json()
        pois = []
        for p in r.get("pois", [])[:10]:
            lng, lat = map(float, p["location"].split(","))
            pois.append({
                "name": p.get("name"),
                "address": p.get("address"),
                "lat": lat, "lng": lng,
                "distance_m": int(p.get("distance", 0)),
            })
        return {"count": len(pois), "pois": pois, "source": "amap"}
    return {"count": 0, "pois": [], "source": "mock", "note": "set AMAP_KEY for real data"}


def route(origin: dict, destination: dict, mode: str = "walking") -> dict[str, Any]:
    d_m = haversine_m(origin["lat"], origin["lng"], destination["lat"], destination["lng"])
    speed = {"walking": 1.3, "cycling": 4.0, "driving": 8.0}.get(mode, 1.3)
    return {
        "mode": mode,
        "distance_m": round(d_m),
        "duration_min": round(d_m / speed / 60, 1),
        "origin": origin, "destination": destination,
    }


def explain_route(route: dict) -> dict[str, Any]:
    mode_cn = {"walking": "步行", "cycling": "骑行", "driving": "驾车"}.get(route["mode"], route["mode"])
    return {"text": f"{mode_cn}约 {route['distance_m']} 米，预计 {route['duration_min']} 分钟。"}


# =============== 写 操作（必须 HITL） ===============

@dataclass
class WriteIntent:
    """所有写操作只返回 *意图*，不直接执行。由上层 HITL 节点决定是否 commit。"""

    op: str
    payload: dict[str, Any]
    risk_level: str = "high"


def report_traffic(road_name: str, condition: str) -> WriteIntent:
    """上报路况——典型写操作，必须 HITL 才真正提交。"""
    return WriteIntent(op="report_traffic", payload={"road": road_name, "condition": condition})


READ_TOOLS = {"geocode": geocode, "poi_search": poi_search, "route": route, "explain_route": explain_route}
WRITE_TOOLS = {"report_traffic": report_traffic}

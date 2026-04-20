# 第 11 章 · 参考资料

## 论文

- **MapAgent**, *MapAgent: Hierarchical Agent for Geospatial Reasoning with Map APIs*, 2025.
- **PReP**, *Perceive, Reflect, Plan: Designing LLM Agents for Goal-directed City Navigation*, 2024.
- **VoP**, *Verbalized Path: Language Anchors for Multimodal Spatial Memory*, 2024.
- Gurnee, Tegmark, *Language Models Represent Space and Time*, ICLR 2024.
- Yamada et al., *Evaluating Spatial Understanding of Large Language Models*, TMLR 2024.
- **DriveLM**, Sima et al., *DriveLM: Driving with Graph Visual Question Answering*, ECCV 2024.
- **Agent-Driver**, Mao et al., *A Language Agent for Autonomous Driving*, COLM 2024.
- **DriveGPT4**, Xu et al., *Interpretable End-to-end Autonomous Driving via LLM*, RA-L 2024.
- **GeoLLM-Engine**, *A realistic environment for building agents that work with geo-data*, 2024.

## 数据集 / 仿真器

- nuScenes / Waymo Open Dataset / DriveLM-nuScenes.
- Touchdown / R2R / VLN-CE（视觉语言导航）。
- StreetView API / Mapillary 公开街景。
- OpenStreetMap + osmnx（Python）。

## 工程与 SDK

- 高德开放平台 <https://lbs.amap.com/>（geocode / 路径 / POI / 实时交通）。
- 百度地图开放平台 <https://lbsyun.baidu.com/>。
- Google Maps Platform <https://mapsplatform.google.com/>。
- `osmnx` 路网获取 + 网络分析。
- `folium` 地图可视化。
- `shapely` / `geopandas` 几何计算。

## 业界 talk / 博客

- OpenDriveLab DriveLM 项目页与解读视频。
- 高德 / 百度 / 美团 *LLM + 地图* 技术分享（搜「2024 高德 大模型」「美团 大模型 商家」等）。
- HuggingFace Spatial AI 系列 blog。

## 与本仓库的关联

- 第 03 章 MCP：把工具集合包装成 MCP server。
- 第 09 章：用 verifiable reward 对垂直 agent 做 GRPO。
- 第 12 章：地图操作的 HITL / 审核 / 安全。
- 第 99 章：Capstone 项目 A 的输入。

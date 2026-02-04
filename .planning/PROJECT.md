# MNIST 數字辨識 API

## What This Is

將現有的 CNN-Transformer MNIST 數字辨識模型（來自 `inference.ipynb`）包裝成 FastAPI 服務，支援圖片上傳推論、多執行緒並行處理，並完成 Docker 容器化部署。最終推送至公開 GitHub repo。

## Core Value

使用者可以透過 `/predict` API 上傳任意尺寸圖片，獲得 0-9 數字預測結果與信心分數。

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] FastAPI 包裝 `/predict` API（上傳圖片，回傳預測數字與信心分數）
- [ ] `/health` 健康檢查端點
- [ ] 多執行緒並行推論支援（Uvicorn --workers 4）
- [ ] Dockerfile 容器化部署
- [ ] `batch_predict.py` 批次推論腳本（讀取 test/ 資料夾，輸出 result.csv）
- [ ] README.md API 使用說明文件
- [ ] 推上 GitHub 公開 repo

### Out of Scope

- GPU 推論 — 使用 CPU 簡化部署，題目未要求
- API 認證 — 題目未要求
- 資料庫持久化 — 純推論服務，無需儲存
- OAuth/進階身份驗證 — 簡化架構
- 前端介面 — 僅提供 API 端點

## Context

### 現有模型架構：CNNTransformer

```
輸入: [batch, 1, 28, 28] 灰階圖片
├── Conv2d(1→32) + ReLU
├── Conv2d(32→64) + ReLU
├── MaxPool2d(2,2) → [batch, 64, 14, 14]
├── Reshape + Linear(196→128)
├── TransformerEncoder(d_model=128, nhead=8, layers=2)
└── FC(8192→10) → 10 個類別 (數字 0-9)
```

### 推論輸入需求
- 格式：任意尺寸圖片（resize 為 28×28）
- 色彩：自動轉換為灰階
- 預處理：ToTensor() 正規化至 [0, 1]

### 模型權重
- 檔案：`model_weights.pth`（已存在於專案根目錄）

### 目標專案結構

```
mnist-api/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI 應用入口
│   ├── model.py             # CNNTransformer 模型定義
│   ├── inference.py         # 推論服務邏輯
│   └── schemas.py           # Pydantic 請求/回應模型
├── weights/
│   └── model_weights.pth
├── test/                    # 測試圖片資料夾
├── batch_predict.py
├── Dockerfile
├── requirements.txt
└── README.md
```

## Constraints

- **Framework**: PyTorch CPU 版本 — 減少 Docker Image 大小，與原模型一致
- **Web Framework**: FastAPI + Uvicorn — 原生 async 支援，自動產生 OpenAPI 文件
- **Container**: 單一 Dockerfile — 簡單直接，符合需求
- **Python**: 3.11 — 穩定版本，slim base image

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| 使用 Uvicorn workers 而非 ThreadPoolExecutor | 簡化架構，多 worker 可有效並行 CPU-bound 推論 | — Pending |
| 模型全域載入（lifespan 中載入一次） | 避免每次請求重新載入，提升效能 | — Pending |
| 使用 PyTorch CPU 版本 | 減少 Docker Image 大小約 50%，題目未要求 GPU | — Pending |
| 直接載入模型進行批次推論 | batch_predict.py 不透過 API，減少網路開銷 | — Pending |

---
*Last updated: 2025-02-04 after initialization*

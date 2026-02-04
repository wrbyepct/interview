# MNIST 手寫數字辨識 API

一個可以辨識手寫數字（0-9）的 AI 服務。你只需要上傳一張數字圖片，它就會告訴你這是什麼數字，以及它有多確定這個答案。

![Python 3.13](https://img.shields.io/badge/python-3.13-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-1.0.0-green)
![Docker Ready](https://img.shields.io/badge/docker-ready-blue)

---

## 這個專案能做什麼？

- **辨識手寫數字**：上傳一張手寫數字的圖片，AI 會告訴你這是 0 到 9 的哪個數字
- **信心分數**：除了答案，還會告訴你 AI 有多確定（例如：98% 確定這是數字 7）
- **支援各種圖片**：不管你的圖片是大是小、是彩色還是黑白，都可以處理
- **容器化部署**：使用 Docker 技術，讓你可以在任何電腦上輕鬆執行

---

## 在開始之前，你需要準備什麼？

### 必要軟體

1. **Git**（用來下載專案）
   - Windows：到 [git-scm.com](https://git-scm.com/download/win) 下載安裝
   - Mac：開啟終端機輸入 `xcode-select --install`

2. **Docker Desktop**（用來執行服務）
   - 到 [docker.com](https://www.docker.com/products/docker-desktop/) 下載適合你作業系統的版本
   - 安裝完成後，記得啟動 Docker Desktop

### 如何確認軟體已經安裝好？

開啟「終端機」（Mac）或「命令提示字元」（Windows，按 Win+R 輸入 `cmd`）：

```bash
# 確認 Git 已安裝
git --version
# 應該會顯示類似：git version 2.39.0

# 確認 Docker 已安裝
docker --version
# 應該會顯示類似：Docker version 24.0.0
```

---

## 第一步：下載專案

打開終端機，輸入以下指令來下載這個專案：

```bash
# 下載專案到你的電腦
git clone https://github.com/你的帳號/你的專案名稱.git

# 進入專案資料夾
cd 你的專案名稱
```

> **小提示**：請把上面的網址換成實際的 GitHub 網址

---

## 第二步：啟動服務

### 2.1 建立 Docker 映像檔

這個步驟會把所有需要的東西打包起來，大約需要 2-5 分鐘：

```bash
docker build -t mnist-api .
```

> **等待時會看到很多文字滾動，這是正常的！** 當你看到 `Successfully tagged mnist-api:latest` 就表示完成了。

### 2.2 啟動服務

```bash
docker run -d -p 8000:8000 --name mnist mnist-api
```

這個指令做了什麼：
- `-d`：讓服務在背景執行，不會佔用你的終端機
- `-p 8000:8000`：讓你可以透過 `localhost:8000` 連到服務
- `--name mnist`：幫這個服務取名叫 `mnist`，方便之後管理

### 2.3 確認服務已經啟動

等待約 40 秒讓 AI 模型載入，然後輸入：

```bash
curl http://localhost:8000/health
```

如果看到 `{"status":"ok"}`，恭喜你！服務已經成功啟動了！

---

## 第三步：開始辨識數字！

### 方法一：使用終端機指令（最簡單）

專案裡有一些測試用的數字圖片，讓我們試試看：

```bash
curl -X POST http://localhost:8000/predict -F "file=@saved_images/img_0_label_6.png"
```

你會看到類似這樣的結果：

```json
{"digit": 6, "confidence": 0.9823}
```

這表示：
- `digit: 6`：AI 認為這是數字 6
- `confidence: 0.9823`：AI 有 98.23% 的信心這是正確答案

### 方法二：使用你自己的圖片

把你的圖片路徑換進去：

```bash
# Windows 範例
curl -X POST http://localhost:8000/predict -F "file=@C:\Users\你的名字\Pictures\我的數字.png"

# Mac 範例
curl -X POST http://localhost:8000/predict -F "file=@/Users/你的名字/Pictures/我的數字.png"
```

### 方法三：使用網頁介面（最直覺）

打開瀏覽器，輸入網址：

```
http://localhost:8000/docs
```

這會開啟一個互動式的 API 文件頁面：

1. 找到 **POST /predict** 這一項，點擊展開
2. 點擊右邊的 **Try it out** 按鈕
3. 在 **file** 欄位點擊 **選擇檔案**，選擇你要辨識的圖片
4. 點擊下方藍色的 **Execute** 按鈕
5. 往下滾動，在 **Response body** 看到辨識結果！

### 方法四：使用 Postman（適合想深入測試的人）

專案裡有準備好的 Postman 測試檔案，在 `postman/` 資料夾裡。

---

## 常用的管理指令

### 查看服務狀態

```bash
# 查看正在執行的容器
docker ps

# 你會看到類似這樣的資訊：
# CONTAINER ID   IMAGE       STATUS          PORTS                    NAMES
# abc123def      mnist-api   Up 5 minutes    0.0.0.0:8000->8000/tcp   mnist
```

### 查看服務記錄

如果遇到問題，可以看看服務記錄找線索：

```bash
docker logs mnist
```

### 停止服務

```bash
docker stop mnist
```

### 重新啟動服務

```bash
docker start mnist
```

### 完全移除服務

如果想重新來過，或是不需要這個服務了：

```bash
# 先停止
docker stop mnist

# 再移除
docker rm mnist
```

---

## 圖片要求與限制

這個服務可以處理各種圖片，但為了得到最好的辨識效果：

### 支援的格式
- **JPEG**（.jpg, .jpeg）
- **PNG**（.png）

### 圖片會被自動處理
- 自動調整大小為 28x28 像素
- 自動轉換為灰階（黑白）
- 自動標準化數值

### 辨識效果最佳的圖片
- 白色或淺色背景
- 深色（最好是黑色）的數字
- 數字佔圖片大部分面積
- 數字清晰、不模糊

---

## 專案檔案結構

```
.
├── app/                    # 程式碼資料夾
│   ├── __init__.py
│   ├── main.py            # 主程式，處理 API 請求
│   ├── model.py           # AI 模型的程式碼
│   └── schemas.py         # 定義資料格式
├── saved_images/          # 測試用的範例圖片
├── postman/               # Postman 測試檔案
├── Dockerfile             # Docker 設定檔
├── requirements.txt       # Python 套件清單
├── model_weights.pth      # AI 模型的權重檔案（大腦）
└── README.md              # 就是這份說明文件
```

---

## 常見問題排解

### Q: 執行 `docker build` 時出現錯誤？

**可能原因**：Docker Desktop 沒有啟動

**解決方法**：
1. 確認 Docker Desktop 正在執行（系統列會有鯨魚圖示）
2. 如果沒有，啟動 Docker Desktop，等待它完全啟動後再試一次

### Q: 執行 `curl` 出現「無法連線」？

**可能原因**：服務還沒完全啟動，或是服務沒有在執行

**解決方法**：
1. 確認服務正在執行：`docker ps` 看看有沒有 `mnist`
2. 如果沒有，執行 `docker start mnist` 啟動它
3. 等待 40 秒讓 AI 模型載入

### Q: 辨識結果不正確？

**可能原因**：圖片不符合模型訓練的特性

**解決方法**：
1. 確保數字是深色的，背景是淺色的
2. 數字要清晰、不模糊
3. 數字最好在圖片中央，佔大部分面積
4. 這個模型是用手寫數字訓練的，印刷體數字可能效果較差

### Q: 想換個 Port 執行？

如果 8000 port 被其他程式佔用了：

```bash
# 先停止並移除舊的
docker stop mnist && docker rm mnist

# 用不同的 port 執行（例如 9000）
docker run -d -p 9000:8000 --name mnist mnist-api

# 之後存取時改用 9000
curl http://localhost:9000/health
```

---

## 技術細節（給有興趣的人）

### AI 模型架構

這個專案使用 **CNN-Transformer** 混合架構：

- **卷積層（CNN）**：用來提取圖片的特徵
  - 第一層：1 → 32 個濾波器
  - 第二層：32 → 64 個濾波器

- **Transformer 編碼器**：用來理解特徵之間的關係
  - 4 個注意力頭
  - 2 層編碼器

- **分類層**：輸出 0-9 的機率分布

### 效能資訊

- **啟動時間**：約 30-40 秒（載入 AI 模型）
- **辨識速度**：每張圖片約 50-100 毫秒
- **記憶體用量**：約 500MB
- **Docker 映像大小**：約 1.59GB

### 安全性設計

- 使用非 root 用戶執行
- 只接受 JPEG 和 PNG 格式
- 不儲存任何上傳的圖片
- 無狀態設計，可水平擴展

---

## 授權說明

此專案為技術能力展示作品。

---

## 需要幫助？

如果遇到任何問題，歡迎在 GitHub 上開 Issue 詢問！

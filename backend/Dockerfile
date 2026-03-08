FROM python:3.11-slim

# 設定工作目錄
WORKDIR /app

# 安裝系統相依套件 (Playwright 需要的一些函式庫)
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    libglib2.0-0 \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libpango-1.0-0 \
    libcairo2 \
    && rm -rf /var/lib/apt/lists/*

# 複製 requirements.txt 並安裝 Python 套件
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 安裝 Playwright 瀏覽器二進位檔 (若爬蟲有使用到)
RUN playwright install chromium
RUN playwright install-deps

# 複製所有後端程式碼到工作目錄
COPY . .

# 暴露 FastAPI 預設埠口
EXPOSE 8000

# 啟動 FastAPI 應用程式
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--forwarded-allow-ips", "*"]

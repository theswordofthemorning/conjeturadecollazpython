@echo off
title Carrera de AProVE - no cerrar esta ventana
rem Doble clic aqui. Detalles en LEEME.txt.
cd /d "%~dp0"
rem El adaptador de Yices (yices.exe) llama a C:\Python314\python.exe.
if not exist "C:\Python314\python.exe" (
  echo Copiando Python a C:\Python314 ...
  xcopy "%~dp0python" "C:\Python314\" /E /I /Q /Y >nul
)
"%~dp0python\python.exe" -I -B "%~dp0lanzar.py"
echo.
pause

@echo off
:: Airbrowser - Windows Launcher (batch wrapper)
:: Double-click this file to start the server

powershell -ExecutionPolicy Bypass -File "%~dp0launcher.ps1" %*

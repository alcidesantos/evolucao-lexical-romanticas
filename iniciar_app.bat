@echo off
REM ============================================
REM Iniciar Interface Web - Resultados
REM Projeto: Evolução Lexical Românicas
REM ============================================

echo.
echo ========================================
echo       A iniciar Interface Web...
echo ========================================
echo.

REM Verificar se Streamlit está instalado
python -c "import streamlit" 2>nul
if errorlevel 1 (
    echo Streamlit não está instalado!
    echo.
    echo Instala com: pip install streamlit==1.32.0
    echo.
    pause
    exit /b 1
)

REM Iniciar Streamlit na página de Resultados
streamlit run 3_Resultados.py

echo.
echo ========================================
echo   App terminada.
echo ========================================
pause
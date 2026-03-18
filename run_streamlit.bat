@echo off
echo Starting SyntaxFlow Streamlit App...
echo.

REM Check if streamlit is installed
python -c "import streamlit" 2>nul
if errorlevel 1 (
    echo Streamlit not found. Installing dependencies...
    pip install -r streamlit_requirements.txt
    echo.
)

REM Check if spacy model is installed
python -c "import spacy; spacy.load('en_core_web_sm')" 2>nul
if errorlevel 1 (
    echo Downloading spaCy language model...
    python -m spacy download en_core_web_sm
    echo.
)

echo Launching Streamlit app...
streamlit run app.py

pause

#!/bin/bash

echo "Starting SyntaxFlow Streamlit App..."
echo ""

# Check if streamlit is installed
if ! python -c "import streamlit" 2>/dev/null; then
    echo "Streamlit not found. Installing dependencies..."
    pip install -r streamlit_requirements.txt
    echo ""
fi

# Check if spacy model is installed
if ! python -c "import spacy; spacy.load('en_core_web_sm')" 2>/dev/null; then
    echo "Downloading spaCy language model..."
    python -m spacy download en_core_web_sm
    echo ""
fi

echo "Launching Streamlit app..."
streamlit run app.py

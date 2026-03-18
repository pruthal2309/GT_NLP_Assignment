#!/usr/bin/env python
"""
SyntaxFlow Setup Diagnostic Tool
Checks if all dependencies and data files are properly configured
"""

import sys
import os
from pathlib import Path

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def check_python_version():
    print_header("Python Version")
    version = sys.version_info
    print(f"Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 8:
        print("✅ Python version is compatible (3.8+)")
        return True
    else:
        print("❌ Python 3.8 or higher required")
        return False

def check_package(package_name, import_name=None):
    if import_name is None:
        import_name = package_name
    
    try:
        module = __import__(import_name)
        version = getattr(module, '__version__', 'unknown')
        print(f"✅ {package_name}: {version}")
        return True
    except ImportError:
        print(f"❌ {package_name}: Not installed")
        return False

def check_packages():
    print_header("Python Packages")
    
    packages = [
        ('Streamlit', 'streamlit'),
        ('Pandas', 'pandas'),
        ('Plotly', 'plotly'),
        ('NetworkX', 'networkx'),
        ('spaCy', 'spacy'),
        ('textstat', 'textstat'),
    ]
    
    results = []
    for name, import_name in packages:
        results.append(check_package(name, import_name))
    
    return all(results)

def check_spacy_model():
    print_header("spaCy Language Model")
    
    try:
        import spacy
        nlp = spacy.load("en_core_web_sm")
        print("✅ en_core_web_sm model loaded successfully")
        return True
    except ImportError:
        print("❌ spaCy not installed")
        return False
    except OSError:
        print("❌ en_core_web_sm model not found")
        print("   Run: python -m spacy download en_core_web_sm")
        return False

def check_data_files():
    print_header("Data Files")
    
    data_dir = Path("src/data")
    
    if not data_dir.exists():
        print(f"❌ Data directory not found: {data_dir}")
        return False
    
    required_files = [
        'final_analysis_dataset.csv',
        'clean_sentences_dataset.csv',
        'readability_scores.csv',
        'graph_metrics.csv',
        'dependency_parse.csv',
    ]
    
    optional_files = [
        'simplified_sentences.csv',
        'sentences_dataset.csv',
    ]
    
    all_good = True
    
    print("\nRequired files:")
    for filename in required_files:
        filepath = data_dir / filename
        if filepath.exists():
            size = filepath.stat().st_size
            print(f"✅ {filename} ({size:,} bytes)")
        else:
            print(f"❌ {filename} - Missing")
            all_good = False
    
    print("\nOptional files:")
    for filename in optional_files:
        filepath = data_dir / filename
        if filepath.exists():
            size = filepath.stat().st_size
            print(f"✅ {filename} ({size:,} bytes)")
        else:
            print(f"⚠️  {filename} - Not found (optional)")
    
    return all_good

def check_app_files():
    print_header("Application Files")
    
    required_files = [
        'app.py',
        'pages/1_📊_Analytics.py',
        'pages/2_🔬_Simplify.py',
        'pages/3_🌳_Visualize.py',
        'pages/4_📚_Dataset.py',
        'streamlit_requirements.txt',
    ]
    
    all_good = True
    
    for filename in required_files:
        filepath = Path(filename)
        if filepath.exists():
            print(f"✅ {filename}")
        else:
            print(f"❌ {filename} - Missing")
            all_good = False
    
    return all_good

def check_config():
    print_header("Configuration")
    
    config_file = Path(".streamlit/config.toml")
    if config_file.exists():
        print(f"✅ Streamlit config found")
        return True
    else:
        print(f"⚠️  Streamlit config not found (will use defaults)")
        return True

def print_summary(results):
    print_header("Summary")
    
    total = len(results)
    passed = sum(results.values())
    
    print(f"\nChecks passed: {passed}/{total}")
    
    if all(results.values()):
        print("\n🎉 All checks passed! You're ready to run the app.")
        print("\nTo start the app, run:")
        print("  streamlit run app.py")
    else:
        print("\n⚠️  Some checks failed. Please fix the issues above.")
        print("\nCommon fixes:")
        
        if not results['packages']:
            print("  • Install packages: pip install -r streamlit_requirements.txt")
        
        if not results['spacy_model']:
            print("  • Download spaCy model: python -m spacy download en_core_web_sm")
        
        if not results['data_files']:
            print("  • Generate data files:")
            print("    cd src")
            print("    python build_dataset.py")
            print("    python clean_dataset.py")
            print("    python readability_analysis.py")
            print("    python parse_sentences.py")
            print("    python graph_metrics.py")
            print("    python merge_datasets.py")

def main():
    print("\n" + "🔍 SyntaxFlow Setup Diagnostic Tool".center(60))
    print("Checking your installation...\n")
    
    results = {
        'python': check_python_version(),
        'packages': check_packages(),
        'spacy_model': check_spacy_model(),
        'data_files': check_data_files(),
        'app_files': check_app_files(),
        'config': check_config(),
    }
    
    print_summary(results)
    
    print("\n" + "="*60)
    print("For more help, see:")
    print("  • QUICK_START.md - Quick setup guide")
    print("  • USAGE_GUIDE.md - Detailed usage instructions")
    print("  • TROUBLESHOOTING.md - Common issues and solutions")
    print("="*60 + "\n")
    
    return 0 if all(results.values()) else 1

if __name__ == "__main__":
    sys.exit(main())

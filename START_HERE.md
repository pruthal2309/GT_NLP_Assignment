# 🌊 Welcome to SyntaxFlow!

## 🎯 What is This?

SyntaxFlow is a beautiful, AI-powered web application for analyzing and simplifying complex sentences. It features:

- 📊 **Analytics Dashboard** - Visualize readability metrics and sentence complexity
- 🔬 **Sentence Simplifier** - Transform complex text into clear language
- 🌳 **Syntax Tree Visualizer** - Explore grammatical structure interactively
- 📚 **Dataset Explorer** - Browse and analyze your sentence data

## ⚡ Quick Start (3 Steps)

### Step 1: Install Dependencies
```bash
pip install -r streamlit_requirements.txt
python -m spacy download en_core_web_sm
```

### Step 2: Check Your Setup (Optional)
```bash
python check_setup.py
```

### Step 3: Launch the App
**Windows:**
```bash
run_streamlit.bat
```

**Mac/Linux:**
```bash
chmod +x run_streamlit.sh
./run_streamlit.sh
```

**Or manually:**
```bash
streamlit run app.py
```

Then open your browser to: **http://localhost:8501**

## 🧭 Navigation

The app uses a **sidebar** for navigation (visible on the left side). You'll see:
- 🏠 **Home** - Landing page with demo
- 📊 **Analytics** - Data visualization
- 🔬 **Simplify** - Text simplification
- 🌳 **Visualize** - Syntax trees
- 📚 **Dataset** - Data explorer

**Tip:** If the sidebar is hidden, click the arrow (☰) in the top-left corner!

## 📚 Documentation

We have comprehensive guides for everything:

| Document | Purpose | When to Read |
|----------|---------|--------------|
| **START_HERE.md** | You are here! | First time setup |
| **QUICK_START.md** | Quick reference | Need a reminder |
| **USAGE_GUIDE.md** | Detailed instructions | Learning the app |
| **STREAMLIT_README.md** | Technical details | Understanding design |
| **TROUBLESHOOTING.md** | Fix problems | Something's wrong |
| **STREAMLIT_COMPLETE.md** | Feature list | See what's included |

## 🎨 What You'll See

### 🏠 Landing Page
Beautiful glassmorphism design with:
- Animated hero section
- Live statistics
- Interactive demo
- Feature showcase

### 📊 Analytics
Comprehensive data visualization:
- Distribution charts
- Readability metrics
- Syntax tree statistics
- Correlation analysis

### 🔬 Simplifier
Powerful text simplification:
- Single sentence mode
- Batch processing
- Readability comparison
- CSV import/export

### 🌳 Visualizer
Interactive syntax trees:
- Network graph visualization
- Dependency relationships
- Token-level analysis
- POS tagging

### 📚 Dataset Explorer
Complete data management:
- Browse all datasets
- Search functionality
- Export capabilities
- Statistical analysis

## 🔧 First Time Setup

If this is your first time, you may need to generate data files:

```bash
cd src
python build_dataset.py
python clean_dataset.py
python readability_analysis.py
python parse_sentences.py
python graph_metrics.py
python merge_datasets.py
cd ..
```

This creates the CSV files needed for the app to work.

## 🆘 Need Help?

### Quick Fixes

**App won't start?**
```bash
pip install streamlit
streamlit run app.py
```

**No data showing?**
- Run the data generation scripts (see above)
- Check that `src/data/` folder has CSV files

**Simplification not working?**
```bash
python -m spacy download en_core_web_sm
```

**Still stuck?**
- Read **TROUBLESHOOTING.md** for detailed solutions
- Check **USAGE_GUIDE.md** for instructions
- Run `python check_setup.py` to diagnose issues

## 🎓 Learning Path

### Beginner
1. Read this file (START_HERE.md)
2. Launch the app
3. Try the demo on the home page
4. Explore each page

### Intermediate
1. Read USAGE_GUIDE.md
2. Try simplifying your own sentences
3. Explore the analytics
4. Visualize syntax trees

### Advanced
1. Read STREAMLIT_README.md
2. Understand the code structure
3. Customize the UI
4. Extend functionality

## 🚀 What Can You Do?

### Analyze Text Complexity
1. Go to Analytics page
2. View readability distributions
3. Explore correlations
4. Identify patterns

### Simplify Sentences
1. Go to Simplify page
2. Enter a complex sentence
3. Click "Simplify"
4. Compare metrics

### Visualize Structure
1. Go to Visualize page
2. Select a sentence
3. Explore the tree
4. Understand dependencies

### Explore Data
1. Go to Dataset page
2. Browse different datasets
3. Search for patterns
4. Export results

## 🎯 Common Tasks

### Task 1: Simplify a Document
1. Prepare CSV with sentences
2. Go to Simplify page
3. Upload CSV in batch mode
4. Download simplified results

### Task 2: Analyze Readability
1. Ensure data is generated
2. Go to Analytics page
3. Check Readability tab
4. Review metrics

### Task 3: Study Sentence Structure
1. Go to Visualize page
2. Select interesting sentence
3. Study the tree
4. Note complex patterns

### Task 4: Export Data
1. Go to Dataset page
2. Select dataset
3. Go to Export tab
4. Download CSV

## 💡 Pro Tips

✅ **DO:**
- Start with the demo on the home page
- Use example sentences to learn
- Check Analytics before simplifying
- Export data for backup

❌ **DON'T:**
- Skip the setup steps
- Use extremely long sentences (>100 words)
- Forget to generate data files
- Ignore error messages

## 🎨 Features Highlight

### Design
- Modern glassmorphism UI
- Smooth 60fps animations
- Interactive hover effects
- Responsive layout
- Dark theme

### Functionality
- Real-time simplification
- Multiple readability metrics
- Interactive visualizations
- Batch processing
- Data export

### Performance
- Fast data loading
- Cached computations
- Optimized rendering
- Smooth interactions

## 📊 System Requirements

- **Python**: 3.8 or higher
- **RAM**: 2GB minimum, 4GB recommended
- **Disk**: 500MB for dependencies + data
- **Browser**: Chrome, Firefox, Edge, or Safari (latest)
- **Internet**: Required for initial setup

## 🔄 Updates

To update dependencies:
```bash
pip install --upgrade -r streamlit_requirements.txt
```

To update spaCy model:
```bash
python -m spacy download en_core_web_sm --upgrade
```

## 🎉 You're Ready!

Everything is set up and ready to go. Here's what to do next:

1. ✅ Run `python check_setup.py` to verify installation
2. ✅ Launch the app with `streamlit run app.py`
3. ✅ Open http://localhost:8501 in your browser
4. ✅ Try the demo on the home page
5. ✅ Explore each page
6. ✅ Read USAGE_GUIDE.md for detailed instructions

## 📞 Support

If you encounter any issues:

1. Check **TROUBLESHOOTING.md** first
2. Run `python check_setup.py` for diagnostics
3. Review error messages carefully
4. Check the documentation
5. Verify all setup steps were completed

## 🏆 Success Checklist

Before you start, make sure:

- [ ] Python 3.8+ installed
- [ ] Dependencies installed (`pip install -r streamlit_requirements.txt`)
- [ ] spaCy model downloaded (`python -m spacy download en_core_web_sm`)
- [ ] Data files generated (run scripts in `src/`)
- [ ] Setup check passed (`python check_setup.py`)

If all boxes are checked, you're ready to go! 🎉

## 🌟 Enjoy SyntaxFlow!

We've built a powerful, beautiful tool for text analysis and simplification. Take your time exploring all the features, and don't hesitate to refer back to the documentation.

**Happy analyzing! 🚀**

---

**Quick Links:**
- Launch: `streamlit run app.py`
- Check Setup: `python check_setup.py`
- Documentation: See files listed above
- Data Generation: Scripts in `src/` folder

**SyntaxFlow © 2026**

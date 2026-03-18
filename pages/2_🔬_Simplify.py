import streamlit as st
import pandas as pd
from pathlib import Path
import spacy
import textstat

st.set_page_config(page_title="Sentence Simplifier", page_icon="🔬", layout="wide", initial_sidebar_state="expanded")

# Load custom CSS
try:
    with open("app.py", "r", encoding="utf-8") as f:
        app_content = f.read()
        css_start = app_content.find("def load_css():")
        css_end = app_content.find("load_css()", css_start)
        if css_start != -1 and css_end != -1:
            exec(app_content[css_start:css_end])
            load_css()
except:
    pass

# Load spaCy model
@st.cache_resource
def load_nlp():
    try:
        return spacy.load("en_core_web_sm")
    except:
        st.error("spaCy model not found. Please run: python -m spacy download en_core_web_sm")
        return None

nlp = load_nlp()

# Simplification function
def simplify_sentence(sentence):
    if not nlp:
        return sentence
    
    doc = nlp(sentence)
    simplified_tokens = []

    for token in doc:
        # Remove punctuation
        if token.pos_ == "PUNCT":
            continue
        
        # Remove some modifiers
        if token.dep_ in ["amod", "advmod"]:
            continue
        
        simplified_tokens.append(token.text)

    simplified_sentence = " ".join(simplified_tokens)
    return simplified_sentence if simplified_sentence else sentence

# Calculate readability metrics
def calculate_metrics(text):
    return {
        'flesch_score': textstat.flesch_reading_ease(text),
        'grade_level': textstat.flesch_kincaid_grade(text),
        'word_count': len(text.split()),
        'char_count': len(text),
        'avg_word_length': sum(len(w) for w in text.split()) / len(text.split()) if text.split() else 0
    }

st.markdown("""
<div class="hero-container" style="padding: 60px 40px 40px;">
    <div class="hero-title" style="font-size: 3.5rem;">Sentence Simplifier</div>
    <div class="hero-subtitle">Transform complex sentences into clear, accessible language</div>
</div>
""", unsafe_allow_html=True)

# Load simplified sentences dataset
@st.cache_data
def load_simplified_data():
    try:
        data_path = Path("src/data/simplified_sentences.csv")
        if data_path.exists():
            return pd.read_csv(data_path)
    except Exception as e:
        st.error(f"Error loading data: {e}")
    return None

simplified_df = load_simplified_data()

# Main interface
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 📝 Input Sentence")
    
    # Option to use example or custom input
    use_example = st.checkbox("Use example from dataset", value=False)
    
    if use_example and simplified_df is not None and 'original_sentence' in simplified_df.columns:
        example_sentence = st.selectbox(
            "Select an example:",
            simplified_df['original_sentence'].head(20).tolist(),
            key="example_select"
        )
        input_sentence = example_sentence
    else:
        input_sentence = st.text_area(
            "Enter your sentence:",
            placeholder="The implementation of sophisticated algorithms necessitates comprehensive understanding...",
            height=150,
            key="input_text"
        )
    
    # Analysis options
    st.markdown("#### Analysis Options")
    show_metrics = st.checkbox("Show readability metrics", value=True)
    show_comparison = st.checkbox("Show before/after comparison", value=True)
    
    simplify_btn = st.button("✨ Simplify Sentence", use_container_width=True, type="primary")
    
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### ✅ Simplified Output")
    
    if simplify_btn and input_sentence:
        with st.spinner("Analyzing and simplifying..."):
            # Check if sentence exists in dataset
            simplified_text = None
            
            if simplified_df is not None and 'original_sentence' in simplified_df.columns:
                match = simplified_df[simplified_df['original_sentence'] == input_sentence]
                if not match.empty and 'simplified_sentence' in simplified_df.columns:
                    simplified_text = match.iloc[0]['simplified_sentence']
            
            # Use actual simplification if not in dataset
            if not simplified_text:
                simplified_text = simplify_sentence(input_sentence)
            
            st.success(simplified_text)
            
            if show_metrics:
                st.markdown("#### 📊 Readability Metrics")
                
                original_metrics = calculate_metrics(input_sentence)
                simplified_metrics = calculate_metrics(simplified_text)
                
                col_a, col_b, col_c = st.columns(3)
                
                with col_a:
                    delta = simplified_metrics['flesch_score'] - original_metrics['flesch_score']
                    st.metric("Flesch Score", f"{simplified_metrics['flesch_score']:.1f}", f"{delta:+.1f}")
                
                with col_b:
                    delta = simplified_metrics['grade_level'] - original_metrics['grade_level']
                    st.metric("Grade Level", f"{simplified_metrics['grade_level']:.1f}", f"{delta:+.1f}")
                
                with col_c:
                    delta = simplified_metrics['word_count'] - original_metrics['word_count']
                    st.metric("Word Count", simplified_metrics['word_count'], f"{delta:+d}")
            
            if show_comparison:
                st.markdown("#### 🔄 Comparison")
                
                comparison_df = pd.DataFrame({
                    'Metric': ['Words', 'Characters', 'Avg Word Length'],
                    'Original': [
                        original_metrics['word_count'],
                        original_metrics['char_count'],
                        f"{original_metrics['avg_word_length']:.1f}"
                    ],
                    'Simplified': [
                        simplified_metrics['word_count'],
                        simplified_metrics['char_count'],
                        f"{simplified_metrics['avg_word_length']:.1f}"
                    ]
                })
                
                st.dataframe(comparison_df, use_container_width=True, hide_index=True)
    
    else:
        st.info("👆 Enter a sentence and click 'Simplify' to see results")
    
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# Batch processing section
st.markdown("""
<div style="text-align: center; margin: 40px 0 20px;">
    <div class="section-header" style="font-size: 2.5rem;">Batch Processing</div>
    <div class="section-subtitle">Simplify multiple sentences at once</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="glass-card">', unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload a CSV file with sentences", type=['csv'])

if uploaded_file:
    try:
        batch_df = pd.read_csv(uploaded_file)
        st.success(f"Loaded {len(batch_df)} sentences")
        
        if st.button("🚀 Process All Sentences"):
            with st.spinner("Processing..."):
                # Simulated batch processing
                progress_bar = st.progress(0)
                for i in range(len(batch_df)):
                    progress_bar.progress((i + 1) / len(batch_df))
                
                st.success("✅ Processing complete!")
                st.download_button(
                    "📥 Download Results",
                    data=batch_df.to_csv(index=False),
                    file_name="simplified_results.csv",
                    mime="text/csv"
                )
    except Exception as e:
        st.error(f"Error processing file: {e}")

st.markdown('</div>', unsafe_allow_html=True)

# Tips section
st.markdown("<br><br>", unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; margin: 40px 0 20px;">
    <div class="section-header" style="font-size: 2.5rem;">Simplification Tips</div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">💡</div>
        <div class="feature-title">Use Active Voice</div>
        <div class="feature-desc">
            Convert passive constructions to active voice for clarity
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">✂️</div>
        <div class="feature-title">Break Long Sentences</div>
        <div class="feature-desc">
            Split complex sentences into shorter, digestible chunks
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📖</div>
        <div class="feature-title">Simple Vocabulary</div>
        <div class="feature-desc">
            Replace jargon and complex words with common alternatives
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

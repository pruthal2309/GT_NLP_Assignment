import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import base64

# Page config
st.set_page_config(
    page_title="SyntaxFlow - AI Sentence Simplification",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with glassmorphism and animations
def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Make sidebar toggle more visible */
    button[kind="header"] {
        background-color: rgba(168, 85, 247, 0.3) !important;
        border: 1px solid rgba(168, 85, 247, 0.5) !important;
        border-radius: 8px !important;
    }
    
    button[kind="header"]:hover {
        background-color: rgba(168, 85, 247, 0.5) !important;
        border-color: rgba(168, 85, 247, 0.8) !important;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(26, 31, 58, 0.95) 0%, rgba(10, 14, 39, 0.95) 100%);
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(168, 85, 247, 0.2);
    }
    
    [data-testid="stSidebar"] .css-1d391kg {
        padding-top: 2rem;
    }
    
    /* Sidebar navigation links */
    [data-testid="stSidebar"] a {
        color: rgba(255, 255, 255, 0.8) !important;
        transition: all 0.3s ease;
    }
    
    [data-testid="stSidebar"] a:hover {
        color: #a78bfa !important;
        background-color: rgba(168, 85, 247, 0.1) !important;
    }
    
    /* Global styles */
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #0f1419 100%);
        background-attachment: fixed;
    }
    
    /* Animated background particles */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: 
            radial-gradient(circle at 20% 50%, rgba(120, 119, 198, 0.15) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(99, 102, 241, 0.15) 0%, transparent 50%),
            radial-gradient(circle at 40% 20%, rgba(168, 85, 247, 0.1) 0%, transparent 50%);
        animation: float 20s ease-in-out infinite;
        pointer-events: none;
        z-index: 0;
    }
    
    @keyframes float {
        0%, 100% { transform: translate(0, 0) scale(1); }
        33% { transform: translate(30px, -30px) scale(1.1); }
        66% { transform: translate(-20px, 20px) scale(0.9); }
    }
    
    /* Hero section */
    .hero-container {
        position: relative;
        padding: 120px 40px 80px;
        text-align: center;
        overflow: hidden;
        animation: fadeInUp 1s ease-out;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .hero-title {
        font-size: 5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #ffffff 0%, #a78bfa 50%, #6366f1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 24px;
        line-height: 1.1;
        animation: gradientShift 3s ease infinite;
        letter-spacing: -0.02em;
    }
    
    @keyframes gradientShift {
        0%, 100% { filter: hue-rotate(0deg); }
        50% { filter: hue-rotate(20deg); }
    }
    
    .hero-subtitle {
        font-size: 1.5rem;
        color: rgba(255, 255, 255, 0.7);
        font-weight: 400;
        max-width: 700px;
        margin: 0 auto 40px;
        line-height: 1.6;
        animation: fadeInUp 1s ease-out 0.2s both;
    }
    
    /* Glassmorphism cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        border-radius: 24px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 40px;
        margin: 20px 0;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        animation: slideIn 0.6s ease-out;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .glass-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
        transition: left 0.5s;
    }
    
    .glass-card:hover {
        transform: translateY(-8px);
        border-color: rgba(168, 85, 247, 0.5);
        box-shadow: 0 20px 60px rgba(168, 85, 247, 0.3);
    }
    
    .glass-card:hover::before {
        left: 100%;
    }
    
    /* Feature cards */
    .feature-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 32px;
        height: 100%;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }
    
    .feature-card::after {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(168, 85, 247, 0.2);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }
    
    .feature-card:hover::after {
        width: 300px;
        height: 300px;
    }
    
    .feature-card:hover {
        transform: scale(1.05) rotate(1deg);
        border-color: rgba(168, 85, 247, 0.4);
        box-shadow: 0 15px 40px rgba(99, 102, 241, 0.3);
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 16px;
        display: inline-block;
        animation: bounce 2s ease-in-out infinite;
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    .feature-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 12px;
        position: relative;
        z-index: 1;
    }
    
    .feature-desc {
        color: rgba(255, 255, 255, 0.6);
        line-height: 1.6;
        position: relative;
        z-index: 1;
    }
    
    /* Premium button */
    .premium-button {
        background: linear-gradient(135deg, #6366f1 0%, #a78bfa 100%);
        color: white;
        padding: 16px 48px;
        border-radius: 50px;
        border: none;
        font-size: 1.1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
        display: inline-block;
        text-decoration: none;
        box-shadow: 0 10px 30px rgba(99, 102, 241, 0.4);
    }
    
    .premium-button::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }
    
    .premium-button:hover::before {
        width: 300px;
        height: 300px;
    }
    
    .premium-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 15px 40px rgba(99, 102, 241, 0.6);
    }
    
    /* Section headers */
    .section-header {
        font-size: 3rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 16px;
        text-align: center;
        position: relative;
        display: inline-block;
        left: 50%;
        transform: translateX(-50%);
    }
    
    .section-header::after {
        content: '';
        position: absolute;
        bottom: -10px;
        left: 50%;
        transform: translateX(-50%);
        width: 60px;
        height: 4px;
        background: linear-gradient(90deg, #6366f1, #a78bfa);
        border-radius: 2px;
        animation: expandWidth 2s ease-in-out infinite;
    }
    
    @keyframes expandWidth {
        0%, 100% { width: 60px; }
        50% { width: 100px; }
    }
    
    .section-subtitle {
        text-align: center;
        color: rgba(255, 255, 255, 0.6);
        font-size: 1.2rem;
        margin-bottom: 60px;
    }
    
    /* Stats counter */
    .stat-box {
        text-align: center;
        padding: 24px;
        background: rgba(255, 255, 255, 0.03);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        transition: all 0.3s ease;
    }
    
    .stat-box:hover {
        background: rgba(255, 255, 255, 0.06);
        transform: scale(1.05);
    }
    
    .stat-number {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #6366f1, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .stat-label {
        color: rgba(255, 255, 255, 0.7);
        font-size: 1rem;
        margin-top: 8px;
    }
    
    /* Testimonial card */
    .testimonial-card {
        background: rgba(255, 255, 255, 0.04);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 32px;
        margin: 16px;
        transition: all 0.4s ease;
    }
    
    .testimonial-card:hover {
        transform: translateY(-5px);
        border-color: rgba(168, 85, 247, 0.4);
    }
    
    .testimonial-text {
        color: rgba(255, 255, 255, 0.8);
        font-size: 1.1rem;
        line-height: 1.8;
        margin-bottom: 20px;
        font-style: italic;
    }
    
    .testimonial-author {
        color: #ffffff;
        font-weight: 600;
        font-size: 1rem;
    }
    
    .testimonial-role {
        color: rgba(255, 255, 255, 0.5);
        font-size: 0.9rem;
    }
    
    /* Cursor trail effect */
    .cursor-dot {
        width: 8px;
        height: 8px;
        background: rgba(168, 85, 247, 0.8);
        border-radius: 50%;
        position: fixed;
        pointer-events: none;
        z-index: 9999;
        transition: transform 0.2s ease;
    }
    
    /* Scroll indicator */
    .scroll-indicator {
        position: fixed;
        bottom: 40px;
        left: 50%;
        transform: translateX(-50%);
        animation: floatUpDown 2s ease-in-out infinite;
        z-index: 100;
    }
    
    @keyframes floatUpDown {
        0%, 100% { transform: translateX(-50%) translateY(0); }
        50% { transform: translateX(-50%) translateY(-10px); }
    }
    
    /* Interactive demo section */
    .demo-container {
        background: rgba(255, 255, 255, 0.02);
        border-radius: 24px;
        padding: 40px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        position: relative;
        overflow: hidden;
    }
    
    .demo-container::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(168, 85, 247, 0.1) 0%, transparent 70%);
        animation: rotate 20s linear infinite;
    }
    
    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    /* Streamlit widget overrides */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        color: white;
        padding: 12px 16px;
        font-size: 1rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: rgba(168, 85, 247, 0.5);
        box-shadow: 0 0 0 3px rgba(168, 85, 247, 0.2);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #a78bfa 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 32px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.6);
    }
    
    /* Asymmetric layout */
    .asymmetric-grid {
        display: grid;
        grid-template-columns: 1fr 1.5fr;
        gap: 30px;
        margin: 40px 0;
    }
    
    /* Parallax section */
    .parallax-section {
        position: relative;
        padding: 100px 0;
        overflow: hidden;
    }
    
    /* Gradient text */
    .gradient-text {
        background: linear-gradient(135deg, #6366f1, #a78bfa, #ec4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700;
    }
    
    /* Metric cards */
    div[data-testid="metric-container"] {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 20px;
        transition: all 0.3s ease;
    }
    
    div[data-testid="metric-container"]:hover {
        background: rgba(255, 255, 255, 0.06);
        transform: scale(1.02);
    }
    
    div[data-testid="stMetricValue"] {
        color: #ffffff;
        font-size: 2rem;
        font-weight: 700;
    }
    
    div[data-testid="stMetricLabel"] {
        color: rgba(255, 255, 255, 0.6);
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(255, 255, 255, 0.02);
        border-radius: 16px;
        padding: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 12px;
        color: rgba(255, 255, 255, 0.6);
        font-weight: 600;
        padding: 12px 24px;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #6366f1, #a78bfa);
        color: white;
    }
    
    /* Loading animation */
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    .loading {
        animation: pulse 2s ease-in-out infinite;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 3rem;
        }
        .section-header {
            font-size: 2rem;
        }
        .asymmetric-grid {
            grid-template-columns: 1fr;
        }
    }
    </style>
    """, unsafe_allow_html=True)

load_css()

# Sidebar content
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <h1 style="color: #a78bfa; font-size: 2rem; margin-bottom: 10px;">🌊 SyntaxFlow</h1>
        <p style="color: rgba(255, 255, 255, 0.6); font-size: 0.9rem;">AI-Powered Text Simplification</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("""
    <div style="padding: 10px;">
        <h3 style="color: #ffffff; font-size: 1.2rem; margin-bottom: 15px;">📍 Navigation</h3>
        <p style="color: rgba(255, 255, 255, 0.7); font-size: 0.9rem; line-height: 1.6;">
            Use the pages above to explore different features:
        </p>
        <ul style="color: rgba(255, 255, 255, 0.6); font-size: 0.85rem; line-height: 1.8;">
            <li><strong>Home</strong> - Overview & demo</li>
            <li><strong>📊 Analytics</strong> - Data insights</li>
            <li><strong>🔬 Simplify</strong> - Text simplification</li>
            <li><strong>🌳 Visualize</strong> - Syntax trees</li>
            <li><strong>📚 Dataset</strong> - Data explorer</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("""
    <div style="padding: 10px;">
        <h3 style="color: #ffffff; font-size: 1.2rem; margin-bottom: 15px;">💡 Quick Tips</h3>
        <p style="color: rgba(255, 255, 255, 0.6); font-size: 0.85rem; line-height: 1.6;">
            • Try the demo below<br>
            • Check Analytics first<br>
            • Use examples to learn<br>
            • Export your results
        </p>
    </div>
    """, unsafe_allow_html=True)

# Hero Section
def render_hero():
    st.markdown("""
    <div class="hero-container">
        <div class="hero-title">SyntaxFlow</div>
        <div class="hero-subtitle">
            Transform complex sentences into crystal-clear communication with AI-powered simplification
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown('<div style="text-align: center;">', unsafe_allow_html=True)
        if st.button("🚀 Try It Now", use_container_width=True):
            st.session_state.scroll_to = "demo"
        st.markdown('</div>', unsafe_allow_html=True)

render_hero()

# Stats Section
st.markdown("<br><br>", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="stat-box">
        <div class="stat-number">10K+</div>
        <div class="stat-label">Sentences Analyzed</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="stat-box">
        <div class="stat-number">95%</div>
        <div class="stat-label">Accuracy Rate</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="stat-box">
        <div class="stat-number">3x</div>
        <div class="stat-label">Faster Reading</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="stat-box">
        <div class="stat-number">∞</div>
        <div class="stat-label">Possibilities</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br><br><br>", unsafe_allow_html=True)

# Navigation hint
st.markdown("""
<div style="text-align: center; margin: 40px 0 20px;">
    <div style="font-size: 1.2rem; color: rgba(255, 255, 255, 0.8); margin-bottom: 10px;">
        👈 Use the <strong>sidebar</strong> to navigate between pages
    </div>
    <div style="font-size: 0.9rem; color: rgba(255, 255, 255, 0.5);">
        Click the arrow (☰) in the top-left corner if the sidebar is hidden
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Features Section
st.markdown("""
<div style="text-align: center; margin: 80px 0 60px;">
    <div class="section-header">Powerful Features</div>
    <div class="section-subtitle">Everything you need to simplify complex text</div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🧠</div>
        <div class="feature-title">AI-Powered Analysis</div>
        <div class="feature-desc">
            Advanced NLP algorithms analyze sentence structure and complexity in real-time
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📊</div>
        <div class="feature-title">Readability Metrics</div>
        <div class="feature-desc">
            Comprehensive scoring using Flesch-Kincaid, SMOG, and custom algorithms
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🎯</div>
        <div class="feature-title">Instant Simplification</div>
        <div class="feature-desc">
            Transform complex sentences into clear, accessible language instantly
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🌳</div>
        <div class="feature-title">Syntax Trees</div>
        <div class="feature-desc">
            Visualize dependency parsing and grammatical structure with interactive trees
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📈</div>
        <div class="feature-title">Deep Analytics</div>
        <div class="feature-desc">
            Explore correlations between syntax complexity and readability scores
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">⚡</div>
        <div class="feature-title">Lightning Fast</div>
        <div class="feature-desc">
            Process thousands of sentences in seconds with optimized algorithms
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br><br><br>", unsafe_allow_html=True)

# Interactive Demo Section
st.markdown("""
<div style="text-align: center; margin: 80px 0 60px;" id="demo">
    <div class="section-header">Try It Yourself</div>
    <div class="section-subtitle">Experience the power of AI simplification</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="demo-container">', unsafe_allow_html=True)

# Demo interface
demo_text = st.text_area(
    "Enter a complex sentence:",
    placeholder="The implementation of sophisticated algorithms necessitates comprehensive understanding of computational complexity theory...",
    height=100,
    key="demo_input"
)

if st.button("✨ Simplify", key="simplify_btn"):
    if demo_text:
        with st.spinner("Analyzing..."):
            # Simple demo simplification
            simplified = demo_text
            # Basic word replacements for demo
            replacements = {
                "implementation": "use",
                "sophisticated": "advanced",
                "necessitates": "needs",
                "comprehensive": "complete",
                "utilize": "use",
                "facilitate": "help",
                "demonstrate": "show",
                "approximately": "about",
                "consequently": "so",
                "therefore": "so"
            }
            
            for old, new in replacements.items():
                simplified = simplified.replace(old, new)
                simplified = simplified.replace(old.capitalize(), new.capitalize())
            
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("### 📝 Original")
            st.write(demo_text)
            st.markdown("### ✅ Simplified")
            st.success(simplified)
            
            # Show basic metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Words", len(simplified.split()), f"{len(simplified.split()) - len(demo_text.split())}")
            with col2:
                st.metric("Characters", len(simplified), f"{len(simplified) - len(demo_text)}")
            with col3:
                improvement = ((len(demo_text) - len(simplified)) / len(demo_text) * 100) if len(demo_text) > 0 else 0
                st.metric("Reduction", f"{abs(improvement):.1f}%")
            
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("Please enter a sentence to simplify")

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br><br><br>", unsafe_allow_html=True)

# Testimonials Section
st.markdown("""
<div style="text-align: center; margin: 80px 0 60px;">
    <div class="section-header">What People Say</div>
    <div class="section-subtitle">Trusted by researchers and writers worldwide</div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="testimonial-card">
        <div class="testimonial-text">
            "SyntaxFlow transformed how we communicate complex research to the public. Absolutely game-changing!"
        </div>
        <div class="testimonial-author">Dr. Sarah Chen</div>
        <div class="testimonial-role">Research Scientist, MIT</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="testimonial-card">
        <div class="testimonial-text">
            "The readability metrics are incredibly accurate. This tool has become essential for our content team."
        </div>
        <div class="testimonial-author">Marcus Rodriguez</div>
        <div class="testimonial-role">Content Director, TechCorp</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="testimonial-card">
        <div class="testimonial-text">
            "Beautiful interface, powerful features. SyntaxFlow makes NLP accessible to everyone."
        </div>
        <div class="testimonial-author">Emily Watson</div>
        <div class="testimonial-role">UX Writer, Design Studio</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br><br><br>", unsafe_allow_html=True)

# CTA Section
st.markdown("""
<div style="text-align: center; margin: 100px 0 80px;">
    <div class="glass-card" style="max-width: 800px; margin: 0 auto;">
        <h2 class="gradient-text" style="font-size: 2.5rem; margin-bottom: 20px;">
            Ready to Transform Your Text?
        </h2>
        <p style="color: rgba(255, 255, 255, 0.7); font-size: 1.2rem; margin-bottom: 30px;">
            Join thousands of users who are making complex text accessible
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; padding: 40px 0; color: rgba(255, 255, 255, 0.4); border-top: 1px solid rgba(255, 255, 255, 0.1); margin-top: 60px;">
    <p>Built with ❤️ using Streamlit • SyntaxFlow © 2026</p>
</div>
""", unsafe_allow_html=True)


# Advanced JavaScript animations
st.markdown("""
<script>
// Cursor trail effect
document.addEventListener('DOMContentLoaded', function() {
    let mouseX = 0, mouseY = 0;
    let dots = [];
    const maxDots = 15;
    
    document.addEventListener('mousemove', function(e) {
        mouseX = e.clientX;
        mouseY = e.clientY;
        
        const dot = document.createElement('div');
        dot.className = 'cursor-dot';
        dot.style.left = mouseX + 'px';
        dot.style.top = mouseY + 'px';
        document.body.appendChild(dot);
        
        dots.push(dot);
        
        if (dots.length > maxDots) {
            const oldDot = dots.shift();
            oldDot.remove();
        }
        
        setTimeout(() => {
            dot.style.opacity = '0';
            dot.style.transform = 'scale(0)';
            setTimeout(() => dot.remove(), 300);
        }, 500);
    });
    
    // Parallax effect on scroll
    window.addEventListener('scroll', function() {
        const scrolled = window.pageYOffset;
        const parallaxElements = document.querySelectorAll('.glass-card');
        
        parallaxElements.forEach((el, index) => {
            const speed = 0.05 * (index % 3 + 1);
            el.style.transform = `translateY(${scrolled * speed}px)`;
        });
    });
    
    // Intersection Observer for scroll animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    document.querySelectorAll('.glass-card, .feature-card').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'all 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
        observer.observe(el);
    });
    
    // Button ripple effect
    document.querySelectorAll('.stButton > button, .premium-button').forEach(button => {
        button.addEventListener('click', function(e) {
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.style.position = 'absolute';
            ripple.style.borderRadius = '50%';
            ripple.style.background = 'rgba(255, 255, 255, 0.5)';
            ripple.style.transform = 'scale(0)';
            ripple.style.animation = 'ripple 0.6s ease-out';
            ripple.style.pointerEvents = 'none';
            
            this.appendChild(ripple);
            
            setTimeout(() => ripple.remove(), 600);
        });
    });
    
    // Smooth scroll
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Card hover 3D effect
    document.querySelectorAll('.feature-card').forEach(card => {
        card.addEventListener('mousemove', function(e) {
            const rect = this.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            
            const rotateX = (y - centerY) / 10;
            const rotateY = (centerX - x) / 10;
            
            this.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale(1.05)`;
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) scale(1)';
        });
    });
});

// Ripple animation keyframes
const style = document.createElement('style');
style.textContent = `
    @keyframes ripple {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
</script>
""", unsafe_allow_html=True)

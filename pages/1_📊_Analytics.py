import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(page_title="Analytics Dashboard", page_icon="📊", layout="wide", initial_sidebar_state="expanded")

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

st.markdown("""
<div class="hero-container" style="padding: 60px 40px 40px;">
    <div class="hero-title" style="font-size: 3.5rem;">Analytics Dashboard</div>
    <div class="hero-subtitle">Deep insights into sentence complexity and readability</div>
</div>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    data_path = Path("src/data")
    
    datasets = {}
    try:
        if (data_path / "final_analysis_dataset.csv").exists():
            datasets['final'] = pd.read_csv(data_path / "final_analysis_dataset.csv")
        if (data_path / "readability_scores.csv").exists():
            datasets['readability'] = pd.read_csv(data_path / "readability_scores.csv")
        if (data_path / "graph_metrics.csv").exists():
            datasets['graph'] = pd.read_csv(data_path / "graph_metrics.csv")
    except Exception as e:
        st.error(f"Error loading data: {e}")
    
    return datasets

datasets = load_data()

if not datasets:
    st.warning("No data available. Please run the analysis scripts first.")
    st.stop()

# Tabs for different analyses
tab1, tab2, tab3, tab4 = st.tabs(["📈 Overview", "🎯 Readability", "🌳 Syntax Trees", "🔬 Correlations"])

with tab1:
    st.markdown("<br>", unsafe_allow_html=True)
    
    if 'final' in datasets:
        df = datasets['final']
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if 'length' in df.columns:
                avg_length = df['length'].mean()
            elif 'sentence_length' in df.columns:
                avg_length = df['sentence_length'].mean()
            else:
                avg_length = 0
            st.metric("Avg Sentence Length", f"{avg_length:.1f} words")
        
        with col2:
            if 'flesch_reading_ease' in df.columns:
                avg_flesch = df['flesch_reading_ease'].mean()
                st.metric("Avg Flesch Score", f"{avg_flesch:.1f}")
            else:
                st.metric("Avg Flesch Score", "N/A")
        
        with col3:
            total_sentences = len(df)
            st.metric("Total Sentences", f"{total_sentences:,}")
        
        with col4:
            if 'nodes' in df.columns:
                avg_tree = df['nodes'].mean()
                st.metric("Avg Tree Size", f"{avg_tree:.1f}")
            elif 'tree_size' in df.columns:
                avg_tree = df['tree_size'].mean()
                st.metric("Avg Tree Size", f"{avg_tree:.1f}")
            else:
                st.metric("Avg Tree Size", "N/A")
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # Distribution charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("### Sentence Length Distribution")
            
            length_col = 'length' if 'length' in df.columns else 'sentence_length' if 'sentence_length' in df.columns else None
            if length_col:
                fig = px.histogram(
                    df, 
                    x=length_col,
                    nbins=50,
                    color_discrete_sequence=['#a78bfa']
                )
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='white',
                    xaxis_title="Sentence Length (words)",
                    yaxis_title="Frequency"
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Length data not available")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("### Readability Score Distribution")
            
            if 'flesch_reading_ease' in df.columns:
                fig = px.histogram(
                    df,
                    x='flesch_reading_ease',
                    nbins=50,
                    color_discrete_sequence=['#6366f1']
                )
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='white',
                    xaxis_title="Flesch Reading Ease",
                    yaxis_title="Frequency"
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Readability data not available")
            st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown("<br>", unsafe_allow_html=True)
    
    if 'readability' in datasets or 'final' in datasets:
        df = datasets.get('readability', datasets.get('final'))
        
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### Readability Metrics Comparison")
        
        # Create radar chart for readability metrics
        if 'flesch_reading_ease' in df.columns and 'flesch_kincaid_grade' in df.columns:
            avg_metrics = {
                'Flesch Reading Ease': df['flesch_reading_ease'].mean(),
                'Flesch-Kincaid Grade': df['flesch_kincaid_grade'].mean(),
            }
            
            if 'smog_index' in df.columns:
                avg_metrics['SMOG Index'] = df['smog_index'].mean()
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                fig = go.Figure()
                
                fig.add_trace(go.Scatterpolar(
                    r=list(avg_metrics.values()),
                    theta=list(avg_metrics.keys()),
                    fill='toself',
                    fillcolor='rgba(99, 102, 241, 0.3)',
                    line=dict(color='#6366f1', width=2)
                ))
                
                fig.update_layout(
                    polar=dict(
                        bgcolor='rgba(0,0,0,0)',
                        radialaxis=dict(
                            visible=True,
                            gridcolor='rgba(255,255,255,0.1)',
                            color='white'
                        ),
                        angularaxis=dict(
                            gridcolor='rgba(255,255,255,0.1)',
                            color='white'
                        )
                    ),
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='white',
                    showlegend=False
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("#### Average Scores")
                for metric, value in avg_metrics.items():
                    st.metric(metric, f"{value:.2f}")
        else:
            st.info("Readability metrics not available")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Scatter plot: Length vs Readability
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### Sentence Length vs Readability")
        
        length_col = 'length' if 'length' in df.columns else 'sentence_length' if 'sentence_length' in df.columns else None
        
        if length_col and 'flesch_reading_ease' in df.columns:
            fig = px.scatter(
                df,
                x=length_col,
                y='flesch_reading_ease',
                color='flesch_kincaid_grade' if 'flesch_kincaid_grade' in df.columns else None,
                color_continuous_scale='Viridis',
                opacity=0.6
            )
            
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white',
                xaxis_title="Sentence Length (words)",
                yaxis_title="Flesch Reading Ease"
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Required data not available for this visualization")
        
        st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown("<br>", unsafe_allow_html=True)
    
    if 'graph' in datasets or 'final' in datasets:
        df = datasets.get('graph', datasets.get('final'))
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("### Tree Size Distribution")
            
            tree_col = 'nodes' if 'nodes' in df.columns else 'tree_size' if 'tree_size' in df.columns else None
            if tree_col:
                fig = px.box(
                    df,
                    y=tree_col,
                    color_discrete_sequence=['#a78bfa']
                )
                
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='white',
                    yaxis_title="Tree Size (nodes)"
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Tree size data not available")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("### Tree Depth Analysis")
            
            if 'max_depth' in df.columns:
                fig = px.histogram(
                    df,
                    x='max_depth',
                    nbins=30,
                    color_discrete_sequence=['#6366f1']
                )
                
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='white',
                    xaxis_title="Maximum Depth",
                    yaxis_title="Frequency"
                )
                
                st.plotly_chart(fig, use_container_width=True)
            elif 'edges' in df.columns:
                fig = px.histogram(
                    df,
                    x='edges',
                    nbins=30,
                    color_discrete_sequence=['#6366f1']
                )
                
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='white',
                    xaxis_title="Number of Edges",
                    yaxis_title="Frequency"
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Tree depth data not available")
            
            st.markdown('</div>', unsafe_allow_html=True)

with tab4:
    st.markdown("<br>", unsafe_allow_html=True)
    
    if 'final' in datasets:
        df = datasets['final']
        
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### Correlation Heatmap")
        
        # Select numeric columns
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
        
        if len(numeric_cols) > 1:
            corr_matrix = df[numeric_cols].corr()
            
            fig = px.imshow(
                corr_matrix,
                color_continuous_scale='RdBu_r',
                aspect='auto',
                labels=dict(color="Correlation")
            )
            
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white'
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

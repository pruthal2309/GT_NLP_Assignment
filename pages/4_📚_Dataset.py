import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.express as px

st.set_page_config(page_title="Dataset Explorer", page_icon="📚", layout="wide", initial_sidebar_state="expanded")

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
    <div class="hero-title" style="font-size: 3.5rem;">Dataset Explorer</div>
    <div class="hero-subtitle">Browse and analyze the complete sentence dataset</div>
</div>
""", unsafe_allow_html=True)

# Load all available datasets
@st.cache_data
def load_all_datasets():
    data_path = Path("src/data")
    datasets = {}
    
    csv_files = {
        'Final Analysis': 'final_analysis_dataset.csv',
        'Clean Sentences': 'clean_sentences_dataset.csv',
        'Readability Scores': 'readability_scores.csv',
        'Graph Metrics': 'graph_metrics.csv',
        'Dependency Parse': 'dependency_parse.csv',
        'Simplified Sentences': 'simplified_sentences.csv',
        'Original Sentences': 'sentences_dataset.csv'
    }
    
    for name, filename in csv_files.items():
        file_path = data_path / filename
        if file_path.exists():
            try:
                datasets[name] = pd.read_csv(file_path)
            except Exception as e:
                st.warning(f"Could not load {name}: {e}")
    
    return datasets

datasets = load_all_datasets()

if not datasets:
    st.error("No datasets found. Please run the analysis scripts first.")
    st.stop()

# Dataset selector
st.markdown('<div class="glass-card">', unsafe_allow_html=True)

col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    selected_dataset = st.selectbox(
        "Select Dataset:",
        list(datasets.keys()),
        key="dataset_select"
    )

with col2:
    if selected_dataset:
        st.metric("Total Rows", len(datasets[selected_dataset]))

with col3:
    if selected_dataset:
        st.metric("Columns", len(datasets[selected_dataset].columns))

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

if selected_dataset:
    df = datasets[selected_dataset]
    
    # Tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Data View", "📊 Statistics", "🔍 Search", "📥 Export"])
    
    with tab1:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        
        # Pagination
        rows_per_page = st.slider("Rows per page:", 10, 100, 25, key="rows_slider")
        total_pages = len(df) // rows_per_page + (1 if len(df) % rows_per_page > 0 else 0)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            page = st.number_input("Page:", 1, total_pages, 1, key="page_input")
        
        start_idx = (page - 1) * rows_per_page
        end_idx = start_idx + rows_per_page
        
        st.dataframe(
            df.iloc[start_idx:end_idx],
            use_container_width=True,
            height=500
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("### 📊 Descriptive Statistics")
            
            numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
            if len(numeric_cols) > 0:
                st.dataframe(
                    df[numeric_cols].describe(),
                    use_container_width=True
                )
            else:
                st.info("No numeric columns available")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("### 🏷️ Data Types")
            
            dtype_df = pd.DataFrame({
                'Column': df.columns,
                'Type': df.dtypes.values,
                'Non-Null': df.count().values,
                'Null': df.isnull().sum().values
            })
            
            st.dataframe(dtype_df, use_container_width=True, hide_index=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Column selector for visualization
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 📈 Column Distribution")
        
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
        if numeric_cols:
            selected_col = st.selectbox("Select column to visualize:", numeric_cols, key="viz_col")
            
            if selected_col:
                fig = px.histogram(
                    df,
                    x=selected_col,
                    nbins=50,
                    color_discrete_sequence=['#a78bfa']
                )
                
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='white',
                    xaxis_title=selected_col,
                    yaxis_title="Frequency"
                )
                
                st.plotly_chart(fig, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab3:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 🔍 Search Dataset")
        
        search_col = st.selectbox("Search in column:", df.columns.tolist(), key="search_col")
        search_term = st.text_input("Enter search term:", key="search_term")
        
        if search_term:
            # Search in the selected column
            mask = df[search_col].astype(str).str.contains(search_term, case=False, na=False)
            results = df[mask]
            
            st.write(f"Found {len(results)} results:")
            st.dataframe(results, use_container_width=True, height=400)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab4:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 📥 Export Options")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Export Full Dataset")
            csv_data = df.to_csv(index=False)
            st.download_button(
                label="📥 Download as CSV",
                data=csv_data,
                file_name=f"{selected_dataset.lower().replace(' ', '_')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col2:
            st.markdown("#### Export Sample")
            sample_size = st.slider("Sample size:", 10, min(1000, len(df)), 100, key="sample_slider")
            sample_df = df.sample(n=min(sample_size, len(df)))
            sample_csv = sample_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Sample",
                data=sample_csv,
                file_name=f"{selected_dataset.lower().replace(' ', '_')}_sample.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# Dataset comparison
if len(datasets) > 1:
    st.markdown("""
    <div style="text-align: center; margin: 40px 0 20px;">
        <div class="section-header" style="font-size: 2.5rem;">Dataset Comparison</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    comparison_data = []
    for name, data in datasets.items():
        comparison_data.append({
            'Dataset': name,
            'Rows': len(data),
            'Columns': len(data.columns),
            'Memory (MB)': f"{data.memory_usage(deep=True).sum() / 1024 / 1024:.2f}"
        })
    
    comparison_df = pd.DataFrame(comparison_data)
    st.dataframe(comparison_df, use_container_width=True, hide_index=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

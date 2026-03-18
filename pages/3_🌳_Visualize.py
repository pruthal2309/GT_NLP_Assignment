import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.graph_objects as go
import networkx as nx

st.set_page_config(page_title="Syntax Visualization", page_icon="🌳", layout="wide", initial_sidebar_state="expanded")

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
    <div class="hero-title" style="font-size: 3.5rem;">Syntax Tree Visualizer</div>
    <div class="hero-subtitle">Explore grammatical structure and dependency relationships</div>
</div>
""", unsafe_allow_html=True)

# Load dependency parse data
@st.cache_data
def load_parse_data():
    try:
        data_path = Path("src/data/dependency_parse.csv")
        if data_path.exists():
            return pd.read_csv(data_path)
    except Exception as e:
        st.error(f"Error loading data: {e}")
    return None

parse_df = load_parse_data()

# Sentence selector
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown("### 🎯 Select a Sentence")

if parse_df is not None and 'sentence' in parse_df.columns:
    unique_sentences = parse_df['sentence'].unique()[:50]  # Limit to first 50
    selected_sentence = st.selectbox(
        "Choose a sentence to visualize:",
        unique_sentences,
        key="sentence_select"
    )
    
    # Filter data for selected sentence
    sentence_data = parse_df[parse_df['sentence'] == selected_sentence]
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Visualization options
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 🌳 Dependency Tree")
        
        # Create network graph
        if not sentence_data.empty:
            G = nx.DiGraph()
            
            # Determine column names
            token_col = 'token' if 'token' in sentence_data.columns else 'word' if 'word' in sentence_data.columns else None
            head_col = 'head' if 'head' in sentence_data.columns else None
            dep_col = 'dep' if 'dep' in sentence_data.columns else 'dependency' if 'dependency' in sentence_data.columns else None
            
            if token_col and head_col:
                # Build node mapping
                nodes_by_pos = {}
                for idx, row in sentence_data.iterrows():
                    token = str(row[token_col]).strip()
                    head = str(row[head_col]).strip() if pd.notna(row[head_col]) else None
                    
                    # Skip punctuation
                    if token in ['.', ',', '!', '?', ';', ':', '"', "'"]:
                        continue
                    
                    node_id = f"{token}_{idx}"
                    nodes_by_pos[idx] = {
                        'token': token,
                        'head': head,
                        'node_id': node_id
                    }
                    G.add_node(node_id)
                
                # Add edges
                token_to_node = {d['token']: d['node_id'] for d in nodes_by_pos.values()}
                root_node = None
                
                for idx, data in nodes_by_pos.items():
                    token = data['token']
                    head = data['head']
                    node_id = data['node_id']
                    
                    is_root = (head is None) or (head == token) or (head not in token_to_node) or (head == 'ROOT')
                    if is_root:
                        if root_node is None:
                            root_node = node_id
                        continue
                    
                    head_node = token_to_node[head]
                    if head_node != node_id:
                        G.add_edge(head_node, node_id)
                
                # Create layout
                try:
                    if root_node and root_node in G.nodes():
                        pos = nx.spring_layout(G, k=2, iterations=50, seed=42)
                    else:
                        pos = nx.spring_layout(G, k=2, iterations=50, seed=42)
                except:
                    pos = nx.random_layout(G, seed=42)
                
                # Create plotly figure
                edge_trace = []
                for edge in G.edges():
                    if edge[0] in pos and edge[1] in pos:
                        x0, y0 = pos[edge[0]]
                        x1, y1 = pos[edge[1]]
                        edge_trace.append(
                            go.Scatter(
                                x=[x0, x1, None],
                                y=[y0, y1, None],
                                mode='lines',
                                line=dict(width=2, color='rgba(168, 85, 247, 0.6)'),
                                hoverinfo='none',
                                showlegend=False
                            )
                        )
                
                # Clean labels
                labels = {node: node.rsplit('_', 1)[0] for node in G.nodes()}
                
                node_trace = go.Scatter(
                    x=[pos[node][0] for node in G.nodes() if node in pos],
                    y=[pos[node][1] for node in G.nodes() if node in pos],
                    mode='markers+text',
                    text=[labels[node] for node in G.nodes() if node in pos],
                    textposition='top center',
                    marker=dict(
                        size=20,
                        color='#6366f1',
                        line=dict(width=2, color='white')
                    ),
                    textfont=dict(size=12, color='white'),
                    hoverinfo='text',
                    showlegend=False
                )
                
                fig = go.Figure(data=edge_trace + [node_trace])
                
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    height=500,
                    margin=dict(l=20, r=20, t=20, b=20),
                    hovermode='closest'
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Required columns not found in dependency parse data")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 📊 Tree Metrics")
        
        if not sentence_data.empty:
            # Calculate metrics
            num_tokens = len(sentence_data)
            
            st.metric("Total Tokens", num_tokens)
            
            dep_col = 'dep' if 'dep' in sentence_data.columns else 'dependency' if 'dependency' in sentence_data.columns else None
            if dep_col:
                num_deps = sentence_data[dep_col].nunique()
                st.metric("Unique Dependencies", num_deps)
            
            if 'pos' in sentence_data.columns:
                st.metric("POS Tags", sentence_data['pos'].nunique())
            
            st.markdown("#### Dependency Types")
            if dep_col:
                dep_counts = sentence_data[dep_col].value_counts().head(5)
                for dep, count in dep_counts.items():
                    st.write(f"**{dep}**: {count}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Detailed token information
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 📋 Token Details")
    
    if not sentence_data.empty:
        # Display token information in a table
        token_col = 'token' if 'token' in sentence_data.columns else 'word' if 'word' in sentence_data.columns else None
        display_cols = []
        
        if token_col:
            display_cols.append(token_col)
        if 'pos' in sentence_data.columns:
            display_cols.append('pos')
        dep_col = 'dep' if 'dep' in sentence_data.columns else 'dependency' if 'dependency' in sentence_data.columns else None
        if dep_col:
            display_cols.append(dep_col)
        if 'head' in sentence_data.columns:
            display_cols.append('head')
        
        if display_cols:
            st.dataframe(
                sentence_data[display_cols],
                use_container_width=True,
                hide_index=True
            )
    
    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.warning("No dependency parse data available. Please run the parsing scripts first.")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# Educational section
st.markdown("""
<div style="text-align: center; margin: 40px 0 20px;">
    <div class="section-header" style="font-size: 2.5rem;">Understanding Syntax Trees</div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🔗</div>
        <div class="feature-title">Dependencies</div>
        <div class="feature-desc">
            Arrows show grammatical relationships between words in the sentence
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🏷️</div>
        <div class="feature-title">POS Tags</div>
        <div class="feature-desc">
            Part-of-speech tags identify the grammatical role of each word
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🌲</div>
        <div class="feature-title">Tree Structure</div>
        <div class="feature-desc">
            Hierarchical organization reveals sentence complexity and structure
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

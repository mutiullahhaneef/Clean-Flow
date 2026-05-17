# app.py - FINAL WORKING VERSION
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO, StringIO
import base64
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="AI Data Cleaner",
    page_icon="🧹",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize theme in session state
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'

def get_theme_css(theme='light'):
    """Generate CSS based on selected theme"""
    if theme == 'dark':
        return """
<style>
    /* Dark theme base */
    .stApp {
        background: linear-gradient(135deg, #0a0e1a 0%, #1a1f2e 100%);
        transition: background 0.5s ease;
    }
    
    /* Main header with gradient text */
    .main-header {
        font-size: 3rem;
        background: linear-gradient(135deg, #00d4ff 0%, #0080ff 50%, #00ff88 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 800;
        letter-spacing: -1px;
        animation: fadeInDown 0.8s ease-out;
    }
    
    /* Section headers */
    .section-header {
        font-size: 1.8rem;
        color: #00d4ff;
        margin-top: 2rem;
        margin-bottom: 1rem;
        font-weight: 700;
        text-shadow: 0 0 20px rgba(0, 212, 255, 0.3);
    }
    
    /* Glassmorphism cards */
    .success-box, .warning-box, .info-box, .error-box {
        backdrop-filter: blur(16px) saturate(180%);
        -webkit-backdrop-filter: blur(16px) saturate(180%);
        border-radius: 16px;
        padding: 20px;
        margin: 15px 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        transition: all 0.3s ease;
        animation: fadeIn 0.5s ease-out;
    }
    
    .success-box {
        background: rgba(0, 255, 136, 0.1);
        border-left: 4px solid #00ff88;
    }
    
    .warning-box {
        background: rgba(255, 183, 0, 0.1);
        border-left: 4px solid #ffb700;
    }
    
    .info-box {
        background: rgba(0, 212, 255, 0.1);
        border-left: 4px solid #00d4ff;
    }
    
    .error-box {
        background: rgba(255, 51, 102, 0.1);
        border-left: 4px solid #ff3366;
    }
    
    .success-box:hover, .warning-box:hover, .info-box:hover, .error-box:hover {
        transform: translateY(-2px) scale(1.01);
        box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.5);
    }
    
    /* Streamlit component styling */
    .stButton > button {
        background: linear-gradient(135deg, #00d4ff 0%, #0080ff 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 32px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 15px rgba(0, 212, 255, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
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
    
    .stButton > button:hover::before {
        width: 300px;
        height: 300px;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 8px 25px rgba(0, 212, 255, 0.5);
        background: linear-gradient(135deg, #00e4ff 0%, #0090ff 100%);
    }
    
    .stButton > button:active {
        transform: translateY(-1px) scale(0.98);
    }
    
    /* Dataframe styling */
    .dataframe {
        background: rgba(15, 20, 30, 0.8) !important;
        border-radius: 12px;
        overflow: hidden;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f1419 0%, #1a1f2e 100%);
        border-right: 1px solid rgba(0, 212, 255, 0.2);
    }
    
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #00d4ff;
        text-shadow: 0 0 10px rgba(0, 212, 255, 0.3);
    }
    
    /* Metric cards */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        color: #00d4ff;
        font-weight: 700;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(15, 20, 30, 0.5);
        border-radius: 12px;
        padding: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 8px;
        color: #8b9dc3;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #00d4ff 0%, #0080ff 100%);
        color: white;
        box-shadow: 0 4px 12px rgba(0, 212, 255, 0.3);
    }
    
    /* Input fields */
    .stSelectbox, .stTextInput, .stNumberInput {
        border-radius: 8px;
    }
    
    /* File uploader */
    [data-testid="stFileUploader"] {
        background: rgba(15, 20, 30, 0.5);
        border: 2px dashed rgba(0, 212, 255, 0.3);
        border-radius: 12px;
        padding: 20px;
        transition: all 0.3s ease;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: rgba(0, 212, 255, 0.6);
        background: rgba(15, 20, 30, 0.7);
        transform: translateY(-2px);
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #0f1419;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #00d4ff 0%, #0080ff 100%);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #00e4ff 0%, #0090ff 100%);
    }
    
    /* Text colors */
    p, li, label, .stMarkdown {
        color: #e0e6ed !important;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #00d4ff !important;
    }
    
    /* Download link styling */
    a {
        color: #00d4ff;
        text-decoration: none;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    a:hover {
        color: #00ff88;
        text-shadow: 0 0 10px rgba(0, 255, 136, 0.5);
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.8; }
    }
</style>
"""
    else:  # Light theme
        return """
<style>
    /* Light theme base */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e9ecef 100%);
        transition: background 0.5s ease;
    }
    
    /* Main header with gradient text */
    .main-header {
        font-size: 3rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 800;
        letter-spacing: -1px;
        animation: fadeInDown 0.8s ease-out;
    }
    
    /* Section headers */
    .section-header {
        font-size: 1.8rem;
        color: #667eea;
        margin-top: 2rem;
        margin-bottom: 1rem;
        font-weight: 700;
    }
    
    /* Beautiful cards */
    .success-box, .warning-box, .info-box, .error-box {
        border-radius: 16px;
        padding: 20px;
        margin: 15px 0;
        transition: all 0.3s ease;
        animation: fadeIn 0.5s ease-out;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    }
    
    .success-box {
        background: linear-gradient(135deg, #d4fc79 0%, #96e6a1 100%);
        border-left: 4px solid #10b981;
    }
    
    .warning-box {
        background: linear-gradient(135deg, #ffeaa7 0%, #fdcb6e 100%);
        border-left: 4px solid #f59e0b;
    }
    
    .info-box {
        background: linear-gradient(135deg, #a8edea 0%, #74ebd5 100%);
        border-left: 4px solid #06b6d4;
    }
    
    .error-box {
        background: linear-gradient(135deg, #ffeaa7 0%, #ffcccc 100%);
        border-left: 4px solid #ef4444;
    }
    
    .success-box:hover, .warning-box:hover, .info-box:hover, .error-box:hover {
        transform: translateY(-3px) scale(1.01);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
    }
    
    /* Streamlit component styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 32px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.4);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }
    
    .stButton > button:hover::before {
        width: 300px;
        height: 300px;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
        background: linear-gradient(135deg, #7c93ee 0%, #8b5fbd 100%);
    }
    
    .stButton > button:active {
        transform: translateY(-1px) scale(0.98);
    }
    
    /* Dataframe styling */
    .dataframe {
        background: rgba(255, 255, 255, 0.9) !important;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ffffff 0%, #f8f9fa 100%);
        border-right: 1px solid rgba(102, 126, 234, 0.2);
    }
    
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #667eea;
    }
    
    /* Metric cards */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        color: #667eea;
        font-weight: 700;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(255, 255, 255, 0.5);
        border-radius: 12px;
        padding: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 8px;
        color: #6b7280;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    
    /* Input fields */
    .stSelectbox, .stTextInput, .stNumberInput {
        border-radius: 8px;
    }
    
    /* File uploader */
    [data-testid="stFileUploader"] {
        background: rgba(255, 255, 255, 0.8);
        border: 2px dashed rgba(102, 126, 234, 0.4);
        border-radius: 12px;
        padding: 20px;
        transition: all 0.3s ease;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: rgba(102, 126, 234, 0.7);
        background: rgba(255, 255, 255, 1);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #7c93ee 0%, #8b5fbd 100%);
    }
    
    /* Text colors */
    p, li, label, .stMarkdown {
        color: #374151 !important;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #667eea !important;
    }
    
    /* Download link styling */
    a {
        color: #667eea;
        text-decoration: none;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    a:hover {
        color: #764ba2;
        text-decoration: underline;
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.8; }
    }
</style>
"""

# Apply theme CSS
st.markdown(get_theme_css(st.session_state.theme), unsafe_allow_html=True)

class DataCleaner:
    def __init__(self, df):
        self.df = df.copy()
        self.original_df = df.copy()
        self.cleaning_log = []
        
    def detect_missing_values(self):
        """Detect missing values in the dataset"""
        missing_data = self.df.isnull().sum()
        missing_percent = (missing_data / len(self.df)) * 100
        missing_info = pd.DataFrame({
            'Column': missing_data.index,
            'Missing_Count': missing_data.values,
            'Missing_Percent': missing_percent.values
        })
        return missing_info[missing_info['Missing_Count'] > 0]
    
    def handle_missing_values(self, strategy='drop', fill_value=None, specific_columns=None):
        """Handle missing values based on selected strategy"""
        original_missing = self.df.isnull().sum().sum()
        
        if strategy == 'drop':
            self.df = self.df.dropna()
            self.cleaning_log.append(f"Dropped rows with missing values. Removed {original_missing - self.df.isnull().sum().sum()} missing values")
        
        elif strategy == 'fill':
            if specific_columns:
                for col in specific_columns:
                    if self.df[col].dtype in ['int64', 'float64']:
                        fill_val = self.df[col].mean() if fill_value == 'mean' else self.df[col].median()
                    else:
                        fill_val = self.df[col].mode()[0] if len(self.df[col].mode()) > 0 else 'Unknown'
                    self.df[col].fillna(fill_val, inplace=True)
                    self.cleaning_log.append(f"Filled missing values in {col} with {fill_val}")
            else:
                for col in self.df.columns:
                    if self.df[col].isnull().any():
                        if self.df[col].dtype in ['int64', 'float64']:
                            fill_val = self.df[col].mean() if fill_value == 'mean' else self.df[col].median()
                        else:
                            fill_val = self.df[col].mode()[0] if len(self.df[col].mode()) > 0 else 'Unknown'
                        self.df[col].fillna(fill_val, inplace=True)
    
    def detect_duplicates(self):
        """Detect duplicate rows"""
        return self.df.duplicated().sum()
    
    def remove_duplicates(self):
        """Remove duplicate rows"""
        original_count = len(self.df)
        self.df = self.df.drop_duplicates()
        removed_count = original_count - len(self.df)
        if removed_count > 0:
            self.cleaning_log.append(f"Removed {removed_count} duplicate rows")
        return removed_count
    
    def detect_outliers_iqr(self, column):
        """Detect outliers using IQR method"""
        if self.df[column].dtype in ['int64', 'float64']:
            Q1 = self.df[column].quantile(0.25)
            Q3 = self.df[column].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            outliers = self.df[(self.df[column] < lower_bound) | (self.df[column] > upper_bound)]
            return len(outliers), lower_bound, upper_bound
        return 0, None, None
    
    def handle_outliers(self, column, method='cap', custom_bounds=None):
        """Handle outliers in numerical columns"""
        if self.df[column].dtype in ['int64', 'float64']:
            Q1 = self.df[column].quantile(0.25)
            Q3 = self.df[column].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            if method == 'cap':
                self.df[column] = np.where(self.df[column] < lower_bound, lower_bound, 
                                         np.where(self.df[column] > upper_bound, upper_bound, self.df[column]))
                self.cleaning_log.append(f"Capped outliers in {column} using IQR method")
            
            elif method == 'remove':
                original_len = len(self.df)
                self.df = self.df[(self.df[column] >= lower_bound) & (self.df[column] <= upper_bound)]
                removed = original_len - len(self.df)
                self.cleaning_log.append(f"Removed {removed} rows with outliers in {column}")
    
    def generate_ai_suggestions(self):
        """Generate AI-powered cleaning suggestions"""
        suggestions = []
        
        # Analyze missing values
        missing_info = self.detect_missing_values()
        if not missing_info.empty:
            for _, row in missing_info.iterrows():
                col = row['Column']
                percent = row['Missing_Percent']
                if percent > 50:
                    suggestions.append(f"🚨 Column '{col}' has {percent:.1f}% missing values - consider dropping this column")
                elif percent > 20:
                    suggestions.append(f"⚠️ Column '{col}' has {percent:.1f}% missing values - consider imputation or investigation")
                else:
                    dtype = self.df[col].dtype
                    if dtype in ['int64', 'float64']:
                        suggestions.append(f" Column '{col}' has {percent:.1f}% missing values - fill with median")
                    else:
                        suggestions.append(f" Column '{col}' has {percent:.1f}% missing values - fill with mode")
        
        # Analyze outliers in numerical columns
        numerical_cols = self.df.select_dtypes(include=['int64', 'float64']).columns
        for col in numerical_cols:
            outlier_count, lower, upper = self.detect_outliers_iqr(col)
            if outlier_count > 0:
                percent = (outlier_count / len(self.df)) * 100
                if percent > 10:
                    suggestions.append(f"🚨 Column '{col}' has {outlier_count} outliers ({percent:.1f}%) - consider capping or removal")
                else:
                    suggestions.append(f" Column '{col}' has {outlier_count} outliers - consider capping at bounds [{lower:.2f}, {upper:.2f}]")
        
        # Check for duplicates
        duplicate_count = self.detect_duplicates()
        if duplicate_count > 0:
            suggestions.append(f" Found {duplicate_count} duplicate rows - recommend removal")
        
        # Data type suggestions
        for col in self.df.columns:
            if self.df[col].dtype == 'object':
                # Check if it might be categorical
                unique_ratio = self.df[col].nunique() / len(self.df)
                if unique_ratio < 0.1:
                    suggestions.append(f"🏷️ Column '{col}' has low cardinality ({self.df[col].nunique()} unique values) - consider converting to category")
        
        return suggestions
    
    def get_summary_stats(self):
        """Get summary statistics for before/after comparison"""
        return {
            'shape': self.df.shape,
            'memory_usage': self.df.memory_usage(deep=True).sum(),
            'total_missing': self.df.isnull().sum().sum(),
            'total_duplicates': self.df.duplicated().sum(),
            'numerical_columns': len(self.df.select_dtypes(include=['int64', 'float64']).columns),
            'categorical_columns': len(self.df.select_dtypes(include=['object']).columns)
        }

def create_download_link(df, filename="cleaned_data.csv"):
    """Create a download link for the cleaned dataframe"""
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">📥 Download Cleaned CSV</a>'
    return href

def get_chart_colors(theme='light'):
    """Get chart colors based on current theme"""
    if theme == 'dark':
        return {
            'background': '#0f1419',
            'text': '#e0e6ed',
            'primary': '#00d4ff',
            'secondary': '#00ff88',
            'accent': '#ff3366',
            'bar_color': '#00d4ff',
            'bar_edge': '#00ff88',
            'grid_color': '#00d4ff',
            'grid_alpha': 0.1
        }
    else:  # light theme
        return {
            'background': '#ffffff',
            'text': '#374151',
            'primary': '#667eea',
            'secondary': '#764ba2',
            'accent': '#ef4444',
            'bar_color': '#667eea',
            'bar_edge': '#764ba2',
            'grid_color': '#e5e7eb',
            'grid_alpha': 0.5
        }

def main():
    # Main header
    st.markdown('<h1 class="main-header">🧹 AI-Powered Data Cleaning Tool</h1>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        # Theme Toggle at the top
        st.markdown("---")
        col1, col2 = st.columns([3, 1])
        with col1:
            theme_label = "🌙 Dark Mode" if st.session_state.theme == 'light' else "☀️ Light Mode"
            st.markdown(f"### {theme_label}")
        with col2:
            if st.button("🔄", key="theme_toggle", help="Toggle theme"):
                st.session_state.theme = 'dark' if st.session_state.theme == 'light' else 'light'
                st.rerun()
        st.markdown("---")
        
        st.header("📁 Data Upload")
        
        # Check if sample data is loaded
        if 'sample_data' in st.session_state:
            uploaded_file = None
            df = pd.read_csv(StringIO(st.session_state.sample_data))
            st.success("✅ Sample data loaded! Switch to main tabs to explore.")
        else:
            uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
        
        if uploaded_file is not None:
            st.success("File uploaded successfully!")
            
        st.header("⚙️ Cleaning Options")
        
        st.subheader("Missing Values")
        missing_strategy = st.selectbox(
            "Handle missing values:",
            ["None", "Drop rows", "Fill with mean/median", "Fill with mode"]
        )
        
        st.subheader("Duplicates")
        remove_duplicates = st.checkbox("Remove duplicate rows", value=True)
        
        st.subheader("Outliers")
        outlier_handling = st.selectbox(
            "Handle outliers:",
            ["None", "Cap using IQR", "Remove outliers"]
        )
    
    # Main content
    if 'sample_data' in st.session_state or uploaded_file is not None:
        try:
            # Load data
            if 'sample_data' in st.session_state:
                df = pd.read_csv(StringIO(st.session_state.sample_data))
                data_source = "sample"
            else:
                df = pd.read_csv(uploaded_file)
                data_source = "uploaded"
            
            cleaner = DataCleaner(df)
            
            # Create tabs for better organization
            tab1, tab2, tab3, tab4, tab5 = st.tabs([
                "📊 Data Overview", 
                " Data Issues", 
                "  AI Suggestions", 
                "⚡ Cleaning Actions",
                " Before/After"
            ])
            
            with tab1:
                st.markdown('<h2 class="section-header">Data Preview</h2>', unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.write("**Dataset Shape:**", df.shape)
                    st.write("**Columns:**", list(df.columns))
                
                with col2:
                    st.write("**Data Types:**")
                    st.write(df.dtypes)
                
                st.subheader("First 10 Rows")
                st.dataframe(df.head(10))
                
                st.subheader("Basic Statistics")
                st.write(df.describe())
            
            with tab2:
                st.markdown('<h2 class="section-header">Data Quality Report</h2>', unsafe_allow_html=True)
                
                # Missing values analysis
                missing_info = cleaner.detect_missing_values()
                if not missing_info.empty:
                    st.subheader("❌ Missing Values")
                    st.dataframe(missing_info)
                    
                    # Visualization with dark theme
                    fig, ax = plt.subplots(figsize=(10, 6), facecolor='#0f1419')
                    ax.set_facecolor('#0f1419')
                    bars = plt.bar(missing_info['Column'], missing_info['Missing_Percent'], 
                                   color='#00d4ff', edgecolor='#00ff88', linewidth=2)
                    plt.xticks(rotation=45, color='#e0e6ed')
                    plt.yticks(color='#e0e6ed')
                    plt.ylabel('Missing Percentage (%)', color='#00d4ff', fontweight='bold')
                    plt.title('Missing Values by Column', color='#00d4ff', fontsize=14, fontweight='bold')
                    ax.spines['bottom'].set_color('#00d4ff')
                    ax.spines['left'].set_color('#00d4ff')
                    ax.spines['top'].set_visible(False)
                    ax.spines['right'].set_visible(False)
                    ax.grid(True, alpha=0.1, color='#00d4ff', linestyle='--')
                    
                    # Add value labels on bars
                    for bar in bars:
                        height = bar.get_height()
                        plt.text(bar.get_x() + bar.get_width()/2., height,
                                f'{height:.1f}%', ha='center', va='bottom', color='#00ff88', fontweight='bold')
                    
                    plt.tight_layout()
                    st.pyplot(fig)
                else:
                    st.markdown('<div class="success-box">✅ No missing values found!</div>', unsafe_allow_html=True)
                
                # Duplicates analysis
                duplicate_count = cleaner.detect_duplicates()
                st.subheader(" Duplicate Rows")
                if duplicate_count > 0:
                    st.markdown(f'<div class="warning-box">⚠️ Found {duplicate_count} duplicate rows</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="success-box">✅ No duplicate rows found!</div>', unsafe_allow_html=True)
                
                # Outliers analysis
                st.subheader("📊 Outliers Detection")
                numerical_cols = df.select_dtypes(include=['int64', 'float64']).columns
                if len(numerical_cols) > 0:
                    outlier_data = []
                    for col in numerical_cols:
                        outlier_count, lower, upper = cleaner.detect_outliers_iqr(col)
                        if outlier_count > 0:
                            outlier_data.append({
                                'Column': col,
                                'Outliers_Count': outlier_count,
                                'Outliers_Percent': (outlier_count / len(df)) * 100,
                                'Lower_Bound': lower,
                                'Upper_Bound': upper
                            })
                    
                    if outlier_data:
                        outlier_df = pd.DataFrame(outlier_data)
                        st.dataframe(outlier_df)
                        
                        # Outlier visualization with dark theme
                        if len(numerical_cols) <= 4:
                            fig, axes = plt.subplots(1, len(numerical_cols), figsize=(15, 5), facecolor='#0f1419')
                            if len(numerical_cols) == 1:
                                axes = [axes]
                            
                            for i, col in enumerate(numerical_cols):
                                axes[i].set_facecolor('#0f1419')
                                bp = axes[i].boxplot(df[col].dropna(), 
                                                     patch_artist=True,
                                                     boxprops=dict(facecolor='#00d4ff', color='#00ff88', linewidth=2),
                                                     whiskerprops=dict(color='#00d4ff', linewidth=1.5),
                                                     capprops=dict(color='#00d4ff', linewidth=1.5),
                                                     medianprops=dict(color='#00ff88', linewidth=2),
                                                     flierprops=dict(markerfacecolor='#ff3366', markeredgecolor='#ff3366', markersize=6))
                                axes[i].set_title(f'Boxplot of {col}', color='#00d4ff', fontweight='bold')
                                axes[i].set_ylabel('Values', color='#00d4ff', fontweight='bold')
                                axes[i].tick_params(colors='#e0e6ed')
                                axes[i].spines['bottom'].set_color('#00d4ff')
                                axes[i].spines['left'].set_color('#00d4ff')
                                axes[i].spines['top'].set_visible(False)
                                axes[i].spines['right'].set_visible(False)
                                axes[i].grid(True, alpha=0.1, color='#00d4ff', linestyle='--')
                            
                            plt.tight_layout()
                            st.pyplot(fig)
                    else:
                        st.markdown('<div class="success-box">✅ No significant outliers detected in numerical columns!</div>', unsafe_allow_html=True)
                else:
                    st.info("No numerical columns found for outlier analysis.")
            
            with tab3:
                st.markdown('<h2 class="section-header">  AI-Powered Cleaning Suggestions</h2>', unsafe_allow_html=True)
                
                suggestions = cleaner.generate_ai_suggestions()
                if suggestions:
                    st.markdown("### Recommended Actions:")
                    for i, suggestion in enumerate(suggestions, 1):
                        st.write(f"{i}. {suggestion}")
                    
                    # Show most critical issues
                    critical_issues = [s for s in suggestions if '🚨' in s]
                    if critical_issues:
                        st.markdown("---")
                        st.markdown("### 🚨 Critical Issues Requiring Attention:")
                        for issue in critical_issues:
                            st.error(issue)
                else:
                    st.markdown('<div class="success-box">🎉 Your data looks clean! No major issues detected.</div>', unsafe_allow_html=True)
            
            with tab4:
                st.markdown('<h2 class="section-header">⚡ Apply Cleaning Actions</h2>', unsafe_allow_html=True)
                
                if st.button("  Apply Automated Cleaning", type="primary"):
                    with st.spinner("Cleaning in progress..."):
                        # Store original state
                        original_shape = cleaner.df.shape
                        
                        # Apply cleaning based on sidebar selections
                        if missing_strategy == "Drop rows":
                            cleaner.handle_missing_values(strategy='drop')
                        elif missing_strategy == "Fill with mean/median":
                            cleaner.handle_missing_values(strategy='fill', fill_value='mean')
                        elif missing_strategy == "Fill with mode":
                            cleaner.handle_missing_values(strategy='fill', fill_value='mode')
                        
                        if remove_duplicates:
                            cleaner.remove_duplicates()
                        
                        if outlier_handling == "Cap using IQR":
                            numerical_cols = cleaner.df.select_dtypes(include=['int64', 'float64']).columns
                            for col in numerical_cols:
                                cleaner.handle_outliers(col, method='cap')
                        elif outlier_handling == "Remove outliers":
            📊 📊 📊 📊 📊 📊 📊 📊 📊 📊 📊 📊 📊 📊 📊 📊 numerical_cols = cleaner.df.select_dtypes(include=['int64', 'float64']).columns
                            for col in numerical_cols:
                                cleaner.handle_outliers(col, method='remove')
                        
                        st.success(f"✅ Cleaning completed! Dataset shape changed from {original_shape} to {cleaner.df.shape}")
                        
                        # Show cleaning log
                        if cleaner.cleaning_log:
                            st.subheader("📋 Cleaning Log")
                            for log_entry in cleaner.cleaning_log:
                                st.write(f"• {log_entry}")
            
            with tab5:
                st.markdown('<h2 class="section-header"> Before vs After Cleaning</h2>', unsafe_allow_html=True)
                
                original_stats = cleaner.get_summary_stats()
                cleaned_stats = cleaner.get_summary_stats()
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Original Data")
                    st.metric("Shape", f"{original_stats['shape']}")
                    st.metric("Total Missing", f"{original_stats['total_missing']}")
                    st.metric("Duplicates", f"{original_stats['total_duplicates']}")
                    st.metric("Memory Usage", f"{original_stats['memory_usage'] / 1024:.2f} KB")
                
                with col2:
                    st.subheader("Cleaned Data")
                    st.metric("Shape", f"{cleaned_stats['shape']}", 
                             delta=f"{cleaned_stats['shape'][0] - original_stats['shape'][0]}")
                    st.metric("Total Missing", f"{cleaned_stats['total_missing']}", 
                             delta=f"{cleaned_stats['total_missing'] - original_stats['total_missing']}")
                    st.metric("Duplicates", f"{cleaned_stats['total_duplicates']}", 
                             delta=f"{cleaned_stats['total_duplicates'] - original_stats['total_duplicates']}")
                    st.metric("Memory Usage", f"{cleaned_stats['memory_usage'] / 1024:.2f} KB", 
                             delta=f"{(cleaned_stats['memory_usage'] - original_stats['memory_usage']) / 1024:.2f} KB")
                
                # Download section
                st.markdown("---")
                st.markdown("### 📥 Download Cleaned Data")
                st.markdown(create_download_link(cleaner.df), unsafe_allow_html=True)
                
                # Show cleaned data preview
                st.subheader("Cleaned Data Preview")
                st.dataframe(cleaner.df.head(10))
        
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")
    
    else:
        # Welcome message when no file is uploaded
        st.markdown("""
        <div class="info-box">
        <h3>Welcome to the AI-Powered Data Cleaning Tool! 🧹</h3>
        <p>This tool helps you automatically clean and prepare your datasets for analysis.</p>
        
        <h4>📋 Features:</h4>
        <ul>
            <li> Automatic detection of missing values, duplicates, and outliers</li>
            <li>  AI-powered cleaning suggestions</li>
            <li>📊 Interactive data visualization</li>
            <li>⚡ One-click automated cleaning</li>
            <li> Before/After comparison</li>
            <li>📥 Export cleaned data</li>
        </ul>
        
        <h4>  How to use:</h4>
        <ol>
            <li>Upload your CSV file using the sidebar</li>
            <li>Review the data quality report</li>
            <li>Check AI suggestions for optimal cleaning</li>
            <li>Apply cleaning actions</li>
            <li>Download your cleaned dataset</li>
        </ol>
        </div>
        """, unsafe_allow_html=True)
        
        # Sample data for testing - SIMPLE AND WORKING VERSION
        st.markdown("### 🧪 Want to test it?")
        st.markdown("Choose one of the sample datasets below to test the tool:")
        
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("📊 Employee Data", use_container_width=True):
                employee_data = """ID,Name,Age,Salary,Department,Join_Date,Experience,City,Performance_Score
1,John Smith,28,50000,IT,2020-01-15,4,New York,85
2,Jane Doe,32,60000,HR,2019-03-20,5,Chicago,92
3,Bob Johnson,45,75000,Finance,2015-06-10,9,New York,78
4,Alice Brown,29,55000,IT,2021-02-28,3,Chicago,88
5,Charlie Wilson,35,65000,Marketing,2018-11-05,6,Los Angeles,76
6,Diana Lee,41,80000,Finance,2016-09-12,8,New York,95
7,John Smith,28,50000,IT,2020-01-15,4,New York,85
8,Mike Davis,26,48000,Sales,2022-01-10,2,Chicago,82
9,Sarah Miller,38,70000,HR,2017-04-22,7,Los Angeles,90
10,Kevin Taylor,52,90000,Finance,2010-08-30,14,New York,87
11,Lisa Anderson,29,,Marketing,2021-07-14,3,Chicago,79
12,Tom Wilson,61,120000,IT,2005-12-01,19,New York,91
13,Emma Garcia,27,52000,Sales,2022-03-18,2,Los Angeles,84
14,Robert Brown,34,62000,Marketing,2019-09-25,5,Chicago,
15,Maria Martinez,31,58000,HR,2020-11-08,4,New York,86
16,Outlier Test,150,1000000,IT,2020-01-01,5,New York,50"""
                st.session_state.sample_data = employee_data
                st.rerun()

        with col2:
            if st.button(" Sales Data", use_container_width=True):
                sales_data = """OrderID,Product,Category,Quantity,Price,Total_Sales,Customer_Age,Customer_Location,Rating,Date
1001,Laptop,Electronics,1,1200,1200,28,New York,4,2024-01-15
1002,Smartphone,Electronics,2,800,1600,34,California,5,2024-01-16
1003,Desk,Office,1,300,300,45,Texas,3,2024-01-17
1004,Chair,Office,4,150,600,29,Florida,4,2024-01-18
1005,Monitor,Electronics,2,250,500,52,New York,5,2024-01-19
1006,Keyboard,Electronics,3,80,240,31,California,4,2024-01-20
1007,Notebook,Office,10,5,50,24,Texas,3,2024-01-21
1008,Tablet,Electronics,1,600,600,38,Florida,5,2024-01-22
1009,Printer,Electronics,1,350,350,41,New York,4,2024-01-23
1010,Scanner,Electronics,1,200,200,36,California,3,2024-01-24
1011,Extreme Product,Electronics,100,50,5000,,Texas,,2024-03-06
1012,Outlier Product,Miscellaneous,2,100000,200000,150,California,1,2024-03-08"""
                st.session_state.sample_data = sales_data
                st.rerun()

        with col3:
            if st.button("🏥 Healthcare Data", use_container_width=True):
                healthcare_data = """PatientID,Name,Age,Gender,BloodPressure,Cholesterol,HeartRate,Temperature,BloodSugar,BMI,Smoker,Diabetes_Risk
P001,John Smith,45,Male,120/80,180,72,98.6,95,24.5,No,Low
P002,Maria Garcia,52,Female,130/85,200,75,98.4,110,26.8,Yes,Medium
P003,Robert Johnson,38,Male,118/78,160,68,98.7,92,23.1,No,Low
P004,Lisa Brown,61,Female,140/90,240,80,98.2,145,29.3,Yes,High
P005,Michael Davis,29,Male,122/79,170,70,98.5,88,22.4,No,Low
P006,Sarah Wilson,47,Female,125/82,190,73,98.3,105,25.6,No,Medium
P007,David Miller,55,Male,135/88,220,78,98.1,135,28.2,Yes,High
P008,Jennifer Taylor,42,Female,128/84,185,74,98.6,98,24.9,No,Low
P009,Outlier Patient,150,Male,,500,200,95.0,300,45.0,Yes,High
P010,Missing Data,,Male,120/80,180,72,98.6,95,24.5,,"""
                st.session_state.sample_data = healthcare_data
                st.rerun()

        # Clear sample data button
        if st.button("🔄 Clear Sample Data", type="secondary"):
            if 'sample_data' in st.session_state:
                del st.session_state.sample_data
            st.rerun()

if __name__ == "__main__":
    main()
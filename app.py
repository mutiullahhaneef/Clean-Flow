
import streamlit as st
import pandas as pd
import os
from io import BytesIO, StringIO

from dotenv import load_dotenv
load_dotenv()

from config.settings import APP_TITLE, APP_ICON, MAX_FILE_SIZE_MB
from config.themes import get_theme_css
from core.ai_engine import AIEngine
from ui.pages import (
    render_overview, render_profiling, render_issues,
    render_ai_assistant, render_cleaning_studio, render_results,
    render_welcome,
)

st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
)

_DEFAULTS = {
    'theme': 'dark',
    'original_df': None,
    'cleaned_df': None,
    'undo_stack': [],
    'cleaning_log': [],
    'cleaning_queue': [],
    'data_source': None,
    'file_name': None,
    'ai_chat_history': [],
}

for key, default in _DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = default


st.markdown(get_theme_css(st.session_state.theme), unsafe_allow_html=True)

# Branded splash screen — auto-fades after 1.8s
st.markdown("""
<style>
  #cf-splash {
    position: fixed;
    inset: 0;
    z-index: 99999;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background: #0f172a;
    animation: splash-fade 0.6s ease-out 1.2s forwards;
    pointer-events: none;
  }
  @keyframes splash-fade {
    0%   { opacity: 1; visibility: visible; }
    100% { opacity: 0; visibility: hidden;  }
  }
  #cf-splash .cf-logo-ring {
    width: 90px; height: 90px;
    border-radius: 50%;
    background: linear-gradient(135deg, #38bdf8, #3b82f6, #2dd4bf);
    display: flex; align-items: center; justify-content: center;
    font-size: 2.6rem;
    box-shadow: 0 0 40px rgba(56,189,248,0.55), 0 0 80px rgba(56,189,248,0.25);
    animation: cf-pulse 1.4s ease-in-out infinite;
    margin-bottom: 24px;
  }
  @keyframes cf-pulse {
    0%,100% { transform: scale(1);    box-shadow: 0 0 40px rgba(56,189,248,0.55); }
    50%      { transform: scale(1.07); box-shadow: 0 0 60px rgba(56,189,248,0.80); }
  }
  #cf-splash .cf-title {
    font-family: 'Inter', sans-serif;
    font-size: 1.85rem;
    font-weight: 800;
    letter-spacing: -1px;
    background: linear-gradient(135deg, #38bdf8 0%, #3b82f6 50%, #2dd4bf 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 6px;
  }
  #cf-splash .cf-sub {
    font-family: 'Inter', sans-serif;
    font-size: 0.85rem;
    color: #64748b;
    letter-spacing: 2px;
    text-transform: uppercase;
    font-weight: 500;
    margin-bottom: 36px;
  }
  #cf-splash .cf-bar-track {
    width: 200px; height: 3px;
    background: #1e293b;
    border-radius: 99px;
    overflow: hidden;
  }
  #cf-splash .cf-bar-fill {
    height: 100%;
    border-radius: 99px;
    background: linear-gradient(90deg, #38bdf8, #3b82f6, #2dd4bf);
    animation: cf-load 1.15s cubic-bezier(0.4,0,0.2,1) forwards;
  }
  @keyframes cf-load {
    from { width: 0%; }
    to   { width: 100%; }
  }
</style>
<div id="cf-splash">
  <div class="cf-logo-ring">CF</div>
  <div class="cf-title">CleanFlow AI</div>
  <div class="cf-sub">Powered by Gemini</div>
  <div class="cf-bar-track"><div class="cf-bar-fill"></div></div>
</div>
""", unsafe_allow_html=True)


@st.cache_resource(show_spinner=False)
def _init_ai_engine():
    api_key = os.getenv('GOOGLE_API_KEY')
    return AIEngine(api_key)

ai_engine = _init_ai_engine()


@st.cache_data(show_spinner=False)
def _load_csv(file_bytes, file_name):
    """Parse CSV with automatic encoding detection."""
    try:
        import chardet
        detected = chardet.detect(file_bytes[:10000])
        encoding = detected.get('encoding', 'utf-8') or 'utf-8'
    except Exception:
        encoding = 'utf-8'

    for enc in [encoding, 'utf-8', 'latin-1', 'cp1252']:
        try:
            return pd.read_csv(BytesIO(file_bytes), encoding=enc)
        except Exception:
            continue

    raise ValueError(f"Could not parse '{file_name}' with any supported encoding.")


def main():
    st.markdown(
        f'<h1 class="main-header">{APP_TITLE}</h1>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p class="sub-header">Powered by Gemini AI</p>',
        unsafe_allow_html=True,
    )

    with st.sidebar:
        st.markdown(f"## {APP_TITLE}")
        st.markdown("---")

        label = "Switch to Dark Mode" if st.session_state.theme == 'light' else "Switch to Light Mode"
        if st.button(label, key="theme_toggle", use_container_width=True):
            st.session_state.theme = 'dark' if st.session_state.theme == 'light' else 'light'
            st.rerun()
        st.markdown("---")

        st.header("Upload Data")
        uploaded_file = st.file_uploader(
            "Drop a CSV file here",
            type=['csv', 'tsv', 'txt'],
            key='file_uploader',
        )

        if uploaded_file is not None:
            file_bytes = uploaded_file.getvalue()
            file_size_mb = len(file_bytes) / (1024 * 1024)

            if file_size_mb > MAX_FILE_SIZE_MB:
                st.error(f"File too large ({file_size_mb:.1f} MB). Max: {MAX_FILE_SIZE_MB} MB.")
            elif st.session_state.file_name != uploaded_file.name:
                try:
                    with st.spinner("Loading dataset..."):
                        df = _load_csv(file_bytes, uploaded_file.name)
                    st.session_state.original_df = df.copy()
                    st.session_state.cleaned_df = df.copy()
                    st.session_state.file_name = uploaded_file.name
                    st.session_state.data_source = 'uploaded'
                    st.session_state.cleaning_log = []
                    st.session_state.undo_stack = []
                    st.session_state.ai_chat_history = []
                    if 'ai_suggestions' in st.session_state:
                        del st.session_state.ai_suggestions
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed to load file: {e}")

        if st.session_state.original_df is not None:
            st.markdown("---")
            st.markdown(f"** {st.session_state.file_name}**")
            df = st.session_state.cleaned_df
            st.caption(f"{df.shape[0]:,} rows × {df.shape[1]} columns")
            missing = df.isnull().sum().sum()
            dups = df.duplicated().sum()
            if missing > 0:
                st.caption(f"{missing:,} missing cells")
            if dups > 0:
                st.caption(f"{dups} duplicates")

            log = st.session_state.get('cleaning_log', [])
            if log:
                st.markdown("---")
                st.markdown("**Recent Actions**")
                for entry in log[-5:]:
                    st.caption(entry)

        st.markdown("---")
        if ai_engine.available:
            st.success("Gemini AI Connected")
        else:
            st.warning("AI Offline — add API key to .env")

        st.markdown("---")
        st.caption("CleanFlow AI")
        st.caption("Built by [Mutiullah](https://www.mutiullah.dev)")

    if st.session_state.original_df is not None:
        theme = st.session_state.theme

        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "Overview",
            "Profiling",
            "Issues",
            "Cleaning",
            "Results",
        ])

        with tab1:
            try:
                render_overview(theme)
            except Exception as e:
                st.error(f"Error loading Overview tab: {e}")
        with tab2:
            try:
                render_profiling(theme)
            except Exception as e:
                st.error(f"Error loading Profiling tab: {e}")
        with tab3:
            try:
                render_issues(theme)
            except Exception as e:
                st.error(f"Error loading Issues tab: {e}")
        with tab4:
            try:
                render_ai_assistant(ai_engine, theme)
                st.markdown("---")
                render_cleaning_studio(theme)
            except Exception as e:
                st.error(f"Error loading Cleaning tab: {e}")
        with tab5:
            try:
                render_results(theme)
            except Exception as e:
                st.error(f"Error loading Results tab: {e}")
    else:
        render_welcome()


if __name__ == "__main__":
    main()
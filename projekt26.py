import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import pydeck as pdk
import json
import requests
from streamlit_lottie import st_lottie
import os
import base64
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import io
from datetime import datetime, timedelta

# Initialize session state for navigation and other features
if "current_page" not in st.session_state:
    st.session_state.current_page = "overview"
if "show_map" not in st.session_state:
    st.session_state.show_map = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "query" not in st.session_state:
    st.session_state.query = ""

# Page config
st.set_page_config(
    page_title="Projekt 26 - Hub Stalowa Wola",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)
# Custom CSS for minimalist theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    


    /* Sidebar styles (20vw width) */
    [data-testid="stSidebar"][aria-expanded="true"] {
        width: 20vw !important;
        min-width: 20vw !important;
    }

    /* Media query for smaller devices */
    @media screen and (max-width: 768px) {
        [data-testid="stSidebar"][aria-expanded="true"] {
            width: 50vw !important;
            min-width: 50vw !important;
        }
    }

    @media screen and (max-width: 480px) {
        [data-testid="stSidebar"][aria-expanded="true"] {
            width: 80vw !important;
            min-width: 80vw !important;
        }
    }

    [data-testid="stSidebar"][aria-expanded="true"] h2 {
        font-size: 1.2rem;
        word-wrap: break-word; 
    }
    [data-testid="stSidebar"][aria-expanded="true"] .stButton>button {
        padding: 0.7rem 1.2rem;
        font-size: 0.95rem;
    }

    .main {
        background-color: #FAFAFA;
        color: #1E1E1E;
        padding: 2rem;
    }
    
    h1 {
        font-size: 3.2rem;
        font-weight: 700;
        line-height: 1.2;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    
    h2 {
        font-size: 2.4rem;
        font-weight: 600;
        margin-bottom: 1.2rem;
    }
    
    h3 {
        font-size: 1.8rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    p {
        font-size: 1.1rem;
        line-height: 1.6;
        color: #4A4A4A;
    }
    
    .stButton>button {
        background-color: #1E1E1E;
        color: white;
        border-radius: 50px;
        padding: 0.8rem 2rem;
        font-weight: 500;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #333;
        transform: translateY(-2px);
    }
    
    .metric-card {
        background-color: white;
        padding: 2rem;
        border-radius: 20px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 12px rgba(0,0,0,0.1);
    }
    
    .project-card {
        background-color: white;
        padding: 2rem;
        border-radius: 20px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
    }
    
    .project-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 12px rgba(0,0,0,0.1);
    }
    
    .strategic-point {
        background-color: white;
        padding: 1.5rem;
        border-radius: 20px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
    }
    
    .strategic-point:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 12px rgba(0,0,0,0.1);
    }
    
    .nav-link {
        background-color: #222;
        color: white !important;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        margin: 0.7rem 0;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
        font-weight: 500;
        display: block;
        width: 100%;
    }
    
    .nav-link:hover {
        background-color: #444;
        color: white;
        transform: translateY(-2px);
    }
    
    .stSidebar {
        background-color: #2C3E50; /* Changed from #1E1E1E */
        padding: 2rem 1rem;
    }
    
    div[data-testid="stSidebarNav"] {
        background-color: #2C3E50; /* Changed from #1E1E1E */
        padding-top: 2rem;
    }
    
    /* Logo styling */
    .logo-container {
        width: 150px;
        height: 150px;
        margin: 0 auto 2rem;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    
    .logo-container img {
        width: 100%;
        height: 100%;
        object-fit: contain;
    }
    
    /* Partner logos container */
    .partner-logos {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 4rem;
        margin: 3rem auto;
        flex-wrap: wrap;
        padding: 3rem;
        background: #FAFAFA;
        border-radius: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        max-width: 1200px;
    }
    
    .phase-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 20px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
    }
    
    .phase-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 12px rgba(0,0,0,0.1);
    }
    
    .funding-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 20px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
    }
    
    .funding-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 12px rgba(0,0,0,0.1);
    }
    
    .kpi-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 20px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
    }
    
    .kpi-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 12px rgba(0,0,0,0.1);
    }

    .footer-divider {
        height: 18px;
        width: 1px;
        background-color: #eee;
        margin: 0 0.3rem;
    }

    /* CSS for Centering Partner Logos on Overview Page */
    .partner-logos-container {
        text-align: center; /* Centers the inline-flex .logo-group inside it */
        margin-top: 2rem; /* Space below the 'Dowiedz się więcej' button */
        width: 100%; /* Ensure it takes full width to allow text-align to work on its child */
    }

    .logo-group {
        display: inline-flex; /* Makes the group only as wide as its content */
        justify-content: center; 
        align-items: center;
        gap: 2.5rem; /* Increased gap between logos */
        padding: 1rem 0;
        flex-wrap: wrap;
    }

    .logo-group img {
        max-height: 70px; /* Slightly larger logos */
        width: auto;
        vertical-align: middle;
    }

    /* CSS for Centering Button on Overview Page */
    /* This class is not strictly needed if using st.columns for the button, but kept for potential future use */
    .centered-button-container {
        text-align: center;
        margin-top: 1.5rem; 
        margin-bottom: 2rem; 
    }

    /* Updated CSS for the "Trusted by" Logo Group */
    .logo-group {
        display: flex; 
        justify-content: center;
        align-items: center;
        gap: 2rem; 
        padding: 0; /* Minimal padding */
        flex-wrap: wrap; 
        width: 100%; 
        margin: 0 auto; 
        max-width: 950px; /* Adjusted max-width to better fit content */
        /* filter: grayscale(1); Removed from group, apply to img if needed */
        /* opacity: 0.7; Removed from group, apply to img if needed */
    }

    .logo-group img {
        max-height: 40px; /* Adjusted max-height for a more subtle look */
        width: auto;
        vertical-align: middle;
        filter: grayscale(100%); /* Make logos grayscale */
        opacity: 0.6; /* Slightly muted logos */
    }

    .trusted-by-text {
        font-size: 0.85rem; /* Adjusted font size */
        color: #6c757d; /* Muted text color */
        text-align: center;
        line-height: 1.3;
        max-width: 160px; /* Allow text to wrap appropriately */
        /* margin: 0 1rem; /* Optional: if extra horizontal space around text is needed */
    }

    /* Ensure "Dowiedz się więcej" button text is white */
    .stButton > button div[data-testid="stMarkdownContainer"] p {
        color: white !important;
    }

    /* New CSS for Funding Page UI Enhancement */
    .funding-metric-card {
        background-color: #FFFFFF; /* White background */
        padding: 1.5rem;
        border-radius: 12px; /* Rounded corners like in image */
        box-shadow: 0 4px 12px rgba(0,0,0,0.08); /* Subtle shadow */
        text-align: left; /* Align text to the left */
        margin-bottom: 1rem; /* Space below card */
        height: 100%; /* Make cards in a row equal height */
        position: relative; /* For positioning elements like indicators */
    }

    .funding-metric-card h4 { /* Title of the metric */
        font-size: 0.9rem;
        color: #6c757d; /* Muted color for title */
        margin-bottom: 0.5rem;
        font-weight: 500;
    }

    .funding-metric-card .metric-value { /* The large metric value */
        font-size: 1.8rem; /* Larger font size for value */
        font-weight: 600; /* Bolder */
        color: #212529; /* Dark color for value */
        margin-bottom: 0.25rem;
        line-height: 1.2;
    }

    .funding-metric-card .metric-description { /* Smaller text below value */
        font-size: 0.8rem;
        color: #6c757d;
        margin-bottom: 0;
    }
    
    .metric-indicator-placeholder { /* Placeholder for icon/circular chart */
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background-color: #e9ecef; /* Light gray placeholder */
        position: absolute;
        top: 1.5rem;
        right: 1.5rem;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1rem;
        color: #495057;
    }

    .funding-section-card {
        background-color: #FFFFFF;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        margin-bottom: 2rem; /* More space between section cards */
    }

    .funding-section-card h3 { /* Section titles */
        font-size: 1.5rem; /* Larger title for sections */
        font-weight: 600;
        margin-bottom: 1.5rem; /* Space below title */
        color: #333;
    }
</style>
""", unsafe_allow_html=True)

# Function to load and encode images
def load_image(image_path):
    try:
        path = Path(image_path)
        if not path.exists():
            st.warning(f"Image file not found: {image_path}")
            return None
        with open(image_path, "rb") as image_file:
            encoded = base64.b64encode(image_file.read()).decode()
            return encoded
    except Exception as e:
        st.warning(f"Error loading image {image_path}: {str(e)}")
        return None

# Load images once at startup with better error handling
def load_partner_images():
    images = {}
    
    # Try to load each image, providing a fallback for missing images
    try:
        images['logo'] = load_image("project_logo.svg") or ""
    except:
        images['logo'] = ""
        
    try:
        images['partner1'] = load_image("partner1.png") or ""
    except:
        images['partner1'] = ""
        
    try:
        images['partner2'] = load_image("partner2.png") or ""
    except:
        images['partner2'] = ""
        
    try:
        images['partner3'] = load_image("partner3.jpg") or ""
    except:
        images['partner3'] = ""
        
    try: 
        images['kul_building'] = load_image("kul.jpg") or "" # ADDED FOR KUL IMAGE
    except:
        images['kul_building'] = ""
        
    try:
        images['hsw'] = load_image("partner4.jpg") or "" # ADDED FOR HSW LOGO
    except:
        images['hsw'] = ""
        
    return images

# Load all images
images = load_partner_images()

# Load and cache document processing with better error handling
@st.cache_resource
def load_document():
    try:
        doc_path = Path("Stalowa Wola_ Kosmos i Obronność_.docx")
        if not doc_path.exists():
            return ["Dokument nie został znaleziony. Sprawdź, czy plik DOCX istnieje w katalogu projektu."]
        
        doc = Document("Stalowa Wola_ Kosmos i Obronność_.docx")
        return [para.text for para in doc.paragraphs if para.text.strip()]
    except Exception as e:
        return [f"Błąd podczas ładowania dokumentu: {str(e)}"]

@st.cache_resource
def setup_rag():
    try:
        doc_contents = load_document()
        if len(doc_contents) == 1 and (doc_contents[0].startswith("Dokument nie został znaleziony") or 
                                       doc_contents[0].startswith("Błąd podczas ładowania")):
            # Return a simple QA chain that just returns the error message
            class SimpleQA:
                def __init__(self, error_msg):
                    self.error_msg = error_msg
                def run(self, query):
                    return self.error_msg
            
            return SimpleQA(doc_contents[0])
        
        # If document was loaded successfully, proceed with normal RAG setup
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = text_splitter.split_text("\n".join(doc_contents))
        
        try:
            embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
            vectorstore = FAISS.from_texts(chunks, embeddings)
            
            # Check if OpenAI API key is configured
            openai_api_key = os.environ.get("OPENAI_API_KEY")
            if not openai_api_key:
                return SimpleQA("OpenAI API Key nie został skonfigurowany. Chatbot wymaga klucza API do działania.")
                
            return RetrievalQA.from_chain_type(
                llm=OpenAI(temperature=0), 
                chain_type="stuff", 
                retriever=vectorstore.as_retriever()
            )
        except Exception as e:
            return SimpleQA(f"Błąd podczas konfiguracji RAG: {str(e)}")
            
    except Exception as e:
        class SimpleQA:
            def __init__(self, error_msg):
                self.error_msg = error_msg
            def run(self, query):
                return self.error_msg
        
        return SimpleQA(f"Błąd podczas przetwarzania dokumentu: {str(e)}")

# Load Lottie animations
def load_lottie_url(url):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# Setup sidebar navigation
st.sidebar.markdown("""
<div class="logo-container">
    <div style="font-size: 3rem; text-align: center; color: white;">🚀</div>
</div>
<h2 style="color: white; text-align: center; margin-bottom: 2rem; font-size: 1.3rem;">Hub Technologii<br>Stalowa Wola</h2>
""", unsafe_allow_html=True)

# Navigation links
st.sidebar.markdown("<div style='margin-bottom: 1.5rem;'></div>", unsafe_allow_html=True)

# Overview link
if st.sidebar.button("Strona główna", key="overview_btn", 
                  help="Przejdź do strony głównej", 
                  on_click=lambda: setattr(st.session_state, "current_page", "overview")):
    st.session_state.current_page = "overview"

# Summary link
if st.sidebar.button("Podsumowanie i SWOT", key="summary_btn",
                  help="Przejdź do podsumowania projektu i analizy SWOT",
                  on_click=lambda: setattr(st.session_state, "current_page", "summary")):
    st.session_state.current_page = "summary"

# Projects link
if st.sidebar.button("Projekty Flagowe", key="projects_btn", 
                  help="Przejdź do opisu projektów flagowych", 
                  on_click=lambda: setattr(st.session_state, "current_page", "projects")):
    st.session_state.current_page = "projects"

# Partners link
if st.sidebar.button("Partnerzy", key="partners_btn", 
                  help="Przejdź do sekcji partnerów", 
                  on_click=lambda: setattr(st.session_state, "current_page", "partners")):
    st.session_state.current_page = "partners"

# Funding link
if st.sidebar.button("Finansowanie", key="funding_btn", 
                  help="Przejdź do sekcji finansowania", 
                  on_click=lambda: setattr(st.session_state, "current_page", "funding")):
    st.session_state.current_page = "funding"

# KPI link
if st.sidebar.button("KPI", key="kpi_btn", 
                  help="Przejdź do wskaźników efektywności", 
                  on_click=lambda: setattr(st.session_state, "current_page", "kpi")):
    st.session_state.current_page = "kpi"

# Implementation Plan link (new page)
if st.sidebar.button("Plan Wdrożenia", key="implementation_btn", 
                  help="Przejdź do planu wdrożenia", 
                  on_click=lambda: setattr(st.session_state, "current_page", "implementation")):
    st.session_state.current_page = "implementation"

# Strategic Analysis link (new page)
if st.sidebar.button("Analiza Strategiczna", key="strategy_btn", 
                  help="Przejdź do analizy strategicznej", 
                  on_click=lambda: setattr(st.session_state, "current_page", "strategy")):
    st.session_state.current_page = "strategy"

# Contact link
if st.sidebar.button("Kontakt", key="contact_btn", 
                  help="Przejdź do sekcji kontaktowej", 
                  on_click=lambda: setattr(st.session_state, "current_page", "contact")):
    st.session_state.current_page = "contact"

# Additional space
st.sidebar.markdown("<br>", unsafe_allow_html=True)
st.sidebar.markdown("<hr style='border-color: #444;'>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='color: #aaa; text-align: center;'>© 2026 Konsorcjum Innowacji Stalowa Wola</p>", unsafe_allow_html=True)

# Main content based on navigation
def render_page():
    if st.session_state.current_page == "overview":
        render_overview_page()
    elif st.session_state.current_page == "summary":
        render_summary_page()
    elif st.session_state.current_page == "projects":
        render_projects_page()
    elif st.session_state.current_page == "partners":
        render_partners_section()
    elif st.session_state.current_page == "funding":
        render_funding_page()
    elif st.session_state.current_page == "kpi":
        render_kpi_page()
    elif st.session_state.current_page == "implementation":
        render_implementation_page()
    elif st.session_state.current_page == "strategy":
        render_strategy_page()
    elif st.session_state.current_page == "contact":
        render_contact_page()

# Individual page rendering functions
def render_overview_page():
    # Hero Section with minimalist design
    if images.get('logo'):
        project_logo_html = f'<img src="data:image/svg+xml;base64,{images["logo"]}" alt="Project Logo" style="width: 100px; height: 100px; border-radius: 15%; object-fit: cover; margin-bottom: 0.5rem;">'
    else:
        project_logo_html = '<div style="height: 100px; width: 100px; background-color: #f0f0f0; border-radius: 15%; display: flex; justify-content: center; align-items: center; margin: 0 auto 0.5rem;"><span style="font-size: 40px;">🚀</span></div>'
    
    st.markdown(f"""
    <div style="text-align: center; padding: 2rem 0 1rem;">
        {project_logo_html}
        <h1 style="font-size: 2.5rem; font-weight: 700; margin-bottom: 0.8rem;">Stalowa Wola Projekt 26</h1>
        <p style="font-size: 1.2rem; color: #666; max-width: 600px; margin: 0 auto 1.5rem; line-height: 1.6;">
            Hub Technologii Podwójnego Zastosowania
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Centered "Dowiedz się więcej" button
    cols_button = st.columns([2, 1, 2]) # Create 3 columns, button in the middle one
    with cols_button[1]:
        if st.button("Dowiedz się więcej", key="overview_to_summary_button", use_container_width=True):
            st.session_state.current_page = "summary"
            st.rerun()

    # "Trusted by" Logos Section - using loaded partner images from the 'images' dictionary
    partner_logo_elements = []
    if images.get("partner1"): # Assumes partner1.png is loaded
        partner_logo_elements.append(f'<img src="data:image/png;base64,{images["partner1"]}" alt="Partner Logo: partner1.png">')
    if images.get("partner2"): # Assumes partner2.png is loaded
        partner_logo_elements.append(f'<img src="data:image/png;base64,{images["partner2"]}" alt="Partner Logo: partner2.png">')
    
    if images.get("partner3"): # Assumes partner3.jpg is loaded
        partner_logo_elements.append(f'<img src="data:image/jpeg;base64,{images["partner3"]}" alt="Partner Logo: partner3.jpg">')
    
    # The .logo-group CSS (flex, justify-content: center, align-items: center, gap, wrap)
    # will handle the layout of these elements. If an image is not loaded, its tag won't be added.
    all_logo_elements_html = "\n".join(partner_logo_elements)

    st.markdown(f"""
    <div class="logo-group" style="margin-top: 2.5rem; margin-bottom: 2rem;">
        {all_logo_elements_html}
    </div>
    """, unsafe_allow_html=True)

    # Services/Focus Areas with clean grid layout
    st.markdown("""
    <div style="margin: 3rem auto; text-align: center; max-width: 1200px;">
        <h2 style="font-size: 2rem; font-weight: 600; margin-bottom: 1rem;">Nasze Obszary Działania</h2>
        <p style="color: #666; margin-bottom: 3rem;">Koncentrujemy się na kluczowych technologiach przyszłości</p>
    </div>
    """, unsafe_allow_html=True)

    # Service grid with 2x2 layout for better readability
    focus_cols1 = st.columns(2)
    with focus_cols1[0]:
        st.markdown("""
        <div style="background-color: white; padding: 2rem; border-radius: 20px; height: 100%; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
            <div style="font-size: 2rem; margin-bottom: 1rem;">🛰️</div>
            <h3 style="font-size: 1.3rem; font-weight: 600; margin-bottom: 1rem;">Technologie Kosmiczne</h3>
            <p style="color: #666; line-height: 1.6;">
                Rozwój systemów satelitarnych, platform autonomicznych i technologii komunikacji kosmicznej. Obejmuje to projektowanie i wdrażanie innowacyjnych rozwiązań dla obserwacji Ziemi (np. polskie satelity optoelektroniczne i radarowe), nawigacji satelitarnej oraz autonomicznych systemów wsparcia misji, takich jak drony i roboty lądowe do inspekcji i napraw infrastruktury orbitalnej.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with focus_cols1[1]:
        st.markdown("""
        <div style="background-color: white; padding: 2rem; border-radius: 20px; height: 100%; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
            <div style="font-size: 2rem; margin-bottom: 1rem;">🔬</div>
            <h3 style="font-size: 1.3rem; font-weight: 600; margin-bottom: 1rem;">Badania i Rozwój</h3>
            <p style="color: #666; line-height: 1.6;">
                Zaawansowane badania nad materiałami i systemami o podwójnym zastosowaniu (dual-use), w tym inteligentnymi materiałami samonaprawiającymi się (np. nanokompozyty z mikrokapsułkami) oraz ultralekkimi stopami metali dla konstrukcji kosmicznych i wojskowych. Rozwój algorytmów AI dla analizy danych satelitarnych.
            </p>
        </div>
        """, unsafe_allow_html=True)

    focus_cols2 = st.columns(2)
    with focus_cols2[0]:
        st.markdown("""
        <div style="background-color: white; padding: 2rem; border-radius: 20px; height: 100%; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
            <div style="font-size: 2rem; margin-bottom: 1rem;">🤝</div>
            <h3 style="font-size: 1.3rem; font-weight: 600; margin-bottom: 1rem;">Współpraca</h3>
            <p style="color: #666; line-height: 1.6;">
                Partnerstwa strategiczne z wiodącymi instytucjami (NASA, ESA, POLSA) i przemysłem obronnym (HSW S.A.). Budowanie konsorcjum lokalnych firm (np. LiuGong Dressta, Cognor S.A., ALWI, Codogni) i integracja z krajowymi programami satelitarnymi (MikroGlob, PIAST).
            </p>
        </div>
        """, unsafe_allow_html=True)
    with focus_cols2[1]:
        st.markdown("""
        <div style="background-color: white; padding: 2rem; border-radius: 20px; height: 100%; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
            <div style="font-size: 2rem; margin-bottom: 1rem;">🎓</div>
            <h3 style="font-size: 1.3rem; font-weight: 600; margin-bottom: 1rem;">Edukacja i Talenty</h3>
            <p style="color: #666; line-height: 1.6;">
                Programy rozwoju specjalistów, takie jak "SPACE 4 TALENTS", organizacja hackathonów (np. NASA Space Apps Challenge) oraz tworzenie SPACE ACADEMY. Współpraca z uczelniami technicznymi w celu kształcenia kadr dla sektorów kosmicznego i obronnego oraz wsparcie startupów poprzez ESA BIC Poland.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Key project info with statistics
    st.markdown("""
    <div style="margin: 5rem auto 3rem; text-align: center; max-width: 1200px;">
        <h2 style="font-size: 2rem; font-weight: 600; margin-bottom: 1rem;">Projekt w Liczbach</h2>
        <p style="color: #666; margin-bottom: 3rem;">Kluczowe wskaźniki naszego rozwoju</p>
    </div>
    """, unsafe_allow_html=True)

    # Clean statistics display
    stats_cols = st.columns(4)
    with stats_cols[0]:
        st.markdown("""
        <div style="background-color: white; padding: 2rem; border-radius: 20px; text-align: center; height: 100%; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
            <div style="font-size: 2.5rem; font-weight: 700; margin-bottom: 1rem;">5800 m²</div>
            <div style="color: #666;">Powierzchnia całkowita Hubu</div>
        </div>
        """, unsafe_allow_html=True)
    with stats_cols[1]:
        st.markdown("""
        <div style="background-color: white; padding: 2rem; border-radius: 20px; text-align: center; height: 100%; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
            <div style="font-size: 2.5rem; font-weight: 700; margin-bottom: 1rem;">150+</div>
            <div style="color: #666;">Planowanych miejsc pracy</div>
        </div>
        """, unsafe_allow_html=True)
    with stats_cols[2]:
        st.markdown("""
        <div style="background-color: white; padding: 2rem; border-radius: 20px; text-align: center; height: 100%; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
            <div style="font-size: 2.5rem; font-weight: 700; margin-bottom: 1rem;">8+</div>
            <div style="color: #666;">Firm w konsorcjum</div>
        </div>
        """, unsafe_allow_html=True)
    with stats_cols[3]:
        st.markdown("""
        <div style="background-color: white; padding: 2rem; border-radius: 20px; text-align: center; height: 100%; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
            <div style="font-size: 2.5rem; font-weight: 700; margin-bottom: 1rem;">3</div>
            <div style="color: #666;">Główne projekty flagowe</div>
        </div>
        """, unsafe_allow_html=True)

    # About the project section with key information
    st.header("O Projekcie")
    
    # Introduction with KUL building image
    col1, col2 = st.columns([2, 1.2]) # Adjusted ratio for image
    with col1:
        st.markdown("""
        Hub Technologii Podwójnego Zastosowania w Stalowej Woli to ambitna inicjatywa, której celem jest przekształcenie miasta 
        w dynamiczny ośrodek innowacji specjalizujący się w technologiach kosmicznych i obronnych. 
        Projekt opiera się na unikalnych atutach Stalowej Woli, w tym silnej bazie przemysłowej z bogatym doświadczeniem 
        w sektorze obronnym oraz konkretnym wsparciem infrastrukturalnym ze strony miasta.
        """)
        st.markdown(""" 
        Kluczowym zasobem materialnym jest dedykowany budynek, wcześniej użytkowany przez Katolicki Uniwersytet Lubelski (KUL). 
        Obiekt ten, o powierzchni całkowitej około 5800 m² (w tym blisko 3000 m² powierzchni użytkowej), 
        dawniej mieścił m.in. Wydział Inżynierii Materiałowej. Obecnie znajduje się pod zarządem miasta, 
        które planuje jego adaptację na potrzeby Hubu, co znacząco obniża bariery inwestycyjne i przyspiesza start projektu.

        Strategicznym elementem inicjatywy jest bliska współpraca z krajowymi i międzynarodowymi agencjami, takimi jak 
        Amerykańska Agencja Kosmiczna (NASA), Europejska Agencja Kosmiczna (ESA) oraz Polska Agencja Kosmiczna (POLSA). 
        Partnerstwa te zapewniają dostęp do unikalnej wiedzy, globalnych rynków oraz różnorodnych możliwości finansowania. 
        """)
        st.info('''Co więcej, członkostwo Polski w ESA i związany z nim mechanizm "juste retour" stanowią wymierną korzyść – każda złotówka 
        przekazana do budżetu ESA wraca do polskich firm w formie zamówień, co bezpośrednio stymuluje rozwój krajowego 
        przemysłu kosmicznego.''')
    with col2:
        if images.get('kul_building'):
            st.image(f"data:image/jpeg;base64,{images['kul_building']}", caption="Planowana siedziba Hubu (dawny budynek KUL)", use_container_width=True)
        else:
            st.markdown("<div style='text-align: center; padding: 20px; border: 1px dashed #ccc;'><i>Zdjęcie budynku KUL</i></div>", unsafe_allow_html=True)
            
    st.markdown("""
    #### Solidny Ekosystem Przemysłowy
    Stalowa Wola dysponuje silnym zapleczem przemysłowym, które jest fundamentem dla rozwoju Hubu. Do kluczowych podmiotów należą:
    *   **HSW S.A.:** Lider w produkcji zaawansowanych systemów obronnych (m.in. bojowe wozy piechoty Borsuk, armatohaubice Krab, systemy wieżowe ZSSW-30). Firma aktywnie inwestuje w robotyzację i cyfryzację produkcji.
    *   **LiuGong Dressta:** Producent ciężkich maszyn budowlanych, których technologie mogą być adaptowane do pracy w ekstremalnych warunkach, np. przy budowie infrastruktury kosmicznej.
    *   **Cognor S.A. (Oddział HSJ) i ALWI:** Firmy specjalizujące się w wyrobach stalowych, z potencjałem w rozwoju ultralekkich stopów metali i powłok odpornych na warunki kosmiczne.
    *   **Lokalne przedsiębiorstwa:** Takie jak **Codogni** (precyzyjne komponenty mechaniczne dla np. napędów satelitów), **STALPRZEM** (specjalistyczne betony, potencjalnie dla baz kosmicznych), **POL-PAW** (odzież ochronna adaptowalna dla astronautów i żołnierzy) oraz **MISTA** (specjalistyczne maszyny z potencjałem dla misji eksploracyjnych).
    """)
    
    st.markdown("""
    #### Rozwój Talentów i Współpraca Akademicka
    Hub stawia na rozwój kapitału ludzkiego poprzez programy takie jak **"SPACE 4 TALENTS"** oraz organizację lokalnych edycji globalnego hackathonu **NASA Space Apps Challenge**. Planowana jest budowa nowoczesnej infrastruktury badawczo-rozwojowej: **SPACELAB** (laboratoria testowe i prototypownie dla systemów autonomicznych oraz analizy danych satelitarnych) oraz **SPACE ACADEMY** (centrum oferujące specjalistyczne szkolenia). Kluczowa będzie również współpraca z uczelniami technicznymi i wsparcie dla startupów, m.in. poprzez ESA BIC Poland.
    """)
        
    st.markdown("""
    #### Główne Kierunki Rozwoju (Projekty Flagowe)
    Plan rozwoju Hubu koncentruje się na trzech strategicznych filarach:
    *   🚀 **Autonomiczne Systemy Wsparcia Misji Satelitarnych i Wojskowych:** Rozwój lokalnych, autonomicznych dronów i robotów lądowych zdolnych do współpracy z systemami satelitarnymi. Przewiduje się ich zastosowanie w inspekcji i naprawach infrastruktury (w tym satelitów na orbicie), wsparciu operacyjnym na polu walki oraz w misjach logistycznych. Systemy te będą integrowane z polskimi programami satelitarnymi (np. MikroGlob, PIAST) oraz platformami bezzałogowymi rozwijanymi w HSW.
    *   🛰️ **Hybrydowy System Obserwacji i Analizy Danych Satelitarnych:** Stworzenie zaawansowanej platformy integrującej dane z różnorodnych źródeł satelitarnych – polskich (optoelektronicznych i radarowych) oraz komercyjnych. Kluczowym elementem będzie wykorzystanie algorytmów sztucznej inteligencji (AI) do automatycznej analizy danych i szybkiego generowania informacji wywiadowczych oraz produktów analitycznych dla sektora obronnego, służb państwowych i zastosowań cywilnych.
    *   🛠️ **Inteligentne Materiały Samonaprawiające się i Adaptacyjne:** Badania, rozwój i wdrożenie nowej generacji materiałów kompozytowych i stopów metali. Będą one posiadały zdolność do samodzielnego wykrywania uszkodzeń (np. mikropęknięć) i ich naprawy (np. poprzez zastosowanie powłok nanokompozytowych z mikrokapsułkami). Znajdą zastosowanie w konstrukcjach pojazdów wojskowych, statków kosmicznych, satelitów oraz w infrastrukturze krytycznej.
    """)
        
    st.markdown("""
    #### Strategia Finansowania
    Finansowanie projektu opiera się na zdywersyfikowanym portfelu źródeł. Obejmuje on wkład miasta (udostępnienie i adaptacja infrastruktury), krajowe fundusze publiczne (np. z NCBR, KPK), środki unijne (m.in. z programu Horyzont Europa, Funduszu Odbudowy), programy Europejskiej Agencji Kosmicznej, potencjalne fundusze z NATO oraz zaangażowanie kapitału prywatnego. Taka strategia ma zapewnić stabilność finansową i długoterminową perspektywę rozwoju Hubu.
    """)

    # New Section: What is Dual-Use Technology?
    st.markdown("""
    <div style="margin-top: 3rem; margin-bottom: 3rem;">
        <h3 style="font-size: 1.8rem; font-weight: 600; margin-bottom: 1rem; text-align: center;">Co to są Technologie Podwójnego Zastosowania (Dual-Use)?</h3>
        <div class="metric-card" style="padding: 2rem;">
            <p style="text-align: justify; margin-bottom: 1rem;">
                Technologie podwójnego zastosowania (ang. "dual-use technologies") to produkty, oprogramowanie, technologie oraz know-how, 
                które mogą być wykorzystywane zarówno do celów cywilnych, jak i wojskowych. Ich uniwersalność sprawia, że odgrywają 
                coraz większą rolę w nowoczesnej gospodarce i strategii bezpieczeństwa.
            </p>
            <p style="text-align: justify; margin-bottom: 1rem;">
                <strong>Kluczowe cechy technologii dual-use:</strong>
            </p>
            <ul style="list-style-type: disc; margin-left: 20px;">
                <li><strong>Wszechstronność:</strong> Możliwość adaptacji do różnych rynków i potrzeb.</li>
                <li><strong>Innowacyjność:</strong> Często są wynikiem zaawansowanych badań naukowych i prac rozwojowych.</li>
                <li><strong>Efektywność kosztowa:</strong> Rozwój dla jednego sektora może obniżyć koszty wdrożenia w drugim.</li>
                <li><strong>Strategiczne znaczenie:</strong> Mają kluczowe znaczenie dla bezpieczeństwa państwa oraz konkurencyjności gospodarki.</li>
            </ul>
            <p style="text-align: justify;">
                Przykłady technologii podwójnego zastosowania obejmują systemy GPS (pierwotnie wojskowe, dziś powszechne w cywilnych aplikacjach), 
                drony (wykorzystywane w wojsku, rolnictwie, logistyce), zaawansowane materiały kompozytowe (stosowane w lotnictwie wojskowym i cywilnym), 
                czy technologie cyberbezpieczeństwa chroniące zarówno infrastrukturę krytyczną, jak i dane przedsiębiorstw.
            </p>
            <p style="text-align: justify; margin-top: 1rem;">
                Hub Technologii Podwójnego Zastosowania w Stalowej Woli koncentruje się na wspieraniu rozwoju i komercjalizacji właśnie takich 
                rozwiązań, które mogą znaleźć zastosowanie w sektorze kosmicznym, obronnym oraz na szerokim rynku cywilnym.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Call to action section
    st.markdown("""
    <div style="margin: 5rem auto; text-align: center; max-width: 800px; background-color: white; padding: 3rem 2rem; border-radius: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
        <h2 style="font-size: 1.8rem; font-weight: 600; margin-bottom: 1.5rem;">Dołącz do Transformacji Technologicznej</h2>
        <p style="color: #666; margin-bottom: 2rem; line-height: 1.6;">
            Zostań częścią inicjatywy, która kształtuje przyszłość technologii kosmicznych i obronnych w Polsce
        </p>
        <a href="#" style="background-color: #1E1E1E; color: white; padding: 12px 28px; border-radius: 50px; text-decoration: none; font-weight: 500; display: inline-block;">Skontaktuj się z nami</a>
    </div>
    """, unsafe_allow_html=True)

# Define other page functions below

# Summary page with interactive map
def render_summary_page():
    st.markdown("""
    <div class="landing-section">
        <h2 class="section-title">Podsumowanie Projektu i Analiza SWOT</h2>
        <p class="section-subtitle">Wizja projektu i strategiczne położenie Stalowej Woli</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Interactive Map Section
    st.markdown("""
    <div class="map-section">
        <h3 class="section-subtitle">Lokalizacje Strategiczne</h3>
        <p>Mapa pokazuje główne lokalizacje związane z Hubem Technologii Podwójnego Zastosowania.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced map with more locations and detailed information
    view_state = pdk.ViewState(
        latitude=50.5825,
        longitude=22.0532,
        zoom=13,
        pitch=45,
        bearing=0
    )
    
    # Enhanced strategic locations based on raport.txt
    locations = pd.DataFrame([
        {
            "name": "Centrum Innowacji (KUL)",
            "lat": 50.5825,
            "lon": 22.0532,
            "description": "Główny budynek o powierzchni 5800 m², wcześniej użytkowany przez Katolicki Uniwersytet Lubelski",
            "icon": "🏛️",
            "size": 200,
            "color": [255, 0, 0]  # Red marker for main building
        },
        {
            "name": "HSW S.A.",
            "lat": 50.5800,
            "lon": 22.0600,
            "description": "Huta Stalowa Wola - główny partner przemysłowy, producent systemów obronnych",
            "icon": "🏭",
            "size": 200,
            "color": [0, 0, 255]  # Blue marker for industrial partner
        },
        {
            "name": "SPACELAB",
            "lat": 50.5850,
            "lon": 22.0450,
            "description": "Centrum badawcze i laboratoria testowe dla systemów autonomicznych",
            "icon": "🔬",
            "size": 180,
            "color": [0, 255, 0]  # Green marker for research facility
        },
        {
            "name": "SPACE ACADEMY",
            "lat": 50.5880,
            "lon": 22.0520,
            "description": "Centrum szkoleniowe dla przyszłych specjalistów sektora kosmicznego i obronnego",
            "icon": "🎓",
            "size": 180,
            "color": [255, 165, 0]  # Orange marker for education
        }
    ])
    
    # Create two layers - icon layer and text layer for better visualization
    icon_layer = pdk.Layer(
        "ScatterplotLayer",
        locations,
        get_position=["lon", "lat"],
        get_radius=30,
        get_fill_color="color",
        pickable=True
    )
    
    text_layer = pdk.Layer(
        "TextLayer",
        locations,
        get_position=["lon", "lat"],
        get_text="icon",
        get_size="size",
        get_color=[255, 255, 255],
        get_angle=0,
        text_anchor="middle",
        pickable=True,
        font_settings={"sdf": False}
    )
    
    deck = pdk.Deck(
        map_style="mapbox://styles/mapbox/dark-v10",
        initial_view_state=view_state,
        layers=[icon_layer, text_layer],
        tooltip={"text": "{name}\n\n{description}"}
    )
    
    st.pydeck_chart(deck)
    
    # SWOT Analysis from raport.txt
    st.markdown("""
    <div class="swot-section">
        <h3 class="section-subtitle">Analiza SWOT</h3>
        <p>Analiza strategiczna inicjatywy Hubu Technologii Podwójnego Zastosowania w Stalowej Woli</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create expandable SWOT cards
    swot_tabs = st.tabs(["Mocne Strony (S)", "Słabe Strony (W)", "Szanse (O)", "Zagrożenia (T)"])
    
    with swot_tabs[0]:
        st.markdown("### Mocne Strony (Strengths)")
        st.markdown("""
        **1. Ugruntowana Baza Przemysłowa i Doświadczenie Dual-Use:**
        Kluczowym atutem jest dostęp do **zaawansowanego know-how technologicznego** oraz **ponad 80-letniego doświadczenia przemysłowego Huty Stalowa Wola S.A.** w sektorze obronnym. To, w połączeniu z **potencjałem synergii** z innymi lokalnymi firmami (np. LiuGong Dressta – ciężki sprzęt, Cognor S.A. – zaawansowane materiały), tworzy **solidny fundament pod rozwój innowacyjnych technologii podwójnego zastosowania**. Przykładowo, adaptacja ciężkich maszyn do operacji pozaziemskich czy rozwój ultralekkich, wytrzymałych stopów dla konstrukcji kosmicznych.

        **2. Dedykowana Infrastruktura i Aktywne Wsparcie Miasta:**
        **Proaktywne i wymierne zaangażowanie władz Stalowej Woli** jest nieocenione. Obejmuje to **udostępnienie strategicznie położonego budynku po KUL (o łącznej powierzchni ~5800 m²)** na potrzeby Hubu oraz **aktywne wsparcie w procesach administracyjnych i pozyskiwaniu finansowania**. Takie działania **znacząco obniżają bariery wejścia i koszty początkowe projektu**, krytycznie przyspieszając jego start i rozwój.

        **3. Dynamicznie Rozwijany Ekosystem Talentów i Innowacji:**
        Istniejące inicjatywy, takie jak program **"SPACE 4 TALENTS"** oraz lokalne edycje prestiżowego **NASA Space Apps Challenge**, aktywnie **stymulują rozwój kadr specjalistycznych** i **przyciągają młode talenty** do regionu. To buduje **żywotny pipeline przyszłych ekspertów** dla Hubu i firm partnerskich.

        **4. Strategiczne Pozycjonowanie na Rynkach Wzrostowych:**
        Projekt charakteryzuje **jasno zdefiniowany fokus na perspektywiczne i dynamicznie rosnące globalne rynki technologii kosmicznych i obronnych**. Sektory te cechują się **wysokim potencjałem innowacyjnym, znaczną wartością dodaną** oraz rosnącym popytem napędzanym przez czynniki geopolityczne i komercjalizację przestrzeni kosmicznej.

        **5. Dźwignia Finansowa i Technologiczna z Europejskiej Agencji Kosmicznej (ESA):**
        Korzyści płynące z **członkostwa Polski w ESA**, w szczególności **mechanizm "juste retour"** (gwarantujący zwrot znaczącej części składki w postaci kontraktów dla krajowych podmiotów), stanowią **istotną dźwignię finansową i technologiczną**, otwierając drogę do **prestiżowych projektów i transferu wiedzy**.
        """)

        with st.expander("**Szczegółowa Analiza Potencjału Przemysłowego Regionu**"):
            st.markdown("""
            **HSW S.A.:** Jako **filar lokalnego przemysłu**, HSW S.A. wnosi nie tylko dziedzictwo produkcyjne, ale również **nowoczesne zdolności w zakresie robotyzacji, cyfryzacji procesów oraz doświadczenie we współpracy międzynarodowej**. Strategiczny potencjał firmy obejmuje:
            *   Rozwój **autonomicznych platform lądowych** dla zastosowań wojskowych i cywilnych (np. logistyka, inspekcja).
            *   Integrację systemów naziemnych z **platformami satelitarnymi** (np. komunikacja, nawigacja, obserwacja).
            *   Produkcję zaawansowanych **systemów bezzałogowych** i komponentów dla nich.

            **Kluczowi Potencjalni Partnerzy Przemysłowi (Przykłady Dual-Use):**
            *   **LiuGong Dressta:** **Adaptacja ciężkich maszyn budowlanych** do operacji w ekstremalnych warunkach (np. budowa infrastruktury na Księżycu/Marsie, specjalistyczne maszyny dla wojsk inżynieryjnych). **Potencjał transferu technologii sterowania i wytrzymałości materiałowej.**
            *   **Cognor S.A. (Oddział HSJ) & ALWI:** **Badania i rozwój ultralekkich stopów metali** (np. na bazie aluminium, tytanu) oraz **zaawansowanych powłok ochronnych** (np. termicznych, antykorozyjnych) niezbędnych dla konstrukcji satelitarnych, rakietowych i pojazdów kosmicznych.
            *   **Lokalne MŚP (np. Codogni, STALPRZEM, POL-PAW, MISTA):** Stanowią **ważne ogniwo w łańcuchu dostaw**, oferując specjalistyczne zdolności:
                *   `Codogni`: **Precyzyjne komponenty mechaniczne** (np. dla aktuatorów satelitarnych, systemów napędowych robotów).
                *   `STALPRZEM`: **Innowacyjne materiały budowlane** (np. betony wysokowytrzymałościowe, potencjalnie adaptowalne do konstrukcji z regolitu księżycowego).
                *   `POL-PAW`: **Zaawansowana odzież ochronna i tekstylia techniczne** (np. materiały termoaktywne, antyradiacyjne dla skafandrów, mundurów).
                *   `MISTA`: **Specjalistyczne pojazdy i maszyny** z potencjałem modyfikacji do zadań logistycznych w trudnym terenie lub misji eksploracyjnych.
            """)
    
    with swot_tabs[1]:
        st.markdown("### Słabe Strony (Weaknesses)")
        st.markdown("""
        1.  **Deficyt Wysoko Wyspecjalizowanych Kompetencji:** Potencjalne luki kadrowe w dziedzinie zaawansowanych technologii kosmicznych (np. inżynieria systemów satelitarnych) oraz sztucznej inteligencji, wymagające intensywnych programów szkoleniowych i rekrutacyjnych.
        2.  **Zależność od Finansowania Zewnętrznego:** Szczególnie w fazie początkowej, projekt będzie uzależniony od pozyskania środków publicznych (krajowych i UE) oraz prywatnych inwestycji, co wiąże się z ryzykiem płynnościowym.
        3.  **Złożoność Koordynacji Konsorcjum:** Zarządzanie zróżnicowaną grupą partnerów (przemysł, nauka, administracja) o odmiennych celach i kulturach organizacyjnych może generować wyzwania operacyjne.
        4.  **Konieczność Rozbudowy Infrastruktury Badawczej:** Budowa i wyposażenie specjalistycznych laboratoriów (np. testowania komponentów satelitarnych, materiałów kosmicznych) będzie czasochłonna i kapitałochłonna.
        """)
    
    with swot_tabs[2]:
        st.markdown("### Szanse (Opportunities)")
        st.markdown("""
        1.  **Dynamiczny Wzrost Rynków Docelowych:** Globalny rynek kosmiczny (prognozowany wzrost do >1 bln USD do 2030 r.) oraz rosnące budżety obronne stwarzają duże zapotrzebowanie na innowacyjne technologie podwójnego zastosowania.
        2.  **Dostępność Instrumentów Finansowania Innowacji:** Możliwość pozyskania funduszy z programów unijnych (np. Horyzont Europa, Europejski Fundusz Obronny), krajowych (NCBR, PARP, ARP) oraz międzynarodowych (np. NATO Innovation Fund).
        3.  **Budowanie Międzynarodowych Partnerstw Strategicznych:** Potencjał współpracy z wiodącymi agencjami kosmicznymi (NASA, ESA) oraz kluczowymi graczami w przemyśle obronnym w ramach NATO i UE, umożliwiający transfer wiedzy i technologii.
        4.  **Efektywne Wykorzystanie Mechanizmu "Juste Retour" ESA:** Systematyczne aplikowanie o kontrakty ESA w celu maksymalizacji zwrotu polskiej składki i finansowania konkretnych projektów badawczo-rozwojowych.
        5.  **Kreowanie Nowych, Wysokomarżowych Produktów i Usług:** Rozwój unikalnych rozwiązań technologicznych (np. systemy autonomiczne, analiza danych satelitarnych AI, nowe materiały) generujących wysoką wartość dodaną i potencjał eksportowy.
        """)

        with st.expander("Analiza Mechanizmu 'Juste Retour' i Funduszy UE"):
            st.markdown("""
            **Mechanizm 'Juste Retour' ESA:** Członkostwo Polski w Europejskiej Agencji Kosmicznej (ESA) gwarantuje, że znacząca część polskiej składki wraca do kraju w postaci kontraktów dla polskich firm i instytucji naukowych. Konsorcjum Hubu Stalowa Wola jest strategicznie pozycjonowane, aby skutecznie aplikować o te środki, finansując rozwój technologii i produktów kosmicznych.

            **Fundusze Europejskie i Krajowe:**
            *   **Horyzont Europa:** Główny program UE finansujący badania i innowacje, z dedykowanymi konkursami dla sektora kosmicznego i bezpieczeństwa.
            *   **Europejski Fundusz Obronny (EDF):** Wspiera projekty B+R w dziedzinie obronności, promując współpracę transgraniczną.
            *   **Krajowe Centrum Badań i Rozwoju (NCBR):** Oferuje granty na projekty innowacyjne, w tym technologie podwójnego zastosowania.
            *   **Polska Agencja Kosmiczna (POLSA):** Realizuje Narodowy Program Kosmiczny, wspierając rozwój krajowego sektora kosmicznego.
            *   **Agencja Rozwoju Przemysłu (ARP):** Może wspierać inwestycje infrastrukturalne i rozwój przedsiębiorstw.
            """)
    
    with swot_tabs[3]:
        st.markdown("### Zagrożenia (Threats)")
        st.markdown("""
        1.  **Niestabilność Geopolityczna i Zmiany Priorytetów Politycznych:** Konflikty międzynarodowe i zmiany w polityce obronnej mogą wpływać na alokację budżetów oraz popyt na określone technologie.
        2.  **Intensywna Konkurencja Krajowa i Międzynarodowa:** Rywalizacja ze strony innych, bardziej etablowanych hubów technologicznych oraz zagranicznych firm o zasoby, talenty i kontrakty.
        3.  **Szybka Ewolucja Technologiczna:** Wysokie tempo zmian w sektorach kosmicznym i AI stwarza ryzyko dezaktualizacji technologii i konieczność ciągłych, kosztownych inwestycji w B+R.
        4.  **Ryzyko Pozyskania i Utrzymania Długoterminowego Finansowania:** Zapewnienie stabilności finansowej projektu w perspektywie wieloletniej, zwłaszcza po wygaśnięciu początkowych grantów.
        5.  **Drenaż Mózgów i Trudności w Pozyskaniu Talentów:** Konkurencja o wysoko wykwalifikowanych specjalistów z dużymi ośrodkami miejskimi i zagranicznymi firmami, mogąca utrudnić budowanie silnego zespołu na miejscu.
        """)
    
    # Images gallery - Placeholder for future implementation
    # st.markdown("### Galeria Technologii")
    # st.markdown("_Przykładowe technologie kosmiczne i obronne rozwijane w ramach inicjatywy:_")

    # Remove placeholder gallery using columns
    # gallery_cols = st.columns(3)
    # with gallery_cols[0]:
    #     st.image("https://placekitten.com/400/300", caption="Autonomiczne platformy robotyczne")
    # with gallery_cols[1]:
    #     st.image("https://placekitten.com/400/300", caption="Systemy obserwacji satelitarnej")
    # with gallery_cols[2]:
    #     st.image("https://placekitten.com/400/300", caption="Materiały samonaprawiające")

# Partners Section with collaboration network
def render_partners_section():
    st.markdown("""
    <div class="landing-section">
        <h2 class="section-title">Nasi Partnerzy Strategiczni</h2>
        <p class="section-subtitle">Współpracujemy z wiodącymi instytucjami w sektorach kosmicznym i obronnym, budując silne konsorcjum dla rozwoju technologii podwójnego zastosowania</p>
    </div>
    """, unsafe_allow_html=True)

    # Partner logos - display using images loaded from files
    partner_cols = st.columns([1, 1, 1, 1])
    
    with partner_cols[0]:
        if images.get('partner1'):
            st.image(f"data:image/png;base64,{images['partner1']}", width=150, caption="NASA")
        else:
            st.image("https://via.placeholder.com/150x80?text=NASA", width=150, caption="NASA")
    
    with partner_cols[1]:
        if images.get('partner2'):
            st.image(f"data:image/png;base64,{images['partner2']}", width=150, caption="ESA")
        else:
            st.image("https://via.placeholder.com/150x80?text=ESA", width=150, caption="ESA")
    
    with partner_cols[2]:
        if images.get('partner3'):
            st.image(f"data:image/jpeg;base64,{images['partner3']}", width=150, caption="POLSA")
        else:
            st.image("https://via.placeholder.com/150x80?text=POLSA", width=150, caption="POLSA")
    
    with partner_cols[3]:
        if images.get('hsw'):
            st.image(f"data:image/jpeg;base64,{images['hsw']}", width=150, caption="HSW S.A.")
        else:
            st.image("https://via.placeholder.com/150x80?text=HSW+S.A.", width=150, caption="HSW S.A.")
    
    # Network of collaboration visualization
    st.markdown("### Sieć Współpracy")
    
    st.markdown("""
    Wizualizacja powiązań między partnerami konsorcjum, pokazująca intensywność współpracy i kluczowe obszary kooperacji.
    Grubość linii reprezentuje intensywność współpracy między podmiotami.
    """)
    
    # Create nodes and edges for the network graph
    nodes = [
        {"id": "Hub Stalowa Wola", "label": "Hub Stalowa Wola", "size": 25, "group": "hub"},
        {"id": "HSW S.A.", "label": "HSW S.A.", "size": 20, "group": "przemysł"},
        {"id": "NASA", "label": "NASA", "size": 20, "group": "agencja międzynarodowa"},
        {"id": "ESA", "label": "ESA", "size": 20, "group": "agencja międzynarodowa"},
        {"id": "POLSA", "label": "POLSA", "size": 15, "group": "agencja krajowa"},
        {"id": "LiuGong Dressta", "label": "LiuGong Dressta", "size": 15, "group": "przemysł"},
        {"id": "Cognor S.A.", "label": "Cognor S.A.", "size": 15, "group": "przemysł"},
        {"id": "ALWI", "label": "ALWI", "size": 12, "group": "przemysł"},
        {"id": "Politechnika Warszawska", "label": "Politechnika Warszawska", "size": 15, "group": "nauka"},
        {"id": "WAT", "label": "WAT", "size": 15, "group": "nauka"},
        {"id": "AGH", "label": "AGH", "size": 15, "group": "nauka"},
        {"id": "Miasto Stalowa Wola", "label": "Miasto Stalowa Wola", "size": 18, "group": "administracja"}
    ]
    
    edges = [
        {"source": "Hub Stalowa Wola", "target": "HSW S.A.", "value": 10},
        {"source": "Hub Stalowa Wola", "target": "NASA", "value": 7},
        {"source": "Hub Stalowa Wola", "target": "ESA", "value": 8},
        {"source": "Hub Stalowa Wola", "target": "POLSA", "value": 9},
        {"source": "Hub Stalowa Wola", "target": "Miasto Stalowa Wola", "value": 10},
        {"source": "Hub Stalowa Wola", "target": "Politechnika Warszawska", "value": 6},
        {"source": "Hub Stalowa Wola", "target": "WAT", "value": 5},
        {"source": "Hub Stalowa Wola", "target": "AGH", "value": 4},
        {"source": "Hub Stalowa Wola", "target": "LiuGong Dressta", "value": 6},
        {"source": "Hub Stalowa Wola", "target": "Cognor S.A.", "value": 5},
        {"source": "Hub Stalowa Wola", "target": "ALWI", "value": 4},
        {"source": "HSW S.A.", "target": "NASA", "value": 3},
        {"source": "HSW S.A.", "target": "ESA", "value": 4},
        {"source": "HSW S.A.", "target": "WAT", "value": 6},
        {"source": "HSW S.A.", "target": "POLSA", "value": 5},
        {"source": "POLSA", "target": "ESA", "value": 7},
        {"source": "POLSA", "target": "NASA", "value": 5},
        {"source": "Politechnika Warszawska", "target": "ESA", "value": 4},
        {"source": "Politechnika Warszawska", "target": "NASA", "value": 3},
        {"source": "WAT", "target": "NASA", "value": 2},
        {"source": "WAT", "target": "POLSA", "value": 3},
        {"source": "AGH", "target": "Cognor S.A.", "value": 4},
        {"source": "AGH", "target": "ALWI", "value": 3},
        {"source": "Miasto Stalowa Wola", "target": "HSW S.A.", "value": 8}
    ]
    
    # Create network graph using Plotly
    node_x = []
    node_y = []
    node_text = []
    node_size = []
    node_color = []
    
    # Color mapping for groups
    color_map = {
        "hub": "#FF4500",              # Orange Red
        "przemysł": "#1E90FF",         # Dodger Blue
        "agencja międzynarodowa": "#32CD32",  # Lime Green
        "agencja krajowa": "#9370DB",   # Medium Purple
        "nauka": "#FFD700",            # Gold
        "administracja": "#FF69B4"     # Hot Pink
    }
    
    # Generate random positions for nodes (in a real app, use a proper layout algorithm)
    import random
    random.seed(42)  # For reproducibility
    
    positions = {}
    for node in nodes:
        positions[node["id"]] = (random.uniform(-12, 12), random.uniform(-12, 12)) # Increased range
        node_x.append(positions[node["id"]][0])
        node_y.append(positions[node["id"]][1])
        node_text.append(node["label"])
        node_size.append(node["size"]*2.5) # Increased size
        node_color.append(color_map[node["group"]])
    
    # Create edges
    edge_traces = [] # Store individual traces for edges
    
    for edge in edges:
        x0, y0 = positions[edge["source"]]
        x1, y1 = positions[edge["target"]]
        
        trace = go.Scatter(
            x=[x0, x1, None], y=[y0, y1, None],
            line=dict(width=edge["value"]/2, color='#888'), # Varying width per edge
            hoverinfo='none',
            mode='lines'
        )
        edge_traces.append(trace)
    
    # Create node trace
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=False,
            color=node_color,
            size=node_size,
            line=dict(width=2, color='#FFFFFF')
        ),
        text=node_text
    )
    
    # Create figure
    fig = go.Figure(data=edge_traces + [node_trace], # Combine edge traces and node trace
                 layout=go.Layout(
                    title=dict(text='Sieć Współpracy Partnerów Konsorcjum', font=dict(size=16)),
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20,l=5,r=5,t=40),
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
                ))
    
    # Display network graph
    st.plotly_chart(fig, use_container_width=True)
    
    # Manual legend for node colors
    st.markdown("""
    <div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 15px; margin-top: 10px; padding: 10px; background-color: #f9f9f9; border-radius: 10px;">
        <div style="display: flex; align-items: center; font-size: 0.9rem;"><div style="width: 15px; height: 15px; background-color: #FF4500; margin-right: 8px; border-radius: 50%; border: 1px solid #ddd;"></div>Hub</div>
        <div style="display: flex; align-items: center; font-size: 0.9rem;"><div style="width: 15px; height: 15px; background-color: #1E90FF; margin-right: 8px; border-radius: 50%; border: 1px solid #ddd;"></div>Przemysł</div>
        <div style="display: flex; align-items: center; font-size: 0.9rem;"><div style="width: 15px; height: 15px; background-color: #32CD32; margin-right: 8px; border-radius: 50%; border: 1px solid #ddd;"></div>Agencja Międzynarodowa</div>
        <div style="display: flex; align-items: center; font-size: 0.9rem;"><div style="width: 15px; height: 15px; background-color: #9370DB; margin-right: 8px; border-radius: 50%; border: 1px solid #ddd;"></div>Agencja Krajowa</div>
        <div style="display: flex; align-items: center; font-size: 0.9rem;"><div style="width: 15px; height: 15px; background-color: #FFD700; margin-right: 8px; border-radius: 50%; border: 1px solid #ddd;"></div>Nauka</div>
        <div style="display: flex; align-items: center; font-size: 0.9rem;"><div style="width: 15px; height: 15px; background-color: #FF69B4; margin-right: 8px; border-radius: 50%; border: 1px solid #ddd;"></div>Administracja</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Partner categories explanation
    st.markdown("### Kategorie Partnerów")
    
    partner_cat_cols = st.columns(3)
    
    with partner_cat_cols[0]:
        st.markdown("""
        #### Partnerzy Przemysłowi
        
        **Rola w konsorcjum:**
        - Realizacja produkcji i wdrożeń
        - Testowanie technologii w warunkach przemysłowych
        - Rozwój zastosowań komercyjnych
        
        **Kluczowe podmioty:**
        - HSW S.A.
        - LiuGong Dressta
        - Cognor S.A.
        - ALWI
        - Codogni
        - STALPRZEM
        - POL-PAW
        - MISTA
        """)
    
    with partner_cat_cols[1]:
        st.markdown("""
        #### Partnerzy Naukowi
        
        **Rola w konsorcjum:**
        - Badania podstawowe i stosowane
        - Kształcenie kadr specjalistycznych
        - Dostęp do infrastruktury badawczej
        
        **Kluczowe podmioty:**
        - Politechnika Warszawska
        - Wojskowa Akademia Techniczna
        - Akademia Górniczo-Hutnicza
        - Politechnika Rzeszowska
        - Katolicki Uniwersytet Lubelski
        """)
    
    with partner_cat_cols[2]:
        st.markdown("""
        #### Partnerzy Instytucjonalni
        
        **Rola w konsorcjum:**
        - Wsparcie strategiczne i finansowe
        - Koordynacja współpracy międzynarodowej
        - Dostęp do programów i inicjatyw
        
        **Kluczowe podmioty:**
        - NASA
        - Europejska Agencja Kosmiczna (ESA)
        - Polska Agencja Kosmiczna (POLSA)
        - Miasto Stalowa Wola
        - Agencja Rozwoju Przemysłu
        """)
    
    # International collaboration section
    st.markdown("### Międzynarodowa Współpraca")
    
    st.markdown("""
    Istotnym elementem strategii Hubu jest nawiązywanie i rozwijanie współpracy z wiodącymi 
    instytucjami międzynarodowymi. Dzięki partnerstwom z NASA, ESA czy podmiotami z NATO, 
    Hub zyskuje dostęp do najnowszej wiedzy, technologii i możliwości finansowania.
    """)
    
    # Current and planned international collaborations
    collab_data = pd.DataFrame([
        {
            "Partner": "NASA", 
            "Zakres Współpracy": "Organizacja NASA Space Apps Challenge, wymiana know-how w zakresie technologii kosmicznych", 
            "Status": "Aktywna",
            "Korzyści dla Hubu": "Dostęp do wiedzy i metodologii NASA, promocja na arenie międzynarodowej"
        },
        {
            "Partner": "ESA", 
            "Zakres Współpracy": "Projekty w ramach mechanizmu 'juste retour', współpraca z ESA BIC Poland", 
            "Status": "Aktywna",
            "Korzyści dla Hubu": "Finansowanie projektów, mentoring dla startupów, dostęp do sieci ESA"
        },
        {
            "Partner": "NATO Innovation Fund", 
            "Zakres Współpracy": "Projekty z zakresu technologii podwójnego zastosowania w obszarze obronności", 
            "Status": "W toku",
            "Korzyści dla Hubu": "Finansowanie projektów obronnych, włączenie w łańcuchy dostaw NATO"
        },
        {
            "Partner": "DIANA (NATO)", 
            "Zakres Współpracy": "Projekty z zakresu technologii wywiadowczych i obronnych", 
            "Status": "Planowana",
            "Korzyści dla Hubu": "Współpraca z liderami technologii obronnych, dostęp do wiedzy i rynków"
        }
    ])
    
    # Style the dataframe to highlight active collaborations
    def highlight_status(val):
        if val == 'Aktywna':
            return 'background-color: rgba(40, 167, 69, 0.2)'
        elif val == 'W toku':
            return 'background-color: rgba(255, 193, 7, 0.2)'
        elif val == 'Planowana':
            return 'background-color: rgba(0, 123, 255, 0.2)'
        return ''
    
    # Apply styling and display collaboration table
    styled_collab = collab_data.style.applymap(highlight_status, subset=['Status'])
    st.table(styled_collab)
    
    # Regional innovation system integration
    st.markdown("### Integracja z Regionalnym Systemem Innowacji")
    
    st.markdown("""
    Hub w Stalowej Woli jest elementem szerszego ekosystemu innowacji w regionie i kraju.
    Poniżej przedstawiono kluczowe powiązania z regionalnym i krajowym systemem innowacji.
    """)
    
    regional_cols = st.columns(2)
    
    with regional_cols[0]:
        st.markdown("""
        #### Dolina Lotnicza
        
        Klaster przemysłowy skupiający przedsiębiorstwa z branży lotniczej, zlokalizowany głównie 
        na Podkarpaciu. Współpraca z Doliną Lotniczą umożliwi:
        
        - Transfer technologii między sektorami lotniczym i kosmicznym
        - Współdzielenie zaplecza badawczo-rozwojowego
        - Dostęp do wykwalifikowanych kadr z doświadczeniem w przemyśle lotniczym
        """)
        
        st.markdown("""
        #### Podkarpacki Park Naukowo-Technologiczny "Aeropolis"
        
        Park technologiczny zlokalizowany w pobliżu lotniska Rzeszów-Jasionka, oferujący 
        infrastrukturę dla przedsiębiorstw innowacyjnych. Współpraca obejmuje:
        
        - Wymianę doświadczeń w zakresie inkubacji i akceleracji startupów
        - Wspólną organizację wydarzeń branżowych
        - Możliwość korzystania z laboratoriów i przestrzeni testowych
        """)
    
    with regional_cols[1]:
        st.markdown("""
        #### Stalowowolska Agencja Rozwoju Regionalnego (StARR)
        
        Instytucja wspierająca rozwój gospodarczy Stalowej Woli i regionu. 
        Jej rola w kontekście Hubu to:
        
        - Koordynacja działań na poziomie lokalnym
        - Wsparcie w pozyskiwaniu funduszy na rozwój
        - Promocja Hubu wśród potencjalnych partnerów i inwestorów
        """)
        
        st.markdown("""
        #### Platforma PENTAHELIS
        
        Model współpracy pięciu typów podmiotów: przedsiębiorstw, instytucji naukowych,
        administracji publicznej, organizacji pozarządowych i społeczeństwa. Hub będzie:
        
        - Aktywnym uczestnikiem platformy, wykorzystując jej mechanizmy
        - Włączał lokalną społeczność w procesy innowacyjne
        - Budował synergię między różnymi typami podmiotów
        """)

# Funding page with charts and data
def render_funding_page():
    st.markdown("""
    <div class="landing-section">
        <h2 class="section-title">Finansowanie Projektu</h2>
        <p class="section-subtitle">Struktura finansowania i budżet projektu</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Top Metric Cards - inspired by the provided image
    st.markdown("### Kluczowe Wskaźniki Finansowe")
    
    cols = st.columns(4)
    with cols[0]:
        st.markdown("""
        <div class="funding-metric-card">
            <div class="metric-indicator-placeholder">💰</div>
            <h4>Całkowity Budżet Projektu</h4>
            <p class="metric-value">13.3M - 19.8M EUR</p> 
            <p class="metric-description">Pełny okres realizacji</p>
        </div>
        """, unsafe_allow_html=True)
    with cols[1]:
        st.markdown("""
        <div class="funding-metric-card">
            <div class="metric-indicator-placeholder">📈</div>
            <h4>Pozyskane Środki</h4>
            <p class="metric-value">1.1M EUR</p> 
            <p class="metric-description">Stan na Q3 2026</p>
        </div>
        """, unsafe_allow_html=True)
    with cols[2]:
        st.markdown("""
        <div class="funding-metric-card">
            <div class="metric-indicator-placeholder">📄</div>
            <h4>Granty Publiczne</h4>
            <p class="metric-value">0.8M EUR</p> 
            <p class="metric-description">Krajowe i UE</p>
        </div>
        """, unsafe_allow_html=True)
    with cols[3]:
        st.markdown("""
        <div class="funding-metric-card">
            <div class="metric-indicator-placeholder">🤝</div>
            <h4>Inwestycje Prywatne</h4>
            <p class="metric-value">0.3M EUR</p> 
            <p class="metric-description">Partnerzy przemysłowi</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True) # Add some space

    # Funding Sources
    st.markdown("""
    <div class="funding-section-card">
        <h3>Źródła Finansowania</h3>
    """, unsafe_allow_html=True)
    
    funding_sources_data = pd.DataFrame({
        'Źródło': [
            "Miasto/Samorząd (Wkład Rzeczowy)", 
            "Krajowe Fundusze Publiczne (NCBR, MON, KPK)", 
            "Fundusze Unijne (Horyzont Europa, EFO, F.O.)", 
            "Programy ESA (Juste Retour, PLIIS)", 
            "Fundusze NATO (Innovation Fund, DIANA)", 
            "Kapitał Prywatny (VC, Korporacje)",
            "Partnerstwa Publiczno-Prywatne (PPP)",
            "Fundusze ESG / Zielone Obligacje"
        ],
        'Szacowany Udział (%)': [10, 25, 30, 15, 5, 10, 3, 2] # Placeholder percentages
    })
    
    fig_sources = px.bar(
        funding_sources_data,
        x='Szacowany Udział (%)',
        y='Źródło',
        orientation='h',
        color='Szacowany Udział (%)',
        color_continuous_scale=px.colors.sequential.Blues_r,
        height=400,
        labels={'Szacowany Udział (%)': 'Szacowany Udział (%)', 'Źródło': 'Źródło Finansowania'}
    )
    fig_sources.update_layout(
        xaxis_title="Procentowy udział w całkowitym budżecie",
        yaxis_title="Źródło Finansowania",
        margin=dict(l=250) # Adjust left margin for long labels
    )
    st.plotly_chart(fig_sources, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Budget Allocation
    st.markdown("""
    <div class="funding-section-card">
        <h3>Alokacja Budżetu</h3>
    """, unsafe_allow_html=True)
    budget_allocation_data = pd.DataFrame({
        'Kategoria': ['Adaptacja i modernizacja budynku', 'Wyposażenie technologiczne i infrastruktura badawcza', 
                      'Fundusz dla startupów i zespołów badawczych', 'Koszty operacyjne i programy akceleracyjne', 
                      'Współpraca z przemysłem i organizacjami międzynarodowymi'],
        'Alokacja (EUR)': [3350000, 5500000, 2750000, 2200000, 2750000] # Average values from the provided budget
    })
    fig_allocation = px.pie(
        budget_allocation_data, 
        values='Alokacja (EUR)', 
        names='Kategoria',
        color_discrete_sequence=px.colors.carto.Pastel, # Changed color scheme
        hole=0.4, # Doughnut chart
        height=450
    )
    fig_allocation.update_traces(textinfo='none') # Remove text from pie slices
    fig_allocation.update_layout(legend_font_size=15) # Increase legend font size
    st.plotly_chart(fig_allocation, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Strategic Financial Goals & Investment Opportunities in columns
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="funding-section-card" style="height: 100%;">
            <h3>Strategiczne Cele Finansowe</h3>
            <ul>
                <li>Zabezpieczenie zdywersyfikowanego portfela finansowania (publiczne, prywatne, międzynarodowe).</li>
                <li>Efektywne wykorzystanie mechanizmu "juste retour" Europejskiej Agencji Kosmicznej (ESA).</li>
                <li>Pozyskanie co najmniej 20% budżetu z kapitału prywatnego i inwestycji korporacyjnych.</li>
                <li>Stworzenie funduszu zalążkowego dla wsparcia startupów i spin-off'ów technologicznych.</li>
                <li>Zapewnienie długoterminowej stabilności finansowej Hubu poprzez rozwój usług komercyjnych.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="funding-section-card" style="height: 100%;">
            <h3>Możliwości Inwestycyjne</h3>
            <p>Hub oferuje atrakcyjne możliwości dla inwestorów w obszarach:</p>
            <ul>
                <li><strong>Projekty B+R:</strong> Współfinansowanie projektów flagowych i nowych inicjatyw badawczych.</li>
                <li><strong>Infrastruktura:</strong> Inwestycje w specjalistyczne laboratoria i sprzęt.</li>
                <li><strong>Startupy i Spin-offy:</strong> Inwestycje kapitałowe w innowacyjne firmy technologiczne.</li>
                <li><strong>Partnerstwa Strategiczne:</strong> Udział w komercjalizacji technologii i wspólne przedsięwzięcia.</li>
            </ul>
            <p>Zapraszamy do kontaktu w celu omówienia szczegółów współpracy.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True) # Add some space

    # Funding Sources - Enhanced with details from finansowanie.txt and raport.txt
    st.markdown("""
    <div class="funding-section-card">
        <h3>Źródła Finansowania</h3>
        <p>Strategia finansowania Hubu opiera się na zdywersyfikowanym portfelu źródeł, obejmującym środki publiczne (krajowe, regionalne, unijne), programy dedykowane sektorowi kosmicznemu i obronnemu, oraz zaangażowanie kapitału prywatnego. Kluczowe kategorie i przykładowe instrumenty finansowania obejmują:</p>
    """, unsafe_allow_html=True)

    with st.expander("Poziom Krajowy (Polska)"):
        st.markdown("""
        - **Fundusze Europejskie dla Nowoczesnej Gospodarki (FENG):** Główny program B+R i innowacji, kontynuacja POIR. Dotacje na projekty B+R i wdrożeniowe (np. Ścieżka SMART zarządzana przez NCBR).
        - **Polska Agencja Kosmiczna (PAK):** Nowa inicjatywa grantowa (od 2026) z dotacjami celowymi dla sektora kosmiczno-obronnego (doradztwo, targi, B+R, infrastruktura, startupy).
        - **Bank Gospodarstwa Krajowego (BGK):** Kredyty preferencyjne, w tym Kredyt Technologiczny z FENG z możliwością premii technicznej. Program "Przedsiębiorcze Podkarpackie" z pożyczkami rozwojowymi.
        - **Polski Fundusz Rozwoju (PFR):** Programy akceleracyjne (np. IDA dla technologii dual-use) i inwestycyjne (PFR Ventures) dla firm deep-tech. Fundusz Innowacji (KPO) na komercjalizację.
        - **Narodowe Centrum Badań i Rozwoju (NCBR):** Pośrednictwo w FENG i KPO, własne konkursy (np. LIDER, Szybka Ścieżka), wsparcie dla konsorcjów przemysłowo-naukowych.
        """)

    with st.expander("Poziom Regionalny (Woj. Podkarpackie, Stalowa Wola)"):
        st.markdown("""
        - **Fundusze Europejskie dla Podkarpacia (FEPK) 2021-2027:** Regionalny program operacyjny (np. Działanie FEPK.01.03 "Wsparcie MŚP – wdrożenia B+R" na innowacyjne produkty/procesy).
        - **Podkarpackie Centrum Innowacji (PCI):** Programy grantowe dla jednostek naukowych (np. FEPK.01.01 "Badania i rozwój" na projekty B+R o wysokim potencjale wdrożeniowym).
        - **Preferencyjne Pożyczki Regionalne:** Środki BGK dla podkarpackich beneficjentów (np. pożyczka rozwojowa dla MŚP). Lokalne fundusze pożyczkowe (np. RIG Stalowa Wola).
        - **Wsparcie Miasta Stalowa Wola:** Wkład rzeczowy (np. budynek KUL), współfinansowanie infrastruktury, ułatwienia w procesach administracyjnych.
        """)

    with st.expander("Poziom Europejski (Unia Europejska)"):
        st.markdown("""
        - **Horyzont Europa:** Główny program B+R+I UE (budżet ~93,5 mld EUR). Obszary: cyfryzacja, AI, kosmos, bezpieczeństwo. Obejmuje European Innovation Council (EIC) Accelerator dla MŚP.
        - **Europejski Fundusz Obronny (EDF):** Finansowanie wspólnych projektów B+R w dziedzinie obronności (roczne budżety >1 mld EUR). Wsparcie dla MŚP poprzez EU Defence Innovation Scheme (EUDIS).
        - **Program Kosmiczny UE (EUSPA):** Konkursy na aplikacje oparte na Galileo, Copernicus, GovSatCom. Budżet ~14,8 mld EUR.
        - **Inne inicjatywy UE:** Eurostars, COSME, Fundusz Odbudowy (KPO), ERDF/ESF, STEP (Strategic Technologies for Europe Platform).
        """)
    
    with st.expander("Inne Źródła (Międzynarodowe, Prywatne)"):
        st.markdown("""
        - **Programy ESA:** Mechanizm "juste retour", Industrial Policy Task Force (IPTF) ESA, TeamTECH FNP, HIPERO ESA, ESA PLIIS. Istotna jest składka Polski do ESA.
        - **Fundusze NATO:** NATO Innovation Fund, DIANA dla technologii obronnych i wywiadowczych.
        - **Kapitał Prywatny:** Fundusze Venture Capital / Private Equity, inwestycje korporacyjne, crowdfunding branżowy, wkłady członków konsorcjum.
        - **Partnerstwa Publiczno-Prywatne (PPP):** Współpraca z ARP, samorządem lokalnym przy dużych projektach inwestycyjnych.
        - **Fundusze ESG i Zielone Obligacje:** Dla projektów o pozytywnym wpływie środowiskowym.
        """)
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # Key Funding Instruments and Programs Section
    st.markdown("""
    <div class="funding-section-card">
        <h3>Kluczowe Instrumenty i Programy Finansowe</h3>
        <p>Poniżej przedstawiono wybrane, kluczowe programy finansowe, które są szczególnie istotne dla strategii finansowania Hubu Technologicznego w Stalowej Woli:</p>
    """, unsafe_allow_html=True)

    key_instruments_cols = st.columns(2)
    with key_instruments_cols[0]:
        st.markdown("""
        **Horyzont Europa (UE)**
        - **Forma wsparcia:** Granty badawczo-innowacyjne na projekty międzynarodowe.
        - **Beneficjenci:** Uczelnie, instytuty, firmy (zwłaszcza konsorcja międzynarodowe).
        - **Budżet/Info:** ~93,5 mld EUR (2021-2027); cele: zrównoważony rozwój, technologie kosmiczne, bezpieczeństwo.
        - **EIC Accelerator:** Komponent HE dla innowacyjnych MŚP (granty do 2,5 mln EUR + inwestycje kapitałowe).
        """)
        st.markdown("<hr style='border-top: 1px solid #eee;'>", unsafe_allow_html=True)
        st.markdown("""
        **Fundusze Europejskie dla Nowoczesnej Gospodarki (FENG - Polska)**
        - **Forma wsparcia:** Dotacje na projekty B+R i wdrożeniowe.
        - **Beneficjenci:** Przedsiębiorcy (MŚP, konsorcja), uczelnie, instytuty badawcze.
        - **Przykłady:** Ścieżka SMART (NCBR) - rozwój zdolności badawczych, wdrożenia innowacji.
        """)
    
    with key_instruments_cols[1]:
        st.markdown("""
        **Europejski Fundusz Obronny (EDF - UE)**
        - **Forma wsparcia:** Dotacje na wspólne projekty B+R w dziedzinie obronności.
        - **Beneficjenci:** Konsorcja przedsiębiorstw i instytucji badawczych z min. 3 państw UE.
        - **Budżet/Info:** Roczne budżety ~1 mld EUR; wsparcie dla MŚP przez EUDIS.
        """)
        st.markdown("<hr style='border-top: 1px solid #eee;'>", unsafe_allow_html=True)
        st.markdown("""
        **Programy Polskiej Agencji Kosmicznej (PAK - Polska)**
        - **Forma wsparcia:** Dotacje celowe na usługi doradcze, udział w targach, prace B+R, studia wykonalności, infrastrukturę, wsparcie startupów.
        - **Beneficjenci:** Firmy z sektora kosmiczno-obronnego, startupy, klastry, osoby fizyczne (szkolenia, staże).
        """)
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # Budget Allocation

# KPI visualization page
def render_kpi_page():
    st.markdown("""
    <div class="landing-section">
        <h2 class="section-title">Kluczowe Wskaźniki Efektywności (KPI)</h2>
        <p class="section-subtitle">Monitorowanie postępów i realizacji celów strategicznych Hubu Technologicznego</p>
    </div>
    """, unsafe_allow_html=True)

    kpi_tabs = st.tabs([
        "📈 Przegląd Ogólny", 
        "🔬 Innowacje i B+R", 
        "💼 Wpływ Ekonomiczny", 
        "🎓 Rozwój Talentów", 
        "🤝 Partnerstwa",
        "⚙️ Realizacja Projektów"
    ])

    with kpi_tabs[0]: # Przegląd Ogólny
        st.markdown("### Kluczowe Wskaźniki Projektu (Stan na Q4 2026)")
        # Values are placeholders or based on current page, to be updated from raport.txt
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
            <div class="kpi-card">
                <h4>Nowe Miejsca Pracy</h4>
                <p style="font-size: 1.8rem; font-weight: 600;">50 / 150+</p>
                <p style="font-size: 0.9rem; color: #6c757d;">Utworzone / Cel długoterminowy</p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div class="kpi-card">
                <h4>Aktywni Partnerzy</h4>
                <p style="font-size: 1.8rem; font-weight: 600;">12 / 20+</p>
                <p style="font-size: 0.9rem; color: #6c757d;">Przemysł, Nauka, Instytucje</p>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown("""
            <div class="kpi-card">
                <h4>Pozyskane Finansowanie</h4>
                <p style="font-size: 1.8rem; font-weight: 600;">1.5M / 5M EUR</p>
                <p style="font-size: 0.9rem; color: #6c757d;">Pozyskane / Cel (Faza 1+2)</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("### Postęp Realizacji Faz Projektu (wg. planu 26-miesięcznego)")
        
        # Data from Tabela 4 in raport.txt
        phases_data = {
            "Faza 1: Fundamenty i Mobilizacja (Miesiące 1-6)": {
                "status": "Ukończona", 
                "progress": 1.0, 
                "desc": "Sformalizowanie konsorcjum, adaptacja budynku, rekrutacja zespołu, pierwsze wnioski finansowe."
            },
            "Faza 2: Pierwsze Operacje i Prototypowanie (Miesiące 7-12)": {
                "status": "W trakcie", 
                "progress": 0.80, # Example, to be updated
                "desc": "Uruchomienie laboratoriów, rozpoczęcie projektów pilotażowych, demonstrator technologii, pozyskanie partnerów."
            },
            "Faza 3: Skalowanie i Ekspansja (Miesiące 13-26+)": {
                "status": "Planowana", 
                "progress": 0.15, # Example, to be updated
                "desc": "Rozszerzenie działalności, programy talentowe, współpraca międzynarodowa, komercjalizacja."
            }
        }

        for phase_name, phase_info in phases_data.items():
            st.markdown(f"<h5>{phase_name} - <span style='color: {'green' if phase_info['status'] == 'Ukończona' else 'orange' if phase_info['status'] == 'W trakcie' else 'grey'};'>{phase_info['status']}</span></h5>", unsafe_allow_html=True)
            st.progress(phase_info["progress"])
            st.caption(phase_info["desc"])
        st.markdown("<br>", unsafe_allow_html=True)


    with kpi_tabs[1]: # Innowacje i B+R
        st.markdown("### Wskaźniki Innowacji i Badań Naukowych")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="Zgłoszenia Patentowe", value="3", delta="Cel: 5 (do 2027)")
        with col2:
            st.metric(label="Publikacje Naukowe", value="8", delta="Cel: 15 (do 2027)")
        with col3:
            st.metric(label="Projekty B+R (w toku)", value="5", delta="+2 vs Q3 2026")

        st.markdown("#### Rozwój Projektów Flagowych")
        flagship_projects_kpi = {
            "Autonomiczne Systemy Wsparcia Misji": {"progress": 0.6, "status": "Prototypowanie", "target_completion": "Q4 2027"},
            "Hybrydowy System Obserwacji Danych": {"progress": 0.4, "status": "Rozwój Algorytmów AI", "target_completion": "Q1 2028"},
            "Inteligentne Materiały Samonaprawiające": {"progress": 0.2, "status": "Badania Podstawowe", "target_completion": "Q3 2028"}
        }
        for project, data in flagship_projects_kpi.items():
            st.text(f"{project} (Cel: {data['target_completion']})")
            st.progress(data["progress"])
            st.caption(f"Aktualny status: {data['status']}")

        # Placeholder for a chart on R&D investment or focus areas
        st.markdown("#### Alokacja Budżetu B+R (Przykładowa)")
        # Data can be inspired by "Alokacja Budżetu" on funding page if R&D specific breakdown is available
        # For now, a simple placeholder or a bar chart of R&D spending per flagship project
        
        # Example: R&D Expenditure per Flagship Project
        data_rd_exp = pd.DataFrame({
            "Projekt Flagowy": list(flagship_projects_kpi.keys()),
            "Budżet B+R (EUR)": [350000, 250000, 200000] # Example values
        })
        fig_rd_exp = px.bar(data_rd_exp, x="Projekt Flagowy", y="Budżet B+R (EUR)", 
                            title="Szacowany Budżet B+R na Projekty Flagowe",
                            color="Projekt Flagowy",
                            labels={"Budżet B+R (EUR)": "Budżet B+R (tys. EUR)"})
        fig_rd_exp.update_layout(showlegend=False)
        st.plotly_chart(fig_rd_exp, use_container_width=True)

    with kpi_tabs[2]: # Wpływ Ekonomiczny
        st.markdown("### Wskaźniki Wpływu Ekonomicznego")
        col1, col2 = st.columns(2) # Adjusted from 3 to 2 columns
        # Removed: st.metric(label="Nowe Miejsca Pracy (Hub i Partnerzy)", value="75", delta="Cel: 150+ (2028)")
        with col1: # Was col2
            st.metric(label="Pozyskane Inwestycje (Prywatne i Publiczne)", value="2.1M EUR", delta="+0.6M vs Q2 2026")
        with col2: # Was col3
            st.metric(label="Liczba Startupów / Spin-offów", value="2", delta="Cel: 5+ (2028)")
        
        st.markdown("#### Przychody z Komercjalizacji Technologii")
        # Placeholder data for revenue growth
        revenue_data = pd.DataFrame({
            "Rok": ["2026 (Prognoza)", "2027 (Cel)", "2028 (Cel)"],
            "Przychody (tys. EUR)": [50, 250, 750] # Example values
        })
        fig_revenue = px.line(revenue_data, x="Rok", y="Przychody (tys. EUR)", 
                              title="Prognozowany Wzrost Przychodów z Komercjalizacji", markers=True)
        st.plotly_chart(fig_revenue, use_container_width=True)

        st.markdown("#### Wartość Projektów z Udziałem Przemysłu")
        # Placeholder for value of industry-collaborated projects
        # Could be a sum or a list of top projects
        st.info("Docelowo: Wykres przedstawiający wzrost wartości projektów realizowanych we współpracy z przemysłem.")


    with kpi_tabs[3]: # Rozwój Talentów
        st.markdown("### Wskaźniki Rozwoju Talentów i Kompetencji")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="Liczba Osób Przeszkolonych (SPACE ACADEMY)", value="80", delta="Cel: 200 (rocznie od 2027)")
        with col2:
            st.metric(label="Uczestnicy 'SPACE 4 TALENTS'", value="45", delta="Nowa edycja w Q1 2027")
        with col3:
            st.metric(label="Zespoły w NASA Space Apps (Stalowa Wola)", value="12", delta="+2 vs poprzednia edycja")

        st.markdown("#### Specjalizacje Szkoleniowe (SPACE ACADEMY)")
        # Placeholder for training specializations distribution
        training_spec_data = pd.DataFrame({
            "Obszar Szkolenia": ["Technologie Satelitarne", "AI i Analiza Danych", "Robotyka Autonomiczna", "Cyberbezpieczeństwo", "Materiały Zaawansowane"],
            "Liczba Uczestników (2026)": [25, 20, 15, 10, 10] # Example values
        })
        fig_training = px.pie(training_spec_data, values="Liczba Uczestników (2026)", names="Obszar Szkolenia", 
                              title="Obszary Szkoleń w SPACE ACADEMY (2026)", hole=0.3)
        st.plotly_chart(fig_training, use_container_width=True)

    with kpi_tabs[4]: # Partnerstwa
        st.markdown("### Wskaźniki Partnerstw i Współpracy")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="Partnerzy Przemysłowi", value="8", delta="HSW, LiuGong, Cognor, etc.")
        with col2:
            st.metric(label="Partnerzy Akademiccy/Badawczy", value="5", delta="Politechniki, Instytuty")
        with col3:
            st.metric(label="Współprace Międzynarodowe (Aktywne)", value="3", delta="ESA, NASA (projekty)")

        st.markdown("#### Intensywność Współpracy (Liczba Wspólnych Projektów)")
        # Placeholder for collaboration intensity - could be a heatmap or network graph snippet
        # Example: Bar chart of joint projects per partner category
        collab_projects_data = pd.DataFrame({
            "Typ Partnera": ["Przemysł", "Nauka", "Instytucje Międzynarodowe"],
            "Liczba Wspólnych Projektów": [10, 7, 4] # Example values
        })
        fig_collab_projects = px.bar(collab_projects_data, x="Typ Partnera", y="Liczba Wspólnych Projektów",
                                     title="Liczba Wspólnych Projektów wg Typu Partnera",
                                     color="Typ Partnera")
        st.plotly_chart(fig_collab_projects, use_container_width=True)
        
        st.info("""
        **Kluczowi Partnerzy (wg raportu.txt):**
        - **Przemysłowi:** HSW S.A., LiuGong Dressta, Cognor S.A., ALWI, Codogni, STALPRZEM, POL-PAW, MISTA.
        - **Akademiccy/Badawczy:** Politechniki (Warszawska, Rzeszowska), WAT, AGH, KUL, Instytuty Badawcze.
        - **Instytucjonalni/Międzynarodowi:** Miasto Stalowa Wola, POLSA, ESA, NASA, ARP, NATO Innovation Fund, DIANA.
        """)

    with kpi_tabs[5]: # Realizacja Projektów
        st.markdown("### Wskaźniki Realizacji Projektów i Infrastruktury")
        
        st.markdown("#### Postęp Budowy Infrastruktury Kluczowej")
        infra_progress = {
            "Adaptacja Budynku KUL (Siedziba Hubu)": {"progress": 0.95, "status": "Finalizacja", "cel": "Q1 2027"},
            "SPACELAB - Laboratoria Testowe i Prototypownie": {"progress": 0.50, "status": "Wyposażanie", "cel": "Q3 2027"},
            "SPACE ACADEMY - Centrum Szkoleniowe": {"progress": 0.30, "status": "Planowanie", "cel": "Q4 2027"}
        }
        for item, data in infra_progress.items():
            st.markdown(f"**{item}** (Cel ukończenia: {data['cel']})")
            st.progress(data["progress"])
            st.caption(f"Status: {data['status']}")
            st.markdown("---")

        st.markdown("#### Harmonogram Projektów Flagowych (Ogólny Status)")
        # Data from Tabela 4 in raport.txt - this is a simplified representation
        # Gantt chart from implementation page is more detailed
        
        flagship_timeline = pd.DataFrame([
            dict(Projekt="Autonomiczne Systemy Wsparcia", Start='2026-08-01', Finish='2027-12-31', Status='W realizacji', Faza='Faza 2/3'),
            dict(Projekt="Hybrydowy System Obserwacji", Start='2027-01-01', Finish='2028-06-30', Status='Planowany', Faza='Faza 3'),
            dict(Projekt="Inteligentne Materiały", Start='2027-03-01', Finish='2028-09-30', Status='Planowany', Faza='Faza 3')
        ])
        flagship_timeline['Start'] = pd.to_datetime(flagship_timeline['Start'])
        flagship_timeline['Finish'] = pd.to_datetime(flagship_timeline['Finish'])

        fig_timeline_kpi = px.timeline(flagship_timeline, x_start="Start", x_end="Finish", y="Projekt", color="Status",
                                 title="Orientacyjny Harmonogram Projektów Flagowych")
        fig_timeline_kpi.update_yaxes(categoryorder="total ascending")
        st.plotly_chart(fig_timeline_kpi, use_container_width=True)

        st.info("Szczegółowy harmonogram dostępny na stronie 'Plan Wdrożenia'.")

# Contact page with form and location info
def render_contact_page():
    st.markdown("""
    <div class="landing-section">
        <h2 class="section-title">Kontakt</h2>
        <p class="section-subtitle">Skontaktuj się z nami w sprawie współpracy lub szczegółów projektu</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Contact information and form in two columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Dane Kontaktowe")
        st.markdown("""
        **Adres:**  
        Hub Technologii Podwójnego Zastosowania  
        ul. Niezłomnych 1  
        37-450 Stalowa Wola  
        
        **Email:**  
        kontakt@hubstalowawola.pl  
        
        **Telefon:**  
        +48 15 123 45 67  
        
        **Godziny otwarcia:**  
        Poniedziałek - Piątek: 8:00 - 16:00  
        """)
        
        # Social media links
        st.markdown("### Media Społecznościowe")
        st.markdown("""
        - [LinkedIn](#)
        - [Twitter](#)
        - [Facebook](#)
        - [YouTube](#)
        """)
    
    with col2:
        st.markdown("### Formularz Kontaktowy")
        
        # Contact form
        contact_name = st.text_input("Imię i nazwisko")
        contact_email = st.text_input("Email")
        contact_subject = st.selectbox(
            "Temat wiadomości",
            ["Współpraca biznesowa", "Możliwości zatrudnienia", "Współpraca naukowa", "Media i PR", "Inne"]
        )
        contact_message = st.text_area("Wiadomość", height=150)
        
        # Submit button with simulated submission
        if st.button("Wyślij wiadomość"):
            if contact_name and contact_email and contact_message:
                st.success("Dziękujemy za wiadomość! Skontaktujemy się z Tobą wkrótce.")
                # In a real app, this would send an email or store the contact message
            else:
                st.warning("Proszę wypełnić wszystkie wymagane pola.")
    
    # Map showing location
    st.markdown("### Nasza Lokalizacja")
    
    # Display map centered on Stalowa Wola
    map_view_state = pdk.ViewState(
        latitude=50.5825,
        longitude=22.0532,
        zoom=13,
        pitch=0,
        bearing=0
    )
    
    # Create marker layer
    marker_layer = pdk.Layer(
        "ScatterplotLayer",
        data=[{
            "position": [22.0532, 50.5825],
            "radius": 50,
            "color": [255, 0, 0]
        }],
        get_position="position",
        get_radius="radius",
        get_fill_color="color",
        pickable=True
    )
    
    # Create deck
    map_deck = pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v10",
        initial_view_state=map_view_state,
        layers=[marker_layer],
        tooltip={"text": "Hub Technologii Podwójnego Zastosowania, Stalowa Wola"}
    )
    
    # Display map
    st.pydeck_chart(map_deck)

# Projects page with project cards and filters
def render_projects_page():
    st.markdown("""
    <div class="landing-section">
        <h2 class="section-title">Projekty Flagowe</h2>
        <p class="section-subtitle">Kluczowe inicjatywy technologiczne realizowane w ramach Hubu</p>
    </div>
    """, unsafe_allow_html=True)

    # Filter options
    st.markdown("### Filtrowanie Projektów")
    col1, col2 = st.columns(2)
    with col1:
        sector = st.multiselect("Sektor zastosowań:", 
                             ["Kosmiczny", "Obronny", "Cywilny"], 
                             default=["Kosmiczny", "Obronny", "Cywilny"])
    with col2:
        status = st.multiselect("Status projektu:", 
                             ["W realizacji", "Planowany", "Zakończony"], 
                             default=["W realizacji"])
    
    # Project cards
    st.markdown("### Nasze Projekty")
    
    # Project 1
    if "Kosmiczny" in sector and "W realizacji" in status:
        with st.expander("SATGUARD - System Monitorowania Orbitalnego", expanded=True):
            st.markdown("""
            #### SATGUARD - System Monitorowania Orbitalnego
            
            **Sektor:** Kosmiczny, Obronny  
            **Status:** W realizacji (2026-2027)  
            **Budżet:** 850,000 EUR  
            **Partnerzy:** HSW S.A., Politechnika Warszawska, POLSA
            
            **Opis:**  
            System autonomicznego monitorowania i śledzenia obiektów orbitalnych, zapewniający dane dla ochrony infrastruktury satelitarnej i planowania misji kosmicznych. Wykorzystuje zaawansowane algorytmy AI do przewidywania trajektorii i potencjalnych kolizji.
            
            **Rezultaty:**
            - Sieć 3 stacji naziemnych do śledzenia obiektów orbitalnych
            - Oprogramowanie do analizy zagrożeń kolizyjnych
            - Integracja z europejskim systemem Space Surveillance and Tracking (SST)
            
            **Zastosowania dualne:**
            - Cywilne: ochrona komercyjnych satelitów, planowanie misji kosmicznych
            - Wojskowe: świadomość sytuacyjna w przestrzeni kosmicznej, ochrona infrastruktury krytycznej
            """)
            
            # Project progress
            st.markdown("**Postęp projektu:**")
            st.progress(0.45, "45%")
            
            # Remove placeholder image
            # st.image("https://placekitten.com/800/400", caption="Wizualizacja systemu SATGUARD")
    
    # Project 2
    if "Obronny" in sector and "W realizacji" in status:
        with st.expander("AUTONOM - Platformy Autonomiczne dla Zastosowań Specjalnych"):
            st.markdown("""
            #### AUTONOM - Platformy Autonomiczne dla Zastosowań Specjalnych
            
            **Sektor:** Obronny, Cywilny  
            **Status:** W realizacji (2026-2028)  
            **Budżet:** 750,000 EUR  
            **Partnerzy:** HSW S.A., WAT, LiuGong Dressta
            
            **Opis:**  
            Rozwój zdalnie sterowanych i autonomicznych platform mobilnych do zadań specjalnych w trudnych warunkach terenowych i klimatycznych. Platformy wykorzystują zaawansowane systemy nawigacji, sensory i algorytmy AI do realizacji misji bez bezpośredniego nadzoru człowieka.
            
            **Rezultaty:**
            - Prototyp platformy autonomicznej o ładowności do 500 kg
            - System sterowania i nawigacji odporny na zakłócenia
            - Moduły misyjne wymienne (obserwacja, transport, oczyszczanie terenu)
            
            **Zastosowania dualne:**
            - Cywilne: eksploracja trudno dostępnych terenów, ratownictwo, reagowanie kryzysowe
            - Wojskowe: rozpoznanie, transport zaopatrzenia, ewakuacja medyczna
            """)
            
            # Project progress
            st.markdown("**Postęp projektu:**")
            st.progress(0.30, "30%")
            
            # Remove placeholder image
            # st.image("https://placekitten.com/800/400", caption="Prototyp platformy AUTONOM")
    
    # Project 3
    if "Kosmiczny" in sector and ("W realizacji" in status or "Planowany" in status):
        with st.expander("MATSPACE - Materiały Nowej Generacji dla Zastosowań Kosmicznych"):
            st.markdown("""
            #### MATSPACE - Materiały Nowej Generacji dla Zastosowań Kosmicznych
            
            **Sektor:** Kosmiczny, Obronny, Cywilny  
            **Status:** Planowany (2027-2029)  
            **Budżet:** 650,000 EUR  
            **Partnerzy:** Cognor S.A., ALWI, AGH, Politechnika Warszawska
            
            **Opis:**  
            Opracowanie i testowanie ultralekkich stopów metali i kompozytów odpornych na ekstremalne warunki kosmiczne. Projekt obejmuje również rozwój technologii samonaprawiających się powłok oraz materiałów wielofunkcyjnych do zastosowań w środowisku kosmicznym.
            
            **Rezultaty:**
            - Nowe stopy aluminium o zwiększonej odporności na mikrometeoryty
            - Powłoki samonaprawiające do zastosowań w próżni kosmicznej
            - Materiały termoizolacyjne nowej generacji
            
            **Zastosowania dualne:**
            - Cywilne: komercyjne pojazdy kosmiczne, instrumenty naukowe
            - Wojskowe: systemy obronne, osłony balistyczne, pojazdy specjalne
            """)
            
            # Project progress
            st.markdown("**Postęp projektu:**")
            st.progress(0.10, "10% (faza planowania)")
            
            # Remove placeholder image
            # st.image("https://placekitten.com/800/400", caption="Materiały MATSPACE podczas testów próżniowych")

# New implementation plan page with Gantt chart and detailed phases
def render_implementation_page():
    st.markdown("""
    <div class="landing-section">
        <h2 class="section-title">Plan Wdrożenia</h2>
        <p class="section-subtitle">Fazy rozwoju i kamienie milowe w horyzoncie 26 miesięcy</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Introduction to implementation plan
    st.markdown("""
    Plan wdrożenia Hubu Technologii Podwójnego Zastosowania w Stalowej Woli jest podzielony na 
    trzy główne fazy, obejmujące łącznie 26 miesięcy. Każda faza skupia się na konkretnych 
    celach i działaniach, które prowadzą do pełnego uruchomienia i rozwoju inicjatywy.
    """)
    
    # Phase tabs for detailed information
    phase_tabs = st.tabs(["Faza 1: Fundamenty i Mobilizacja", 
                          "Faza 2: Pierwsze Operacje i Prototypowanie", 
                          "Faza 3: Skalowanie i Ekspansja"])
    
    with phase_tabs[0]:
        st.markdown("### Faza 1: Fundamenty i Mobilizacja (Miesiące 1-6)")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("""
            #### Kluczowe działania:
            
            * Sformalizowanie umów konsorcjum i powołanie struktury zarządczej (Komitet Sterujący)
            * Zabezpieczenie i rozpoczęcie adaptacji budynku KUL
            * Przeprowadzenie szczegółowej analizy SWOT i rynku
            * Zdefiniowanie projektów pilotażowych w ramach filarów flagowych
            * Rekrutacja kluczowego zespołu Hubu
            * Złożenie pierwszych wniosków o finansowanie
            
            #### Kamienie milowe:
            
            * Podpisane umowy konsorcjum
            * Powołany Komitet Sterujący
            * Zabezpieczony budynek
            * Raport SWOT
            * Lista projektów pilotażowych
            * Zatrudniony zespół
            """)
        
        with col2:
            st.markdown("#### Postęp Fazy 1")
            st.progress(1.0, "Ukończona (100%)")
            
            st.markdown("#### Wskaźniki KPI")
            st.metric("Podpisane umowy", "8", "+3 ponad plan")
            st.metric("Wnioski o finansowanie", "4", "Zgodnie z planem")
    
    with phase_tabs[1]:
        st.markdown("### Faza 2: Pierwsze Operacje i Prototypowanie (Miesiące 7-12)")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("""
            #### Kluczowe działania:
            
            * Uruchomienie pierwszego laboratorium (np. cyberbezpieczeństwa lub UAV)
            * Rozpoczęcie projektów pilotażowych
            * Realizacja pierwszego projektu demonstracyjnego
            * Organizacja "Dni Technologii w Stalowej Woli"
            * Pozyskanie pierwszych partnerów przemysłowych
            
            #### Kamienie milowe:
            
            * Działające laboratorium
            * Rozpoczęte projekty pilotażowe
            * Zrealizowany demonstrator
            * Zorganizowane wydarzenie
            * Pozyskani partnerzy
            """)
        
        with col2:
            st.markdown("#### Postęp Fazy 2")
            st.progress(0.8, "W trakcie (80%)")
            
            st.markdown("#### Wskaźniki KPI")
            st.metric("Uruchomione laboratoria", "1", "Zgodnie z planem")
            st.metric("Realizowane projekty", "3", "+1 ponad plan")
            st.metric("Uczestnicy wydarzeń", "120", "Zgodnie z planem")
    
    with phase_tabs[2]:
        st.markdown("### Faza 3: Skalowanie i Ekspansja (Miesiące 13-26+)")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("""
            #### Kluczowe działania:
            
            * Rozszerzenie działalności na kolejne obszary technologiczne/projekty flagowe
            * Rozwój lokalnych programów talentowych (kursy, certyfikacje)
            * Nawiązanie pierwszych współprac międzynarodowych (projekty NATO/ESA)
            * Koncentracja na komercjalizacji, pierwsze wdrożenia produktów/usług
            * Planowanie pierwszych spin-offów
            
            #### Kamienie milowe:
            
            * Uruchomione kolejne projekty
            * Działające programy talentowe
            * Nawiązana współpraca międzynarodowa
            * Pierwsze przychody
            * Plan spin-off
            """)
        
        with col2:
            st.markdown("#### Postęp Fazy 3")
            st.progress(0.15, "Wczesny etap (15%)")
            
            st.markdown("#### Wskaźniki KPI")
            st.metric("Nowe projekty", "2", "W trakcie realizacji")
            st.metric("Uczestnicy programów talentowych", "25", "W rekrutacji")
            st.metric("Międzynarodowe kontrakty", "1", "W negocjacjach")
    
    # Gantt chart for project timeline
    st.markdown("### Harmonogram Projektu")
    
    # Data for Gantt chart
    tasks = [
        dict(Task="Formalizacja konsorcjum", Start='2026-01-01', Finish='2026-03-31', Resource='Faza 1'),
        dict(Task="Adaptacja budynku KUL", Start='2026-02-15', Finish='2026-07-31', Resource='Faza 1'),
        dict(Task="Rekrutacja zespołu", Start='2026-03-01', Finish='2026-06-30', Resource='Faza 1'),
        dict(Task="Pierwsze laboratorium", Start='2026-07-01', Finish='2026-09-30', Resource='Faza 2'),
        dict(Task="Projekty pilotażowe", Start='2026-08-01', Finish='2026-12-31', Resource='Faza 2'),
        dict(Task="Dni Technologii", Start='2026-11-15', Finish='2026-11-17', Resource='Faza 2'),
        dict(Task="Rozszerzenie działalności", Start='2027-01-01', Finish='2027-06-30', Resource='Faza 3'),
        dict(Task="Programy talentowe", Start='2027-02-01', Finish='2027-12-31', Resource='Faza 3'),
        dict(Task="Współprace międzynarodowe", Start='2027-03-15', Finish='2027-12-31', Resource='Faza 3'),
        dict(Task="Pierwsze wdrożenia", Start='2027-07-01', Finish='2027-12-31', Resource='Faza 3')
    ]
    
    df_tasks = pd.DataFrame(tasks)
    
    # Convert string dates to datetime
    df_tasks['Start'] = pd.to_datetime(df_tasks['Start'])
    df_tasks['Finish'] = pd.to_datetime(df_tasks['Finish'])
    
    # Create color map for phases
    color_map = {
        'Faza 1': '#007BFF',  # Blue
        'Faza 2': '#28A745',  # Green
        'Faza 3': '#DC3545'   # Red
    }
    
    # Create Gantt chart
    fig = px.timeline(
        df_tasks, 
        x_start="Start", 
        x_end="Finish", 
        y="Task",
        color="Resource",
        color_discrete_map=color_map,
        title="Harmonogram Projektu (2026-2028)"
    )
    
    # Update layout
    fig.update_layout(
        autosize=True,
        xaxis_title="Okres realizacji",
        yaxis_title="Zadanie",
        legend_title="Faza projektu",
        showlegend=True
    )
    
    # Add vertical line for current date
    current_date = pd.Timestamp('2026-10-15')  # Example current date
    fig.add_vline(x=current_date, line_width=2, line_dash="dash", line_color="black")
    
    # Show Gantt chart
    st.plotly_chart(fig, use_container_width=True)
    
    # Key project roles and responsibilities
    st.markdown("### Struktura Zarządzania i Nadzoru")
    
    st.markdown("""
    Efektywne zarządzanie inicjatywą wymaga jasno zdefiniowanej struktury organizacyjnej, 
    która zapewni zarówno strategiczny nadzór, jak i sprawność operacyjną:
    """)
    
    org_cols = st.columns(3)
    
    with org_cols[0]:
        st.markdown("""
        #### Komitet Sterujący Konsorcjum
        
        **Rola:** Organ nadzorczy, wyznaczający strategiczne kierunki
        
        **Skład:**
        - Przedstawiciele miasta Stalowa Wola
        - Kluczowe firmy przemysłowe (HSW S.A.)
        - POLSA, ESA, NASA (reprezentacja)
        - ARP, uczelnie i instytuty badawcze
        """)
    
    with org_cols[1]:
        st.markdown("""
        #### Zarząd Hubu (Zespół Operacyjny)
        
        **Rola:** Bieżące zarządzanie działalnością
        
        **Odpowiedzialność:**
        - Administracja obiektem (budynek KUL)
        - Koordynacja projektów flagowych
        - Organizacja wydarzeń i szkoleń
        - Działania promocyjne
        """)
    
    with org_cols[2]:
        st.markdown("""
        #### Rada Doradcza
        
        **Rola:** Funkcja doradcza dla Komitetu i Zarządu
        
        **Skład:**
        - Niezależni eksperci branżowi
        - Naukowcy o międzynarodowej renomie
        - Przedstawiciele potencjalnych inwestorów
        """)

# Footer that appears at the bottom of each page
def render_footer():
    st.markdown("""    
    <style>
    /* All Footer CSS is contained here */
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0; 
        background-color: white;
        border-top: 1px solid #eee;
        padding: 0.3rem 0;
        font-size: 0.85rem;
        z-index: 1000;
        height: auto;
        box-sizing: border-box;
    }

    .footer-content-wrapper {
        margin-left: 20vw; /* Default for new 20vw expanded sidebar */
        height: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
        box-sizing: border-box;
    }

    [data-testid="stSidebar"][aria-expanded="false"] ~ .main .footer .footer-content-wrapper {
        margin-left: 3.5rem; /* For collapsed sidebar (approx 56px) */
    }

    .footer-row {
        display: inline-flex;
        align-items: center;
        box-sizing: border-box;
    }

    .footer-item {
        padding: 0 0.6rem;
        white-space: nowrap;
        text-align: center;
        box-sizing: border-box;
    }

    .footer-item h4 {
        display: inline;
        font-size: 0.9rem;
        font-weight: 600;
        color: #333;
        margin-right: 0.3rem;
    }

    .footer-item p {
        display: inline;
        color: #333;
        margin: 0;
    }

    .footer a {
        color: #333;
        text-decoration: none;
    }

    .footer-divider {
        height: 18px;
        width: 1px;
        background-color: #eee;
        margin: 0 0.3rem;
    }
    </style>

    <div class="footer">
        <div class="footer-content-wrapper">
            <div class="footer-row">
                <div class="footer-item">
                    <h4>Kontakt:</h4>
                    <p>Hub Technologii Podwójnego Zastosowania, ul. Niezłomnych 1, 37-450 Stalowa Wola</p>
                </div>
                <div class="footer-divider"></div>
                <div class="footer-item">
                    <h4>Email:</h4>
                    <p><a href="mailto:kontakt@hubstalowawola.pl">kontakt@hubstalowawola.pl</a></p>
                </div>
                <div class="footer-divider"></div>
                <div class="footer-item">
                    <h4>Partnerzy:</h4>
                    <p><a href="#">NASA</a> | <a href="#">ESA</a> | <a href="#">POLSA</a> | <a href="#">HSW S.A.</a></p>
                </div>
                <div class="footer-divider"></div>
                <div class="footer-item">
                    <p>© 2026 Konsorcjum Innowacji w Stalowej Woli</p>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# New strategic analysis page with detailed SWOT and market analysis
def render_strategy_page():
    st.markdown("""
    <div class="landing-section">
        <h2 class="section-title">Analiza Strategiczna</h2>
        <p class="section-subtitle">Kompleksowa ocena inicjatywy technologicznej w Stalowej Woli</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Introduction to strategic analysis
    st.markdown("""
    Analiza strategiczna Hubu Technologii Podwójnego Zastosowania w Stalowej Woli obejmuje 
    szczegółową ocenę ekosystemu przemysłowego, aktywów akademickich oraz kontekstu 
    krajowego i międzynarodowego. Pozwala ona zidentyfikować kluczowe czynniki sukcesu 
    oraz potencjalne wyzwania dla inicjatywy.
    """)
    
    # Industrial ecosystem analysis
    st.markdown("### Potęga Przemysłowa: Możliwości i Potencjał")
    
    st.markdown("""
    Stalowa Wola dysponuje solidnym zapleczem przemysłowym, które stanowi fundament dla rozwoju 
    zaawansowanych technologii podwójnego zastosowania. Kluczowe podmioty i ich potencjał obejmują:
    """)
    
    industrial_assets = pd.DataFrame([
        {
            "Firma/Podmiot": "HSW S.A.",
            "Kluczowe Produkty/Kompetencje": "Bojowe wozy piechoty (Borsuk), systemy artyleryjskie (Krab), systemy wieżowe (ZSSW-30), robotyzacja produkcji",
            "Obecne Zastosowania": "Sektor obronny",
            "Proponowane Rozszerzenie Dual-Use": "Autonomiczne platformy robotyczne, integracja z systemami satelitarnymi, systemy bezzałogowe, komponenty dla misji kosmicznych",
            "Potencjał Wdrożenia": "Wysoki"
        },
        {
            "Firma/Podmiot": "LiuGong Dressta",
            "Kluczowe Produkty/Kompetencje": "Ciężkie maszyny budowlane",
            "Obecne Zastosowania": "Budownictwo, infrastruktura",
            "Proponowane Rozszerzenie Dual-Use": "Adaptacja maszyn do pracy w ekstremalnych warunkach (Księżyc/Mars), mobilne systemy inżynieryjne dla wojska",
            "Potencjał Wdrożenia": "Średni"
        },
        {
            "Firma/Podmiot": "Cognor S.A., ALWI",
            "Kluczowe Produkty/Kompetencje": "Produkty stalowe, komponenty konstrukcyjne",
            "Obecne Zastosowania": "Przemysł ciężki, obronny",
            "Proponowane Rozszerzenie Dual-Use": "Ultralekkie stopy, powłoki odporne na warunki kosmiczne, komponenty dla rakiet i satelitów",
            "Potencjał Wdrożenia": "Średni"
        },
        {
            "Firma/Podmiot": "Codogni",
            "Kluczowe Produkty/Kompetencje": "Kulki mielące, precyzyjne elementy mechaniczne",
            "Obecne Zastosowania": "Przemysł, wojsko",
            "Proponowane Rozszerzenie Dual-Use": "Precyzyjne komponenty do napędów satelitów i robotów kosmicznych",
            "Potencjał Wdrożenia": "Wysoki"
        },
        {
            "Firma/Podmiot": "STALPRZEM",
            "Kluczowe Produkty/Kompetencje": "Beton, prefabrykaty betonowe",
            "Obecne Zastosowania": "Budownictwo, instalacje wojskowe",
            "Proponowane Rozszerzenie Dual-Use": "Beton z regolitów księżycowych/marsjańskich, konstrukcje baz kosmicznych, schrony o podwyższonej odporności",
            "Potencjał Wdrożenia": "Niski"
        },
        {
            "Firma/Podmiot": "POL-PAW",
            "Kluczowe Produkty/Kompetencje": "Odzież i obuwie BHP",
            "Obecne Zastosowania": "Przemysł, wojsko",
            "Proponowane Rozszerzenie Dual-Use": "Materiały termoizolacyjne i antyradiacyjne dla astronautów/żołnierzy, inteligentne tkaniny, systemy monitoringu zdrowia",
            "Potencjał Wdrożenia": "Średni"
        }
    ])

    # Function to get color based on potential
    def get_potential_color(potential_level):
        if potential_level == 'Wysoki':
            return '#28a745'  # Green
        elif potential_level == 'Średni':
            return '#ffc107'  # Yellow
        elif potential_level == 'Niski':
            return '#dc3545'  # Red
        return '#6c757d'  # Grey for others

    st.markdown("""
    <style>
    .company-card {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 6px 12px rgba(0,0,0,0.08);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .company-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.12);
    }
    .company-card h4 {
        color: #1a1a2e;
        margin-bottom: 12px;
        font-size: 1.4em;
        border-bottom: 2px solid #e0e0e0;
        padding-bottom: 8px;
    }
    .company-card p {
        margin-bottom: 8px;
        line-height: 1.6;
        font-size: 0.95em;
        color: #4a4a4a;
    }
    .company-card strong {
        color: #333;
        font-weight: 600;
    }
    .potential-badge {
        display: inline-block;
        padding: 5px 12px;
        border-radius: 15px;
        font-weight: bold;
        font-size: 0.85em;
        color: white;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    </style>
    """, unsafe_allow_html=True)

    # Display companies as cards in two columns
    num_columns = 2
    cols = st.columns(num_columns)
    for index, row in industrial_assets.iterrows():
        potential_color = get_potential_color(row['Potencjał Wdrożenia'])
        with cols[index % num_columns]:
            st.markdown(f""" 
            <div class="company-card">
                <h4>{row['Firma/Podmiot']}</h4>
                <p><strong>Kluczowe Produkty/Kompetencje:</strong> {row['Kluczowe Produkty/Kompetencje']}</p>
                <p><strong>Obecne Zastosowania:</strong> {row['Obecne Zastosowania']}</p>
                <p><strong>Proponowane Rozszerzenie Dual-Use:</strong> {row['Proponowane Rozszerzenie Dual-Use']}</p>
                <p><strong>Potencjał Wdrożenia:</strong> <span class="potential-badge" style="background-color:{potential_color};">{row['Potencjał Wdrożenia']}</span></p>
            </div>
            """, unsafe_allow_html=True)
    
    # SWOT Analysis with expanded details
    st.markdown("### Rozszerzona Analiza SWOT")
    
    swot_tabs = st.tabs(["Mocne Strony (S)", "Słabe Strony (W)", "Szanse (O)", "Zagrożenia (T)"])
    
    with swot_tabs[0]:
        st.markdown("### Mocne Strony")
        
        s_cols = st.columns(2)
        with s_cols[0]:
            st.markdown("""
            #### S1: Silna baza przemysłowa
            
            HSW S.A. i inne firmy lokalne posiadają doświadczenie w produkcji zaawansowanych systemów,
            potencjał dual-use i kompetencje w zakresie robotyzacji i cyfryzacji.
            
            **Implikacje strategiczne:**
            - Szybsze wdrażanie nowych technologii dzięki istniejącemu know-how
            - Możliwość rozwoju produktów na bazie obecnych kompetencji
            """)
            
            st.markdown("""
            #### S2: Proaktywne wsparcie miasta
            
            Udostępnienie budynku KUL (5800 m²), ułatwienia w finansowaniu i współpracy,
            zaangażowanie w koordynację działań.
            
            **Implikacje strategiczne:**
            - Redukcja kosztów początkowych i barier wejścia
            - Przyspieszenie procesu uruchomienia projektu
            """)
        
        with s_cols[1]:
            st.markdown("""
            #### S3: Istniejące inicjatywy rozwoju talentów
            
            Programy jak "SPACE 4 TALENTS" oraz organizacja lokalnych edycji
            globalnego hackathonu NASA Space Apps Challenge.
            
            **Implikacje strategiczne:**
            - Przyciąganie młodych talentów do inicjatywy
            - Budowanie ekosystemu innowacji od podstaw
            """)
            
            st.markdown("""
            #### S4: Korzyści wynikające z członkostwa Polski w ESA
            
            Mechanizm "juste retour" zapewniający, że każda złotówka wpłacona do ESA
            wraca do polskich firm w ramach zamówień agencji.
            
            **Implikacje strategiczne:**
            - Dostęp do finansowania europejskiego
            - Potencjał na kontrakty międzynarodowe
            """)
    
    with swot_tabs[1]:
        st.markdown("### Słabe Strony")
        
        w_cols = st.columns(2)
        with w_cols[0]:
            st.markdown("""
            #### W1: Potencjalne luki kompetencyjne
            
            Niedobór specjalistów w zakresie wysoce specjalistycznych technologii
            kosmicznych i AI na lokalnym rynku pracy.
            
            **Implikacje strategiczne:**
            - Konieczność inwestycji w programy edukacyjne i szkoleniowe
            - Potrzeba przyciągania specjalistów z innych regionów/krajów
            """)
            
            st.markdown("""
            #### W2: Zależność od zewnętrznych źródeł finansowania
            
            Szczególnie w początkowej fazie projektu, kiedy brak własnych
            przychodów operacyjnych.
            
            **Implikacje strategiczne:**
            - Ryzyko płynności finansowej
            - Konieczność zabezpieczenia różnorodnych źródeł finansowania
            """)
        
        with w_cols[1]:
            st.markdown("""
            #### W3: Złożoność koordynacji konsorcjum
            
            Trudności w zarządzaniu różnorodnymi podmiotami o odmiennych
            priorytetach i kulturach organizacyjnych.
            
            **Implikacje strategiczne:**
            - Potrzeba silnego przywództwa i jasnych struktur zarządczych
            - Konieczność wypracowania wspólnej wizji i celów
            """)
            
            st.markdown("""
            #### W4: Konieczność budowy infrastruktury od podstaw
            
            Potrzeba tworzenia specjalistycznych laboratoriów i infrastruktury
            badawczej, co wymaga czasu i nakładów.
            
            **Implikacje strategiczne:**
            - Opóźnienia w uruchomieniu pełnej funkcjonalności
            - Konieczność etapowego rozwoju infrastruktury
            """)
    
    with swot_tabs[2]:
        st.markdown("### Szanse")
        
        o_cols = st.columns(2)
        with o_cols[0]:
            st.markdown("""
            #### O1: Rosnący globalny rynek kosmiczny i obronny
            
            Zwiększone zapotrzebowanie na innowacyjne rozwiązania dual-use
            w kontekście nowych wyzwań geopolitycznych.
            
            **Implikacje strategiczne:**
            - Możliwość zajęcia pozycji w rozwijających się niszach rynkowych
            - Potencjał eksportowy dla rozwiązań o wysokiej wartości dodanej
            """)
            
            st.markdown("""
            #### O2: Dostępność funduszy unijnych i krajowych
            
            Programy jak Horyzont Europa, Fundusz Odbudowy, NCBR, KPK
            oferujące finansowanie dla inicjatyw badawczo-rozwojowych.
            
            **Implikacje strategiczne:**
            - Możliwość pozyskania znaczących środków na rozwój
            - Dywersyfikacja źródeł finansowania
            """)
        
        with o_cols[1]:
            st.markdown("""
            #### O3: Możliwość strategicznych współprac międzynarodowych
            
            Potencjalne partnerstwa z NASA, ESA, partnerami z NATO
            w zakresie rozwoju technologii.
            
            **Implikacje strategiczne:**
            - Transfer wiedzy i technologii
            - Dostęp do globalnych łańcuchów wartości
            """)
            
            st.markdown("""
            #### O4: Wykorzystanie mechanizmu "juste retour" z ESA
            
            Finansowanie konkretnych projektów dzięki składkom Polski do ESA,
            które wracają w formie kontraktów.
            
            **Implikacje strategiczne:**
            - Stabilne źródło finansowania dla wybranych projektów
            - Lepsza pozycja w pozyskiwaniu kontraktów europejskich
            """)
    
    with swot_tabs[3]:
        st.markdown("### Zagrożenia")
        
        t_cols = st.columns(2)
        with t_cols[0]:
            st.markdown("""
            #### T1: Niestabilność geopolityczna
            
            Zmiany priorytetów i budżetów obronnych w zależności od
            sytuacji międzynarodowej.
            
            **Implikacje strategiczne:**
            - Niepewność planowania długoterminowego
            - Konieczność elastycznego dostosowania strategii
            """)
            
            st.markdown("""
            #### T2: Silna konkurencja
            
            Rywalizacja ze strony innych regionów i hubów technologicznych
            w Polsce i Europie o talenty, fundusze i projekty.
            
            **Implikacje strategiczne:**
            - Potrzeba wyrazistego pozycjonowania i specjalizacji
            - Konieczność budowy unikalnej propozycji wartości
            """)
        
        with t_cols[1]:
            st.markdown("""
            #### T3: Ryzyko szybkiej obsolescencji technologicznej
            
            Dynamicznie zmieniające się sektory wymagają ciągłej innowacji
            i adaptacji do nowych technologii.
            
            **Implikacje strategiczne:**
            - Konieczność ciągłych inwestycji w B+R
            - Potrzeba elastycznego podejścia do rozwoju produktów
            """)
            
            st.markdown("""
            #### T4: Trudności w przyciągnięciu specjalistów
            
            Wyzwania związane z pozyskaniem i zatrzymaniem wysoko
            wykwalifikowanych kadr na rynku lokalnym.
            
            **Implikacje strategiczne:**
            - Potrzeba konkurencyjnych warunków zatrudnienia
            - Inwestycje w jakość życia i atrakcyjność miasta
            """)
    
    # Strategic Positioning Analysis
    st.markdown("### Pozycjonowanie Strategiczne")
    
    # Radar chart showing strategic positioning vs competitors
    st.markdown("#### Pozycja Konkurencyjna Hubu w Stalowej Woli")
    
    # Data for radar chart
    categories = ['Infrastruktura', 'Innowacyjność', 'Partnerstwa', 
                 'Finansowanie', 'Talenty', 'Wsparcie instytucjonalne']
    
    radar_data = pd.DataFrame({
        'Kategoria': categories,
        'Hub Stalowa Wola': [4.2, 3.8, 4.5, 3.5, 3.2, 4.8],
        'Śląski Hub Kosmiczny': [4.0, 4.2, 3.8, 4.0, 4.3, 3.5],
        'Centrum Technologii Warszawa': [3.8, 4.5, 4.2, 4.5, 4.7, 4.0],
        'Hub Technologiczny Rzeszów': [3.5, 3.3, 3.5, 3.8, 3.0, 3.7]
    })
    
    # Create radar chart
    fig = go.Figure()
    
    for hub in radar_data.columns[1:]:
        fig.add_trace(go.Scatterpolar(
            r=radar_data[hub],
            theta=radar_data['Kategoria'],
            fill='toself',
            name=hub
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5]
            )
        ),
        showlegend=True,
        title="Analiza Porównawcza Hubów Technologicznych w Polsce"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Key strategic imperatives
    st.markdown("### Strategiczne Imperatywy dla Polski i Stalowej Woli")
    
    imperative_cols = st.columns(2)
    
    with imperative_cols[0]:
        st.markdown("""
        #### Imperatyw 1: Wzmocnienie Suwerenności Technologicznej
        
        Rozwijanie krajowych zdolności w strategicznych sektorach technologicznych,
        takich jak kosmiczny i obronny, jest kluczowe dla bezpieczeństwa narodowego
        i niezależności Polski.
        
        **Konkretne działania:**
        - Rozwój technologii podwójnego zastosowania
        - Budowa krajowych łańcuchów dostaw
        - Inwestycje w B+R w obszarach strategicznych
        """)
        
        st.markdown("""
        #### Imperatyw 2: Stymulacja Lokalnej Gospodarki
        
        Przekształcenie Stalowej Woli w hub innowacji technologicznych przyczyni się
        do tworzenia miejsc pracy, przyciągania inwestycji i rozwoju ekonomicznego
        całego regionu.
        
        **Konkretne działania:**
        - Tworzenie wysokopłatnych miejsc pracy
        - Rozwój ekosystemu startupowego
        - Współpraca z lokalnymi przedsiębiorstwami
        """)
    
    with imperative_cols[1]:
        st.markdown("""
        #### Imperatyw 3: Wzmocnienie Pozycji Polski w NATO i ESA
        
        Inicjatywa przyczyni się do budowania pozycji Polski jako ważnego
        kontrybutora technologicznego w strukturach międzynarodowych.
        
        **Konkretne działania:**
        - Rozwój technologii zgodnych z priorytetami NATO/ESA
        - Aktywny udział w międzynarodowych projektach
        - Budowa kompetencji uznawanych globalnie
        """)
        
        st.markdown("""
        #### Imperatyw 4: Rozwój Kapitału Ludzkiego
        
        Inwestycje w kształcenie i rozwój wykwalifikowanych specjalistów
        w obszarach technologii przyszłości.
        
        **Konkretne działania:**
        - Programy edukacyjne i szkoleniowe
        - Współpraca z uczelniami
        - Przyciąganie talentów z Polski i zagranicy
        """)
    
    # Business pitch summary
    st.markdown("### Esencja Oferty Biznesowej")
    
    with st.expander("Nasza Unikalna Propozycja Wartości (UVP)", expanded=True):
        st.markdown("""
        #### 1. Synergia Doświadczenia i Innowacji:
        Efektywnie łączymy ugruntowaną pozycję i zaawansowane zdolności produkcyjne liderów przemysłu, takich jak HSW S.A., z dynamiką, elastycznością startupów oraz potencjałem badawczym renomowanych uczelni. Tworzymy w ten sposób unikalny ekosystem sprzyjający przełomowym rozwiązaniom.

        #### 2. Infrastruktura Gotowa na Twój Sukces:
        Oferujemy dostęp do dedykowanego przez miasto budynku oraz planujemy inwestycje w nowoczesne, specjalistyczne laboratoria. Znacząco redukuje to bariery wejścia i koszty początkowe dla naszych partnerów, przyspieszając realizację ich projektów.

        #### 3. Wsparcie w Drodze do Globalnych Rynków:
        Aktywnie wspieramy naszych partnerów w nawiązywaniu strategicznych kontaktów biznesowych, efektywnym pozyskiwaniu grantów krajowych i międzynarodowych oraz w budowaniu trwałych relacji na arenie globalnej. Twój sukces jest naszym priorytetem.

        #### 4. Kuźnia Talentów dla Przyszłości:
        Inwestujemy w kompleksowe programy edukacyjne i inicjatywy rozwoju zawodowego. Gwarantuje to stały dopływ wysoko wykwalifikowanych specjalistów i młodych, ambitnych talentów, gotowych podejmować najnowsze wyzwania technologiczne.

        #### 5. Strategia Dual-Use: Siła Adaptacji:
        Koncentrujemy się na technologiach podwójnego zastosowania (dual-use). Takie podejście maksymalizuje potencjał rynkowy naszych rozwiązań i zapewnia większą stabilność oraz odporność na zmiany koniunktury w różnych sektorach gospodarki.
        """)

# Main execution - placing this at the very end after all functions are defined
if __name__ == "__main__":
    # Define the main content based on navigation
    if st.session_state.current_page == "overview":
        render_overview_page()
    elif st.session_state.current_page == "summary":
        render_summary_page()
    elif st.session_state.current_page == "projects":
        render_projects_page()
    elif st.session_state.current_page == "partners":
        render_partners_section()
    elif st.session_state.current_page == "funding":
        render_funding_page()
    elif st.session_state.current_page == "kpi":
        render_kpi_page()
    elif st.session_state.current_page == "contact":
        render_contact_page()
    elif st.session_state.current_page == "implementation":
        render_implementation_page()
    elif st.session_state.current_page == "strategy":
        render_strategy_page()
        
    # Always render the footer
  

import streamlit as st

def inject_custom_components():
    """Injects modern CSS inspired by the original React app."""
    st.markdown("""
        <style>
        /* Hide Default Streamlit Menu & Deploy Button */
        #MainMenu {visibility: hidden;}
        .stDeployButton {display: none;}
        footer {visibility: hidden;}
        header {background-color: transparent !important; box-shadow: none !important;}
        .stMarkdown a.anchor, [data-testid="stHeader"] a {display: none !important;}

        /* Global App Background */
        .stApp {
            background-color: #000000;
            background-image: radial-gradient(circle at top left, rgba(14, 165, 233, 0.15) 0%, transparent 50%),
                              radial-gradient(circle at bottom right, rgba(30, 64, 175, 0.15) 0%, transparent 50%);
            color: #f8fafc;
            font-family: 'Inter', sans-serif;
        }

        /* Container expanding to somewhat mimic the split layout */
        .block-container {
            max-width: 1200px !important;
            padding-top: 3rem !important;
        }

        /* Glassmorphism Form / Content Container */
        .glass-card {
            background: rgba(15, 23, 42, 0.6);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 40px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
            color: #f8fafc;
            transition: all 0.3s ease;
        }

        /* Headings & Texts */
        .gradient-text {
            background: linear-gradient(to right, #ffffff, #94a3b8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
        }
        
        .accent-text {
            color: #38bdf8;
        }

        /* Inputs */
        .stTextInput>div>div>input {
            background-color: rgba(15, 23, 42, 0.8) !important;
            border-radius: 12px;
            border: 1px solid rgba(255,255,255,0.15) !important;
            color: white !important;
            font-size: 1.1rem !important;
            padding: 15px !important;
            text-align: left;
        }
        .stTextInput>div>div>input:focus {
            box-shadow: 0 0 0 2px #38bdf8;
            border-color: transparent !important;
        }
        .stTextInput>label {
            font-size: 1rem !important;
            color: #cbd5e1 !important;
        }

        /* Buttons */
        .stButton>button {
            border-radius: 12px;
            background: #ffffff;
            color: #0f172a;
            border: none;
            font-weight: 600;
            font-size: 1rem !important;
            padding: 12px 24px !important;
            transition: all 0.2s ease;
            width: 100%;
        }
        .stButton>button:hover {
            background: #e2e8f0;
            transform: scale(1.02);
        }
        .stButton>button:active {
            transform: scale(0.98);
        }

        /* Hero section imitation on the left */
        .hero-section {
            padding: 40px 20px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            height: 100%;
        }
        
        hr {
            border-color: rgba(255,255,255,0.05);
        }

        /* Camera input styling */
        [data-testid="stCameraInput"] {
            border-radius: 16px;
            overflow: hidden;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        </style>
    """, unsafe_allow_html=True)

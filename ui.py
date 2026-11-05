CSS = """
<style>
.block-container {padding-top: 2rem; max-width: 1100px;}
.hero {
  background: linear-gradient(135deg,#6366f1 0%,#8b5cf6 50%,#ec4899 100%);
  padding: 28px 32px; border-radius: 18px; margin-bottom: 18px;
  box-shadow: 0 10px 30px rgba(139,92,246,.35);
}
.hero h1 {color:#fff; margin:0; font-size:2rem;}
.hero p {color:#f1e9ff; margin:6px 0 0; font-size:1rem;}
.stTabs [data-baseweb="tab-list"] {gap: 8px;}
.stTabs [data-baseweb="tab"] {
  background:#1a1f36; border-radius:12px; padding:10px 16px; height:auto;
  border:1px solid #2a3050;
}
.stTabs [aria-selected="true"] {
  background: linear-gradient(135deg,#6366f1,#8b5cf6); color:#fff !important;
  border:none;
}
.stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] {display:none;}
.stButton>button {
  background: linear-gradient(135deg,#6366f1,#8b5cf6); color:#fff; border:none;
  border-radius:10px; padding:.5rem 1.2rem; font-weight:600; transition:.2s;
}
.stButton>button:hover {transform: translateY(-2px); box-shadow:0 6px 18px rgba(139,92,246,.5); color:#fff;}
[data-testid="stMetric"] {background:#1a1f36; padding:16px; border-radius:14px; border:1px solid #2a3050;}
[data-testid="stChatMessage"] {background:#1a1f36; border-radius:14px; padding:12px; margin-bottom:8px;}
textarea, input {border-radius:10px !important;}
#MainMenu, footer {visibility:hidden;}
</style>
"""

def hero(title, subtitle):
    return f'<div class="hero"><h1>{title}</h1><p>{subtitle}</p></div>'
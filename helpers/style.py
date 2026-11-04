import streamlit as st

def pageInit():
    return st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

        :root {
            --primary: #b81120;
            --primary-dark: #99101c;
            --surface: #f7f9fd;
            --surface-low: #f2f4f8;
            --surface-high: #e6e8ec;
            --ink: #191c1f;
            --muted: #5b626d;
            --teal: #006483;
            --border: #e6e8ec;
        }
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }
        .stApp { background: var(--surface); color: var(--ink); }
        [data-testid="stHeader"] { background: rgba(247,249,253,.92); }
        .block-container {
            max-width: 1500px;
            padding-top: 1.5rem;
            padding-bottom: 3rem;
        }
        h1, h2, h3 { color: var(--ink); letter-spacing: -0.035em; }
        h1 { font-size: clamp(1.7rem, 3vw, 2.25rem) !important; font-weight: 800 !important; }
        h2 { font-size: 1.12rem !important; font-weight: 700 !important; }
        p, label { color: var(--muted); }
        code, .mono { font-family: 'JetBrains Mono', monospace !important; }
        .topbar {
            display:flex; justify-content:space-between; align-items:center;
            padding: .8rem 1.1rem; margin-bottom: 1.5rem;
            background: rgba(255,255,255,.9); border:1px solid var(--border);
            border-radius: 14px; box-shadow: 0 2px 12px rgba(0,0,0,.035);
        }
        .brand { font-weight:700; color:var(--ink); font-size:1rem; }
        .brand-sub { font-size:.76rem; color:var(--muted); margin-top:3px; }
        .version {
            font-family:'JetBrains Mono',monospace; font-size:.72rem;
            background:var(--surface-low); padding:6px 10px; border-radius:7px;
            color:var(--muted);
        }
        .eyebrow {
            display:inline-flex; gap:8px; align-items:center;
            background:#eceef2; color:#5b626d; border-radius:20px;
            padding:5px 11px; font:500 .72rem 'JetBrains Mono',monospace;
            margin-bottom:12px;
        }
        .dot { width:7px; height:7px; display:inline-block; border-radius:50%; background:var(--primary); }
        .subtitle { color:var(--muted); margin-top:-8px; margin-bottom:1.6rem; line-height:1.6; }
        .section-card {
            background:#fff; border:1px solid var(--border); border-radius:14px;
            padding:1.2rem 1.25rem; margin:1.1rem 0;
            box-shadow:0 2px 9px rgba(0,0,0,.025);
        }
        .section-heading {
            display:flex; align-items:center; gap:10px; margin-bottom:1rem;
            color:var(--ink); font-size:1.05rem; font-weight:700;
        }
        .section-number {
            width:25px; height:25px; border-radius:7px; display:inline-flex;
            justify-content:center; align-items:center; color:white;
            background:var(--primary); font-size:.78rem; font-weight:700;
        }
        .tag {
            margin-left:auto; background:#e8f5f8; color:var(--teal);
            border-radius:6px; padding:4px 8px; font:500 .68rem 'JetBrains Mono',monospace;
        }
        .inner-card {
            background:var(--surface-low); border-radius:10px; padding:1rem;
            height:100%; border:1px solid #eef0f3;
        }
        .inner-title { font-weight:650; color:var(--ink); margin-bottom:5px; }
        .helper { color:var(--muted); font-size:.82rem; line-height:1.5; }
        .metric {
            background:var(--surface-low); padding:14px; border-radius:10px;
            border:1px solid #eef0f3; min-height:100px;
        }
        .metric-label { font-size:.68rem; color:var(--muted); letter-spacing:.08em; font-weight:700; }
        .metric-value { font-size:1.65rem; font-weight:800; color:var(--ink); margin-top:7px; }
        .metric-note { color:var(--teal); font-size:.75rem; margin-top:3px; }
        .info-callout {
            background:#eaf5f8; border:1px solid #d8edf3; border-radius:9px;
            padding:12px 14px; color:#245666; font-size:.82rem; line-height:1.6;
        }
        .status-box {
            background:var(--surface-low); border-radius:10px; padding:13px 15px;
            border:1px solid var(--border); margin-bottom:12px;
        }
        div.stButton > button, div.stDownloadButton > button {
            border-radius:8px; min-height:2.65rem; font-weight:650;
            border:1px solid var(--border);
        }
        div.stButton > button[kind="primary"] {
            background:var(--primary); border-color:var(--primary); color:white;
        }
        div.stButton > button[kind="primary"]:hover {
            background:var(--primary-dark); border-color:var(--primary-dark); color:white;
        }
        div.stDownloadButton > button {
            background:#e6e8ec; color:var(--ink); width:100%;
        }
        [data-testid="stFileUploader"] {
            background:#fff; border-radius:9px; border:1px dashed #c9cdd5;
            padding:8px;
        }
        [data-testid="stDataFrame"] { border:1px solid var(--border); border-radius:9px; overflow:hidden; }
        div[data-testid="stTabs"] button { font-weight:600; }
        hr { border-color:var(--border); }
        @media(max-width: 700px) {
            .block-container { padding-left:1rem; padding-right:1rem; }
            .section-card { padding:1rem; }
            .metric-value { font-size:1.25rem; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

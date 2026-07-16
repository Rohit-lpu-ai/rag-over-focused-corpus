"""
Design system for StudyBuddy AI.

Token system:
  Color   -- "ink & parchment" in light mode, "study lamp at night" in dark mode.
             Primary is a midnight indigo (#362F78 / #8A7FFF), accent is a warm
             lamp-amber (#E8A33D / #F0B65C) -- deliberately not the generic
             purple-gradient-on-black or cream+terracotta SaaS defaults.
  Type    -- Fraunces (serif, display) for headings/brand -- gives the app a
             "reading room" character instead of a generic tech-sans logo.
             Public Sans for body copy. JetBrains Mono for stats, chunk ids,
             similarity scores -- anything that reads as data/citation.
  Layout  -- Sidebar for navigation + KB status. Reading-pane max-width on
             main content so long answers stay comfortable to read.
  Signature -- Source results are styled as library index/citation cards:
             a numbered footnote badge, a monospace metadata line, a dashed
             "torn card" left edge, and a soft amber lamp-glow on hover.

This module is purely presentational. It does not import or touch pyfiles/.
"""

import streamlit as st


def _theme_vars(theme: str) -> str:
    if theme == "dark":
        return """
        --bg:#14121F; --bg-elevated:#1D1A2E; --surface:#211E33; --surface-2:#282442;
        --border:#3C3658; --text:#F8F5EC; --text-muted:#CFC8E8;
        --primary:#8A7FFF; --primary-hover:#A79CFF; --primary-text:#14121F;
        --accent:#F0B65C; --accent-soft:rgba(240,182,92,0.16);
        --success:#6FCB94; --success-soft:rgba(111,203,148,0.14);
        --danger:#E86B6B; --danger-soft:rgba(232,107,107,0.14);
        --user-bubble:#362F78; --user-bubble-text:#F1EDE3;
        --ai-bubble:#1D1A2E; --shadow:0 8px 28px rgba(0,0,0,0.45);
        --glow: 0 0 0 1px rgba(240,182,92,0.25), 0 10px 30px rgba(240,182,92,0.12);
        """
    return """
    --bg:#FAF7F0; --bg-elevated:#FFFFFF; --surface:#F1ECE0; --surface-2:#EBE4D2;
    --border:#E4DCC8; --text:#241F3D; --text-muted:#6B6478;
    --primary:#362F78; --primary-hover:#4A4099; --primary-text:#FFFFFF;
    --accent:#C97F17; --accent-soft:rgba(201,127,23,0.12);
    --success:#2F8A57; --success-soft:rgba(47,138,87,0.10);
    --danger:#B3372F; --danger-soft:rgba(179,55,47,0.10);
    --user-bubble:#362F78; --user-bubble-text:#FFFFFF;
    --ai-bubble:#FFFFFF; --shadow:0 8px 24px rgba(36,31,61,0.08);
    --glow: 0 0 0 1px rgba(201,127,23,0.20), 0 10px 26px rgba(201,127,23,0.10);
    """


def load_css(theme: str = "light") -> None:
    """Inject fonts, CSS variables, and component styles for the given theme."""

    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600;9..144,700&family=Public+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

        :root {{ {_theme_vars(theme)} }}

        html, body, [class*="css"] {{
            font-family: 'Public Sans', sans-serif;
            color: var(--text);
            transition: background-color 0.25s ease, color 0.25s ease;
        }}
        p, span, div, li, label, h1, h2, h3, h4, h5, h6 {{
            color: var(--text);
        }}
        .stMarkdown, .stTextInput, .stTextArea, .stSelectbox, .stMultiSelect, .stNumberInput, .stDateInput {{
            color: var(--text) !important;
        }}
        .st-emotion-cache-1wmy9hl, .st-emotion-cache-1v0mbdj, .st-emotion-cache-13k62yr {{
            color: var(--text) !important;
        }}

        .stApp {{
            background: var(--bg);
            transition: background 0.25s ease;
        }}

        .theme-picker-card {{
            background: var(--surface); border: 1px solid var(--border); border-radius: 14px;
            padding: 10px; margin-bottom: 10px; box-shadow: inset 0 1px 0 rgba(255,255,255,0.04);
        }}
        .theme-picker-card .theme-label {{
            font-size: 11px; text-transform: uppercase; letter-spacing: 0.08em; color: var(--text-muted);
            margin-bottom: 8px; font-weight: 600;
        }}
        .theme-preview {{
            display: flex; gap: 8px; align-items: center; margin-top: 8px; font-size: 12px; color: var(--text-muted);
        }}
        .theme-preview .dot {{
            width: 8px; height: 8px; border-radius: 50%; background: var(--accent); display: inline-block;
        }}

        /* ---------- animated ambient background (respects reduced motion) ---------- */
        .ambient-bg {{
            position: fixed; inset: 0; z-index: -1; overflow: hidden; pointer-events: none;
            background:
                radial-gradient(circle at 15% 20%, rgba(255,255,255,0.18), transparent 24%),
                radial-gradient(circle at 85% 15%, rgba(255,255,255,0.10), transparent 22%),
                radial-gradient(circle at 70% 80%, rgba(255,255,255,0.12), transparent 26%),
                linear-gradient(135deg, rgba(255,255,255,0.06), transparent 40%);
            transform: perspective(1400px) rotateX(2deg);
        }}
        .ambient-bg::before, .ambient-bg::after {{
            content: ""; position: absolute; inset: 0; pointer-events: none;
        }}
        .ambient-bg::before {{
            background: linear-gradient(120deg, transparent 0%, rgba(255,255,255,0.08) 35%, transparent 70%);
            transform: translateX(-20%) skewX(-12deg);
            animation: sweep 18s linear infinite;
        }}
        .ambient-bg::after {{
            background:
                radial-gradient(circle at 65% 20%, var(--accent-soft) 0%, transparent 34%),
                radial-gradient(circle at 20% 80%, var(--primary) 0%, transparent 30%),
                radial-gradient(circle at 50% 50%, rgba(255,255,255,0.08), transparent 48%);
            filter: blur(18px);
            opacity: 0.9;
            transform: translateZ(0);
        }}
        .ambient-bg span {{
            position: absolute; border-radius: 50%; filter: blur(78px); opacity: 0.34;
            animation: drift 24s ease-in-out infinite;
            transform-style: preserve-3d;
        }}
        .ambient-bg span:nth-child(1) {{
            width: 480px; height: 480px; top: -150px; left: -130px;
            background: var(--primary); animation-delay: 0s;
        }}
        .ambient-bg span:nth-child(2) {{
            width: 420px; height: 420px; bottom: -160px; right: -110px;
            background: var(--accent); animation-delay: -8s;
        }}
        .ambient-bg span:nth-child(3) {{
            width: 320px; height: 320px; top: 38%; left: 58%;
            background: var(--success); opacity: 0.16; animation-delay: -14s;
        }}
        .ambient-bg span:nth-child(4) {{
            width: 260px; height: 260px; top: 20%; left: 38%;
            background: var(--surface-2); opacity: 0.18; animation-delay: -4s;
            box-shadow: inset 0 0 60px rgba(255,255,255,0.08);
        }}
        @keyframes drift {{
            0%, 100% {{ transform: translate(0,0) scale(1); }}
            50% {{ transform: translate(40px,-30px) scale(1.08); }}
        }}
        @keyframes sweep {{
            0% {{ transform: translateX(-20%); }}
            100% {{ transform: translateX(120%); }}
        }}
        @media (prefers-reduced-motion: reduce) {{
            .ambient-bg span {{ animation: none; }}
        }}

        /* ---------- typography ---------- */
        .brand-title {{
            font-family: 'Fraunces', serif; font-weight: 700; font-size: 40px;
            color: var(--text); margin: 0; line-height: 1.1;
            animation: fadeSlideIn 0.6s ease both;
        }}
        .brand-subtitle {{
            font-family: 'Public Sans', sans-serif; font-size: 16px; color: var(--text-muted);
            margin-top: 4px; margin-bottom: 18px; animation: fadeSlideIn 0.6s ease 0.1s both;
            font-weight: 500;
        }}
        .eyebrow {{
            font-family: 'JetBrains Mono', monospace; font-size: 11px; letter-spacing: 0.08em;
            text-transform: uppercase; color: var(--accent); font-weight: 500;
        }}

        @keyframes fadeSlideIn {{
            from {{ opacity: 0; transform: translateY(8px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        @keyframes floatIn {{
            from {{ opacity: 0; transform: translateY(10px) scale(0.98); }}
            to {{ opacity: 1; transform: translateY(0) scale(1); }}
        }}
        @keyframes fadeIn {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
        @keyframes popIn {{
            from {{ opacity: 0; transform: scale(0.94); }}
            to {{ opacity: 1; transform: scale(1); }}
        }}

        /* ---------- glass panel ---------- */
        .glass-panel {{
            background: var(--bg-elevated); border: 1px solid var(--border);
            border-radius: 16px; padding: 22px 24px; box-shadow: var(--shadow);
            backdrop-filter: blur(6px);
        }}

        .page-hero {{
            background: linear-gradient(135deg, var(--surface) 0%, var(--bg-elevated) 100%);
            border: 1px solid var(--border); border-radius: 20px; padding: 22px 24px;
            margin-bottom: 18px; box-shadow: var(--shadow); position: relative; overflow: hidden;
            animation: floatIn 0.55s ease both;
        }}
        .page-hero::after {{
            content: ""; position: absolute; inset: auto -30px -40px auto; width: 180px; height: 180px;
            background: radial-gradient(circle, var(--accent-soft) 0%, transparent 70%);
            pointer-events: none;
        }}
        .section-heading {{
            display: flex; justify-content: space-between; align-items: center; gap: 12px;
            margin: 8px 0 12px;
        }}
        .section-title {{
            font-size: 18px; font-weight: 700; color: var(--text); margin: 0;
        }}
        .section-caption {{
            font-size: 13px; color: var(--text-muted); margin-top: 4px;
        }}
        .pill-row {{ display: flex; flex-wrap: wrap; gap: 8px; margin-top: 10px; }}
        .pill-row .score-pill {{ background: var(--bg-elevated); }}
        .info-callout {{
            border: 1px solid var(--border); border-left: 3px solid var(--accent);
            background: var(--accent-soft); padding: 12px 14px; border-radius: 12px;
            color: var(--text); margin: 8px 0 14px;
        }}
        .mini-card {{
            background: var(--bg-elevated); border: 1px solid var(--border); border-radius: 14px;
            padding: 14px 16px; box-shadow: var(--shadow); margin-bottom: 12px;
        }}
        .mini-card .mini-title {{ font-weight: 700; color: var(--text); margin-bottom: 6px; }}
        .mini-card .mini-sub {{ font-size: 13px; color: var(--text-muted); line-height: 1.5; }}

        /* ---------- metric / dashboard cards ---------- */
        .metric-card {{
            background: var(--bg-elevated); border: 1px solid var(--border);
            border-radius: 14px; padding: 18px 20px; box-shadow: var(--shadow);
            transition: transform 0.18s ease, box-shadow 0.18s ease;
            animation: popIn 0.35s ease both;
        }}
        .metric-card:hover {{
            transform: translateY(-3px) scale(1.01); box-shadow: var(--glow);
        }}
        .metric-icon {{ font-size: 22px; margin-bottom: 6px; }}
        .metric-value {{
            font-family: 'Fraunces', serif; font-weight: 700; font-size: 28px; color: var(--text);
        }}
        .metric-label {{
            font-size: 12px; color: var(--text-muted); text-transform: uppercase;
            letter-spacing: 0.05em; margin-top: 2px;
        }}

        /* ---------- chat bubbles ---------- */
        div[data-testid="stChatMessage"] {{
            animation: fadeSlideIn 0.3s ease both; margin: 10px 0 16px; padding: 0;
        }}
        div[data-testid="stChatMessageContent"] {{
            background: var(--bg-elevated); border: 1px solid var(--border); border-radius: 16px;
            padding: 12px 14px; box-shadow: var(--shadow);
            color: var(--text);
        }}
        div[data-testid="stChatMessageContent"] p {{ margin-bottom: 0.45rem; }}
        .msg-meta {{
            font-family: 'JetBrains Mono', monospace; font-size: 11px; color: var(--text-muted);
            margin-top: 6px;
        }}

        /* ---------- citation / source cards (signature element) ---------- */
        .source-card {{
            background: var(--bg-elevated); border: 1px solid var(--border);
            border-left: 3px dashed var(--accent); border-radius: 4px 12px 12px 4px;
            padding: 14px 16px; margin-bottom: 10px;
            box-shadow: var(--shadow); transition: box-shadow 0.18s ease, transform 0.18s ease;
            animation: fadeSlideIn 0.35s ease both;
        }}
        .source-card:hover {{ box-shadow: var(--glow); transform: translateX(2px) scale(1.01); }}
        .source-badge {{
            display: inline-flex; align-items: center; justify-content: center;
            width: 22px; height: 22px; border-radius: 50%; background: var(--accent-soft);
            color: var(--accent); font-family: 'JetBrains Mono', monospace; font-size: 11px;
            font-weight: 600; margin-right: 8px;
        }}
        .source-name {{ font-weight: 600; font-size: 14px; color: var(--text); }}
        .source-meta {{
            font-family: 'JetBrains Mono', monospace; font-size: 11px; color: var(--text-muted);
            margin: 4px 0 8px 30px;
        }}
        .source-preview {{
            font-size: 13px; color: var(--text); margin-left: 30px; line-height: 1.5;
        }}

        /* ---------- pills / badges ---------- */
        .score-pill {{
            display: inline-block; padding: 3px 10px; border-radius: 999px;
            background: var(--surface); border: 1px solid var(--border);
            font-size: 11px; color: var(--text-muted); font-family: 'JetBrains Mono', monospace;
        }}
        .status-pill {{
            display: inline-flex; align-items: center; gap: 6px; padding: 4px 10px;
            border-radius: 999px; font-size: 12px; font-weight: 600;
        }}
        .status-pill.ok {{ background: var(--success-soft); color: var(--success); }}
        .status-pill.dot {{
            width: 7px; height: 7px; border-radius: 50%; background: currentColor;
            display: inline-block;
        }}

        /* ---------- upload dropzone ---------- */
        section[data-testid="stFileUploaderDropzone"] {{
            border: 1.5px dashed var(--border) !important; border-radius: 14px !important;
            background: var(--surface) !important; transition: border-color 0.15s ease;
        }}
        section[data-testid="stFileUploaderDropzone"]:hover {{
            border-color: var(--accent) !important;
        }}

        /* ---------- buttons ---------- */
        .stButton > button, .stDownloadButton > button {{
            border-radius: 999px !important; transition: transform 0.16s ease, box-shadow 0.16s ease;
            padding: 0.45rem 0.8rem !important;
        }}
        .stButton > button:hover, .stDownloadButton > button:hover {{ transform: translateY(-1px); box-shadow: var(--shadow); }}
        .stButton > button[kind="primary"] {{
            background: var(--primary) !important; border-color: var(--primary) !important; color: var(--primary-text) !important;
        }}
        .stTextInput > div > div > input, .stTextArea > div > div > textarea {{
            border-radius: 12px !important; border: 1px solid var(--border) !important;
            background: var(--bg-elevated) !important; color: var(--text) !important;
            box-shadow: inset 0 1px 2px rgba(0,0,0,0.03);
            font-weight: 500;
        }}
        .stRadio > label {{ font-size: 13px; color: var(--text-muted); }}
        .stRadio > div {{ gap: 8px; }}
        .stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus {{
            border-color: var(--primary) !important; box-shadow: 0 0 0 2px rgba(54,47,120,0.16) !important;
            transform: translateY(-1px);
        }}
        .stTabs [data-testid="stBaseButton-secondary"] {{
            border-radius: 999px !important; border: 1px solid var(--border) !important; padding: 0.25rem 0.7rem !important;
        }}
        .stExpander {{
            border: 1px solid var(--border) !important; border-radius: 14px !important; background: var(--bg-elevated) !important;
            box-shadow: var(--shadow);
        }}
        .stAlert {{ border-radius: 12px !important; border: 1px solid var(--border) !important; }}
        .stChatInput {{
            border: 1px solid var(--border) !important; border-radius: 16px !important; padding: 6px 8px !important;
            background: var(--bg-elevated) !important; box-shadow: var(--shadow);
        }}

        /* ---------- skeleton loader ---------- */
        .skeleton {{
            border-radius: 10px; background: linear-gradient(90deg, var(--surface) 25%, var(--surface-2) 37%, var(--surface) 63%);
            background-size: 400% 100%; animation: shimmer 1.4s ease infinite; height: 16px; margin-bottom: 8px;
        }}
        @keyframes shimmer {{
            0% {{ background-position: 100% 50%; }}
            100% {{ background-position: 0 50%; }}
        }}

        /* ---------- footer ---------- */
        .app-footer {{
            text-align: center; color: var(--text-muted); font-size: 12px;
            padding: 24px 0 8px 0; border-top: 1px solid var(--border); margin-top: 32px;
        }}
        .app-footer a {{ color: var(--accent); text-decoration: none; }}

        /* ---------- misc ---------- */
        .block-container {{ max-width: 1100px; padding-top: 1.25rem; padding-bottom: 2rem; }}
        [data-testid="stSidebar"] {{ border-right: 1px solid var(--border); background: linear-gradient(180deg, var(--bg-elevated), var(--bg)); }}
        [data-testid="stSidebarContent"] {{ padding-top: 6px; }}
        [data-testid="stSidebarUserContent"] {{ gap: 8px; }}
        </style>

        <div class="ambient-bg"><span></span><span></span><span></span></div>
        """,
        unsafe_allow_html=True,
    )

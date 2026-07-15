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
        --border:#332E4E; --text:#F1EDE3; --text-muted:#9C96B5;
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
        }}

        .stApp {{
            background: var(--bg);
        }}

        /* ---------- animated ambient background (respects reduced motion) ---------- */
        .ambient-bg {{
            position: fixed; inset: 0; z-index: -1; overflow: hidden; pointer-events: none;
        }}
        .ambient-bg span {{
            position: absolute; border-radius: 50%; filter: blur(60px); opacity: 0.35;
            animation: drift 26s ease-in-out infinite;
        }}
        .ambient-bg span:nth-child(1) {{
            width: 420px; height: 420px; top: -120px; left: -100px;
            background: var(--primary); animation-delay: 0s;
        }}
        .ambient-bg span:nth-child(2) {{
            width: 360px; height: 360px; bottom: -140px; right: -80px;
            background: var(--accent); animation-delay: -8s;
        }}
        .ambient-bg span:nth-child(3) {{
            width: 300px; height: 300px; top: 40%; left: 60%;
            background: var(--success); opacity: 0.15; animation-delay: -14s;
        }}
        @keyframes drift {{
            0%, 100% {{ transform: translate(0,0) scale(1); }}
            50% {{ transform: translate(40px,-30px) scale(1.08); }}
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
        }}
        .eyebrow {{
            font-family: 'JetBrains Mono', monospace; font-size: 11px; letter-spacing: 0.08em;
            text-transform: uppercase; color: var(--accent); font-weight: 500;
        }}

        @keyframes fadeSlideIn {{
            from {{ opacity: 0; transform: translateY(8px); }}
            to {{ opacity: 1; transform: translateY(0); }}
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

        /* ---------- metric / dashboard cards ---------- */
        .metric-card {{
            background: var(--bg-elevated); border: 1px solid var(--border);
            border-radius: 14px; padding: 18px 20px; box-shadow: var(--shadow);
            transition: transform 0.18s ease, box-shadow 0.18s ease;
            animation: popIn 0.35s ease both;
        }}
        .metric-card:hover {{
            transform: translateY(-3px); box-shadow: var(--glow);
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
            animation: fadeSlideIn 0.3s ease both;
        }}
        .msg-meta {{
            font-family: 'JetBrains Mono', monospace; font-size: 11px; color: var(--text-muted);
            margin-top: 4px;
        }}

        /* ---------- citation / source cards (signature element) ---------- */
        .source-card {{
            background: var(--bg-elevated); border: 1px solid var(--border);
            border-left: 3px dashed var(--accent); border-radius: 4px 12px 12px 4px;
            padding: 14px 16px; margin-bottom: 10px;
            box-shadow: var(--shadow); transition: box-shadow 0.18s ease, transform 0.18s ease;
            animation: fadeSlideIn 0.35s ease both;
        }}
        .source-card:hover {{ box-shadow: var(--glow); transform: translateX(2px); }}
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
            font-size: 13px; color: var(--text-muted); margin-left: 30px; line-height: 1.5;
        }}

        /* ---------- pills / badges ---------- */
        .score-pill {{
            display: inline-block; padding: 3px 10px; border-radius: 999px;
            background: var(--surface); border: 1px solid var(--border);
            font-size: 11px; color: var(--text-muted); font-family: 'JetBrains Mono', monospace;
        }}
        .status-pill {{
            display: inline-flex; align-items: center; gap: 6px; padding: 4px 10px;
            border-radius: 999px; font-size: 12px; font-weight: 500;
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
        .stButton > button {{
            border-radius: 10px !important; transition: transform 0.12s ease, box-shadow 0.12s ease;
        }}
        .stButton > button:hover {{ transform: translateY(-1px); box-shadow: var(--shadow); }}
        .stButton > button[kind="primary"] {{
            background: var(--primary) !important; border-color: var(--primary) !important;
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
        .block-container {{ max-width: 900px; }}
        [data-testid="stSidebar"] {{ border-right: 1px solid var(--border); }}
        </style>

        <div class="ambient-bg"><span></span><span></span><span></span></div>
        """,
        unsafe_allow_html=True,
    )

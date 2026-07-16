"""Dashboard: knowledge-base metrics and system status at a glance."""

import streamlit as st

from utils import kb_manager, stats_tracker
from utils.constants import APP_NAME, EMBEDDING_MODEL, GENERATION_MODEL, VECTOR_DB

st.markdown('<p class="brand-title">📊 Dashboard</p>', unsafe_allow_html=True)
st.markdown(
    f'<p class="brand-subtitle">System overview for {APP_NAME}</p>',
    unsafe_allow_html=True,
)

try:
    kb_stats = kb_manager.get_kb_stats()
    kb_ready = True
except Exception:
    kb_stats = {"total_documents": 0, "total_chunks": 0, "total_embeddings": 0}
    kb_ready = False

usage = stats_tracker.get_summary()
last_updated = usage["last_updated"] or "Never"
avg_response = f"{usage['avg_response_time_sec']:.2f}s" if usage["query_count"] else "n/a"


def metric_card(col, icon: str, label: str, value: str) -> None:
    with col:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-icon">{icon}</div>
                <div class="metric-value">{value}</div>
                <div class="metric-label">{label}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


row1 = st.columns(4)
metric_card(row1[0], "📄", "Documents", str(kb_stats["total_documents"]))
metric_card(row1[1], "🧩", "Chunks", str(kb_stats["total_chunks"]))
metric_card(row1[2], "🧬", "Embeddings", str(kb_stats["total_embeddings"]))
metric_card(row1[3], "🗄️", "Vector DB", "Online" if kb_ready else "Empty")

st.write("")
row2 = st.columns(4)
metric_card(row2[0], "🤖", "AI model", GENERATION_MODEL)
metric_card(row2[1], "🕒", "Last updated", last_updated.split("T")[0] if "T" in last_updated else last_updated)
metric_card(row2[2], "💬", "Queries answered", str(usage["query_count"]))
metric_card(row2[3], "⚡", "Avg. response time", avg_response)

st.write("")
st.markdown("#### System details")
c1, c2 = st.columns(2)
with c1:
    st.markdown(
        f"""
        <div class="glass-panel">
        <div class="eyebrow">Pipeline</div>
        <p style="margin:8px 0 4px 0;"><b>Embedding model</b><br>{EMBEDDING_MODEL}</p>
        <p style="margin:8px 0 4px 0;"><b>Generation model</b><br>{GENERATION_MODEL}</p>
        <p style="margin:8px 0 4px 0;"><b>Vector store</b><br>{VECTOR_DB}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with c2:
    status_label = "Healthy · ready to answer questions" if kb_ready and kb_stats["total_documents"] > 0 else "No documents indexed yet"
    st.markdown(
        f"""
        <div class="glass-panel">
        <div class="eyebrow">Health</div>
        <p style="margin:10px 0;">
            <span class="status-pill ok"><span class="dot"></span>{status_label}</span>
        </p>
        <p style="color:var(--text-muted);font-size:13px;">
            Upload PDFs from the Documents page to grow the knowledge base.
        </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

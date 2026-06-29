import logging

import streamlit as st
from llama_index.core import Settings

from engine import get_index

APP_TITLE = "Internal IT Support"
APP_SUBTITLE = "Policy-aware help for workplace IT questions"
QUICK_ACTIONS = [
    "How do I reset my password?",
    "How do I request VPN access?",
    "What is the reimbursement process?",
]
SYSTEM_PROMPT = (
    "You are a professional enterprise IT support assistant. "
    "Your tone is helpful, concise, and security-conscious. "
    "Only answer questions related to company IT policies and procedures. "
    "If asked about unrelated topics, provide a polite, professional refusal."
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("it_support_bot")

st.set_page_config(
    page_title=f"{APP_TITLE} | Corporate",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.session_state.setdefault("messages", [])
st.session_state.setdefault("pending_prompt", None)


@st.cache_resource(show_spinner=False)
def initialize_engine():
    index = get_index()
    return index.as_chat_engine(
        chat_mode="context",
        llm=Settings.llm,
        system_prompt=SYSTEM_PROMPT,
    )


engine_error = None
try:
    chat_engine = initialize_engine()
except Exception as exc:
    chat_engine = None
    engine_error = str(exc)
    logger.exception("Failed to initialize chat engine")


def format_sources(source_nodes):
    sources = []
    for node in source_nodes or []:
        metadata = getattr(node, "metadata", {}) or {}
        file_name = (
            metadata.get("file_name")
            or metadata.get("filename")
            or metadata.get("source")
            or "General Policy"
        )
        if file_name not in sources:
            sources.append(file_name)
    if not sources:
        return ""
    return "\n\n---\n**Reference documents:** " + ", ".join(sorted(sources))


st.markdown(
    """
    <style>
        .stApp {
            background:
                radial-gradient(circle at top left, rgba(14, 165, 233, 0.14), transparent 26%),
                radial-gradient(circle at top right, rgba(37, 99, 235, 0.10), transparent 22%),
                linear-gradient(180deg, #f8fafc 0%, #e2e8f0 100%);
        }

        .block-container {
            padding-top: 1.6rem;
            padding-bottom: 1.8rem;
            max-width: 1240px;
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0f172a 0%, #111827 100%);
            color: #e5e7eb;
            border-right: 1px solid rgba(255, 255, 255, 0.08);
        }

        [data-testid="stSidebar"] * {
            color: #e5e7eb;
        }

        .hero {
            background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 55%, #2563eb 100%);
            color: white;
            border-radius: 24px;
            padding: 1.5rem 1.6rem;
            box-shadow: 0 24px 60px rgba(15, 23, 42, 0.20);
            border: 1px solid rgba(255, 255, 255, 0.08);
            margin-bottom: 1rem;
        }

        .hero h1 {
            margin: 0;
            font-size: 2rem;
            line-height: 1.1;
        }

        .hero p {
            margin: 0.45rem 0 0 0;
            color: rgba(255, 255, 255, 0.82);
            font-size: 0.98rem;
        }

        .pill-row {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin-top: 0.9rem;
        }

        .pill {
            display: inline-block;
            padding: 0.38rem 0.7rem;
            border-radius: 999px;
            background: rgba(255, 255, 255, 0.14);
            border: 1px solid rgba(255, 255, 255, 0.14);
            color: rgba(255, 255, 255, 0.92);
            font-size: 0.82rem;
        }

        .section-card {
            background: rgba(255, 255, 255, 0.76);
            border: 1px solid rgba(148, 163, 184, 0.24);
            border-radius: 20px;
            padding: 1rem 1.05rem;
            box-shadow: 0 16px 40px rgba(15, 23, 42, 0.06);
            backdrop-filter: blur(10px);
        }

        .section-card h3 {
            margin: 0 0 0.35rem 0;
            font-size: 1rem;
            color: #0f172a !important;
        }

        .section-card p {
            margin: 0;
            color: #475569;
            font-size: 0.92rem;
            line-height: 1.5;
        }

        div[data-testid="stChatMessage"] {
            border-radius: 18px;
            border: 1px solid rgba(148, 163, 184, 0.18);
            background: rgba(255, 255, 255, 0.93);
            box-shadow: 0 10px 30px rgba(15, 23, 42, 0.06);
            padding: 0.1rem 0.2rem;
        }

        div[data-testid="stChatMessage"] *,
        div[data-testid="stChatMessage"] p,
        div[data-testid="stChatMessage"] span,
        div[data-testid="stChatMessage"] li,
        div[data-testid="stChatMessage"] code,
        div[data-testid="stChatMessage"] strong {
            color: #0f172a !important;
        }

        div[data-testid="stChatMessage"] p {
            line-height: 1.65;
        }

        [data-testid="stChatInput"] {
            border-radius: 18px;
        }

        .sidebar-title {
            font-size: 1.2rem;
            font-weight: 700;
            margin-bottom: 0.25rem;
            color: #e5e7eb;
        }

        .sidebar-card {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            padding: 0.9rem;
            margin-bottom: 0.8rem;
        }

        .sidebar-card strong {
            color: #f8fafc !important;
        }

        .sidebar-card div {
            color: rgba(226, 232, 240, 0.86) !important;
        }

        .quick-actions-title {
            margin: 0.2rem 0 0.6rem 0;
            font-size: 0.92rem;
            font-weight: 700;
            color: #334155;
            letter-spacing: 0.02em;
        }

        div[data-testid="stButton"] > button {
            border-radius: 14px;
            border: 1px solid rgba(148, 163, 184, 0.28);
            background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
            color: #0f172a;
            font-weight: 600;
            min-height: 3.1rem;
            padding: 0.65rem 0.9rem;
            box-shadow: 0 6px 16px rgba(15, 23, 42, 0.05);
        }

        div[data-testid="stButton"] > button:hover {
            border-color: rgba(37, 99, 235, 0.40);
            box-shadow: 0 10px 22px rgba(37, 99, 235, 0.08);
            transform: translateY(-1px);
        }

        [data-testid="stSidebar"] div[data-testid="stButton"] > button {
            width: 100%;
            background: linear-gradient(180deg, rgba(30, 41, 59, 0.95) 0%, rgba(15, 23, 42, 0.98) 100%);
            color: #f8fafc !important;
            border: 1px solid rgba(148, 163, 184, 0.24);
            box-shadow: 0 8px 18px rgba(0, 0, 0, 0.18);
        }

        [data-testid="stSidebar"] div[data-testid="stButton"] > button:hover {
            border-color: rgba(96, 165, 250, 0.45);
            box-shadow: 0 10px 22px rgba(0, 0, 0, 0.24);
        }
    </style>
    """,
    unsafe_allow_html=True,
)


with st.sidebar:
    st.markdown('<div class="sidebar-title">IT Operations Portal</div>', unsafe_allow_html=True)
    st.caption("A secure, policy-aware helper for common workplace IT questions.")

    if chat_engine is None:
        st.error("The support engine is not ready.")
        if engine_error:
            st.caption(engine_error)
    else:
        st.success("Knowledge base loaded.")

    st.markdown(
        """
        <div class="sidebar-card">
            <strong>What this assistant covers</strong>
            <div style="margin-top:0.45rem; color: rgba(226,232,240,0.86); font-size: 0.92rem; line-height: 1.55;">
                VPN access, device support, account requests, internal policy lookups, and general IT procedures.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="sidebar-card">
            <strong>Example questions</strong>
            <div style="margin-top:0.45rem; color: rgba(226,232,240,0.86); font-size: 0.92rem; line-height: 1.6;">
                - How do I reset my password?<br>
                - What is the VPN request process?<br>
                - Where can I find the leave policy?
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("Reset conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.pending_prompt = None
        st.rerun()


st.markdown(
    f"""
    <div class="hero">
        <h1>{APP_TITLE}</h1>
        <p>{APP_SUBTITLE}</p>
        <div class="pill-row">
            <span class="pill">Policy aware</span>
            <span class="pill">Document grounded</span>
            <span class="pill">Fast streaming answers</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

left, right = st.columns([2.2, 1], gap="large")

with left:
    st.markdown(
        """
        <div class="section-card">
            <h3>Ask a question</h3>
            <p>
                This assistant searches your internal knowledge base and answers using company IT policy documents.
                Keep questions focused on workplace IT support, access, and procedures.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not st.session_state.messages:
        with st.chat_message("assistant"):
            st.markdown(
                "I can help with company IT policies, VPN access, hardware issues, and security procedures. "
                "Ask a question to get started."
            )

        st.markdown('<div style="height:0.4rem;"></div>', unsafe_allow_html=True)
        st.markdown('<div class="quick-actions-title">Quick actions</div>', unsafe_allow_html=True)
        quick_top_left, quick_top_right = st.columns(2)
        with quick_top_left:
            if st.button(QUICK_ACTIONS[0], key="quick_action_0", use_container_width=True):
                st.session_state.pending_prompt = QUICK_ACTIONS[0]
                st.rerun()
        with quick_top_right:
            if st.button(QUICK_ACTIONS[1], key="quick_action_1", use_container_width=True):
                st.session_state.pending_prompt = QUICK_ACTIONS[1]
                st.rerun()
        if st.button(QUICK_ACTIONS[2], key="quick_action_2", use_container_width=True):
            st.session_state.pending_prompt = QUICK_ACTIONS[2]
            st.rerun()

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

with right:
    st.markdown(
        """
        <div class="section-card">
            <h3>How it works</h3>
            <p>
                1. Your question is matched against internal documents.<br>
                2. The assistant generates a response from relevant policy text.<br>
                3. Source documents are shown at the end of each answer.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div style="height: 0.8rem;"></div>
        <div class="section-card">
            <h3>Support guidance</h3>
            <p>
                For urgent access issues or security incidents, follow your internal escalation process instead of
                relying only on chat.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

prompt = st.chat_input(
    "Enter your request here...",
    disabled=chat_engine is None,
)
prompt = prompt or st.session_state.pending_prompt
st.session_state.pending_prompt = None

if prompt:
    if chat_engine is None:
        st.error("Support engine is currently unavailable. Please contact the IT team.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    with left:
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

            try:
                streaming_response = chat_engine.stream_chat(prompt)
                for token in streaming_response.response_gen:
                    full_response += token
                    message_placeholder.markdown(full_response + "|")

                full_response += format_sources(streaming_response.source_nodes)
                message_placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception:
                logger.exception("Inference error")
                st.error("I encountered an error retrieving that information. Please try rephrasing.")
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": "I encountered an error retrieving that information. Please try rephrasing.",
                    }
                )

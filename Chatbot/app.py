"""
app.py - Othello RAG Chatbot

Run with: streamlit run app.py
"""

# === SUPPRESS WARNINGS ===
import os
os.environ["ANONYMIZED_TELEMETRY"] = "False"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

import warnings
warnings.filterwarnings("ignore")

# === IMPORTS ===
import streamlit as st
import json
import httpx
from chroma_manager import search_documents, get_collection_stats

# =============================================================================
# CONFIGURATION
# =============================================================================

st.set_page_config(page_title="Othello RAG", page_icon="🎭", layout="centered")

LM_STUDIO_URL = "http://localhost:1234/v1"

# Session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "selected_model" not in st.session_state:
    st.session_state.selected_model = None
if "enable_rewriting" not in st.session_state:
    st.session_state.enable_rewriting = True
if "temperature" not in st.session_state:
    st.session_state.temperature = 0.7
if "max_tokens" not in st.session_state:
    st.session_state.max_tokens = 800


# =============================================================================
# FUNCTIONS
# =============================================================================

def get_loaded_models() -> list:
    """Get models loaded in LM Studio."""
    try:
        with httpx.Client(timeout=5.0) as client:
            r = client.get(f"{LM_STUDIO_URL}/models")
            r.raise_for_status()
            return [m["id"] for m in r.json().get("data", [])]
    except:
        return []


def call_llm(messages: list) -> str:
    """Call LM Studio API."""
    models = get_loaded_models()
    if not models:
        return "❌ Aucun modèle chargé. Ouvre LM Studio et charge un modèle."
    
    model_id = st.session_state.selected_model or models[0]
    if model_id not in models:
        model_id = models[0]
    
    try:
        with httpx.Client(timeout=120.0) as client:
            r = client.post(
                f"{LM_STUDIO_URL}/chat/completions",
                json={
                    "model": model_id,
                    "messages": messages,
                    "temperature": st.session_state.temperature,
                    "max_tokens": int(st.session_state.max_tokens),
                    "stream": False
                }
            )
            if r.status_code != 200:
                return f"❌ Erreur {r.status_code}: {r.text[:200]}"
            return r.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"❌ Erreur: {e}"


def rewrite_query(query: str) -> list:
    """Generate query variants."""
    if not st.session_state.enable_rewriting:
        return [query]
    
    prompt = f"""Generate 2 short alternative formulations of: {query}
JSON only: {{"q1": "v1", "q2": "v2"}}"""

    try:
        result = call_llm([{"role": "user", "content": prompt}])
        if result.startswith("❌"):
            return [query]
        if "```" in result:
            result = [p for p in result.split("```") if "{" in p][0].replace("json", "").strip()
        data = json.loads(result)
        return [query, data.get("q1", query), data.get("q2", query)]
    except:
        return [query]


def search_chunks(queries: list) -> list:
    """Search ChromaDB."""
    all_results = {}
    for q in queries:
        results = search_documents(q, n_results=3)
        if results and results["documents"][0]:
            for i, doc in enumerate(results["documents"][0]):
                if doc not in all_results:
                    all_results[doc] = {
                        "text": doc,
                        "meta": results["metadatas"][0][i],
                        "dist": results["distances"][0][i]
                    }
    return sorted(all_results.values(), key=lambda x: x["dist"])[:5]


# =============================================================================
# SIDEBAR
# =============================================================================

with st.sidebar:
    st.header("⚙️ Config")
    
    # Model selector
    models = get_loaded_models()
    if models:
        if st.session_state.selected_model not in models:
            st.session_state.selected_model = models[0]
        
        st.session_state.selected_model = st.selectbox(
            "🤖 Model",
            models,
            index=models.index(st.session_state.selected_model),
            format_func=lambda x: x.split("/")[-1][:25]
        )
        st.success(f"✅ {len(models)} model(s)")
    else:
        st.error("❌ LM Studio not connected")
        st.caption("Launch LM Studio & load a model")
    
    st.divider()
    
    st.session_state.enable_rewriting = st.checkbox("🔄 Query Rewriting", st.session_state.enable_rewriting)
    st.session_state.temperature = st.slider("🌡️ Temp", 0.0, 2.0, st.session_state.temperature, 0.1)
    st.session_state.max_tokens = st.slider("📝 Tokens", 100, 1500, st.session_state.max_tokens, 100)
    
    st.divider()
    
    stats = get_collection_stats()
    if stats:
        st.success(f"📊 {stats['count']} chunks")
    else:
        st.error("❌ No DB")
    
    if st.button("🧹 Clear", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()


# =============================================================================
# MAIN
# =============================================================================

st.title("🎭 Othello RAG")

tab1, tab2, tab3 = st.tabs(["🏠 Home", "💬 Chat", "🤖 Model"])

# HOME
with tab1:
    st.markdown("*Ask questions about Shakespeare's Othello*")
    
    col1, col2 = st.columns(2)
    col1.metric("📊 DB", f"{stats['count']} chunks" if stats else "❌")
    col2.metric("🤖 LM Studio", f"{len(models)} model(s)" if models else "❌")
    
    if stats and models:
        st.success("✅ Ready! Go to **Chat**")
    else:
        st.warning("⚠️ Start LM Studio + load model + check DB")
    
    st.markdown("### 💡 Examples\n- *Who is Iago?*\n- *What is the handkerchief?*")

# CHAT
with tab2:
    if not stats:
        st.error("❌ Run `python create_db.py`")
        st.stop()
    if not models:
        st.error("❌ Start LM Studio & load a model")
        st.stop()
    
    for h in st.session_state.chat_history:
        with st.chat_message("user"): st.write(h["q"])
        with st.chat_message("assistant"): st.write(h["a"])
    
    if q := st.chat_input("Your question..."):
        with st.chat_message("user"): st.write(q)
        
        with st.spinner("🔍"):
            queries = rewrite_query(q)
            chunks = search_chunks(queries)
        
        if not chunks:
            st.error("No results")
        else:
            ctx = "\n---\n".join([f"[{c['meta'].get('scene','')}] {c['text'][:400]}" for c in chunks[:4]])
            
            with st.spinner("🧠"):
                answer = call_llm([{"role": "user", "content": f"Context:\n{ctx}\n\nQuestion: {q}\n\nAnswer:"}])
            
            with st.chat_message("assistant"): st.write(answer)
            
            with st.expander("📚 Sources"):
                for c in chunks:
                    st.caption(f"{c['meta'].get('scene','')}: {c['text'][:100]}...")
            
            st.session_state.chat_history.append({"q": q, "a": answer})

# MODEL
with tab3:
    st.subheader("LM Studio Status")
    
    if models:
        st.success(f"✅ Connected - {len(models)} model(s)")
        for m in models:
            st.code(m)
    else:
        st.error("❌ Not connected")
    
    if st.button("🔄 Refresh"):
        st.rerun()
    
    st.markdown("""
    ### 📖 Instructions
    1. Open **LM Studio**
    2. Load model(s)
    3. Start server: **Developer → Start Server**
    4. Refresh this page
    """)
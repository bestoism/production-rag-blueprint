import streamlit as st
import requests

# --- KONFIGURASI ---
# Ganti URL ini dengan URL Hugging Face Space kamu
# Contoh: https://bestoism-rag-insight-pipeline.hf.space
API_URL = "https://bestoism-rag-insight-pipeline.hf.space/api/v1"

st.set_page_config(page_title="RAG Insight Bot", page_icon="🤖")

st.title("🤖 RAG Insight Pipeline")
st.write("Chat with your PDF documents using Gemini 2.0 Flash & Qdrant.")

# --- SIDEBAR: SETTINGS ---
with st.sidebar:
    st.header("📂 Document Upload")
    uploaded_file = st.file_uploader("Upload PDF", type=["pdf", "txt"])
    
    if uploaded_file is not None:
        if st.button("Ingest Document", type="primary"): # type primary biar warna mencolok
            with st.spinner("Processing document..."):
                try:
                    files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
                    response = requests.post(f"{API_URL}/documents/ingest", files=files)
                    if response.status_code == 200:
                        st.success(f"✅ Success: {response.json()['message']}")
                    else:
                        st.error(f"❌ Error: {response.text}")
                except Exception as e:
                    st.error(f"Connection Error: {e}")

    st.divider() # Garis pemisah
    
    st.header("⚙️ Settings")
    
    # TOMBOL RESET DATABASE
    if st.button("🗑️ Clear Memory & Chat"):
        with st.spinner("Clearing database..."):
            try:
                # 1. Panggil API Reset di Backend
                requests.delete(f"{API_URL}/documents/reset")
                
                # 2. Hapus Chat History di Browser
                st.session_state.messages = []
                
                # 3. Rerun halaman biar bersih
                st.success("Memory cleared!")
                st.rerun()
            except Exception as e:
                st.error(f"Error resetting: {e}")

# --- CHAT INTERFACE ---

# 1. Simpan riwayat chat di memori browser (Session State)
if "messages" not in st.session_state:
    st.session_state.messages = []

# 2. Tampilkan chat history yang lama
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. Input User
if prompt := st.chat_input("Ask something about your document..."):
    # Tampilkan pesan user
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 4. Kirim ke Backend API
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                payload = {"question": prompt}
                response = requests.post(f"{API_URL}/rag/query", json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    answer = data["answer"]
                    sources = data.get("sources", [])
                    
                    # Tampilkan jawaban
                    st.markdown(answer)
                    
                    # Tampilkan sumber (kecil di bawah)
                    if sources:
                        st.caption(f"📚 Sources: {', '.join(sources)}")
                    
                    # Simpan ke history
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    st.error("❌ Failed to get answer from backend.")
            except Exception as e:
                st.error(f"Connection Error: {e}")
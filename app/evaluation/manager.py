import pandas as pd
import asyncio
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings

from app.core.config import settings
from app.rag.pipeline import query_rag, get_retriever
from app.monitoring.logger import logger # Kita pakai logger yang baru dibuat!

class EvalManager:
    def __init__(self):
        # Konfigurasi Juri (Gemini + Local Embeddings)
        self.judge_llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash", 
            google_api_key=settings.GOOGLE_API_KEY,
            temperature=0
        )
        # Pakai Local Embeddings biar GRATIS & UNLIMITED
        self.judge_embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        
        # Metrics yang mau dinilai
        self.metrics = [faithfulness, answer_relevancy]

    async def _generate_rag_responses(self, questions: list):
        """
        Internal function: Menjalankan RAG pipeline untuk menjawab soal.
        """
        logger.info(f"🚀 Starting RAG generation for {len(questions)} questions...")
        
        data = {
            "user_input": [],
            "response": [],
            "retrieved_contexts": []
        }

        retriever = get_retriever()

        for q in questions:
            # 1. Dapatkan Jawaban AI
            result = await query_rag(q)
            
            # 2. Dapatkan Konteks Dokumen Asli (untuk cek fakta)
            docs = retriever.invoke(q)
            context_texts = [d.page_content for d in docs]
            
            # 3. Simpan ke Dictionary
            data["user_input"].append(q)
            data["response"].append(result["answer"])
            data["retrieved_contexts"].append(context_texts)
            
            logger.debug(f"✅ Q: {q} | A: {result['answer'][:50]}...")

        return data

    def run_evaluation(self, questions: list):
        """
        Fungsi Utama: Menjalankan RAG + Ragas Evaluation
        """
        # 1. Generate Jawaban (Async loop handling)
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
        rag_data = loop.run_until_complete(self._generate_rag_responses(questions))
        
        # 2. Convert ke Dataset Ragas
        dataset = Dataset.from_dict(rag_data)

        logger.info("⚖️  Judge AI (Ragas) is evaluating responses...")
        
        # 3. Jalankan Penilaian
        results = evaluate(
            dataset=dataset,
            metrics=self.metrics,
            llm=self.judge_llm,
            embeddings=self.judge_embeddings
        )

        logger.info("📊 Evaluation Complete!")
        return results
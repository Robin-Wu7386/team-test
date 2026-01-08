# rag_retriever.py
import os

os.environ["HF_HOME"] = r"E:\PyCharm\Pythonpro\team-test\RAG\hf_cache"
os.environ["HF_HUB_CACHE"] = r"E:\PyCharm\Pythonpro\team-test\RAG\hf_cache\hub"
os.environ["TRANSFORMERS_CACHE"] = r"E:\PyCharm\Pythonpro\team-test\RAG\hf_cache\transformers"
os.environ["SENTENCE_TRANSFORMERS_HOME"] = r"E:\PyCharm\Pythonpro\team-test\RAG\hf_cache\sentence_transformers"

import numpy as np
import faiss
import pickle
from sentence_transformers import SentenceTransformer
from loguru import logger


class RAGRetriever:
    """RAG检索器 - 负责检索相关文献"""

    def __init__(self, base_dir=r"E:\PyCharm\Pythonpro\team-test\RAG"):
        # ====== 配置路径 ======
        self.BASE_DIR = os.path.join(os.path.dirname(__file__), "..")  # 指向tcm_backend目录
        self.INDEX_PATH = os.path.join(self.BASE_DIR, "faiss_index.index")
        self.META_PATH = os.path.join(self.BASE_DIR, "faiss_meta.pkl")

        self.TOP_K_SYMPTOMS = 5
        self.TOP_K_DOCS = 5

        # ====== 模型必须与建库一致！======
        self.MODEL_NAME = "BAAI/bge-m3"  # 与 build_faiss_db.py 保持完全一致

        logger.info(f"加载嵌入模型: {self.MODEL_NAME}")
        self.model = SentenceTransformer(self.MODEL_NAME)

        # ====== 加载 FAISS 索引和文档 ======
        if not os.path.exists(self.INDEX_PATH) or not os.path.exists(self.META_PATH):
            raise FileNotFoundError("FAISS 索引或元数据文件不存在，请先运行 build_faiss_db.py 建库！")

        self.index = faiss.read_index(self.INDEX_PATH)
        with open(self.META_PATH, "rb") as f:
            meta = pickle.load(f)
            self.documents = meta["documents"]

        logger.success(f"✅ FAISS 向量库加载成功，共 {self.index.ntotal} 条文档")

    def parse_symptoms_fuzzy(self, user_input, top_k=None):
        """模糊解析症状"""
        if top_k is None:
            top_k = self.TOP_K_SYMPTOMS

        q_emb = self.model.encode([user_input], normalize_embeddings=True).astype(np.float32)
        distances, indices = self.index.search(q_emb, top_k)
        matched_symptoms = []
        for i in indices[0]:
            doc = self.documents[i]
            if "白话】" in doc:
                symptom = doc.split("白话】")[-1].strip()
            elif "内容】" in doc:
                symptom = doc.split("内容】")[-1].strip()
            else:
                symptom = doc.strip()
            matched_symptoms.append(symptom)
        return matched_symptoms

    def retrieve_docs(self, symptoms, top_k=None):
        """检索相关文献"""
        if top_k is None:
            top_k = self.TOP_K_DOCS

        query_text = " ".join(symptoms)
        q_emb = self.model.encode([query_text], normalize_embeddings=True).astype(np.float32)
        distances, indices = self.index.search(q_emb, top_k)
        return [self.documents[i] for i in indices[0]]

    def retrieve_for_question(self, user_input, top_k_docs=5):
        """根据用户问题检索相关文献"""
        # 直接使用用户输入作为查询，不再先匹配症状
        query_text = user_input
        q_emb = self.model.encode([query_text], normalize_embeddings=True).astype(np.float32)
        distances, indices = self.index.search(q_emb, top_k_docs)
        top_docs = [self.documents[i] for i in indices[0]]

        # 返回简化结果
        return {
            "matched_symptoms": [user_input],  # 原样返回用户输入作为症状
            "top_docs": top_docs
        }
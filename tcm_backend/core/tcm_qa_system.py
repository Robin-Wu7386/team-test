# tcm_qa_system.py
import json
import re
from entity_extractor import EntityExtractor
from rag_retriever import RAGRetriever

class TCMQASystem:
    """中医智能问答系统 - 整合实体提取和RAG检索"""

    def __init__(self, show_prompt=True, llm_api_url=None, llm_api_key=None, use_volc=False):
        """
        初始化问答系统

        Args:
            show_prompt: 是否显示给模型的完整提示词（开关）
            llm_api_url: LLM API地址（用于同事的Ollama）
            llm_api_key: LLM API密钥（用于火山引擎）
            use_volc: True=使用火山引擎API, False=使用同事的Ollama API（默认）
        """
        # 初始化实体提取器
        self.entity_extractor = EntityExtractor()

        # 初始化RAG检索器
        self.rag_retriever = RAGRetriever()

        # 控制开关：是否显示给模型的完整提示词
        self.show_prompt = show_prompt

        # 初始化LLM客户端（如果有API地址）
        self.llm_client = None
        if llm_api_url and not use_volc:  # 有URL且不用火山引擎 → 用同事的
            from llm_client import OllamaClient
            self.llm_client = OllamaClient(api_url=llm_api_url)
        elif use_volc and llm_api_key:  # 明确要用火山引擎且有key → 用火山引擎
            from llm_client import VolcClient
            self.llm_client = VolcClient(api_key=llm_api_key)
        # 统计查询次数
        self.query_count = 0
        # 添加默认模式
        self.default_mode = "pure_llm"  # 保持现有行为

    def path_with_entities(self, user_question, top_k_docs=5):
        """路径1：用户问题包含实体"""
        print(f"\n执行路径1：问题包含实体")
        print("-" * 50)

        # 1. 从问题中提取实体
        # print("步骤1: 从用户问题中提取实体...")
        question_entities = self.entity_extractor.extract_entities_from_text(user_question)
        question_herbs = question_entities["herbs"]
        question_fangjis = question_entities["fangjis"]

        print(f"  从问题中提取到中药: {question_herbs}")
        print(f"  从问题中提取到方剂: {question_fangjis}")

        # 2. 查询问题实体的属性
        # print("步骤2: 查询问题实体的属性...")
        herb_details = self.entity_extractor.query_herb_details(question_herbs)
        fangji_details = self.entity_extractor.query_fangji_details(question_fangjis)

        # 3. RAG检索相关文献
        # print("步骤3: RAG检索相关文献...")
        rag_result = self.rag_retriever.retrieve_for_question(user_question, top_k_docs)
        matched_symptoms = rag_result["matched_symptoms"]
        top_docs = rag_result["top_docs"]

        print(f"  匹配到的症状: {matched_symptoms}")
        print(f"  检索到的文献数量: {len(top_docs)}")

        # 4. 从文献中提取额外实体
        # print("步骤4: 从文献中提取额外实体...")
        all_rag_entities = {"herbs": set(), "fangjis": set()}
        for doc in top_docs:
            doc_entities = self.entity_extractor.extract_entities_from_text(doc, max_entities=3)
            all_rag_entities["herbs"].update(doc_entities["herbs"])
            all_rag_entities["fangjis"].update(doc_entities["fangjis"])

        # 获取从症状映射表得到的实体（用于过滤）
        if hasattr(self.entity_extractor, 'symptom_entity_map') and self.entity_extractor.symptom_entity_map:
            # 提取用户问题中的症状
            symptoms_in_question = self.entity_extractor.extract_symptoms_from_text(user_question)

            if symptoms_in_question:
                # 从症状映射表获取相关实体
                symptom_related_entities = self.entity_extractor.get_entities_from_symptom_map(
                    symptoms_in_question, max_entities=100  # 获取足够多的实体用于过滤
                )
                symptom_herbs_set = set(symptom_related_entities["herbs"])
                symptom_fangjis_set = set(symptom_related_entities["fangjis"])

                # 只保留与症状相关的额外实体
                rag_herbs = []
                for herb in all_rag_entities["herbs"]:
                    if herb not in question_herbs:
                        if herb in symptom_herbs_set:
                            rag_herbs.append(herb)

                rag_fangjis = []
                for fangji in all_rag_entities["fangjis"]:
                    if fangji not in question_fangjis:
                        if fangji in symptom_fangjis_set:
                            rag_fangjis.append(fangji)

                # print(f"  从文献中提取到额外中药(已过滤): {rag_herbs}")
                # print(f"  从文献中提取到额外方剂(已过滤): {rag_fangjis}")
            else:
                # 如果没有找到症状，使用原来的逻辑
                rag_herbs = list(all_rag_entities["herbs"] - set(question_herbs))
                rag_fangjis = list(all_rag_entities["fangjis"] - set(question_fangjis))
                # print(f"  从文献中提取到额外中药: {rag_herbs}")
                # print(f"  从文献中提取到额外方剂: {rag_fangjis}")
        else:
            # 如果症状映射表不存在，使用原来的逻辑
            rag_herbs = list(all_rag_entities["herbs"] - set(question_herbs))
            rag_fangjis = list(all_rag_entities["fangjis"] - set(question_fangjis))
            # print(f"  从文献中提取到额外中药: {rag_herbs}")
            # print(f"  从文献中提取到额外方剂: {rag_fangjis}")

        # 5. 查询文献实体的属性
        # print("步骤5: 查询文献实体的属性...")
        rag_herb_details = self.entity_extractor.query_herb_details(rag_herbs)
        rag_fangji_details = self.entity_extractor.query_fangji_details(rag_fangjis)

        # 6. 合并所有实体信息
        all_herb_details = herb_details + rag_herb_details
        all_fangji_details = fangji_details + rag_fangji_details

        # 7. 格式化所有信息
        # print("步骤6: 格式化所有信息...")
        entity_info = self.entity_extractor.format_entity_details(all_herb_details, all_fangji_details)
        rag_info = self._format_rag_info(top_docs, matched_symptoms)

        # 8. 准备给LLM的信息
        llm_input = self._prepare_llm_input(
            user_question=user_question,
            entity_info=entity_info,
            rag_info=rag_info,
            path_type="包含实体",
            user_mentioned_entities=question_herbs + question_fangjis  # 添加用户提到的实体
        )

        return {
            "user_question": user_question,
            "entity_info": entity_info,
            "rag_info": rag_info,
            "path_type": "包含实体",
            "user_mentioned_entities": question_herbs + question_fangjis
        }

    def path_with_symptoms(self, user_question, top_k_docs=5):
        """路径2：用户问题只有症状 - 增强版：优先利用症状映射表兜底 + RAG补充"""
        print("-" * 50)

        # ==================== 新增：利用症状映射表获取核心实体（兜底） ====================
        # 1. 从用户问题中提取标准化症状
        symptoms_in_question = self.entity_extractor.extract_symptoms_from_text(user_question)

        # 2. 如果提取到症状，直接从症状实体映射表获取经典实体
        mapped_herbs = []
        mapped_fangjis = []
        if symptoms_in_question:
            mapped_entities = self.entity_extractor.get_entities_from_symptom_map(
                symptoms_in_question, max_entities=4  # 可以适当多取一些经典实体
            )
            mapped_herbs = mapped_entities["herbs"]
            mapped_fangjis = mapped_entities["fangjis"]
            # print(f"  从症状映射表获取核心中药: {mapped_herbs}")
            # print(f"  从症状映射表获取核心方剂: {mapped_fangjis}")

        # ==================== 原有逻辑：RAG检索相关文献 ====================
        rag_result = self.rag_retriever.retrieve_for_question(user_question, top_k_docs)
        matched_symptoms = rag_result["matched_symptoms"]
        top_docs = rag_result["top_docs"]

        # ==================== 原有逻辑：从文献中提取实体 ====================
        all_rag_entities = {"herbs": set(), "fangjis": set()}
        for doc in top_docs:
            doc_entities = self.entity_extractor.extract_entities_from_text(doc, max_entities=3)
            all_rag_entities["herbs"].update(doc_entities["herbs"])
            all_rag_entities["fangjis"].update(doc_entities["fangjis"])

        rag_herbs = list(all_rag_entities["herbs"])
        rag_fangjis = list(all_rag_entities["fangjis"])

        # ==================== 新增：合并映射表实体 + RAG实体（去重，映射表优先） ====================
        # 映射表实体放在前面，保证经典推荐优先被查询和呈现
        final_herbs = mapped_herbs + [h for h in rag_herbs if h not in mapped_herbs]
        final_fangjis = mapped_fangjis + [f for f in rag_fangjis if f not in mapped_fangjis]

        # 可选：限制最终实体数量，避免提示词过长（与原逻辑保持一致）
        final_herbs = final_herbs[:5]  # 原路径2没有严格限制，这里保守取10
        final_fangjis = final_fangjis[:5]

        # print(f"  最终合并中药: {final_herbs}")
        # print(f"  最终合并方剂: {final_fangjis}")

        # ==================== 原有逻辑：查询实体属性 ====================
        herb_details = self.entity_extractor.query_herb_details(final_herbs)
        fangji_details = self.entity_extractor.query_fangji_details(final_fangjis)

        # ==================== 原有逻辑：格式化信息 ====================
        entity_info = self.entity_extractor.format_entity_details(herb_details, fangji_details)
        rag_info = self._format_rag_info(top_docs, matched_symptoms)

        # ==================== 原有逻辑：准备给LLM的输入 ====================
        llm_input = self._prepare_llm_input(
            user_question=user_question,
            entity_info=entity_info,
            rag_info=rag_info,
            path_type="只有症状",
            user_mentioned_entities=None  # 用户没有明确提到实体
        )

        return {
            "user_question": user_question,
            "entity_info": entity_info,
            "rag_info": rag_info,
            "path_type": "只有症状",
            "user_mentioned_entities": None
        }

    def _format_rag_info(self, top_docs, matched_symptoms, max_total_chars=1000, max_per_doc=300):
        """格式化RAG信息 - 优化字数分配"""
        formatted = "【相关古籍文献】\n\n"

        # 简化症状显示
        if matched_symptoms and matched_symptoms[0] != matched_symptoms[0]:
            formatted += f"用户症状描述: {matched_symptoms[0]}\n\n"

        if not top_docs:
            return formatted + "未检索到相关古籍文献。\n"

        # 计算理论上限
        theoretical_max = len(top_docs) * max_per_doc

        # 如果理论值小于总限制，可以提高每篇限制
        if theoretical_max < max_total_chars:
            # 重新计算每篇能分到的字数
            max_per_doc = max_total_chars // len(top_docs)

        total_used = 0

        for i, doc in enumerate(top_docs, 1):
            cleaned_doc = self._clean_pinyin_from_doc(doc)

            # 剩余可用字数
            remaining = max_total_chars - total_used

            # 如果这是最后一篇文献，可以用完所有剩余字数
            if i == len(top_docs):
                per_doc_limit = remaining
            else:
                per_doc_limit = min(max_per_doc, remaining)

            if len(cleaned_doc) > per_doc_limit:
                preview = cleaned_doc[:per_doc_limit] + "..."
            else:
                preview = cleaned_doc

            formatted += f"文献{i}:\n{preview}\n\n"
            total_used += len(preview)

        return formatted

    def _clean_pinyin_from_doc(self, doc_text):
        """清理文本中所有拉丁拼音、英文药名、括号标注等无关内容"""
        if not doc_text or not isinstance(doc_text, str):
            return doc_text if doc_text else ""  # 确保返回字符串

        text = doc_text

        # 1. 去除所有括号内的内容
        text = re.sub(r'\([^()]*\)', '', text)

        text = re.sub(r'【类型】.*?\n', '', text)        # 新增：去除【类型】行

        text = re.sub(r'【原文】.*?\n', '', text)        # 新增：去除【原文】行
        # 2. 去除英文药名
        text = re.sub(r'\b([A-Z][a-z]+[A-Z][a-z]+|[A-Z][a-z]+[A-Z]|[A-Z][a-z]+\s+[A-Z][a-z]+)\b', '', text)

        # 3. 去除拉丁前缀
        text = re.sub(r'\b(Radix|Herba|Fructus|Semen|Cortex|Rhizoma|Flos|Folium|Pericarpium)\b\.?', '', text,
                      flags=re.I)

        # 4. 去除英文缩写
        text = re.sub(r'\b[A-Z]\.\s*[A-Za-z]+', '', text)

        # 5. 修改：只压缩连续空格，不处理换行
        # 分两步处理：
        # 5.1 先按行分割，清理每行内的多余空格
        lines = text.split('\n')
        cleaned_lines = []
        for line in lines:
            line = re.sub(r' +', ' ', line.strip())  # 只压缩连续空格
            if line:  # 保留非空行
                cleaned_lines.append(line)

        # 5.2 重新组合，保留原有的换行结构
        text = '\n'.join(cleaned_lines)

        return text.strip()

    def _prepare_llm_input(self, user_question, entity_info, rag_info, path_type, user_mentioned_entities=None,history=None):
        """准备给LLM的输入信息 - 灵活版"""
        self.query_count += 1
        # 清理信息中的拼音标注
        entity_info = self._clean_pinyin_from_doc(entity_info)

        # ==================== 灵活系统提示词 ====================
        if path_type == "包含实体":
            system_prompt = """你是专业的中医医生，请用专业知识直接回答用户问题：
    1. 参考提供的实体和文献信息，但以回答用户问题为主要目标
    2. 不需要复述所有参考信息，只提取对回答有帮助的部分，选择性遗忘上下文历史
    3. 用专业、自然的中医语言回答"""
        else:  # "只有症状"
            system_prompt = """你是专业的中医医生，请用专业知识直接回答用户问题：
    1. 参考提供的实体和文献信息，但以回答用户问题为主要目标
    2. 不需要复述所有参考信息，只提取对回答有帮助的部分，选择性遗忘上下文历史
    3. 用专业、自然的中医语言回答"""

        # ==================== 构建用户提示词 ====================
        user_prompt = f"用户问题：{user_question}\n\n"

        # 如果有用户提到的实体，在提示词中特别强调
        if user_mentioned_entities:
            user_prompt += f"用户提到的中药：{', '.join(user_mentioned_entities)}\n\n"

        # 提供参考信息，但强调这是参考资料
        if entity_info:
            user_prompt += f"【参考资料】（仅供参考）：\n{entity_info[:800]}\n\n"

        # 添加RAG文献
        if rag_info.strip() and rag_info != "【相关古籍文献】\n\n未检索到相关古籍文献。\n":
            user_prompt += f"【古籍参考】：\n{rag_info}\n\n"

        user_prompt += "请基于你的中医专业知识，给出直接、有用的回答。"

        # ==================== 关键修改：过滤assistant消息 ====================
        messages = [{"role": "system", "content": system_prompt}]

        # 如果有历史，只保留用户消息（过滤掉所有assistant消息）
        if history and isinstance(history, list):
            for msg in history:
                # 只添加用户消息，过滤掉assistant消息
                # if msg.get("role") == "user":
                if msg.get("role") in ["user", "assistant"]:
                    messages.append(msg)
            # 限制最多保留3条用户历史消息
            messages = messages[:4]  # system + 最多3条用户历史

        # 添加当前用户问题
        messages.append({"role": "user", "content": user_prompt})

        return messages

    def answer_question(self, user_question, top_k_docs=5, history=None, mode=None):
        """回答用户问题 - 支持四种模式"""
        print(f"\n{'=' * 60}")
        print(f"处理用户问题 [{self.query_count + 1}]: {user_question}")
        print(f"执行模式: {mode if mode else self.default_mode}")
        print('=' * 60)
        if history is None:
            history = []
        # 确定使用哪种模式
        if mode is None:
            mode = self.default_mode

        # 根据模式选择执行路径
        if mode == "pure_llm":
            return self._pure_llm_path(user_question, history=None)
        elif mode == "knowledge_graph":
            return self._knowledge_graph_path(user_question, history=None)
        elif mode == "rag_only":
            return self._rag_only_path(user_question, top_k_docs, history=None)
        elif mode == "full_function":
            return self._full_function_path(user_question, top_k_docs, history=None)
        else:
            raise ValueError(f"未知模式: {mode}，可选：pure_llm, knowledge_graph, rag_only, full_function")

    # ========== 纯LLM模式 ==========
    def _pure_llm_path(self, user_question, history):
        """模式1：纯大模型，不使用外部知识"""
        self.query_count += 1

        # 确保history是列表
        if history is None:
            history = []
        # 精简系统提示词
        system_prompt = """你是一名经验丰富的中医医生。
        你的任务是【直接回答】用户提出的问题。

        要求：
        1. 无论问题是否简短、是否明显，都必须直接给出明确答案
        2. 不要反问用户，不要要求用户补充问题
        3. 不要输出“请继续提问”“请说明情况”等引导性客服用语
        4. 使用专业、简洁、可信的中医表述
        5. 如果问题本身是可以直接判断的（如功效、是否可用），请直接回答结论并简要说明理由
        """

        # 构建messages
        messages = self._build_simple_messages(system_prompt, user_question, history)

        # 调用LLM
        answer = self._call_llm(messages)

        return self._format_response(user_question, answer, "纯LLM模式")

    # ========== 知识图谱模式 ==========
    def _knowledge_graph_path(self, user_question, history):
        """模式2：仅使用知识图谱，不使用RAG"""
        self.query_count += 1

        # 1. 判断问题类型（复用原有逻辑）
        question_entities = self.entity_extractor.extract_entities_from_text(user_question, max_entities=3)

        question_herbs = question_entities["herbs"]
        question_fangjis = question_entities["fangjis"]

        # 2. 根据是否有实体选择处理方式
        if question_herbs or question_fangjis:
            print(f"[DEBUG KG详细] 执行有实体路径")
            path_data = self._entities_only_path(user_question)
        else:
            print(f"[DEBUG KG详细] 执行只有症状路径")
            path_data = self._symptoms_only_path(user_question)

        # 3. 构建messages（不包含RAG信息）
        messages = self._prepare_llm_input(
            user_question=path_data["user_question"],
            entity_info=path_data["entity_info"],
            rag_info="",  # 空RAG信息
            path_type=path_data["path_type"],  # 使用返回的path_type
            user_mentioned_entities=path_data["user_mentioned_entities"],
            history=history
        )

        # 4. 调用LLM
        answer = self._call_llm(messages)

        return self._format_response(user_question, answer, "知识图谱模式")

    # ========== RAG模式 ==========
    def _rag_only_path(self, user_question, top_k_docs, history):
        """模式3：仅使用RAG检索，不使用知识图谱"""
        self.query_count += 1

        # 1. RAG检索
        rag_result = self.rag_retriever.retrieve_for_question(user_question, top_k_docs)
        top_docs = rag_result["top_docs"]
        matched_symptoms = rag_result["matched_symptoms"]

        # 格式化RAG信息
        rag_info = self._format_rag_info(top_docs, matched_symptoms)

        # 2. 构建专用系统提示词
        system_prompt = """你是一名专业的中医医生。请基于你的专业知识，并参考提供的古籍文献内容回答问题，重点关注用户最新的问题"""

        # 3. 构建用户提示词
        user_prompt = f"问题：{user_question}\n\n"
        if rag_info.strip() and rag_info != "【相关古籍文献】\n\n未检索到相关古籍文献。\n":
            user_prompt += f"【古籍参考文献】\n{rag_info}\n\n"
        user_prompt += "请基于你的专业知识和以上古籍文献内容，给出专业、准确的中医建议。"

        # 4. 构建messages
        messages = self._build_simple_messages(system_prompt, user_prompt, history)

        # 5. 调用LLM
        answer = self._call_llm(messages)

        return self._format_response(user_question, answer, "RAG模式")

    # ========== 全功能模式 ==========
    def _full_function_path(self, user_question, top_k_docs, history):
        """模式4：现有完整系统（知识图谱+RAG+LLM）"""
        self.query_count += 1

        # 使用现有的逻辑
        question_entities = self.entity_extractor.extract_entities_from_text(user_question, max_entities=3)
        question_herbs = question_entities["herbs"]
        question_fangjis = question_entities["fangjis"]

        if question_herbs or question_fangjis:
            print(f"[DEBUG full_function] 执行path_with_entities")
            path_data = self.path_with_entities(user_question, top_k_docs)
        else:
            print(f"[DEBUG full_function] 执行path_with_symptoms")
            path_data = self.path_with_symptoms(user_question, top_k_docs)

        # 打印实体信息预览
        entity_info = path_data.get('entity_info', '')
        print(f"[DEBUG full_function] entity_info 长度: {len(entity_info)}")
        if entity_info:
            print(f"[DEBUG full_function] entity_info 预览(前800字符): {entity_info[:800]}")

        # 打印RAG信息预览
        rag_info = path_data.get('rag_info', '')
        print(f"[DEBUG full_function] rag_info 长度: {len(rag_info)}")
        if rag_info:
            print(f"[DEBUG full_function] rag_info 预览(前800字符): {rag_info[:800]}")

        messages = self._prepare_llm_input(
            user_question=path_data["user_question"],
            entity_info=path_data["entity_info"],
            rag_info=path_data["rag_info"],
            path_type=path_data["path_type"],
            user_mentioned_entities=path_data["user_mentioned_entities"],
            history=history
        )
        answer = self._call_llm(messages)
        return self._format_response(user_question, answer, "全功能模式")

    # ========== 辅助方法 ==========
    def _entities_only_path(self, user_question):
        """仅实体路径（知识图谱模式用）"""
        # 从现有path_with_entities中提取，去掉RAG部分
        question_entities = self.entity_extractor.extract_entities_from_text(user_question)
        question_herbs = question_entities["herbs"]
        question_fangjis = question_entities["fangjis"]

        # 查询问题实体的属性
        herb_details = self.entity_extractor.query_herb_details(question_herbs)
        fangji_details = self.entity_extractor.query_fangji_details(question_fangjis)

        # 格式化实体信息
        entity_info = self.entity_extractor.format_entity_details(herb_details, fangji_details)

        if entity_info and len(entity_info) > 0:
            print(f"[DEBUG _entities_only_path] entity_info 预览(前500字符): {entity_info[:500]}")

        return {
            "user_question": user_question,
            "entity_info": entity_info,
            "user_mentioned_entities": question_herbs + question_fangjis,
            "path_type": "包含实体"  # 新增此行
        }

    def _symptoms_only_path(self, user_question):
        """仅症状路径（知识图谱模式用）"""
        # 从现有path_with_symptoms中提取，去掉RAG部分
        symptoms_in_question = self.entity_extractor.extract_symptoms_from_text(user_question)

        if symptoms_in_question:
            mapped_entities = self.entity_extractor.get_entities_from_symptom_map(
                symptoms_in_question, max_entities=8
            )
            mapped_herbs = mapped_entities["herbs"]
            mapped_fangjis = mapped_entities["fangjis"]

            # 查询实体属性
            herb_details = self.entity_extractor.query_herb_details(mapped_herbs)
            fangji_details = self.entity_extractor.query_fangji_details(mapped_fangjis)

            entity_info = self.entity_extractor.format_entity_details(herb_details, fangji_details)

            return {
                "user_question": user_question,
                "entity_info": entity_info,
                "user_mentioned_entities": [],
                "path_type": "只有症状"
            }
        else:
            return {
                "user_question": user_question,
                "entity_info": "未找到相关症状或实体信息。",
                "user_mentioned_entities": [],
                "path_type": "只有症状"
            }

    def _build_simple_messages(self, system_prompt, user_prompt, history):
        messages = [{"role": "system", "content": system_prompt}]

        if history and isinstance(history, list):
            for msg in history:
                # if msg.get("role") == "user":
                if msg.get("role") in ["user", "assistant"]:
                    messages.append(msg)

        messages.append({"role": "user", "content": user_prompt})

        if self.show_prompt:
            print(f"[DEBUG] _build_simple_messages输出:")
            for i, msg in enumerate(messages):
                print(f"  [{i}] {msg['role']}: {msg['content'][:300]}...")

        return messages

    def _call_llm(self, messages):
        """调用LLM的通用方法"""
        if not self.llm_client:
            return "请设置llm_api_url参数以启用LLM功能"

        try:
            answer = self.llm_client.generate_answer(messages)
            return answer if isinstance(answer, str) else str(answer)
        except Exception as e:
            return f"调用大模型时发生错误: {str(e)}"

    def _format_response(self, user_question, answer, path_type):
        """格式化响应"""
        return {
            "query_id": self.query_count,
            "user_question": user_question,
            "final_answer": answer,
            "path_type": path_type
        }

    def close(self):
        """关闭所有连接"""
        self.entity_extractor.close()


# 测试函数
def test_system():
    """测试问答系统"""
    print("启动中医智能问答系统测试...")
    print("=" * 60)
    # 方式1：使用同事的Ollama（默认）
    OLLAMA_API_URL = "https://prostomiate-bell-buildingless.ngrok-free.dev/chat"  # 你同事的API地址
    system1 = TCMQASystem(
        show_prompt=True,
        llm_api_url=OLLAMA_API_URL,  # 使用同事的Ollama
        use_volc=False  # 默认值，可以省略
    )

    # 方式2：使用火山引擎DeepSeek-V3
    # ARK_API_KEY = "b68fab52-f4cd-4fb7-8c50-d67ccc8e6a12"
    # system2 = TCMQASystem(
    #     show_prompt=True,
    #     llm_api_key=ARK_API_KEY,  # 使用火山引擎
    #     use_volc=True
    # )

    test_cases = ["头痛发热怎么治疗？"]

    # 先测试同事的Ollama
    print("\n=== 测试同事Ollama API ===")
    for question in test_cases:
        result = system1.answer_question(question, top_k_docs=3)

    # 再测试火山引擎
    # print("\n=== 测试火山引擎API ===")
    # for question in test_cases:
    #     result = system2.answer_question(question, top_k_docs=3)

    system1.close()
    # system2.close()
    print("\n测试完成！")


if __name__ == "__main__":
    test_system()
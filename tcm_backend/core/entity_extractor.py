# entity_extractor.py
import os
import jieba
import re
import json
from neo4j import GraphDatabase
from typing import Dict, List, Set


class EntityExtractor:
    """统一的实体提取器 - 整合症状映射功能"""

    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password="12345678",
                 synonym_path=None, symptom_map_path=None):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

        # 从Neo4j加载实体列表
        self.herb_list = self._load_entities("Herb", "name")
        self.fangji_list = self._load_entities("Fangji", "name")

        # 确定JSON文件路径（相对当前文件位置）
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # 设置默认路径
        if synonym_path is None:
            synonym_path = os.path.join(current_dir, "json_table", "中医症状同义词表.json")
        if symptom_map_path is None:
            symptom_map_path = os.path.join(current_dir, "json_table", "症状实体映射表.json")

        # 加载症状同义词表和症状实体映射表
        self.symptom_synonyms = self._load_json_file(synonym_path)
        self.symptom_entity_map = self._load_json_file(symptom_map_path)

        # 构建反向同义词映射：同义词 -> 核心症状
        self.reverse_synonym_map = self._build_reverse_synonym_map()

    def _load_json_file(self, file_path: str) -> Dict:
        """加载JSON文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"加载JSON文件失败 {file_path}: {e}")
            return {}

    def _build_reverse_synonym_map(self) -> Dict[str, str]:
        """构建反向同义词映射：同义词 -> 核心症状"""
        reverse_map = {}
        if self.symptom_synonyms:
            for core_symptom, synonyms in self.symptom_synonyms.items():
                # 核心症状本身也映射到自己
                reverse_map[core_symptom] = core_symptom
                # 同义词映射到核心症状
                for synonym in synonyms:
                    reverse_map[synonym] = core_symptom
        return reverse_map

    def _load_entities(self, label, property_name):
        """从Neo4j加载实体列表"""
        query = f"MATCH (n:{label}) RETURN n.{property_name} as name"
        try:
            with self.driver.session() as session:
                result = session.run(query)
                return [record["name"] for record in result if record["name"]]
        except Exception as e:
            print(f"从Neo4j加载{label}列表失败: {e}")
            return []

    def extract_symptoms_from_text(self, text: str) -> List[str]:
        """从文本中提取并标准化症状词"""
        symptoms_found = set()

        if not self.reverse_synonym_map:
            return []

        # 遍历反向映射表，检查文本是否包含症状词
        for symptom_word, core_symptom in self.reverse_synonym_map.items():
            if symptom_word and symptom_word in text:
                symptoms_found.add(core_symptom)

        # 使用jieba分词再检查一次
        words = jieba.lcut(text)
        for word in words:
            if word in self.reverse_synonym_map:
                core_symptom = self.reverse_synonym_map[word]
                symptoms_found.add(core_symptom)

        return list(symptoms_found)

    def get_entities_from_symptom_map(self, symptoms: List[str], max_entities: int = 3) -> Dict[str, List[str]]:
        """从症状映射表中获取相关实体"""
        result = {"herbs": set(), "fangjis": set()}

        if not self.symptom_entity_map:
            return {"herbs": [], "fangjis": []}

        # 按症状顺序处理，每个症状贡献一部分实体
        herbs_per_symptom = max(1, max_entities // len(symptoms))
        fangjis_per_symptom = max(1, max_entities // len(symptoms))

        for symptom in symptoms:
            if symptom in self.symptom_entity_map:
                symptom_data = self.symptom_entity_map[symptom]

                # 添加中药（按表中顺序取前几个）
                herbs = symptom_data.get("herbs", [])
                herbs_to_add = herbs[:herbs_per_symptom]  # 每个症状取前几个
                for herb in herbs_to_add:
                    if herb in self.herb_list and len(result["herbs"]) < max_entities:
                        result["herbs"].add(herb)

                # 添加方剂（按表中顺序取前几个）
                fangjis = symptom_data.get("fangjis", [])
                fangjis_to_add = fangjis[:fangjis_per_symptom]  # 每个症状取前几个
                for fangji in fangjis_to_add:
                    if fangji in self.fangji_list and len(result["fangjis"]) < max_entities:
                        result["fangjis"].add(fangji)

        # 如果还有空间，可以再从所有症状中补充
        if len(result["herbs"]) < max_entities:
            additional_herbs = set()
            for symptom in symptoms:
                if symptom in self.symptom_entity_map:
                    herbs = self.symptom_entity_map[symptom].get("herbs", [])
                    # 跳过已经添加的，取后面的
                    for herb in herbs:
                        if herb in self.herb_list and herb not in result["herbs"]:
                            additional_herbs.add(herb)
                            if len(additional_herbs) + len(result["herbs"]) >= max_entities:
                                break
                if len(additional_herbs) + len(result["herbs"]) >= max_entities:
                    break
            result["herbs"].update(additional_herbs)

        # 方剂同理
        if len(result["fangjis"]) < max_entities:
            additional_fangjis = set()
            for symptom in symptoms:
                if symptom in self.symptom_entity_map:
                    fangjis = self.symptom_entity_map[symptom].get("fangjis", [])
                    for fangji in fangjis:
                        if fangji in self.fangji_list and fangji not in result["fangjis"]:
                            additional_fangjis.add(fangji)
                            if len(additional_fangjis) + len(result["fangjis"]) >= max_entities:
                                break
                if len(additional_fangjis) + len(result["fangjis"]) >= max_entities:
                    break
            result["fangjis"].update(additional_fangjis)

        # 转换为列表并限制数量
        herbs_list = list(result["herbs"])[:max_entities]
        fangjis_list = list(result["fangjis"])[:max_entities]

        return {"herbs": herbs_list, "fangjis": fangjis_list}

    def extract_entities_from_text(self, text: str, max_entities: int = 3) -> Dict[str, List[str]]:
        """从任意文本中提取实体 - 优先使用症状映射表"""

        # 1. 首先提取症状
        symptoms = self.extract_symptoms_from_text(text)

        # 2. 如果找到症状，尝试从症状映射表获取实体
        if symptoms:
            # print(f"  提取到症状: {symptoms}")
            mapped_entities = self.get_entities_from_symptom_map(symptoms, max_entities)

            # 如果从映射表获取到实体，直接返回
            if mapped_entities["herbs"] or mapped_entities["fangjis"]:
                # print(f"  从症状映射表获取实体: {mapped_entities}")
                return mapped_entities

        # 3. 如果没有从映射表获取到实体，使用原有的文本匹配方法
        # print(f"  未从症状映射表获取到实体，使用文本匹配")
        return self._extract_entities_by_text_match(text, max_entities)

    def _extract_entities_by_text_match(self, text: str, max_entities: int = 3) -> Dict[str, List[str]]:
        """原有的文本匹配方法"""
        herbs_found = []
        fangjis_found = []

        # 方法1: 直接字符串匹配
        for herb in self.herb_list:
            if herb and herb in text:
                herbs_found.append(herb)

        for fangji in self.fangji_list:
            if fangji and fangji in text:
                fangjis_found.append(fangji)

        # 方法2: 用jieba分词后再检查
        words = jieba.lcut(text)
        for word in words:
            if word in self.herb_list and word not in herbs_found:
                herbs_found.append(word)
            if word in self.fangji_list and word not in fangjis_found:
                fangjis_found.append(word)

        # 去重
        herbs_found = list(set(herbs_found))
        fangjis_found = list(set(fangjis_found))

        # 限制数量
        herbs_found = herbs_found[:max_entities]
        fangjis_found = fangjis_found[:max_entities]

        return {
            "herbs": herbs_found,
            "fangjis": fangjis_found
        }

    def query_herb_details(self, herb_names):
        """查询中药详细信息 - 按摘录分开，只查询核心属性"""
        if not herb_names:
            return []

        all_herb_details = []
        for herb_name in herb_names:
            # 只查询8个核心属性 + 摘录
            query = """
            MATCH (h:Herb {name: $herb_name})-[r:FROM_SOURCE]->(a:Attributes)
            RETURN h.name as herb_name,
                   a.摘录 as 摘录,
                   a.性味 as 性味,
                   a.功能主治 as 功能主治,
                   a.用法用量 as 用法用量,
                   a.归经 as 归经,
                   a.注意 as 注意,
                   a.相关药方 as 相关药方,
                   a.出处 as 出处
            ORDER BY a.摘录
            """

            try:
                with self.driver.session() as session:
                    results = list(session.run(query, herb_name=herb_name))

                    if results:
                        herb_records = []
                        max_length = 0
                        best_record = None

                        for record in results:
                            details = {"药材名": herb_name}
                            current_length = 0

                            for key, value in dict(record).items():
                                if key == 'herb_name':
                                    continue

                                if value is not None and str(value).strip() and str(value).strip().lower() != 'nan':
                                    cleaned_value = str(value).strip()
                                    # 对性味、功能主治、归经、注意、出处进行清洗
                                    if key in ['性味', '功能主治', '归经', '注意', '出处']:
                                        cleaned_value = self._clean_property_text(cleaned_value)
                                    details[key] = cleaned_value
                                    current_length += len(str(value).strip())

                            if '摘录' in details:
                                # 比较当前记录的总字数
                                if current_length > max_length:
                                    max_length = current_length
                                    best_record = details

                        # 只保留最长的记录
                        if best_record:
                            herb_records.append(best_record)

                        if herb_records:
                            all_herb_details.append(herb_records)
                        else:
                            print(f"  未找到中药 '{herb_name}' 的详细信息")
            except Exception as e:
                print(f"  查询中药 '{herb_name}' 出错: {e}")

        return all_herb_details

    def query_fangji_details(self, fangji_names):
        """查询方剂详细信息"""
        if not fangji_names:
            return []

        fangji_details = []
        for fangji_name in fangji_names:
            query = """
            MATCH (f:Fangji {name: $fangji_name})
            OPTIONAL MATCH (f)-[:HAS_HERB]->(h:Herb)
            RETURN f.name as name,
                   f.function as 功能主治,
                   f.prescription as 组成,
                   f.usage as 用法用量,
                   f.caution as 注意,
                   f.excerpt as 摘录,
                   collect(DISTINCT h.name) as 包含药材
            """

            try:
                with self.driver.session() as session:
                    result = session.run(query, fangji_name=fangji_name)
                    record = result.single()

                    if record:
                        details = {}
                        for key, value in dict(record).items():
                            # 严格过滤
                            if value is not None and str(value).strip() and str(
                                    value).strip().lower() != 'nan' and value != []:
                                if isinstance(value, list):
                                    details[key] = value
                                else:
                                    cleaned_value = str(value).strip()
                                    # 对方剂的功能主治、注意进行清洗
                                    if key in ['功能主治', '注意']:
                                        cleaned_value = self._clean_property_text(cleaned_value)
                                    details[key] = cleaned_value
                        fangji_details.append(details)
                    else:
                        print(f"  未找到方剂 '{fangji_name}' 的详细信息")
            except Exception as e:
                print(f"  查询方剂 '{fangji_name}' 出错: {e}")

        return fangji_details

    @staticmethod
    def _clean_property_text(text):
        """清洗属性文本，去掉序号及后面的引用"""
        # 匹配序号模式：①、②、③等
        # 找到第一个序号，保留序号前的内容
        first_index_match = re.search(r'([①-⑨])', text)
        if first_index_match:
            # 获取第一个序号的位置
            first_index_pos = first_index_match.start()
            # 保留第一个序号之前的内容
            cleaned = text[:first_index_pos].strip()
            # 如果清理后为空，返回原始文本
            return cleaned if cleaned else text
        return text

    def format_entity_details(self, herb_details_list, fangji_details):
        """格式化实体详细信息为字符串（用于给LLM）"""
        formatted_text = ""

        # 格式化中药信息
        if herb_details_list:
            formatted_text += "【中药信息】\n"
            for herb_records in herb_details_list:
                formatted_text += f"\n药材名: {herb_records[0].get('药材名', '未知')}\n"
                formatted_text += "=" * 40 + "\n"

                for i, record in enumerate(herb_records, 1):
                    formatted_text += f"摘录来源 {i}: {record.get('摘录', '未知来源')}\n"

                    # 只输出8个核心属性
                    core_properties = ['性味', '功能主治', '用法用量', '归经', '注意', '相关药方', '出处']

                    for prop in core_properties:
                        if prop in record:
                            formatted_text += f"  {prop}: {record[prop]}\n"

                    if i < len(herb_records):
                        formatted_text += "\n"
                formatted_text += "\n"

        # 格式化方剂信息
        if fangji_details:
            formatted_text += "【方剂信息】\n"
            for fangji in fangji_details:
                formatted_text += f"\n方剂名: {fangji.get('name', '未知')}\n"
                formatted_text += "=" * 40 + "\n"

                if '摘录' in fangji:
                    formatted_text += f"摘录: {fangji['摘录']}\n"

                # 输出方剂核心属性
                properties_order = ['功能主治', '组成', '用法用量', '注意', '包含药材']
                for prop in properties_order:
                    if prop in fangji:
                        if isinstance(fangji[prop], list):
                            formatted_text += f"  {prop}: {', '.join(fangji[prop])}\n"
                        else:
                            formatted_text += f"  {prop}: {fangji[prop]}\n"
                formatted_text += "\n"

        if not herb_details_list and not fangji_details:
            formatted_text = "未查询到任何实体详细信息。\n"

        return formatted_text

    def print_entity_details(self, herb_details_list, fangji_details):
        """打印实体详细信息到控制台"""
        formatted_text = self.format_entity_details(herb_details_list, fangji_details)
        print(formatted_text)

    def close(self):
        self.driver.close()
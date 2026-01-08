import pandas as pd
import json
import os
import random
from typing import List, Dict


def load_excel_data(excel_path: str) -> pd.DataFrame:
    """
    加载Excel文件，处理文件不存在、读取失败等异常
    :param excel_path: Excel文件路径
    :return: 读取后的DataFrame
    """
    # 检查文件是否存在
    if not os.path.exists(excel_path):
        raise FileNotFoundError(f"找不到Excel文件：{excel_path}\n请确认文件路径是否正确")

    # 读取Excel（适配不同格式，优先openpyxl引擎）
    try:
        df = pd.read_excel(excel_path, engine='openpyxl')
        print(f"✅ 成功读取Excel文件，共 {len(df)} 行数据，{len(df.columns)} 列字段")
        print(f"📋 Excel包含的列名：{list(df.columns)}")
        return df
    except ImportError:
        raise ImportError("读取Excel失败：未安装openpyxl库\n请执行命令安装：pip install openpyxl")
    except Exception as e:
        raise Exception(f"读取Excel异常：{str(e)}")


def clean_duplicate_data(df: pd.DataFrame, max_count: int = 100) -> pd.DataFrame:
    """
    数据去重，保留核心字段，并限制数据量
    :param df: 原始DataFrame
    :param max_count: 最大数据量（默认100条）
    :return: 去重后的核心数据DataFrame
    """
    # 定义核心字段（适配Excel实际列名，若有差异需根据Excel列名调整）
    core_fields = ['药材ID', '药材名称', '别名', '性味', '归经', '功能主治', '用法用量', '生境分布', '注意']

    # 检查核心字段是否存在，缺失字段用默认值填充
    missing_fields = [f for f in core_fields if f not in df.columns]
    if missing_fields:
        print(f"⚠️  警告：Excel中缺失以下核心字段，将用'暂无数据'填充：{missing_fields}")
        # 为缺失字段添加默认值列
        for field in missing_fields:
            df[field] = '暂无数据'

    # 按药材ID和名称去重（避免重复数据）
    df_unique = df.drop_duplicates(subset=['药材ID', '药材名称'], keep='first').reset_index(drop=True)
    df_core = df_unique[core_fields].copy()

    # 处理空值（将NaN替换为'暂无数据'）
    for col in core_fields:
        df_core[col] = df_core[col].fillna('暂无数据').astype(str)

    # 限制数据量为100条（随机抽取，保证分类均匀）
    total_count = len(df_core)
    if total_count > max_count:
        # 设置随机种子，保证每次抽取结果一致
        random.seed(42)
        # 随机抽取100条
        sample_index = random.sample(range(total_count), max_count)
        df_core = df_core.iloc[sample_index].reset_index(drop=True)
        print(f"✅ 数据量超过{max_count}条，已随机抽取{max_count}条不重复药材")
    else:
        print(f"✅ 数据去重完成，剩余 {len(df_core)} 种不重复药材（未超过{max_count}条限制）")

    return df_core


def classify_herb(function: str) -> tuple[str, str]:
    """
    根据功能主治对药材分类（补气/补血/滋阴等）
    :param function: 药材功能主治
    :return: (分类名称, 分类ID)
    """
    function = function.lower()
    if any(keyword in function for keyword in ['补气', '益气', '健脾', '补中', '扶正']):
        return '补气', 'qi'
    elif any(keyword in function for keyword in ['补血', '养血', '活血', '调经', '化瘀']):
        return '补血', 'xue'
    elif any(keyword in function for keyword in ['滋阴', '养阴', '生津', '润肺', '清心', '润燥']):
        return '滋阴', 'yin'
    elif any(keyword in function for keyword in ['补阳', '温肾', '壮阳', '散寒', '温经', '助阳']):
        return '补阳', 'yang'
    elif any(keyword in function for keyword in ['清热', '解毒', '泻火', '凉血', '退烧', '消炎']):
        return '清热', 'qingre'
    elif any(keyword in function for keyword in ['祛湿', '化湿', '利水', '消肿', '渗湿', '燥湿']):
        return '祛湿', 'qushi'
    else:
        return '其他', 'other'


def extract_tags(function: str) -> List[str]:
    """
    从功能主治中提取标签（如补气、清热）
    :param function: 药材功能主治
    :return: 标签列表
    """
    tag_keywords = {
        '补气': '补气', '益气': '补气',
        '补血': '补血', '养血': '补血',
        '滋阴': '滋阴', '养阴': '滋阴',
        '补阳': '补阳', '温肾': '补阳',
        '清热': '清热', '解毒': '解毒',
        '祛湿': '祛湿', '利水': '利水',
        '止咳': '止咳', '化痰': '化痰',
        '止痛': '止痛', '活血': '活血',
        '散寒': '散寒', '调经': '调经'
    }
    tags = []
    for keyword, tag in tag_keywords.items():
        if keyword in function and tag not in tags:
            tags.append(tag)
    return tags if tags else ['其他']


def extract_benefits(function: str) -> List[str]:
    """
    提取核心功效（拆分功能主治为短句）
    :param function: 药材功能主治
    :return: 核心功效列表
    """
    if function == '暂无数据':
        return ['暂无详细功效信息']

    # 按常见分隔符拆分句子
    separators = ['。', '；', '，', '、', '：', ';', ',']
    benefits = [function.strip()]
    for sep in separators:
        temp = []
        for benefit in benefits:
            temp.extend([b.strip() for b in benefit.split(sep) if b.strip() and len(b.strip()) > 2])
        benefits = temp

    # 去重并保留前5个有效功效（长度>5的句子）
    valid_benefits = list(set([b for b in benefits if len(b) > 5]))
    return valid_benefits[:5] if valid_benefits else ['暂无详细功效信息']


def format_usage(usage: str) -> str:
    """
    格式化用法用量（统一格式）
    :param usage: 原始用法用量
    :return: 格式化后的用法用量
    """
    if usage == '暂无数据':
        return '暂无推荐用法'
    # 补充"内服/外用"前缀（若缺失）
    if '内服' not in usage and '外用' not in usage:
        if any(unit in usage for unit in ['钱', 'g', '克', '两', '毫升', '勺']):
            return f'内服：{usage}'
        else:
            return usage
    return usage


def generate_herb_info(df_core: pd.DataFrame) -> Dict:
    """
    生成完整的药材信息字典（含焦点药材、分类统计等）
    :param df_core: 去重后的核心数据
    :return: 前端所需的完整数据字典
    """
    print("🚀 开始处理药材数据（分类、标签提取等）...")

    # 应用数据处理函数
    df_core[['category', 'categoryId']] = df_core.apply(
        lambda x: pd.Series(classify_herb(x['功能主治'])), axis=1
    )
    df_core['shortTags'] = df_core.apply(lambda x: extract_tags(x['功能主治']), axis=1)
    df_core['benefits'] = df_core.apply(lambda x: extract_benefits(x['功能主治']), axis=1)
    df_core['usage'] = df_core.apply(lambda x: format_usage(x['用法用量']), axis=1)
    df_core['image'] = '/static/pictures/' + df_core['药材ID'] + '_1.jpg'  # 适配前端图片路径
    df_core['brief'] = df_core['功能主治'].apply(
        lambda x: x[:120] + '...' if len(x) > 120 else x
    )

    # 生成药材列表
    complete_herb_list = []
    for idx, row in df_core.iterrows():
        herb_info = {
            "id": idx + 1,  # 前端展示ID
            "name": row['药材名称'],
            "herbId": row['药材ID'],  # 原始药材ID
            "image": row['image'],
            "category": row['category'],
            "categoryId": row['categoryId'],
            "alias": row['别名'],
            "xingwei": row['性味'],
            "guijing": row['归经'],
            "brief": row['brief'],
            "shortTags": row['shortTags'],
            "tags": list(set([row['category'], row['性味'], row['归经']] + row['shortTags'])),  # 合并所有标签
            "benefits": row['benefits'],
            "usage": row['usage'],
            "habitat": row['生境分布'],
            "warning": row['注意']
        }
        complete_herb_list.append(herb_info)

    # 选择"补气类"作为今日焦点药材（无则选第一个）
    focus_herb = next((h for h in complete_herb_list if h['categoryId'] == 'qi'), complete_herb_list[0])

    # 生成分类统计
    categories = [
        {"id": "all", "name": "全部"},
        {"id": "qi", "name": "补气"},
        {"id": "xue", "name": "补血"},
        {"id": "yin", "name": "滋阴"},
        {"id": "yang", "name": "补阳"},
        {"id": "qingre", "name": "清热"},
        {"id": "qushi", "name": "祛湿"},
        {"id": "other", "name": "其他"}
    ]

    # 统计各分类数量
    category_stats = {"all": len(complete_herb_list)}
    for herb in complete_herb_list:
        cat_id = herb['categoryId']
        category_stats[cat_id] = category_stats.get(cat_id, 0) + 1

    # 为分类添加数量
    categories_with_count = [
        {**cat, "count": category_stats.get(cat["id"], 0)} for cat in categories
    ]

    print("✅ 药材数据处理完成！")
    return {
        "focusHerb": focus_herb,
        "herbList": complete_herb_list,
        "categories": categories_with_count,
        "categoryStats": category_stats,
        "totalCount": len(complete_herb_list)
    }


def save_to_json(data: Dict, output_path: str) -> None:
    """
    将数据保存为JSON文件（UTF-8编码，确保中文正常显示）
    :param data: 要保存的数据
    :param output_path: 输出文件路径
    """
    try:
        # 创建输出目录（若不存在）
        output_dir = os.path.dirname(output_path)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # 保存JSON
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"✅ JSON文件保存成功！")
        print(f"📁 文件路径：{output_path}")
        print(f"📊 数据概览：共{data['totalCount']}种药材，{len(data['categories']) - 1}个分类")
    except Exception as e:
        raise Exception(f"保存JSON失败：{str(e)}")


def print_sample_data(data: Dict) -> None:
    """
    打印示例数据，方便验证
    :param data: 完整药材数据
    """
    print("\n" + "=" * 60)
    print("📌 数据示例（今日焦点药材）：")
    focus = data['focusHerb']
    print(f"  药材名称：{focus['name']}")
    print(f"  药材ID：{focus['herbId']}")
    print(f"  分类：{focus['category']}（{focus['categoryId']}）")
    print(f"  性味：{focus['xingwei']}")
    print(f"  归经：{focus['guijing']}")
    print(f"  图片路径：{focus['image']}")
    print(f"  核心功效：{focus['benefits']}")
    print("=" * 60)


if __name__ == "__main__":
    # ===================== 配置参数（请根据实际情况修改）=====================
    # Excel文件路径（Windows用双反斜杠，macOS/Linux用斜杠）
    EXCEL_FILE_PATH = "C:\\Users\\李旭东\\Desktop\\team-test\\frontend\\src\\data\\medicines_details_converted.xlsx"
    # 输出JSON路径（建议保存到Vue项目的assets目录）
    OUTPUT_JSON_PATH = "C:\\Users\\李旭东\\Desktop\\team-test\\frontend\\src\\data\\complete_herb_data.json"
    # 最大数据量限制（修改这里可以调整数量，当前设为100）
    MAX_HERB_COUNT = 100
    # ========================================================================

    try:
        print("=" * 60)
        print(f"📦 开始执行药材数据生成脚本（限制{MAX_HERB_COUNT}条数据）")
        print("=" * 60)

        # 1. 加载Excel数据
        df = load_excel_data(EXCEL_FILE_PATH)

        # 2. 数据去重和清洗（传入最大数量限制）
        df_core = clean_duplicate_data(df, MAX_HERB_COUNT)

        # 3. 生成完整药材信息
        herb_data = generate_herb_info(df_core)

        # 4. 保存为JSON
        save_to_json(herb_data, OUTPUT_JSON_PATH)

        # 5. 打印示例数据
        print_sample_data(herb_data)

        print(f"\n🎉 所有操作完成！已生成{MAX_HERB_COUNT}条药材数据，JSON文件可直接供Vue前端使用")

    except Exception as e:
        print(f"\n❌ 执行失败：{str(e)}")
        exit(1)
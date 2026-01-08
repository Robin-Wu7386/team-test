import pandas as pd
import json
import os
import random
import time
from typing import List, Dict
from datetime import datetime, timedelta


# ===================== 原有函数（仅修改generate_herb_info） =====================
def load_excel_data(excel_path: str) -> pd.DataFrame:
    if not os.path.exists(excel_path):
        raise FileNotFoundError(f"找不到Excel文件：{excel_path}")
    try:
        df = pd.read_excel(excel_path, engine='openpyxl')
        print(f"✅ 读取Excel：{len(df)}行数据")
        return df
    except ImportError:
        raise ImportError("请安装openpyxl：pip install openpyxl")
    except Exception as e:
        raise Exception(f"读取Excel失败：{str(e)}")


def clean_duplicate_data(df: pd.DataFrame, max_count: int = 10) -> pd.DataFrame:
    core_fields = ['药材ID', '药材名称', '别名', '性味', '归经', '功能主治', '用法用量', '生境分布', '注意']
    missing_fields = [f for f in core_fields if f not in df.columns]
    if missing_fields:
        print(f"⚠️  填充缺失字段：{missing_fields}")
        for field in missing_fields:
            df[field] = '暂无数据'
    df_unique = df.drop_duplicates(subset=['药材ID', '药材名称'], keep='first').reset_index(drop=True)
    df_core = df_unique[core_fields].copy()
    for col in core_fields:
        df_core[col] = df_core[col].fillna('暂无数据').astype(str)
    total_count = len(df_core)
    if total_count > max_count:
        random.seed(random.randint(1, 1000))  # 关键：每次随机种子不同，抽取不同数据
        sample_index = random.sample(range(total_count), max_count)
        df_core = df_core.iloc[sample_index].reset_index(drop=True)
        print(f"✅ 随机抽取{max_count}条数据")
    else:
        print(f"✅ 去重后剩余{len(df_core)}条")
    return df_core


def classify_herb(function: str) -> tuple[str, str]:
    function = function.lower()
    if any(k in function for k in ['补气', '益气']):
        return '补气', 'qi'
    elif any(k in function for k in ['补血', '养血']):
        return '补血', 'xue'
    elif any(k in function for k in ['滋阴', '养阴']):
        return '滋阴', 'yin'
    elif any(k in function for k in ['补阳', '温肾']):
        return '补阳', 'yang'
    elif any(k in function for k in ['清热', '解毒']):
        return '清热', 'qingre'
    elif any(k in function for k in ['祛湿', '利水']):
        return '祛湿', 'qushi'
    else:
        return '其他', 'other'


def extract_tags(function: str) -> List[str]:
    tag_keywords = {'补气': '补气', '补血': '补血', '滋阴': '滋阴', '补阳': '补阳', '清热': '清热', '祛湿': '祛湿'}
    tags = [v for k, v in tag_keywords.items() if k in function]
    return tags if tags else ['其他']


def extract_benefits(function: str) -> List[str]:
    if function == '暂无数据':
        return ['暂无功效']
    separators = ['。', '；', '，']
    benefits = [function.strip()]
    for sep in separators:
        temp = []
        for b in benefits:
            temp.extend([x.strip() for x in b.split(sep) if x.strip() and len(x.strip()) > 2])
        benefits = temp
    return list(set(benefits))[:3] if benefits else ['暂无功效']


def format_usage(usage: str) -> str:
    if usage == '暂无数据':
        return '暂无用法'
    if '内服' not in usage and '外用' not in usage:
        return f'内服：{usage}'
    return usage


def generate_herb_info(df_core: pd.DataFrame) -> Dict:
    print("🚀 处理药材数据...")
    df_core[['category', 'categoryId']] = df_core.apply(lambda x: pd.Series(classify_herb(x['功能主治'])), axis=1)
    df_core['shortTags'] = df_core.apply(lambda x: extract_tags(x['功能主治']), axis=1)
    df_core['benefits'] = df_core.apply(lambda x: extract_benefits(x['功能主治']), axis=1)
    df_core['usage'] = df_core.apply(lambda x: format_usage(x['用法用量']), axis=1)
    df_core['image'] = '/static/pictures/' + df_core['药材ID'] + '_1.jpg'
    df_core['brief'] = df_core['功能主治'].apply(lambda x: x[:50] + '...' if len(x) > 50 else x)

    complete_herb_list = []
    for idx, row in df_core.iterrows():
        herb_info = {
            "id": idx + 1,
            "name": row['药材名称'],
            "herbId": row['药材ID'],
            "image": row['image'],
            "category": row['category'],
            "categoryId": row['categoryId'],
            "alias": row['别名'],
            "xingwei": row['性味'],
            "guijing": row['归经'],
            "brief": row['brief'],
            "shortTags": row['shortTags'],
            "tags": list(set([row['category']] + row['shortTags'])),
            "benefits": row['benefits'],
            "usage": row['usage'],
            "habitat": row['生境分布'],
            "warning": row['注意'],
            "updateTime": datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 关键：新增更新时间标记
        }
        complete_herb_list.append(herb_info)

    # 每次随机选一个焦点药材（确保不同）
    focus_herb = random.choice(complete_herb_list)

    categories = [
        {"id": "all", "name": "全部"}, {"id": "qi", "name": "补气"}, {"id": "xue", "name": "补血"},
        {"id": "yin", "name": "滋阴"}, {"id": "yang", "name": "补阳"}, {"id": "qingre", "name": "清热"},
        {"id": "qushi", "name": "祛湿"}, {"id": "other", "name": "其他"}
    ]
    category_stats = {"all": len(complete_herb_list)}
    for herb in complete_herb_list:
        cat_id = herb['categoryId']
        category_stats[cat_id] = category_stats.get(cat_id, 0) + 1
    categories_with_count = [{**cat, "count": category_stats.get(cat["id"], 0)} for cat in categories]

    # 新增全局更新时间（直观看到JSON变化）
    return {
        "focusHerb": focus_herb,
        "herbList": complete_herb_list,
        "categories": categories_with_count,
        "categoryStats": category_stats,
        "totalCount": len(complete_herb_list),
        "globalUpdateTime": datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 全局更新时间
    }


def save_to_json(data: Dict, output_path: str) -> None:
    try:
        output_dir = os.path.dirname(output_path)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        # 关键：强制覆盖文件，添加flush确保写入
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.flush()  # 强制写入磁盘
        # 验证文件是否更新
        file_mtime = os.path.getmtime(output_path)
        mtime_str = datetime.fromtimestamp(file_mtime).strftime('%H:%M:%S')
        print(f"✅ JSON保存成功！修改时间：{mtime_str}")
        print(f"📄 文件路径：{output_path}")
    except Exception as e:
        raise Exception(f"保存JSON失败：{str(e)}")


def print_sample_data(data: Dict) -> None:
    print("\n📌 本次更新：")
    print(f"  全局更新时间：{data['globalUpdateTime']}")
    print(f"  焦点药材：{data['focusHerb']['name']} | 更新时间：{data['focusHerb']['updateTime']}")
    print("-" * 50)


# ===================== 修复后的定时逻辑 =====================
def run_script_once(excel_path: str, output_path: str, max_count: int = 10) -> None:
    """单次执行（强制更新）"""
    try:
        print(f"\n{'=' * 60}")
        print(f"⏱️  执行时间：{datetime.now().strftime('%H:%M:%S')}")
        print(f"{'=' * 60}")

        # 核心流程
        df = load_excel_data(excel_path)
        df_core = clean_duplicate_data(df, max_count)
        herb_data = generate_herb_info(df_core)
        save_to_json(herb_data, output_path)

        # 打印验证
        print_sample_data(herb_data)
        print(f"🎉 执行完成！")

    except Exception as e:
        print(f"\n❌ 执行失败：{str(e)}")


def run_script_demo_mode(excel_path: str, output_path: str, interval_seconds: int = 30, max_count: int = 10) -> None:
    """演示模式：30秒间隔，强制更新JSON"""
    print("🚀 演示模式启动！")
    print(f"🔄 间隔：{interval_seconds}秒 | 按Ctrl+C停止")
    print(f"📄 Excel：{excel_path}")
    print(f"📤 JSON：{output_path}")
    print("=" * 60)

    # 首次执行
    run_script_once(excel_path, output_path, max_count)

    # 循环执行（确保真的触发）
    execute_count = 1
    while True:
        try:
            # 倒计时
            for i in range(interval_seconds, 0, -1):
                print(f"\r⌛ 下次执行倒计时：{i}秒", end="", flush=True)
                time.sleep(1)

            # 强制执行（每次随机数据）
            execute_count += 1
            print(f"\n\n【第{execute_count}次执行】")
            run_script_once(excel_path, output_path, max_count)

        except KeyboardInterrupt:
            print(f"\n\n🛑 演示停止！累计执行{execute_count}次")
            break
        except Exception as e:
            print(f"\n⚠️  异常，{interval_seconds}秒后重试：{str(e)}")
            time.sleep(interval_seconds)


# ===================== 主函数 =====================
if __name__ == "__main__":
    # 请确认路径正确！！！
    EXCEL_FILE_PATH = "C:\\Users\\李旭东\\Desktop\\team-test\\frontend\\src\\data\\medicines_details_converted.xlsx"
    OUTPUT_JSON_PATH = "C:\\Users\\李旭东\\Desktop\\team-test\\frontend\\src\\data\\complete_herb_data.json"
    MAX_HERB_COUNT = 100  # 演示用小数据量，加快执行
    DEMO_INTERVAL_SECONDS = 30

    # 启动演示
    run_script_demo_mode(
        excel_path=EXCEL_FILE_PATH,
        output_path=OUTPUT_JSON_PATH,
        interval_seconds=DEMO_INTERVAL_SECONDS,
        max_count=MAX_HERB_COUNT
    )
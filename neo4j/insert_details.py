from neo4j import GraphDatabase
import pandas as pd

driver = GraphDatabase.driver(
    "bolt://localhost:7687",
    auth=("neo4j", "12345678")
)

df_converted = pd.read_excel("medicines_details_converted.xlsx")

def insert_herb_details(tx, row):
    tx.run(
        """
        MATCH (h:Herb {herb_id: $herb_id})
        MERGE (source:Source {name: $source_book})
        CREATE (h)-[:FROM_SOURCE {book: $source_book}]->(attrs:Attributes)
        SET attrs += $properties
        """,
        herb_id=row["药材ID"],
        source_book=row["来源书籍"],
        properties={
            "临床应用": row.get("临床应用"),
            "主要成分": row.get("主要成分"),
            "出处": row.get("出处"),
            "别名": row.get("别名"),
            "制剂": row.get("制剂"),
            "制法": row.get("制法"),
            "功能主治": row.get("功能主治"),
            "动物形态": row.get("动物形态"),
            "化学成分": row.get("化学成分"),
            "原形态": row.get("原形态"),
            "各家论述": row.get("各家论述"),
            "含量测定": row.get("含量测定"),
            "备注": row.get("备注"),
            "复方": row.get("复方"),
            "归经": row.get("归经"),
            "性味": row.get("性味"),
            "性味归经": row.get("性味归经"),
            "性状": row.get("性状"),
            "拼音注音": row.get("拼音注音"),
            "摘录": row.get("摘录"),
            "来源": row.get("来源"),
            "栽培": row.get("栽培"),
            "植物形态": row.get("植物形态"),
            "毒性": row.get("毒性"),
            "注意": row.get("注意"),
            "炮制": row.get("炮制"),
            "生境分布": row.get("生境分布"),
            "用法用量": row.get("用法用量"),
            "相关药方": row.get("相关药方"),
            "英文名": row.get("英文名"),
            "药理作用": row.get("药理作用"),
            "药用部位": row.get("药用部位"),
            "规格": row.get("规格"),
            "贮藏": row.get("贮藏"),
            "采收加工": row.get("采收加工"),
            "鉴别": row.get("鉴别")
        }
    )

with driver.session() as session:
    for _, row in df_converted.iterrows():
        session.execute_write(insert_herb_details, row)

driver.close()
print(f"✅ 已插入 {len(df_converted)} 条来源详细信息")
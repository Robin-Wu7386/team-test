# insert_fangji_nodes.py
from neo4j import GraphDatabase
import pandas as pd


def insert_fangji_nodes():
    """插入所有方剂节点"""
    # 读取方剂数据
    df_fangji = pd.read_excel("zhongyaofang_data.xlsx")

    # 连接Neo4j
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "12345678"))

    with driver.session() as session:
        for _, row in df_fangji.iterrows():
            session.run(
                """
                MERGE (f:Fangji {name: $name})
                SET f.prescription = $prescription,
                    f.preparation = $preparation,
                    f.function = $function,
                    f.usage = $usage,
                    f.caution = $caution,
                    f.excerpt = $excerpt
                """,
                name=row["中药方剂"],
                prescription=row.get("处方"),
                preparation=row.get("制法"),
                function=row.get("功能主治"),
                usage=row.get("用法用量"),
                caution=row.get("注意"),
                excerpt=row.get("摘录")
            )

    driver.close()
    print(f"✅ 已插入 {len(df_fangji)} 个方剂节点")


if __name__ == "__main__":
    insert_fangji_nodes()
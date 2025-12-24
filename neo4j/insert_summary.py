from neo4j import GraphDatabase
import pandas as pd

driver = GraphDatabase.driver(
    "bolt://localhost:7687",
    auth=("neo4j", "12345678")
)

df_summary = pd.read_excel("medicines_summary.xlsx")

def insert_herbs(tx, row):
    tx.run(
        """
        MERGE (h:Herb {herb_id: $herb_id})
        SET h.name = $name,
            h.pic_local_url = $pic_local_url,
            h.pic_ori_url = $pic_ori_url,
            h.source_url = $source_url,
            h.source_num = $source_num,
            h.source_list = $source_list,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
            h.collect_time = $collect_time
        """,
        herb_id=row["药材ID"],
        name=row["药材名称"],
        pic_local_url=row.get("图片本地路径"),
        pic_ori_url=row.get("图片原始URL"),
        source_url=row.get("来源页面URL"),
        source_num=row.get("来源数量"),
        source_list=row.get("来源列表"),
        collect_time=row.get("采集时间")
    )


with driver.session() as session:
    for _, row in df_summary.iterrows():
        session.execute_write(insert_herbs, row)

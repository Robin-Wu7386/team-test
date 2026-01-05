import pandas as pd

df_rel = pd.read_excel("h_p_relations.xlsx")

print(df_rel.head())

from neo4j import GraphDatabase

driver = GraphDatabase.driver(
    "bolt://localhost:7687",
    auth=("neo4j", "12345678")
)
def insert_relations_batch(tx, rows):
    tx.run(
        """
        UNWIND $rows AS r
        MATCH (f:Fangji {name: r.fangji})
        MATCH (h:Herb {name: r.herb})
        MERGE (f)-[:HAS_HERB]->(h)
        """,
        rows=rows
    )

batch_size = 8000
rows = [
    {"fangji": row["方剂名"], "herb": row["药材名"]}
    for _, row in df_rel.iterrows()
]

with driver.session() as session:
    for i in range(0, len(rows), batch_size):
        session.execute_write(
            insert_relations_batch,
            rows[i:i + batch_size]
        )


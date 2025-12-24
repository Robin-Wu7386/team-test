import pandas as pd

# 读取药材表
df_herb = pd.read_excel("medicines_summary.xlsx")

# 药材名词典（去重、去空、转字符串）
herb_set = set(
    df_herb["药材名称"]
    .dropna()
    .astype(str)
    .str.strip()
)
print(f"药材词典数量: {len(herb_set)}")

df_formula = pd.read_excel("zhongyaofang_data.xlsx")

relations = []  # 用来存 (方剂名, 药材名)

for _, row in df_formula.iterrows():
    formula_name = str(row["中药方剂"]).strip()
    prescription = row["处方"]

    if pd.isna(prescription):
        continue

    text = str(prescription)

    for herb in herb_set:
        if herb and herb in text:
            relations.append((formula_name, herb))

relations = list(set(relations))
print(f"匹配到的 方剂-药材 关系数: {len(relations)}")

df_rel = pd.DataFrame(relations, columns=["方剂名", "药材名"])
df_rel.to_excel("h_p_relations.xlsx", index=False)

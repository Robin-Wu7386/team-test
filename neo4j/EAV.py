import pandas as pd

# 读取数据
df_details = pd.read_excel("medicines_details.xlsx")

# 删除重复，保留第一个
df_details = df_details.drop_duplicates(
    subset=['药材ID', '药材名称', '来源书籍', '属性名称'],
    keep='first'
)

# 转换
df_converted = df_details.pivot(
    index=['药材ID', '药材名称', '来源书籍'],
    columns='属性名称',
    values='属性值'
).reset_index()

# 清理列名
df_converted.columns.name = None

# 保存
df_converted.to_excel("medicines_details_converted.xlsx", index=False)

print(f"✅ 转换完成！药材数: {len(df_converted)}，列数: {len(df_converted.columns)}")
print(f"列名: {list(df_converted.columns)}")
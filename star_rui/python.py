import pandas as pd

df = pd.read_csv('fyx_chinamoney .xlsx')
data = df
batch_size = 80  # 每个批次的大小

# 使用切片将数据列表拆分成多个批次并打印输出
for i in range(0, len(data), batch_size):
    batch = data[i:i+batch_size]
    print(batch)
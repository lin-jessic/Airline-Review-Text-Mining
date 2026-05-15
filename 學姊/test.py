import pandas as pd
df = pd.read_csv('sampled_20k_with_tokens.csv')
print(df.columns.tolist())        # 確認有 tokens 和 token_count
print(df['tokens'].iloc[0])       # 應該看到 pipe 分隔的字串
print(df['token_count'].iloc[0])  # 應該是一個數字
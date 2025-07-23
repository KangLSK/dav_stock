import openai
import textwrap
import os

def summary(df, stock_id):
    client = openai.OpenAI("")
    rsp = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "你是台股分析師"},
            {"role": "user", "content": f"請分析 {stock_id} 的資料：{df.head().to_dict()}"}
        ]
    )
    return rsp.choices[0].message.content

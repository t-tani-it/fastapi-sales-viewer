from fastapi import FastAPI
import pandas as pd
from fastapi.responses import HTMLResponse

# FastAPIのインスタンスを作成
app = FastAPI()

# ルートエンドポイントを定義
@app.get("/sales")
def get_sales():
    # csvファイルを読み込み、販売金額合計を計算する
    df = pd.read_csv("data/sample_sales.csv", encoding="cp932")
    df['販売単価'] = pd.to_numeric(df['販売単価'], errors='coerce')
    df['販売数量'] = pd.to_numeric(df['販売数量'], errors='coerce')
    df['販売金額合計'] = df['販売単価'] * df['販売数量']
    
    # 日付ごとに販売金額合計を集計する
    df = df.dropna().groupby("日付")["販売金額合計"].sum().reset_index()
    
    # return {"message": "Hello, FastAPI!"}  # FastAPIのデバッグ用のメッセージ
    # return df.to_dict(orient="records")  # データをJSON形式で返す場合
    return HTMLResponse(df.to_html(index=False))  # データをHTMLテーブル形式で返す場合(こちらの方が見やすい)

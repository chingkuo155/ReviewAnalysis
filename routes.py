# routes.py
import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from review_manager import ReviewManager, Review, ReviewDelete
from data_visualizer import DataVisualizer
import pandas as pd
from datetime import datetime

file_path = 'sample1.csv'
model_path = 'roberta_sentiment_model_Final.pth'
review_manager = ReviewManager(file_path, model_path)

router = APIRouter()

@router.post("/add_review/")
async def add_review(review: Review):
    review_manager.add_review(review.product_id, review.rating, review.labels, review.reviews)
    return {"message": "Review added successfully!"}

@router.post("/delete_review/")
async def delete_review(review_delete: ReviewDelete):
    review_manager.delete_review(review_delete.index)
    return {"message": "Review deleted successfully!"}

@router.get("/random_reviews/")
async def get_random_reviews():
    reviews = review_manager.show_random_reviews()
    return reviews

@router.get("/all_reviews/")
async def get_all_reviews():
    reviews = review_manager.show_all_reviews()
    return reviews

@router.get("/bar_chart/")
async def get_bar_chart():
    df = pd.read_csv(file_path)
    visualizer = DataVisualizer(df)
    bar_chart_path = "bar_chart.png"
    visualizer.plot_bar_chart(bar_chart_path)
    return FileResponse(bar_chart_path, media_type="image/png")

@router.get("/word_cloud/")
async def get_word_cloud():
    word_cloud_path = "word_cloud.png"
    
    # 檢查文件是否已存在
    if os.path.exists(word_cloud_path):
        return FileResponse(word_cloud_path, media_type="image/png")
    
    # 如果文件不存在,則創建新的文字雲
    try:
        df = pd.read_csv(file_path)
        visualizer = DataVisualizer(df)
        visualizer.plot_word_cloud(word_cloud_path)
        return FileResponse(word_cloud_path, media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating word cloud: {str(e)}")

@router.get("/area_chart/")
async def get_area_chart(start_date: str, end_date: str):
    try:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")
    
    df = pd.read_csv(file_path)
    visualizer = DataVisualizer(df)
    area_chart_path = "area_chart.png"
    visualizer.plot_area_chart(start_date, end_date, area_chart_path)
    return FileResponse(area_chart_path, media_type="image/png")

@router.get("/api/reviews")
async def get_reviews():
    # 讀取CSV文件
    df = pd.read_csv("Keyword_Sentiment_Statistics.csv")
    
    # 將數據轉換為字典格式
    data = {}
    for _, row in df.iterrows():
        data[row['Keyword']] = {
            'total': row['Total'],
            'positive': row['Positive'],
            'neutral': row['Neutral'],
            'negative': row['Negative']
        }
    return data
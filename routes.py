# routes.py

# routes.py

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import FileResponse
from review_manager import ReviewManager, Review, ReviewDelete
from data_visualizer import DataVisualizer
import pandas as pd
from datetime import datetime
from typing import List, Dict, Any

router = APIRouter()

def get_review_manager():
    return ReviewManager('sample1.csv')

def get_data_visualizer():
    df = pd.read_csv('sample1.csv')
    return DataVisualizer(df)

@router.post("/add_review/")
async def add_review(review: Review, review_manager: ReviewManager = Depends(get_review_manager)):
    review_manager.add_review(review)
    return {"message": "Review added successfully!"}

@router.post("/delete_review/")
async def delete_review(review_delete: ReviewDelete, review_manager: ReviewManager = Depends(get_review_manager)):
    review_manager.delete_review(review_delete.index)
    return {"message": "Review deleted successfully!"}

@router.get("/random_reviews/")
async def get_random_reviews(review_manager: ReviewManager = Depends(get_review_manager)) -> List[Dict[str, Any]]:
    return review_manager.show_random_reviews()

@router.get("/all_reviews/")
async def get_all_reviews(review_manager: ReviewManager = Depends(get_review_manager)) -> List[Dict[str, Any]]:
    return review_manager.show_all_reviews()

@router.get("/bar_chart/")
async def get_bar_chart(visualizer: DataVisualizer = Depends(get_data_visualizer)):
    bar_chart_path = "bar_chart.png"
    visualizer.plot_bar_chart(bar_chart_path)
    return FileResponse(bar_chart_path, media_type="image/png")

@router.get("/word_cloud/")
async def get_word_cloud(visualizer: DataVisualizer = Depends(get_data_visualizer)):
    word_cloud_path = "word_cloud.png"
    visualizer.plot_word_cloud(word_cloud_path)
    return FileResponse(word_cloud_path, media_type="image/png")

@router.get("/area_chart/")
async def get_area_chart(start_date: str, end_date: str, visualizer: DataVisualizer = Depends(get_data_visualizer)):
    try:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")
    
    area_chart_path = "area_chart.png"
    visualizer.plot_area_chart(start_date, end_date, area_chart_path)
    return FileResponse(area_chart_path, media_type="image/png")
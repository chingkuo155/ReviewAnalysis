# review_manager.py
# review_manager.py

from typing import List, Dict, Any
from pydantic import BaseModel
import pandas as pd
from datetime import datetime

class Review(BaseModel):
    product_id: str
    rating: int
    labels: str
    reviews: str

class ReviewDelete(BaseModel):
    index: int

class ReviewManager:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.df = self._load_or_create_dataframe()

    def _load_or_create_dataframe(self) -> pd.DataFrame:
        try:
            return pd.read_csv(self.file_path)
        except FileNotFoundError:
            df = pd.DataFrame(columns=['index', 'product_id', 'rating', 'labels', 'reviews', 'review_date'])
            df.to_csv(self.file_path, index=False)
            return df

    def add_review(self, review: Review) -> None:
        new_index = self.df['index'].max() + 1 if not self.df.empty else 1
        new_review = {
            'index': new_index,
            'product_id': review.product_id,
            'rating': review.rating,
            'labels': review.labels,
            'reviews': review.reviews,
            'review_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        }
        self.df = pd.concat([self.df, pd.DataFrame([new_review])], ignore_index=True)
        self._save_dataframe()

    def delete_review(self, index: int) -> None:
        self.df = self.df[self.df['index'] != index]
        self._save_dataframe()

    def show_random_reviews(self, n: int = 3) -> List[Dict[str, Any]]:
        return self.df.sample(n=n, random_state=1).to_dict(orient='records')

    def show_all_reviews(self) -> List[Dict[str, Any]]:
        return self.df.to_dict(orient='records')

    def _save_dataframe(self) -> None:
        self.df.to_csv(self.file_path, index=False)

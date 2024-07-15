# review_manager.py

from pydantic import BaseModel
import pandas as pd
import os
from datetime import datetime

class Review(BaseModel):
    product_id: str
    rating: int
    labels: str
    reviews: str

class ReviewDelete(BaseModel):
    index: int

class ReviewManager:
    def __init__(self, file_path):
        self.file_path = file_path
        if not os.path.isfile(file_path):
            df = pd.DataFrame(columns=['index', 'product_id', 'rating', 'labels', 'reviews', 'review_date'])
            df.to_csv(file_path, index=False)
        self.df = pd.read_csv(file_path)

    def add_review(self, product_id, rating, labels, reviews):
        new_index = self.df['index'].max() + 1 if not self.df.empty else 1
        review_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        new_review = {
            'index': new_index,
            'product_id': product_id, 
            'rating': rating, 
            'labels': labels, 
            'reviews': reviews,
            'review_date': review_date,
        }
        self.df = pd.concat([self.df, pd.DataFrame([new_review])], ignore_index=True)
        self.df.to_csv(self.file_path, index=False)
    
    def delete_review(self, index):
        self.df = self.df[self.df['index'] != index]
        self.df.to_csv(self.file_path, index=False)
    
    def show_random_reviews(self):
        return self.df.sample(n=3, random_state=1).to_dict(orient='records')
    
    def show_all_reviews(self):
        return self.df.to_dict(orient='records')

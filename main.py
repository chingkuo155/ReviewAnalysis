from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import os
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud, STOPWORDS

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

class Review(BaseModel):
    product_id: str
    rating: int
    labels: str
    reviews: str

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

file_path = 'sample1.csv'
review_manager = ReviewManager(file_path)

@app.post("/add_review/")
async def add_review(review: Review):
    review_manager.add_review(review.product_id, review.rating, review.labels, review.reviews)
    return {"message": "Review added successfully!"}

@app.post("/delete_review/")
async def delete_review(index: int):
    review_manager.delete_review(index)
    return {"message": "Review deleted successfully!"}

@app.get("/random_reviews/")
async def get_random_reviews():
    reviews = review_manager.show_random_reviews()
    return reviews

@app.get("/all_reviews/")
async def get_all_reviews():
    reviews = review_manager.show_all_reviews()
    return reviews

class DataVisualizer:
    def __init__(self, df):
        self.df = df

    def plot_bar_chart(self, file_path):
        counts = self.df['labels'].value_counts()
        sns.barplot(x=counts.index, y=counts, palette='viridis', hue=counts.index)
        plt.xlabel('Labels')
        plt.ylabel('Counts')
        plt.title('Label Counts')
        plt.legend([], [], frameon=False)  # 隱藏圖例
        plt.savefig(file_path)
        plt.close()

    def plot_word_cloud(self, file_path):
        self.df['reviews'] = self.df['reviews'].astype(str)
        text = " ".join(review for review in self.df.reviews)

        stopwords = set(STOPWORDS)
        stopwords.update(["product", "good", "bit", "average", "expected", "will", "buy", "next", "time"])

        wordcloud = WordCloud(stopwords=stopwords, width=800, height=800, background_color='white', colormap='viridis').generate(text)

        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title('Word Cloud')
        plt.savefig(file_path)
        plt.close()

@app.get("/bar_chart/")
async def get_bar_chart():
    df = pd.read_csv(file_path)
    visualizer = DataVisualizer(df)
    bar_chart_path = "bar_chart.png"
    visualizer.plot_bar_chart(bar_chart_path)
    return FileResponse(bar_chart_path, media_type="image/png")

@app.get("/word_cloud/")
async def get_word_cloud():
    df = pd.read_csv(file_path)
    visualizer = DataVisualizer(df)
    word_cloud_path = "word_cloud.png"
    visualizer.plot_word_cloud(word_cloud_path)
    return FileResponse(word_cloud_path, media_type="image/png")

@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return f.read()

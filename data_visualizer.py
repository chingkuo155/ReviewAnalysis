# data_visualizer.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud, STOPWORDS

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
        stopwords.update(["product"])

        wordcloud = WordCloud(stopwords=stopwords, width=800, height=800, background_color='white', colormap='viridis').generate(text)

        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title('Word Cloud')
        plt.savefig(file_path)
        plt.close()
    
    def plot_area_chart(self, start_date, end_date, file_path):
        self.df['review_date'] = pd.to_datetime(self.df['review_date'])
        self.df['month'] = self.df['review_date'].dt.to_period('M')
        # 過濾數據以符合查詢區間
        filtered_df = self.df[(self.df['review_date'] >= start_date) & (self.df['review_date'] <= end_date)]
        df_grouped = filtered_df.groupby(['month', 'labels']).size().unstack().fillna(0)

        df_grouped.plot(kind='area', stacked=True, colormap='viridis')
        plt.title('Sentiment Distribution Over Time')
        plt.xlabel('Date')
        plt.ylabel('Volume')

        plt.savefig(file_path)
        plt.close()
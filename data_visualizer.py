# data_visualizer.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud, STOPWORDS

class DataVisualizer:
    def __init__(self, df):
        self.df = df
        self.n = 90

    def plot_bar_chart(self, file_path):
        counts = self.df['labels'].value_counts()
        total_count = counts.sum()

        plt.figure(figsize=(6, 8))
        sns.barplot(x=counts.index, y=counts, palette='viridis', hue=counts.index)
        plt.xlabel('Labels')
        plt.ylabel('Counts')
        plt.title('Label Counts')
        plt.legend([], [], frameon=False)  # 隱藏圖例

        # 根據counts.index利用表情符號顯示(unicode正:U+1F600 中:U+1F642 負:U+1F625)
        # 表情符號映射
        emoji_map = {
        'Positive': '☺',  # 😀\U0001F600 ☺
        'Neutral': '\U0001F636',   # 🙂
        'Negative': '\U0001F625'   # 😥
        }
        emoji = emoji_map.get(self.df['labels'].value_counts().idxmax(), '')
        plt.text(2, 72, emoji, ha='center', va='bottom', fontsize=48)

        for index, value in enumerate(counts):
            percentage = (value / total_count) * 100
            plt.text(index, value, f'{value}({percentage:.1f}%)', ha='center', va='bottom')
            self.n -= 5
            plt.text(-0.48 ,self.n,f'{counts.index[index]}:{value}({percentage:.1f}%)', fontsize=12, ha='left', va='top')

        plt.text(len(counts)-1, max(counts)-1, f'Total: {total_count}', ha='center', va='bottom', fontsize=12, color='black')
        plt.tight_layout()
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
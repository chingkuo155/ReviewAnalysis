# data_visualizer.py

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from tqdm import tqdm
from preprocessing import process_reviews

class DataVisualizer:
    def __init__(self, df):
        self.df = df
        self.n = 90
    
    def plot_bar_chart(self, file_path):
        counts = self.df['labels'].value_counts()
        total_count = counts.sum()

        plt.figure(figsize=(8, 8))
        sns.barplot(x=counts.index, y=counts, palette='viridis', hue=counts.index)
        plt.xlabel('Labels',fontsize = 13)
        plt.ylabel('Counts',fontsize = 13)
        plt.title('Label Counts', fontsize = 16)
        plt.xticks(fontsize = 11)
        plt.yticks(fontsize = 11)
        plt.legend([], [], frameon=False)  # 隱藏圖例

        # 根據counts.index利用表情符號顯示(unicode正:U+1F600 中:U+1F642 負:U+1F625)
        # 表情符號映射
        emoji_map = {
        'Positive': '☺',  # 😀\U0001F600 ☺
        'Neutral': '\U0001F636',   # 🙂
        'Negative': '\U0001F625'   # 😥
        }
        emoji = emoji_map.get(self.df['labels'].value_counts().idxmax(), '')
        plt.text(len(counts)-1, max(counts)*1.1, emoji, ha='center', va='bottom', fontsize=50)

        for index, value in enumerate(counts):
            percentage = (value / total_count) * 100
            plt.text(-0.5, max(counts) * (1.3 - index * 0.05), 
                     f'{counts.index[index]}: {value} ({percentage:.1f}%)', 
                     fontsize=15, ha='left', va='top')
            plt.text(index, value, f'{value} ({percentage:.1f}%)', ha='center', va='bottom',fontsize = 14)

        plt.text(len(counts)-1, max(counts)-2, f'Total: {total_count}', ha='center', va='bottom', fontsize=16, color='black')
        plt.tight_layout(pad=2)
        plt.savefig(file_path)
        plt.close()

    def plot_word_cloud(self, file_path):
        cleaned_reviews = process_reviews(self.df)

        tfidf_vectorizer = TfidfVectorizer(stop_words='english', max_features=200)
        tfidf_matrix = tfidf_vectorizer.fit_transform(tqdm(cleaned_reviews, desc="計算 TF-IDF"))
        tfidf_feature_names = tfidf_vectorizer.get_feature_names_out()
        tfidf_scores = tfidf_matrix.sum(axis=0).A1
        tfidf_keywords_with_scores = sorted(zip(tfidf_feature_names, tfidf_scores), key=lambda x: x[1], reverse=True)[:100]
        top_keywords_with_scores = [(kw, round(score, 2)) for kw, score in tfidf_keywords_with_scores]

        output_df = pd.DataFrame(top_keywords_with_scores, columns=['Keyword', 'Score'])
        output_df.to_csv("Top100_Keywords_TFIDF_Final.csv", index=False)
        
        keyword_freq = {kw: score for kw, score in top_keywords_with_scores}
        wordcloud = WordCloud(width=800, height=800, background_color='white').generate_from_frequencies(keyword_freq)
        
        plt.figure(figsize=(10, 10))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')

        #plt.title('Word Cloud')
        plt.savefig(file_path)
        plt.close()
    
    def plot_area_chart(self, start_date, end_date, file_path):
        self.df['review_date'] = pd.to_datetime(self.df['review_date'])
        self.df['month'] = self.df['review_date'].dt.to_period('M')
        # 過濾數據以符合查詢區間
        filtered_df = self.df[(self.df['review_date'] >= start_date) & (self.df['review_date'] <= end_date)]
        df_grouped = filtered_df.groupby(['month', 'labels']).size().unstack().fillna(0)

        plt.figure(figsize=(8, 8))
        df_grouped.plot(kind='area', stacked=True, colormap='viridis')
        plt.title('Sentiment Distribution Over Time')
        plt.xlabel('Date')
        plt.ylabel('Volume')
        
        plt.tight_layout()
        plt.savefig(file_path)
        plt.close()

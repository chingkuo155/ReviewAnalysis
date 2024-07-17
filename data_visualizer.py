# data_visualizer.py

from typing import Dict
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud, STOPWORDS

EMOJI_MAP: Dict[str, str] = {
    'Positive': '☺',
    'Neutral': '\U0001F636',
    'Negative': '\U0001F625'
}

class DataVisualizer:
    """A class for visualizing review data."""

    def __init__(self, df: pd.DataFrame):
        """
        Initialize the DataVisualizer with a DataFrame.

        Args:
            df (pd.DataFrame): The DataFrame containing review data.
        """
        self.df = df

    def plot_bar_chart(self, file_path: str) -> None:
        """
        Plot a bar chart of label counts and save it to a file.

        Args:
            file_path (str): The path where the chart will be saved.
        """
        counts = self.df['labels'].value_counts()
        total_count = counts.sum()
        sns.barplot(x=counts.index, y=counts, palette='viridis', hue=counts.index)
        plt.xlabel('Labels')
        plt.ylabel('Counts')
        plt.title('Label Counts')
        plt.legend([], [], frameon=False)

<<<<<<< HEAD
        emoji = EMOJI_MAP.get(self.df['labels'].value_counts().idxmax(), '')
=======
        # 根據counts.index利用表情符號顯示(unicode正:U+1F600 中:U+1F642 負:U+1F625)
        # 表情符號映射
        emoji_map = {
        'Positive': '\U0001F600',  # 😀
        'Neutral': '\U0001F636',   # 🙂
        'Negative': '\U0001F625'   # 😥
        }
        emoji = emoji_map.get(self.df['labels'].value_counts().idxmax(), '')
>>>>>>> parent of e2f51c9 (加入readme.md)
        plt.text(2, 60, emoji, ha='center', va='bottom', fontsize=48)

        for index, value in enumerate(counts):
            percentage = (value / total_count) * 100
            plt.text(index, value, f'{value}({percentage:.1f}%)', ha='center', va='bottom')

        plt.text(len(counts)-1, max(counts)-1, f'Total: {total_count}', ha='center', va='bottom', fontsize=12, color='black')

        self._save_plot(file_path)

    def plot_word_cloud(self, file_path: str) -> None:
        """
        Generate a word cloud from review text and save it to a file.

        Args:
            file_path (str): The path where the word cloud will be saved.
        """
        self.df['reviews'] = self.df['reviews'].astype(str)
        text = " ".join(review for review in self.df.reviews)

        stopwords = set(STOPWORDS)
        stopwords.update(["product"])

        wordcloud = WordCloud(stopwords=stopwords, width=800, height=800, 
                              background_color='white', colormap='viridis').generate(text)

        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title('Word Cloud')
        self._save_plot(file_path)
    
    def plot_area_chart(self, start_date: str, end_date: str, file_path: str) -> None:
        """
        Plot an area chart of sentiment distribution over time and save it to a file.

        Args:
            start_date (str): The start date for filtering data.
            end_date (str): The end date for filtering data.
            file_path (str): The path where the chart will be saved.
        """
        self.df['review_date'] = pd.to_datetime(self.df['review_date'])
        self.df['month'] = self.df['review_date'].dt.to_period('M')
        filtered_df = self.df[(self.df['review_date'] >= start_date) & (self.df['review_date'] <= end_date)]
        df_grouped = filtered_df.groupby(['month', 'labels']).size().unstack().fillna(0)

        df_grouped.plot(kind='area', stacked=True, colormap='viridis')
        plt.title('Sentiment Distribution Over Time')
        plt.xlabel('Date')
        plt.ylabel('Volume')

        self._save_plot(file_path)

    def _save_plot(self, file_path: str) -> None:
        """
        Save the current plot to a file and close it.

        Args:
            file_path (str): The path where the plot will be saved.
        """
        plt.savefig(file_path)
        plt.close()
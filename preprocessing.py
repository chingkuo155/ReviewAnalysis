import nltk
import re
from textblob import TextBlob
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import pandas as pd
from concurrent.futures import ProcessPoolExecutor
from tqdm import tqdm

nltk.download('stopwords')
nltk.download('wordnet')

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    result = {'preprocess': text}

    # 轉換為小寫
    text = text.lower()

    # 擴展縮寫
    text = text.replace("n't", " not").replace("'re", " are").replace("'s", " is")
    text = text.replace("'d", " would").replace("'ll", " will").replace("'t", " not")
    text = text.replace("'ve", " have").replace("'m", " am")

    # 去除標點符號和特殊字符
    text = re.sub(r'[^a-z\s]', '', text)

    # 修正拼寫錯誤
    text = str(TextBlob(text).correct())

    # 分詞
    words = text.split()

    # 去除停用詞
    words = [word for word in words if word not in stop_words]

    # 詞形還原
    words = [lemmatizer.lemmatize(word) for word in words]

    text = ' '.join(words)
    result['preprocess'] = text
    return result

def process_reviews(df):
    reviews = df['reviews'].dropna().tolist()
    with ProcessPoolExecutor() as executor:
        processed_results = list(tqdm(executor.map(preprocess_text, reviews), total=len(reviews), desc="預處理文本"))

    processed_df = pd.DataFrame(processed_results)
    return processed_df['preprocess'].tolist()
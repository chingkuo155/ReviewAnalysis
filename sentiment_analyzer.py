import torch
from transformers import RobertaTokenizer, RobertaForSequenceClassification

class SentimentAnalyzer:
    def __init__(self, model_path):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.tokenizer = RobertaTokenizer.from_pretrained('roberta-base')
        self.model = RobertaForSequenceClassification.from_pretrained('roberta-base', num_labels=3)
        self.model.load_state_dict(torch.load(model_path, map_location=self.device))
        self.model.to(self.device)
        self.model.eval()

    def analyze_sentiments_batch(self, reviews, batch_size=32):
        sentiments = []
        for i in range(0, len(reviews), batch_size):
            batch = reviews[i:i+batch_size]
            inputs = self.tokenizer(batch, return_tensors="pt", truncation=True, padding=True, max_length=512)
            with torch.no_grad():
                outputs = self.model(**inputs)
            probabilities = torch.nn.functional.softmax(outputs.logits, dim=1)
            batch_sentiments = torch.argmax(probabilities, dim=1).tolist()
            sentiments.extend(batch_sentiments)
        return sentiments

    @staticmethod
    def get_sentiment_label(sentiment):
        if sentiment == 0:
            return "Negative"
        elif sentiment == 1:
            return "Neutral"
        else:
            return "Positive"

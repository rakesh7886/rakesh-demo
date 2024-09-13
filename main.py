from fastapi import FastAPI
from pydantic import BaseModel
from transformers import BertTokenizer, BertForSequenceClassification
import torch

# Initialize FastAPI app
app = FastAPI()

# Load the fine-tuned model and tokenizer globally (load once to avoid reloading)
model = BertForSequenceClassification.from_pretrained('model')
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

# Set the model to evaluation mode
model.eval()

# Input schema
class ReviewInput(BaseModel):
    review_text: str

def predict_sentiment(review_text: str) -> str:
    """
    Predict the sentiment of a given review.

    Parameters:
    review_text (str): The text of the review to classify.

    Returns:
    str: The predicted sentiment (positive, neutral, or negative).
    """
    # Tokenize the input text
    inputs = tokenizer(review_text, return_tensors='pt', padding=True, truncation=True)

    # Get model predictions
    with torch.no_grad():
        outputs = model(**inputs)

    # Convert logits to probabilities (optional)
    probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)

    # Get the predicted class index
    predicted_class_idx = torch.argmax(probabilities, dim=1).item()

    # Mapping class index to sentiment label
    class_mapping = {0: 'negative', 1: 'neutral', 2: 'positive'}

    # Get the predicted sentiment
    return class_mapping[predicted_class_idx]

# FastAPI endpoint
@app.post("/predict/")
def predict(review: ReviewInput):
    """
    FastAPI endpoint to predict sentiment for a given review text.

    Parameters:
    review (ReviewInput): A JSON object containing the review text.

    Returns:
    dict: The predicted sentiment.
    """
    sentiment = predict_sentiment(review.review_text)
    return {"sentiment": sentiment}

# # sentiment_analysis_module.py

# from textblob import TextBlob

# def analyze_sentiment(text):
#     analysis = TextBlob(text)
#     if analysis.sentiment.polarity > 0:
#         return 'Positive'
#     elif analysis.sentiment.polarity == 0:
#         return 'Neutral'
#     else:
#         return 'Negative'


import openai

# OpenAI API key
OPENAI_API_KEY = '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'
openai.api_key = OPENAI_API_KEY

class OpenAIError(Exception):
    pass

def analyze_sentiment(response):
    try:
        analysis = openai.Analysis.create(model="text-davinci-003", inputs=response)
        return analysis.sentiment['label']
    except openai.Error as e:
        # Handle OpenAI API error gracefully
        raise OpenAIError(f"Error analyzing sentiment using OpenAI: {e}")



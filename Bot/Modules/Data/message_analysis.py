from textblob import TextBlob
import translate
import re


def analyse_message(message_text: str) -> dict :
    translator = translate.Translator(from_lang='pt', to_lang="en")
    message_text = translator.translate(message_text)
    message_sentiment = TextBlob(message_text).sentiment
    subjectivity = TextBlob(message_text).subjectivity

    if re.search(r'https?://', message_text):  # Check for links
        message_type = "link"
    elif re.search(r'\.(jpg|jpeg|png|gif|bmp|webp|svg)', message_text):  # Check for image extensions
        message_type = "image"
    else:
        message_type = "text"

    return {
        "sentiment_score": message_sentiment[0]*100,
        "subjectivity": subjectivity*100,
        "message_type": message_type,
    }

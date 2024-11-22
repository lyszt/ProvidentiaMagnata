from textblob import TextBlob
import translate
import re


def analyse_message(message_text: str) -> dict :
    message_text = translate.Translator(to_lang="en").translate(message_text)
    message_sentiment = [TextBlob(message_text).sentiment,TextBlob(message_text).subjectivity]

    if re.search(r'https?://', message_text):  # Check for links
        message_type = "link"
    elif re.search(r'\.(jpg|jpeg|png|gif|bmp|webp|svg)', message_text):  # Check for image extensions
        message_type = "image"
    else:
        message_type = "text"

    return {
        "sentiment_score": message_sentiment,
        "message_type": message_type,
    }

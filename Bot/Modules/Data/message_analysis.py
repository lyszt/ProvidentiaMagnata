from textblob import TextBlob
import translate
import re


def get_message_sentiment(message_text: str) -> list :
    message_text = translate.Translator(to_lang="en").translate(message_text)
    message_sentiment = [TextBlob(message_text).sentiment,TextBlob(message_text).subjectivity]
    return message_sentiment
import logging

import requests
from bs4 import BeautifulSoup
# App imports
import discord
from nltk import FreqDist
from peewee import DoesNotExist

from Bot.Modules.Data.database_models import Profiles
from Bot.Modules.Data.database_models import Messages
from Bot.Modules.Data.database_models import MessageTopics



def bing_search(target):
    url = f"https://www.bing.com/search?q=\"{target}\""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    # print(soup.prettify())
    results = []

    for item in soup.find_all("li", {"class": "b_algo"}):
        link = item.find("a")["href"]
        snippet = item.find("p")  # Bing typically places the description in a <p> tag

        if snippet:
            snippet_text = snippet.get_text()
        else:
            snippet_text = "No description available"

        results.append(snippet_text)
        return results

def get_from_database(user: discord.Member) -> dict:
    try:
        user = Profiles.get(Profiles.userid == user.id)
    except DoesNotExist:
        logging.info("User does not have a profile in database.")
        return {}

    messages = Messages.select().where(Messages.user_id == user.id).execute()


    sentiment = user.sentiment_score
    topic_query = (
        MessageTopics
        .select(MessageTopics.topic_name)
        .join(Messages, on=(MessageTopics.message_id == Messages.id))
        .where(Messages.user_id == user.id)
    )

    topics = [topic for topic in topic_query]
    topic_distribution = FreqDist(topics)
    preferred_topics = topic_distribution.most_common()
    messages = [message.message_text for message in messages]
    return {
        'messages': messages,
        'topics': topics,
        'preferred_topics': preferred_topics,
        'sentiment': sentiment
    }
import logging

import peewee
import requests
from bs4 import BeautifulSoup
# App imports
import discord
from collections import Counter
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
        description_text = ""
        description = item.find("p")
        title = item.find("a")
        if title:
            description_text += title.get_text()
        if description:
            description_text += f" {description.get_text()}"

        if description_text == "":
            description_text = "No description available"

        results.append(description_text)
        return results

def get_from_database(user: discord.Member) -> dict:
    try:
        # Try to fetch the user profile
        user_profile = Profiles.get(Profiles.userid == user.id)
        sentiment = user_profile.sentiment_score
    except peewee.DoesNotExist:
        logging.info('User profile not found in database.')
        sentiment = None

    try:
        # Try to fetch user messages
        messages = Messages.select().where(Messages.user_id == user_profile.id)
        messages = [message.message_text for message in messages]
    except peewee.DoesNotExist:
        logging.info('No messages found for the user.')
        messages = []

    try:
        # Try to fetch and process topics
        topic_query = (
            MessageTopics
            .select(MessageTopics.topic_name)
            .join(Messages, on=(MessageTopics.message_id == Messages.message_id))
            .where(Messages.user_id == user_profile.id)
        )
        topics = [topic.topic_name for topic in topic_query]
        topic_distribution = Counter(topics)
        preferred_topics = topic_distribution.most_common(1)[0][0] if topic_distribution.most_common(1) else None
    except peewee.DoesNotExist:
        logging.info('No topics found for the user.')
        topics = []
        preferred_topics = []

    return {
        'messages': messages if messages else 'No messages available',
        'amount of messages': len(messages) if messages else 'No message counted.',
        'topics': topics if topics else 'No topics available',
        'preferred_topics': preferred_topics if preferred_topics else 'No preferred topics available',
        'sentiment': sentiment if sentiment is not None else 'Sentiment data unavailable'
    }

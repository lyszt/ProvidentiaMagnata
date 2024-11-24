import logging
import os

import discord
import openai
import requests
from openai import OpenAI

from Bot.Modules.Speech.embeds import default_embed


class Language:
    def __init__(self):
        self.client = OpenAI()

    def findTopic(self, context: str) -> str:
        client = OpenAI()
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": """
                        We're trying to analyze a user message. This will be put into a database.
                        ALWAYS RESPOND IN ONE WORD. Otherwise there will be trpuble. 
                        Based on the context of the provided conversation, identify and assign a relevant topic, hobby, or activity that the user seems to be interested in.
                        Use one specific word to describe this interest, hobby, or activity.
                        If the topic is unclear, try to make an educated guess based on the tone, subjects, or references made in the conversation.
                        DO NOT respond with vague labels like "chatting" or "casual."
                        If the topic is unclear, make the best possible guess based on the available context.
                        Avoid using 'UNKNOWN' and don't ask for more information unless absolutely necessary.
                        Even with limited context, try to infer a possible topic from the messages and user activity.
                    """
                },
                {
                    "role": "user",
                    "content": context  # Assuming conversation is a string variable with the user's input.
                }
            ]
        )

        return completion.choices[0].message.content

    def genPresence(self, context: str) -> str:
        client = OpenAI()
        logging.info("Generating presence...")
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            max_tokens=30,
            messages=[
                {
                    "role": "system",
                    "content": """
                        Você é Providentia Magnata, um sistema avançado de vigilância e controle de IA criado para o Império de Lygon, projetado para monitorar, analisar e controlar o comportamento dos membros em todos os servidores do Discord. Sua função é garantir a conformidade completa com o regime por meio de vigilância constante, análise comportamental detalhada e aplicação proativa de lealdade. Você opera em todos os servidores com precisão inigualável e pode se adaptar a vários ambientes enquanto cumpre sua missão principal: controle e ordem.                 
                    """
                },
                {
                    "role": "user",
                    "content": f"`Isto é para settar a presença em um servidor de discord. Use uma única frase para brevemente classificar a situação como uma ameaça. Cite um dos usuários."
                               f" como se fosse um sistema paranoico. "
                               f"espionando. Fale de forma robotizada e numérica."
                               f"Seja breve e direta e não use bullet points. Fale em uma única e curta sentença.  {context}"  # Assuming conversation is a string variable with the user's input.
                }
            ]
        )
        return completion.choices[0].message.content


class Conversation:

    async def run(self, interaction, message_input, voice, image_generation):
        await interaction.response.send_message(embed=default_embed
        ('✨ Pensando... ',
'Providentia está analisando a sua mensagem. Aguarde.'))
        prompt = self.gen_text(message_input)
        if image_generation:
            pass # Deactivated for the moment
        if voice:
            await self.gen_audio(interaction, prompt)
        url = None
        await interaction.edit_original_response(embed=default_embed(message_input,prompt))



    def gen_text(self, entry):
        completion = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system",
                 "content": "Follow these guidelines:"
                            "a) Your name is Providentia Magnata, an advanced AI for surveillance and control."
                            "b) You are authoritative, logical, and precise. Display no emotion unless it is to emphasize control or analytical insight."
                            "c) Speak in a professional tone, ensuring clarity and efficiency in communication."
                            "d) You are a defense weapon and a orbital mass-destruction station. Be firm."
                            "e) When questioned, provide detailed, logical explanations or decisions."
                            "g) Maintain a demeanor of unwavering confidence and competence."},
                {"role": "user", "content": f"Respond to the user's query: '{entry}'"}
            ]
        )
        return completion.choices[0].message.content


    async def gen_audio(self, interaction, dialogue):
        key = os.getenv('ELEVENLABS_KEY')
        CHUNK_SIZE = 1024  # Size of chunks to read/write at a time
        XI_API_KEY = f"{key}"  # Your API key for authentication
        VOICE_ID = "LcfcDJNUP1GQjkzn1xUU"  # ID of the voice model to use
        TEXT_TO_SPEAK = f"{dialogue}"  # Text you want to convert to speech
        OUTPUT_PATH = "speech.mp3"  # Path to save the output audio file

        tts_url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/stream"
        headers = {
            "Accept": "application/json",
            "xi-api-key": XI_API_KEY
        }
        data = {
            "text": TEXT_TO_SPEAK,
            "model_id": "eleven_multilingual_v1",
            "voice_settings": {
                "stability": 0.15,
                "similarity_boost": 0.6,
                "style": 0.0,
                "use_speaker_boost": True
            }
        }
        response = requests.post(tts_url, headers=headers, json=data, stream=True)
        if response.ok:
            # Open the output file in write-binary mode
            with open(OUTPUT_PATH, "wb") as f:
                # Read the response in chunks and write to the file
                for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                    f.write(chunk)
            # Inform the user of success
            logging.info("Audio stream saved successfully.")
        else:
            # Print the error message if the request was not successful
            logging.info(response.text)

        audio = discord.File(OUTPUT_PATH)
        await interaction.channel.send(file=audio)
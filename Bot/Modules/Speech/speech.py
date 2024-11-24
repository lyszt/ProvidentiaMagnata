# Utils
import logging
import os
# Application
import discord
import openai
import requests
from openai import OpenAI
from pydub import AudioSegment
from pydub.effects import speedup

# Specifics
from Bot.Modules.Speech.embeds import default_embed
# Audio
from io import BytesIO
import tempfile
import requests
import numpy as np
import scipy.signal as sg
import pydub
import matplotlib.pyplot as plt
from IPython.display import Audio, display
import tempfile

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
        CHUNK_SIZE = 1024
        XI_API_KEY = f"{key}"
        VOICE_ID = "LcfcDJNUP1GQjkzn1xUU"
        TEXT_TO_SPEAK = f"{dialogue}"
        OUTPUT_PATH = "temp/speech.mp3"
        BACKGROUND_PATH = "../Speech/hexcore.mp3"

        tts_url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/stream"
        headers = {
            "Accept": "application/json",
            "xi-api-key": XI_API_KEY
        }

        data = {
            "text": TEXT_TO_SPEAK,
            "model_id": "eleven_multilingual_v1",
            "voice_settings": {
                "stability": 0.1,
                "similarity_boost": 0.4,
                "style": 0.0,
                "use_speaker_boost": True
            }
        }

        response = requests.post(tts_url, headers=headers, json=data, stream=True)

        if response.ok:
            with open(OUTPUT_PATH, "wb") as f:
                for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                    f.write(chunk)

            logging.info("Audio stream saved successfully.")
        else:
            logging.error(response.text)
            return None, None

        audio = AudioSegment.from_mp3(OUTPUT_PATH)
        background_song = AudioSegment.from_mp3(BACKGROUND_PATH)
        background_song = background_song - 20
        if len(background_song) < len(audio):
            times_to_loop = len(audio) // len(background_song) + 1
            background_song = background_song * times_to_loop
        background_song = background_song[:len(audio)]
        silence_duration = 300
        words = audio.split_to_mono()
        segments_with_delay = []
        for segment in words:
            segments_with_delay.append(segment)
            silence = AudioSegment.silent(duration=silence_duration)
            segments_with_delay.append(silence)

        delayed_audio = sum(segments_with_delay)
        eq_filtered_audio = delayed_audio.low_pass_filter(1000)

        distorted_audio = eq_filtered_audio

        delay_ms = 500
        decay = 0.5
        delay_samples = int(distorted_audio.frame_rate * (delay_ms / 1000.0))
        echo_audio = AudioSegment.silent(duration=len(distorted_audio))
        delayed_audio = distorted_audio[delay_samples:]
        faded_audio = delayed_audio.fade_out(int(len(delayed_audio) * decay))
        echo_audio = distorted_audio.overlay(faded_audio, position=delay_samples)

        combined_audio = background_song.overlay(echo_audio)
        combined_audio.export(OUTPUT_PATH, format='mp3')

        audio = discord.File(OUTPUT_PATH)
        await interaction.channel.send(file=audio)
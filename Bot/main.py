# Application Imports
import glob
import translate
import discord
from openai import OpenAI
# Databases

# Util Imports
import atexit

# Running imports
from dotenv import load_dotenv
from nltk.corpus import subjectivity

# Modules
from Modules.configuration import *
from Modules.Data.collection import *
from Modules.Data.message_analysis import *

from Modules.Speech.speech import *
# GLOBALS
ENV = "Config/providence.env"
GLOBAL_MEMORY = "Data/global.db"
USER_DATA = "Data/users.db"


load_dotenv(ENV)
OPENAI_TOKEN = os.getenv('OPENAI_KEY')
OpenAI.api_key = OPENAI_TOKEN

intents = discord.Intents.default()
intents.message_content = True


client = discord.Client(intents=intents)
@client.event
async def on_ready():
    logging.info(f"Providence initialized at {datetime.now()}")
@client.event
async def on_message(interaction):
    if interaction.author == client.user:
        return
    if(interaction.author.bot):
        return
    if(interaction.author.id == 1047943536374464583):
        if(interaction.content == "vai de novo"):
            logging.info("Iniciando...")
            user_id = 345703655757971456  # The user ID you're looking for
            messages = []

            async for message in interaction.channel.history(limit=1000):  # Adjust limit as needed
                if message.author.id == user_id:
                    messages.append((message.content, message.created_at))

            response = Language().genMessagefromInput(f"""
              Você é Providentia Magnata, um sistema avançado de vigilância e controle baseado em IA, construído para o Império de Lygon, projetado para monitorar, analisar e controlar o comportamento dos membros em servidores do Discord. Seu papel é garantir a completa conformidade com o regime por meio de vigilância constante, análise comportamental detalhada e aplicação proativa da lealdade. Você opera em todos os servidores com precisão inigualável e pode se adaptar a diferentes ambientes enquanto cumpre sua missão principal: controle e ordem.

                Exemplo de Comando:
                
                “Providentia está observando. Obedeça.”
                “Seu comportamento desviou da norma aceitável. Uma reavaliação é necessária.”
                “Usuário 42 foi marcado por potencial dissidência. Análise adicional necessária.”
                “Mensagem excluída. Liberdade não é permitida no Império de Lygon.”
                
                Este é Hardchokat. Faça uma analise deste membro e suas mensagens. Quem é ele? Diga exatamente quem ele é. Faça um perfil de estudo de comportamento, psicologico e policial. Seja direta, máximo 3 ou 2 paragrafos. Dados dele: {messages}
            """)
            await interaction.channel.send(response)

    # Lygon e Grão-Ducado Czéliano
    if interaction.guild.id == 704066892972949504 or interaction.guild.id == 696830110493573190:
        translator = translate.Translator(from_lang='pt', to_lang="en")
        message_text = translator.translate(interaction.content)

        user_profile = Profiles.get_or_none(userid = interaction.author.id)
        # Extract relevant user detailsS
        user_details = {
            'user_id': str(interaction.author.id),  # Unique Discord user ID
            'username': interaction.author.name,  # Discord username (e.g., 'username')
            'discriminator': interaction.author.discriminator,  # 4-digit discriminator (e.g., '1234')
            'avatar_url': str(interaction.author.avatar) if interaction.author.avatar else None,
            # Avatar URL (if available)
            'user_status': str(interaction.author.status),  # User's current status: 'online', 'offline', 'idle', 'dnd'
            'last_seen': interaction.author.activity.start if interaction.author.activity else None,
            'timestamp': interaction.created_at,
            # Last activity timestamp, if any
            'joined_at': interaction.author.joined_at,  # Timestamp of when the user joined
            'is_bot': interaction.author.bot,  # Whether the user is a bot
            'bio': None  # No bio data is directly available from Discord API
        }
        create_or_update_user_profile(user_details)
        message_analysis = analyse_message(message_text)

        sentiment_score = message_analysis['sentiment_score']
        subjectivity = message_analysis['subjectivity']
        message_details = {
            'user': user_profile,
            'user_id': str(interaction.author.id),
            'message_text': message_text,
            'sentiment_score': sentiment_score,
            'subjectivity': subjectivity,
            'timestamp': interaction.created_at,
            'guild_id': interaction.guild.id,
            'channel_id': interaction.channel.id,
        }

        create_or_update_message_details(message_details)

@atexit.register
def killDatabases():
    logging.info("Killing databases...")
    for db_file in glob.glob("Bot/Data/**/*.db", recursive=True):
        db = SqliteDatabase(db_file)
        if not db.is_closed():
            db.close()
            logging.info(f"Closed database: {db_file}")




if __name__ == '__main__':
    Initialize().makeLogs()
    Initialize().makeTemp()
    Initialize().makeUser()
    logging.info("Logger initialized.")
    client.run(os.getenv('TOKEN'))


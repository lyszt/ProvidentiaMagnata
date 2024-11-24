import logging

from openai import OpenAI

class IncrementalProcessor:
    def __init__(self):
        self.processed_ids = set()

    def process_new_messages(self,messages):
        new_messages = [msg for msg in messages if id(msg) not in self.processed_ids]
        for msg in new_messages:
            logging.info(f"Processing: {msg}")
            self.processed_ids.add(id(msg))

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
            max_tokens=20,
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


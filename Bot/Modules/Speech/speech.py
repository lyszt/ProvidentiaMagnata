from openai import OpenAI


class Language:
    def __init__(self):
        client = OpenAI()

    def genMessagefromInput(self,input: str) -> str:
        from openai import OpenAI
        client = OpenAI()

        completion = client.chat.completions.create(
            model="o1-preview",
            messages=[
                {
                    "role": "user",
                    "content": f"{input}"
                }
            ]
        )
        return completion.choices[0].message.content


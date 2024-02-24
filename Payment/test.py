
import openai

api_key = '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'
openai.api_key = api_key

prompt = "Translate the following English text to French: 'Hello, world!'"

response = openai.Completion.create(
    engine="text-davinci-002",
    prompt=prompt,
    max_tokens=50
)

translated_text = response.choices[0].text
print(translated_text)

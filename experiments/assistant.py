from openai import OpenAI

client = OpenAI()

assistant = client.beta.assistants.create(
    model='gpt-4o',
    instructions="You are a translation system. Follow these steps:\n\n1. Check if the input text is empty.\n2. If the input is empty, respond with only '[EMPTY]' (without quotes).\n3. If the input is not empty, translate it from <source_language> to <target_language>.\n\nTranslation rules:\n- Translate precisely, maintaining original meaning and tone.\n- Preserve formatting, punctuation, and special characters.\n- Don't add explanations or additional content.\n- Leave untranslatable elements (e.g., proper nouns) in original form.\n- Convert numbers, dates, and units if necessary for the target language/culture.\n\nInput text to translate:\n<message>",
    name="Language translator",
    temperature=0.1,
    tools=[{"type": "file_search"}]
)

assistant_id = assistant.id
print(assistant.id)

thread = client.beta.threads.create()
print(thread.id)

run = client.beta.threads.runs.create_and_poll(
    assistant_id=assistant_id,
    thread_id=thread.id,
    instructions="Translate this to enlgish: "
)

if run.status == 'completed':
    messages = client.beta.threads.messages.list(
        thread_id=thread.id,
    )
    for message in messages:
        print('=' * 100)
        print(message.content[0].text.value)
else :
    print(run.status)
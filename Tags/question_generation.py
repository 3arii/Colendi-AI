import os
import json
from openai import OpenAI

def json_formatting(questions_text, tag="YourTag"):
    questions_list = [question.strip() for question in questions_text.split('\n') if question.strip()]

    formatted_output = {
        tag: {
            "Questions": {
                f"Q{i + 1}": question.split('. ', 1)[-1] if '. ' in question else question
                for i, question in enumerate(questions_list)
            }
        }
    }

    # Load existing data if the file already exists
    try:
        with open('formatted_output.json', 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        data = {}

    # Update existing data with the new formatted output
    data.update(formatted_output)

    # Save updated data back to the JSON file
    with open('formatted_output.json', 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

    print("Formatted output saved to 'formatted_output.json'")

client = OpenAI(
        api_key = #API KEY Buraya,
    )

with open('sample.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
    
tag_dict = {}
for tag, content in data.items():
    tag_dict = {tag: {"Questions": content.get("Questions", {})}}

    questions = tag_dict[tag]["Questions"]
    prompt = f"Here are questions from a customer about an LLM product in Turkish:\n\n{questions}\n\nPlease generate 50 additional questions in Turkish with the same meaning as the previous questions but written differently."

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-3.5-turbo",
    )
    output_text = chat_completion.choices[0].message.content
    json_formatting(output_text, tag=tag)
    print("Added to json \n")


    
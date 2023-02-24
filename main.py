import openai
import os

openai.api_key = "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"

model_engine = "text-davinci-003"

def ask(prompt):
    completion = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    return completion.choices[0].text

folder = 'warriorthesis'
# topic = 'ozone sanitization in the food industry'
topic = 'bullying'
title = 'How to Recognize the Signs of Bullying'

def generate_ideas(topic):
    response = ask(f"give me some blog post ideas for {topic}")
    with open(f'./{folder}/ideas.txt', 'w') as f: f.write(response)

def generate_title(title):
    response = ask(f"Write a title for a blog post about {topic}")
    with open(f'./{folder}/title.txt', 'w') as f: f.write(response)

def generate_outline():
    response = ask(f'write me a blog outline for the following title [{title}]. Only use numbers for sections and dashes for subsections. Make the outline unreasonably long.')
    with open(f'./{folder}/outline.txt', 'w') as f: f.write(response)
    print(response)

def generate_sections():
    with open(f'./{folder}/outline-refined.txt') as f: lines = f.readlines()

    subtitles = []
    for line in lines:
        if line == '\n' or line == '': pass
        else: subtitles.append(line.replace('\n', '').strip())

    i = 0
    for subtitle in subtitles:
        response = ask(f"write me a blog section for: {subtitles[i]} {topic}")
        filename = subtitle.lower().replace(' ', '_')
        with open(f'./{folder}/sections/{i}_{filename}.txt', 'w') as f: f.write(response)
        i += 1
        print(response)


def generate_post():
    with open(f'./{folder}/post.txt', 'w') as f: pass

    for section in os.listdir(f'./{folder}/sections/'):
        filepath = f'./{folder}/sections/{section}'
        with open(filepath) as f: 
            content = f.read()

        with open(f'./{folder}/post.txt', 'a') as f:
            f.write(content)


# generate_outline()
generate_sections()
generate_post()

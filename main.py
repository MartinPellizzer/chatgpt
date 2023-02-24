import openai
import os

with open('api.txt') as f:
    openai.api_key = f.read()

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
folder = 'ozonogroup'
topic = 'bullying'
topic = 'ozone sanitization in the food industry'

def generate_ideas():
    response = ask(f"give me 10 blog post ideas for {topic}")
    with open(f'./{folder}/ideas.txt', 'w') as f: f.write(response)
    print(response)

def generate_title():
    response = ask(f"Write a title for a blog post about {topic}")
    with open(f'./{folder}/title.txt', 'w') as f: f.write(response)
    print(response)

def generate_outline(title):
    response = ask(f'write me a blog outline for the following title [{title}]. Only use numbers for sections and dashes for subsections. Make the outline unreasonably long.')
    with open(f'./{folder}/outline.txt', 'w') as f: f.write(response)
    print(response)

def generate_sections():
    with open(f'./{folder}/outline.txt') as f: lines = f.readlines()

    subtitles = []
    for line in lines:
        if line == '\n' or line == '': pass
        else: subtitles.append(line.replace('\n', '').strip())

    i = 0
    for subtitle in subtitles:
        response = ask(f"write me a blog section for {subtitles[i]} (context: {topic})")
        filename = subtitle.lower().replace(' ', '_')
        with open(f'./{folder}/sections/{i}_{filename}.txt', 'w') as f: f.write(response)
        i += 1
        print(response)

def generate_sections_ita():
    for section in os.listdir(f'./{folder}/sections/'):
        with open(f'./{folder}/sections/{section}') as f: 
            content = f.read()

        response = ask(f"translate in italian: {content}")
        with open(f'./{folder}/sections_ita/{section}', 'w') as f: 
            f.write(response)
        print(response)



def generate_post():
    with open(f'./{folder}/post.txt', 'w') as f: pass

    for section in os.listdir(f'./{folder}/sections/'):
        filepath = f'./{folder}/sections/{section}'
        with open(filepath) as f: 
            content = f.read()

        with open(f'./{folder}/post.txt', 'a') as f:
            f.write('\n')
            f.write('\n')
            section = section[5:-4].replace('_', ' ').title()
            f.write(section)
            f.write(content)


# generate_ideas()

# with open(f'./{folder}/ideas.txt') as f: 
#     lines = f.readlines()
# title = lines[10]
# generate_outline(title)

# generate_sections()
generate_sections_ita()
# generate_post()

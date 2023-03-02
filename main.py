import openai
import os
import re

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

# folder = 'ozonogroup'
folder = 'temp'
topic = 'bullying'
# topic = 'ozone sanitization in the food industry'

prompt_list = [
    'give me 10 blog post ideas about ',
    'write a title for a blog post about ',
    'write me a blog outline for ',
    'write me a blog post about ',
]

def generate_ideas():
    with open(f'./content/keyword.txt') as f: content = f.read()
    response = ask(f"give me 10 blog post ideas for {content}")
    with open(f'./{folder}/ideas.txt', 'w') as f: f.write(response)
    print(response)

def generate_title():
    with open(f'./content/keyword.txt') as f: content = f.read()
    response = ask(f"Write a title for a blog post about {topic}")
    with open(f'./{folder}/title.txt', 'w') as f: f.write(response)
    print(response)

def generate_main_outline():
    with open(f'./content/keyword.txt') as f: content = f.read()
    response = ask(f'write a list of form of bullying')
    with open(f'./{folder}/outline.txt', 'w') as f: f.write(response)
    print(response)


def generate_sub_outline():
    with open(f'./tmp/sub_outline.txt', 'w') as f: pass

    with open(f'./content/main_outline.txt') as f: lines = f.readlines()
    for line in lines:
        response = ask(f'write a crazy long list of {line} behaviours, number the list items')
        response = response.strip()
        with open(f'./tmp/sub_outline.txt', 'a') as f: 
            f.write(line)
            f.write(f'{response}')
            f.write(f'\n\n')
        print(response)
        

def generate_sub_outline_clean():
    with open(f'./tmp/sub_outline_clean.txt', 'w') as f: pass

    with open(f'./tmp/sub_outline.txt') as f: lines = f.readlines()
    unique_list = []
    for line in lines:
        # line = ' '.join(line.split(' ')[1:])
        new_name = re.sub("^\d+.\s", '', line)
        if new_name in unique_list: continue
        else: unique_list.append(new_name)
        with open(f'./tmp/sub_outline_clean.txt', 'a') as f: f.write(line)


def generate_section(filename):
    with open(f'./content/sub_outline/{filename}') as f: lines = f.readlines()

    i = 0
    for line in lines:
        response = ask(f"write me a 100-words or more blog post paragraph about {line}")
        if i < 10: i_str = '0' + str(i)
        else: i_str = str(i) 
        with open(f'./content/sections/{i_str}.txt', 'w') as f: f.write(response)
        i += 1
        print(response)


def generate_sections():
    sub_outline = [ x for x in os.listdir('./content/sub_outline/')]

    i = 0
    for item in sub_outline:
        with open(f'./content/sub_outline/{item}') as f: lines = f.readlines()

        for line in lines:
            response = ask(f"write me a 100-words or more blog post paragraph about {line}")
            response = response.replace("’", "'")
            if i < 10: i_str = '0' + str(i)
            else: i_str = str(i) 
            with open(f'./content/sections/{i_str}.txt', 'w') as f: f.write(response)
            i += 1
            print(response)


# def generate_sections():
#     with open(f'./{folder}/outline-refined.txt') as f: lines = f.readlines()

#     subtitles = []
#     for line in lines:
#         if line == '\n' or line == '': pass
#         else: subtitles.append(line.replace('\n', '').strip())

#     i = 0
#     for subtitle in subtitles:
#         response = ask(f"write me a blog section for {subtitles[i]} (context: {topic}) [use only ascii characters]")
#         filename = subtitle.lower().replace(' ', '_')
#         if i < 10: i_str = '0' + str(i)
#         else: i_str = str(i) 
#         with open(f'./{folder}/sections/{i}_{filename}.txt', 'w') as f: f.write(response)
#         i += 1
#         print(response)


def generate_sections_ita():
    for section in os.listdir(f'./{folder}/sections/'):
        with open(f'./{folder}/sections/{section}') as f: 
            content = f.read()

        response = ask(f"translate in italian: {content}")
        with open(f'./{folder}/sections_ita/{section}', 'w') as f: 
            f.write(response)
        print(response)


# def generate_post():
#     with open(f'./{folder}/post.txt', 'w') as f: pass

#     for section in os.listdir(f'./{folder}/sections/'):
#         filepath = f'./{folder}/sections/{section}'
#         with open(filepath) as f: 
#             content = f.read()

#         with open(f'./{folder}/post.txt', 'a') as f:
#             f.write('\n')
#             f.write('\n')
#             section = section[5:-4].replace('_', ' ').title()
#             f.write(section)
#             f.write(content)

def generate_post_list():
    title = "101 Signs You've Just Being Bullied (March 2023)"
    with open(f'./content/main_outline.txt') as f: 
        outline = f.readlines()
    
    sub_outline_filenames = [x for x in os.listdir('./content/sub_outline/')]
    # sub_outline = [x.replace("_", ' ')[3:].title() for x in sub_outline_filenames]
    sub_outline = []
    for sub_outline_filename in sub_outline_filenames:
        with open(f'./content/sub_outline/{sub_outline_filename}') as f: 
            sub_outline.append(f.readlines()) 

    sections_filenames = [x for x in os.listdir('./content/sections/')]
    
    sections_content = []
    for section_filename in sections_filenames:
        with open(f'./content/sections/{section_filename}') as f: 
            sections_content.append(f.read())


    print(title)
    print(outline)
    print(sub_outline)
    print(sections_filenames)

    # for section_content in sections_content:
    #     print(section_content)

    with open('./content/final.html', 'w') as f:
        f.write(f'<h1>{title}</h1>')
        i = 0
        for h2 in outline:
            f.write(f'<h2>{h2}</h2>')
            for k in range(10):
                f.write(f'<h3>{sub_outline[i][k]}</h3>')
                f.write(f'<p>{sections_content[i * 10 + k]}</p>')
            i += 1
    
    with open('./content/final.md', 'w') as f:
        f.write(f'# {title}\n')
        i = 0
        for h2 in outline:
            f.write(f'## {h2}\n')
            for k in range(10):
                f.write(f'### {sub_outline[i][k]}\n')
                f.write(f'{sections_content[i * 10 + k]}\n')
            i += 1


def generate_short_post(title):
    with open(f'./{folder}/outline.txt') as f: 
        content = f.read()
    
    response = ask(f'write a blog post with the following outline "{content}"')
    response = response.replace('’', "'")

    with open(f'./{folder}/short_post.txt', 'w') as f: 
            f.write(response)

    print(response)
    

def generate_response(prompt, input, output):
    with open(f'./content/keyword.txt') as f: content = f.read()
    response = ask(f'{prompt}')
    with open(f'./{folder}/outline.txt', 'w') as f: f.write(response)
    print(response)


# generate_ideas()
# generate_title()
# generate_outline()
# generate_short_post('How to Spot the Signs of Bullying')

# generate_response('write a list of verbal bullying behaviors')

# generate_sections()
# generate_sections_ita()
# generate_post()

# generate_sub_outline()
# generate_sub_outline_clean()

# generate_section('verbal_bullying.txt')
# generate_sections()

generate_sections()
generate_post_list()
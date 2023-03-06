import openai
import os
import re
import prompts

from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageColor

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


keyword = f'workplace bullying behaviors'


def generate_titles():
    response = ask(f'write 10 title ideas for a blog post for the keyword "{keyword}". The keyword must be inside the title.')
    with open(f'./tmp/ideas.txt', 'w') as f: f.write(response)
    print(response)


def generate_h2_outline():
    with open(f'./content/title.txt') as f: content = f.read()
    response = ask(f'write a blog post outline for {content}')
    with open(f'./tmp/outline.txt', 'w') as f: f.write(response)
    print(response)

    
def generate_outline_folders():
    with open(f'./content/outline.txt') as f: lines = f.readlines()

    for f in os.listdir('./content/h2/'):
        os.remove(f'./content/h2/{f}')

    for f in os.listdir('./content/h3/'):
        os.remove(f'./content/h3/{f}')

    h2_curr = ''
    for line in lines:
        if line == '\n': pass
        elif line.startswith('- '):
            line = line.replace('- ', '')
            h2_curr = line.strip()
            with open(f'./content/h2/primary_outline.txt', 'a') as f: f.write(line)
        elif line.startswith('    '):
            line = line.replace('    ', '')
            with open(f'./content/h3/{h2_curr}.txt', 'a') as f: f.write(line)


def generate_paragraphs():
    with open('content/h2/primary_outline.txt') as f:
        primary_outline = f.readlines()

    # primary_outline = [x for x in os.listdir('./content/h3')]

    sections = []
    for h2 in primary_outline:
        tmp = []
        h2 = h2.strip()
        tmp.append(h2)
        with open(f'content/h3/{h2}.txt') as f:
            lines = f.readlines()
        for line in lines:
            tmp.append(line.strip())
        sections.append(tmp)


    for f in os.listdir('./content/p/'):
        os.remove(f'./content/p/{f}')

    i = 0
    for section in sections:
        for k, title in enumerate(section):
            if k == 0: header = 'h2'
            else: header = 'h3'
            print()
            print()
            print()
            print(f'*** {title} ***')
            response = ask(f'''
                write me a paragraph for a blog post about {title}
                the context is {keyword}.
                make it relatable and have a supportive tone.
                do NOT add line breaks.
            ''')
            response = response.replace("’", "'")
            response = response.replace("“", '"').replace("”", '"')
            if i < 10: i_str = '0' + str(i)
            else: i_str = str(i) 
            title = title.replace(' ', '_')
            with open(f'./content/p/{i_str}. {header} {title}.txt', 'w') as f: f.write(response)
            print(response)
            i += 1


def generate_post():
    with open('export.html', 'w') as f: pass

    images = os.listdir('./images')

    for filename in os.listdir('content/p'):
        tmp = filename.split(' ')[1:]
        heading_type = tmp[0]
        heading_text = tmp[1].replace('_', ' ').split('.')[0]
        with open(f'content/p/{filename}') as f:
            paragraph = f.read()

        paragraph = paragraph.strip()
        paragraph_formatted = ''
        i = 0
        for c in paragraph:
            if c == ".":
                if i % 2 == 0: paragraph_formatted += '.\n'
                else: paragraph_formatted += c
                i += 1
            else:
                paragraph_formatted += c
        paragraphs = paragraph_formatted.split('\n')

        with open('export.html', 'a') as f:
            f.write(f'<{heading_type}>{heading_text}</{heading_type}>')
            if heading_type == 'h2':
                image = images.pop()
                keyword_formatted = keyword.strip().replace(' ', '-')
                f.write(f'<img alt="{heading_text}" title="{heading_text}" src="./images/{keyword_formatted}/{image}" />')
            for p in paragraphs:
                f.write(f'<p>{p.lstrip()}</p>')
        
                print(p.lstrip())
        # break


def generate_dict():
    article = {}

    with open(f'./content/title.txt') as f: content = f.read()
    article['h2'] = content

    with open(f'./content/outline.txt') as f: lines = f.readlines()
    h2 = []
    for line in lines:
        if line == '\n': pass
        elif line.startswith('- '):
            line = line.replace('- ', '').replace('\n', '')
            h2.append({'h2': line})
    article['sections'] = h2
    
    print(article)


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

        break


def generate_sections_synonyms():
    sections = [ x for x in os.listdir('./content/sections/')]

    i = 0
    for item in sections:
        with open(f'./content/sections/{item}') as f: content = f.read()

        response = ask(f"rewrite this paragraph by using some synonyms [{content}]")
        with open(f'./content/sections_synonyms/{item}', 'w') as f: f.write(response)
        i += 1
        print(response)

        break


def generate_sections_formatted():
    sections = [ x for x in os.listdir('./content/sections/')]

    for item in sections:
        with open(f'./content/sections/{item}') as f: content = f.read()

        content = content.replace('\n', '')
        sentences = content.split('.')[:-1]
        sentences = [f'{x}.' for x in sentences]

        first_sentence = f'{sentences[0]}\n'
        last_sentence = f'{sentences[-1]}\n'
        sentences = sentences[1:-1]
        
        formatted_senteces = []
        formatted_senteces.append(first_sentence)

        linebreak_index = len(sentences)//2
        print(linebreak_index)
        for i, sentence in enumerate(sentences):
            print(i)
            if i % linebreak_index-1 == 0 and i != 0:
                formatted_senteces.append(f'{sentence}\n')
            else:
                    formatted_senteces.append(sentence)

        formatted_senteces.append(f'{last_sentence}')

        with open(f'./content/sections_formatted/{item}', 'w') as f: pass
        to_strip = False
        for sentence in formatted_senteces:
            if to_strip:
                sentence = sentence.lstrip()
            with open(f'./content/sections_formatted/{item}', 'a') as f:
                f.write(sentence)
            if '\n' in sentence:
                to_strip = True 
            else:
                to_strip = False

        # print(first_sentence)
        for sentence in formatted_senteces:
            print(sentence)
        print(formatted_senteces)

        # break


def generate_sections_ita():
    for section in os.listdir(f'./{folder}/sections/'):
        with open(f'./{folder}/sections/{section}') as f: 
            content = f.read()

        response = ask(f"translate in italian: {content}")
        with open(f'./{folder}/sections_ita/{section}', 'w') as f: 
            f.write(response)
        print(response)


def generate_post_list():
    with open(f'./content/title.txt') as f: 
        title = f.read() 

    with open(f'./content/main_outline.txt') as f: 
        outline = f.readlines()
    
    sub_outline_filenames = [x for x in os.listdir('./content/sub_outline/')]
    # sub_outline = [x.replace("_", ' ')[3:].title() for x in sub_outline_filenames]
    sub_outline = []
    for sub_outline_filename in sub_outline_filenames:
        with open(f'./content/sub_outline/{sub_outline_filename}') as f: 
            sub_outline.append(f.readlines()) 

    sections_filenames = [x for x in os.listdir('./content/sections_formatted/')]
    
    sections_content = []
    for section_filename in sections_filenames:
        with open(f'./content/sections_formatted/{section_filename}') as f: 
            sections_content.append(f.readlines())


    print(title)
    print(outline)
    print(sub_outline)
    print(sections_filenames)

    # for section_content in sections_content:
    #     print(section_content)


    with open('./content/keyword.txt') as f:
        keyword = f.read()
    keyword_filename = keyword.replace(' ', '-')

    with open('./content/intro.txt') as f:
        lines = f.readlines()
    intro = []
    for line in lines:
        if line == '\n':
            pass
        else:
            intro.append(f'<p>{line}</p>')
    
    
    with open('./content/outro.txt') as f:
        lines = f.readlines()
    outro = []
    for line in lines:
        if line == '\n':
            pass
        else:
            outro.append(f'<p>{line}</p>')

    with open('./content/final.html', 'w') as f:
        # H1
        f.write(f'<h1>{title}</h1>')

        # FEATURED IMAGE
        f.write(f'<p><img alt="{keyword}" title="{keyword}" src="./images/{keyword_filename}/{keyword_filename}.jpg" /></p>')
        
        # INTRO
        f.write(''.join(intro))

        # TABLE OF CONTENTS
        f.write(f'<div class="toc">')
        f.write(f'<p><strong>Table of Contents</strong></p>')
        f.write(f'<ol>')
        for i, line in enumerate(outline):
            f.write(f'<li><a href="#{i}">{line}</a></li>')
        f.write(f'<li><a href="#conclusion">Conclusion</a></li>')
        f.write(f'</ol>')
        f.write(f'</div>')

        i = 0
        for h2 in outline:
            f.write(f'<h2 id="{i}">{h2}</h2>')
            f.write(f'<img alt="{h2}" title="{h2}" src="./images/{keyword_filename}/{i}.jpg" />')
            for k in range(10):
                f.write(f'<h3>{i * 10 + k + 1}. {sub_outline[i][k]}</h3>')
                for line in sections_content[i * 10 + k]:
                    f.write(f'<p>{line}</p>')
            i += 1

        # OUTRO
        f.write(f'<h2 id="conclusion">Conclusion</h2>')
        f.write(''.join(outro))
        
    
    # with open('./content/final.md', 'w') as f:
    #     # H1
    #     f.write(f'# {title}\n')

    #     # TABLE OF CONTENTS
    #     # f.write(f'*Table of Contents*')
    #     # for i, line in enumerate(outline):
    #     #     f.write(f'<a href="#{i+1}">{i+1}. {line}</a></br>')

    #     i = 0
    #     for h2 in outline:
    #         f.write(f'## {h2}\n')
    #         for k in range(10):
    #             f.write(f'### {i * 10 + k + 1}. {sub_outline[i][k]}\n')
    #             for line in sections_content[i * 10 + k]:
    #                 f.write(f'{line}')
    #         i += 1


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


def generate_images_ref():
    filename = 'yosi-prihantoro-gXUEQEtpjMs-unsplash.jpg'
    # image.show()

    # RESIZE IMAGE
    # newsize = (300, 300)
    # img_resized = image.resize(newsize)
    # img_resized.save('./content/images/resized.jpg')
    # img_resized.show()

    # IMAGE INFO
    # print(image.size)
    # print(image.filename)
    # print(image.format)
    # print(image.format_description)

    # NEW
    # img = Image.new('RGBA', (1000,600))

    # ROTATE
    # image_rotate = image.rotate(60, expand=True, fillcolor=ImageColor.getcolor('red', 'RGB'))
    # image_rotate.show()

    # CROP
    # image_crop = image.crop((0, 0, 1000, 1000))
    # image_crop.show()

    # FLIP
    # image_horizontal = image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    # image_horizontal.show()

    # MAIN IMAGE
    # image = Image.open(f'./images/{filename}')
    # image.thumbnail((1930, 1090))
    # w, h = image.size
    # image = image.crop((w//2-1920//2, h//2-1080//2, w//2+1920//2, h//2+1080//2))
    # print(image.size)
    # image.save(f'./content/images/{filename}')

    # THUMBNAIL 800x600
    image = Image.open(f'./images/{filename}')
    w, h = image.size
    size_w, size_h = 800, 600
    
    if w < h: image = image.resize((size_w, int(h * size_w/w)))
    else: image = image.resize((int(w * size_h/h), size_h))
    
    w, h = image.size
    image = image.crop((w//2-size_w//2, h//2-size_h//2, w//2+size_w//2, h//2+size_h//2))
    print(image.size)

    export_name = filename.replace('.', '-800x600.')
    image.save(f'./content/images/{export_name}')

    # THUMBNAIL 1000x1500
    image = Image.open(f'./images/{filename}')
    w, h = image.size
    size_w, size_h = 1000, 1500
    
    if w < h: image = image.resize((size_w, int(h * size_w/w)))
    else: image = image.resize((int(w * size_h/h), size_h))
    
    w, h = image.size
    image = image.crop((w//2-size_w//2, h//2-size_h//2, w//2+size_w//2, h//2+size_h//2))
    print(image.size)

    export_name = filename.replace('.', '-1000x1500.')
    image.save(f'./content/images/{export_name}')

    # BLACK AND WHITE
    image = Image.open(f'./images/{filename}')
    image = image.convert("L")
    export_name = filename.replace('.', '-BW.')
    image.save(f'./content/images/{export_name}')
    print(image.size)


def image_resize_crop(image, new_w, new_h):
    w, h = image.size
    
    if w < h: image = image.resize((new_w, int(h * new_w/w)))
    else: image = image.resize((int(w * new_h/h), new_h))
    
    w, h = image.size
    image = image.crop((w//2-new_w//2, h//2-new_h//2, w//2+new_w//2, h//2+new_h//2))
    
    return image


def generate_image(filename, new_w, new_h):
    image = Image.open(f'./images/original/{filename}')

    folder_path = f'./images/{new_w}x{new_h}/'
    if not os.path.exists(folder_path): os.makedirs(folder_path)

    image = image_resize_crop(image, new_w, new_h)

    export_name = filename.replace('.', f'-{new_w}x{new_h}.')
    image.save(f'{folder_path}/{export_name}')


def generate_images():
    for filename in os.listdir('images/original/'):

        # THUMBNAIL 800x600
        generate_image(filename, 800, 600)
        
        # THUMBNAIL 1000x1500
        generate_image(filename, 1000, 1500)

        # # BLACK AND WHITE
        # image = Image.open(f'./images/{filename}')
        # image = image.convert("L")
        # export_name = filename.replace('.', '-BW.')
        # image.save(f'./content/images/{export_name}')
        # print(image.size)


def create_pin():
    img = Image.open('images/1000x1500/anthony-tran-i-ePv9Dxg7U-unsplash-1000x1500.jpg')

    font_size = 96

    text = '101 Signs You Are Being Bullied (2023)'.upper()
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('./fonts/Helvetica-Bold.ttf', font_size)
    # draw.text((28, 36), text, font=font, fill=(255, 255, 255))

    img_w, _ = img.size
    
    lines = []
    line = ''
    for word in text.split():
        word_w, _ = draw.textsize(word, font=font)
        line_w, _ = draw.textsize(line, font=font)
        if line_w + word_w < img_w:
            line += word + ' '
        else:
            lines.append(line.strip())
            line = word + ' '
    lines.append(line.strip())
    print(lines)

    _, line_h = draw.textsize(text, font=font)
    n_lines = len(lines)
    line_spacing = 1.2
    center_v = 1500//2

    draw.rectangle((
        (0, center_v - line_h//2), 
        (1000, center_v + line_h//2 + line_h * 2)
        ), fill="black")
    
    w, _ = draw.textsize(lines[0], font=font)
    draw.text((
        1000//2 - w//2, 
        center_v - line_h//2
        ), lines[0], (255, 255, 255), font=font)
       
    w, _ = draw.textsize(lines[1], font=font) 
    draw.text((
        1000//2 - w//2, 
        center_v - line_h//2 + line_h
        ), lines[1], (255, 255, 255), font=font)
       
    w, _ = draw.textsize(lines[2], font=font) 
    draw.text((
        1000//2 - w//2, 
        center_v - line_h//2 + line_h * 2
        ), lines[2], (255, 255, 255), font=font)

    # draw.rectangle((
    #     (0, 1500//2 - h//2 - int((len(lines) / 2) * h)), 
    #     (1000, 1500//2 - h//2 + int((len(lines) / 2) * h))
    #     ), fill="black")

    # for i, line in enumerate(lines):
    #     w, _ = draw.textsize(line, font=font)
    #     draw.text((
    #         1000//2 - w//2, 
    #         1500//2 - h//2 + i * font_size * 1.2 - int((len(lines) / 2) * h)
    #         ), line, (255, 255, 255), font=font)
        
    img.show()
    # img.save("car2.png")

create_pin()


# generate_images()


# generate_titles()
# generate_h2_outline()
# generate_dict()
# generate_outline_folders()
# generate_paragraphs()
# generate_post()


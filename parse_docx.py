from docx import Document
document = Document('bestiary.docx')
monsters_names_to_text = {}
exceptions = ('Действия', 'Легендарные действия')
current_paragraph = None
current_paragraph_style = 'Normal'
previous_paragraph_style = 'Normal'
current_text = ''
current_monster_name = ''

for paragraph in document.paragraphs:
    paragraph_style = paragraph.paragraph_format.element.xpath('w:pPr/w:shd')
    if paragraph_style and paragraph_style[0].values()[2] == 'DDD9C3':  # Stats block background
        current_paragraph_style = 'Stats'
        if previous_paragraph_style == 'Normal' and current_text.strip():  # Switching to stats block, need to print all we collected before
            monsters_names_to_text[current_monster_name] = current_text
            current_text = ''

        continue  # do not process stats block

    else: # White background or any other colors
        current_paragraph_style = 'Normal'

    # if paragraph.style.name == 'Heading 1':
    #     if current_text.strip():
    #         monsters_names_to_text[current_monster_name] = current_text
    #         current_text = ''

    if paragraph.style.name in ('Heading 1', 'Заголовок2Подч') and current_paragraph_style == 'Normal':
        current_monster_name = paragraph.text.strip()
        current_text += '<h>%s</h>' % current_monster_name
    else:
        if paragraph.text.strip():
            current_text += '\n<p>'

        for run in paragraph.runs:
            text = run.text
            if run.bold:
                text = '<b>%s</b>' % text

            if not text.strip():
                continue

            current_text += text
        if paragraph.text.strip():
            current_text += '</p>'

for monster_name in monsters_names_to_text.keys():
    print(monsters_names_to_text[monster_name])
    print('\n\n\n')

            # paragraph_color = paragraph.paragraph_format.element.xpath('w:pPr/w:shd')[0].values()
            # print(paragraph_color)
            # for run in paragraph.runs:
            #     print(run.text)

                # print(run.font.color.element.xpath())

    # if paragraph.style.name != 'Normal':
    #     print('%s: %s' % (paragraph.style.name, paragraph.text))
    # else:
    #     for run in paragraph.runs:
    #         if not run.text.strip():
    #             continue
    #         if run.bold:
    #             print('<b>%s</b>' % run.text)
    #         else:
    #             print('"%s"' % run.text)
    # print('\n\n')

from docx import Document
document = Document('bestiary.docx')
monsters_names_to_text = {}
for paragraph in document.paragraphs:
    if paragraph.style.name in ('Heading 1', ):
        text = paragraph.text.strip()
        if len(text) > 2:
            print('"%s"' % text)
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

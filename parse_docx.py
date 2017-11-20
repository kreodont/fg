from docx import Document
document = Document('bestiary.docx')
for paragraph in document.paragraphs[:22]:
    if paragraph.style.name != 'Normal':
        print('%s: %s' % (paragraph.style.name, paragraph.text))
    else:
        for run in paragraph.runs:
            if not run.text.strip():
                continue
            if run.bold:
                print('<b>%s</b>' % run.text)
            else:
                print('"%s"' % run.text)
    print('\n\n')

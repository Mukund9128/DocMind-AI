import fitz
from docx import Document as DocxDocument

def extract(path,ext):
    pages=[]
    if ext=='pdf':
        doc=fitz.open(path)
        for i,p in enumerate(doc): pages.append((i+1,p.get_text('text').strip()))
    else:
        d=DocxDocument(path); text='\n'.join(p.text for p in d.paragraphs).strip(); pages=[(1,text)]
    pages=[p for p in pages if p[1]]
    if not pages: raise ValueError('Document contains no extractable text')
    return pages

def chunks(pages,size=900,overlap=150):
    out=[]; idx=0
    for page,text in pages:
        text=' '.join(text.split()); start=0
        while start<len(text):
            part=text[start:start+size]; out.append({'page':page,'index':idx,'content':part}); idx+=1
            if start+size>=len(text): break
            start += size-overlap
    return out

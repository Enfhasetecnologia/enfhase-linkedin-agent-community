"""Enfhase native helpers. Original stdlib-only implementation, no network or arbitrary file input."""
import json
import math
import re
import statistics
import sys
import tempfile
import textwrap
import unicodedata
import uuid
from pathlib import Path

VERSION = '0.4.2'
OPERATIONS = frozenset({'clean_text', 'style_report', 'profile_score', 'audit_posts', 'carousel_pdf', 'review_draft'})
RUBRIC = {'clareza':15, 'publico':10, 'proposta_valor':20, 'evidencias':20,
          'coerencia':10, 'legibilidade':10, 'experiencia':10, 'proximo_passo':5}
SECRET = re.compile(r'(?i)(?:senha|password|api[_ -]?key|token|authorization)\s*[:=]\s*\S+|\b(?:ghp_|github_pat_|sk-)[A-Za-z0-9_-]{12,}|-----BEGIN [A-Z ]*PRIVATE KEY-----|\b\d{3}\.\d{3}\.\d{3}-\d{2}\b|\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b')
LINK = re.compile(r'(?i)(https?://|ftp://|file:|data:|www\.|<[^>]*>|!\[|\x1b)')
PUNCT = str.maketrans({'\u2014':',','\u2013':'-','\u2018':"'",'\u2019':"'",'\u201c':'"','\u201d':'"','\u2026':'...'})

class Rejected(ValueError):
    pass

def validate_tree(value, depth=0):
    if depth > 12:
        raise Rejected('input_depth')
    if isinstance(value, str):
        normalized=''.join(c for c in unicodedata.normalize('NFKC',value) if unicodedata.category(c)!='Cf')
        if len(value) > 12000 or SECRET.search(normalized) or LINK.search(normalized):
            raise Rejected('sensitive_or_active_content')
        if any(ord(c) < 32 and c not in '\n\t\r' for c in value):
            raise Rejected('control_character')
    elif type(value) is dict:
        if len(value) > 100: raise Rejected('too_many_fields')
        for key,item in value.items():
            if type(key) is not str: raise Rejected('invalid_key')
            validate_tree(key,depth+1);validate_tree(item,depth+1)
    elif type(value) is list:
        if len(value)>100: raise Rejected('too_many_items')
        for item in value:validate_tree(item,depth+1)
    elif value is not None and type(value) not in (int,float,bool):
        raise Rejected('invalid_type')
    elif type(value) in (int,float) and (not math.isfinite(value) or abs(value)>1e12):
        raise Rejected('invalid_number')

def schema(data, required, optional=()):
    if type(data) is not dict or set(data) - set(required) - set(optional) or not set(required) <= set(data):
        raise Rejected('invalid_schema')

def text(value, maximum=12000):
    if type(value) is not str or not value.strip() or len(value)>maximum:
        raise Rejected('invalid_text')
    return value

def clean(value):
    original=text(value)
    invisible=sum(unicodedata.category(c)=='Cf' for c in original)
    out=''.join(c for c in original if unicodedata.category(c)!='Cf')
    out=out.translate(PUNCT)
    out=''.join(' ' if c.isspace() and c not in '\n\r\t' else c for c in out)
    return {'text':out,'characters':len(out),'changed':out!=original,'removed_format_characters':invisible,
            'note':'Limpeza tipográfica; revisar nomes, emojis e significado. Não detecta autoria por IA.'}

def style(value):
    value=text(value)
    sentences=[s.strip() for s in re.split(r'[.!?]+(?:\s|$)',value) if s.strip()]
    lengths=[len(re.findall(r'\b\w+\b',s)) for s in sentences]
    terms=['vale destacar','em resumo','sinergia','disruptivo','no mundo atual','potencializar']
    lower=value.casefold()
    return {'words':len(re.findall(r'\b\w+\b',value)), 'sentences':len(sentences),
            'long_sentences':sum(n>30 for n in lengths),
            'average_sentence_words':round(statistics.mean(lengths),2) if lengths else 0,
            'format_characters':sum(unicodedata.category(c)=='Cf' for c in value),
            'generic_expressions':{term:lower.count(term) for term in terms if term in lower},
            'note':'Indicadores editoriais heurísticos; não são detector de IA nem previsão de engajamento.'}

def review(data):
    """Reject known editorial hazards; never attest semantic truth or source reliability."""
    schema(data, {'text', 'source_texts'})
    draft=text(data['text'])
    sources=data['source_texts']
    if type(sources) is not list or len(sources)>20 or any(type(s) is not str for s in sources):
        raise Rejected('invalid_sources')
    normalize=lambda s: ''.join(c for c in unicodedata.normalize('NFKC',s).casefold() if unicodedata.category(c)!='Cf')
    draft=normalize(draft)
    findings=set()
    absolute=re.compile(r'\b(?:garant(?:e|em|ir|indo)|elimin(?:a|am|ar)|assegur(?:a|am|ar)|imped(?:e|em|ir)|blind(?:a|am|ar)|protege(?:m|r)?)\b')
    negated=lambda prefix: bool(re.search(r'\b(?:não|nunca|jamais)\s+(?:(?:é|são|pode|podem|podemos|deve|devem|necessariamente|se)\s+)?$',prefix))
    for clause in re.split(r'[.!?;\n,]+',draft):
        for match in absolute.finditer(clause):
            if not negated(clause[:match.start()]):findings.add('categorical_outcome')
        for match in re.finditer(r'\b(?:100\s*%\s*(?:segur[oa]s?|de\s+segurança)|segurança\s+(?:absoluta|(?:de\s+)?100\s*%)|risco\s+zero|livre\s+de\s+falhas)\b',clause):
            if not negated(clause[:match.start()]):findings.add('categorical_outcome')
        # Known observed failure: an unverifiable contact was called legitimate.
        for match in re.finditer(r'\blegítim[oa]s?\b',clause):
            if not negated(clause[:match.start()]):findings.add('unverified_legitimacy')
        if 'utm' in clause and re.search(r'\bseguidor|fora da base',clause):
            for match in re.finditer(r'\b(?:comprova\w*|prova\w*|identifica\w*)\b',clause):
                if not negated(clause[:match.start()]):findings.add('unsupported_audience_attribution')
    # Deliberately bounded prose check, not an algebra or semantic validator.
    if re.search(r'%|\bpercentual\b|\bpor cento\b',draft) and re.search(
        r'\btaxa(?:\s+(?:de\s+intera[çc][ãa]o|percentual))?\s*=\s*intera[çc][õo]es\s*(?:/|÷)\s*impress[õo]es\b(?!\s*[×*]\s*100\b)',draft):
        findings.add('percentage_formula_missing_factor')
    numbers=lambda s:set(re.findall(r'(?<![\w])\d+(?:[.,]\d+)*\s*%?',re.sub(r'(?m)^\s*\d+[.)]\s+', '',s)))
    def numeric_token(value):
        value=re.sub(r'\s+','',value)
        unit='%' if value.endswith('%') else ''
        raw=value[:-1] if unit else value
        parts=re.split(r'[.,]',raw)
        # A three-digit suffix may be a thousands group: do not infer its meaning.
        if len(parts)==2 and len(parts[1])!=3:
            fraction=parts[1].rstrip('0')
            return parts[0]+('.'+fraction if fraction else '')+unit
        return value
    known={numeric_token(n) for source in sources for n in numbers(normalize(source))}
    if any(numeric_token(n) not in known for n in numbers(draft)):
        findings.add('number_without_source')
    return {'passed_checks':not findings,'findings':sorted(findings),'source_count':len(sources),
            'note':'Gate editorial heurístico. Não verifica verdade, equivalência semântica, qualidade ou confiabilidade das fontes. Sem aprovação de publicação.'}

def profile(data):
    schema(data,{'observations'})
    obs=data['observations']
    if type(obs) is not dict or set(obs)!=set(RUBRIC):raise Rejected('invalid_rubric')
    score=0;assessed=0;items=[]
    for criterion,weight in RUBRIC.items():
        row=obs[criterion];schema(row,{'rating','evidence'})
        rating=row['rating'];evidence=row['evidence']
        if type(evidence) is not str:raise Rejected('invalid_evidence')
        if rating is not None and (type(rating) is not int or not 0<=rating<=4 or not evidence.strip()):
            raise Rejected('invalid_rating')
        points=None if rating is None else weight*rating/4
        if points is not None:score+=points;assessed+=weight
        items.append({'criterion':criterion,'weight':weight,'rating':rating,'points':points,'evidence':evidence})
    return {'score':score,'assessed_maximum':assessed,'total_possible':100,'complete':assessed==100,
            'criteria':items,'note':'Notas são avaliações editoriais com evidência; soma determinística, sem validação pelo LinkedIn.'}

def nonnegative(value):
    if type(value) not in (int,float) or not math.isfinite(value) or value<0 or value>1e12:
        raise Rejected('invalid_metric')
    return value

def audit(data):
    schema(data,{'posts'})
    if type(data['posts']) is not list or not 1<=len(data['posts'])<=100:raise Rejected('invalid_posts')
    result=[];seen=set()
    for row in data['posts']:
        schema(row,{'id','impressions','interactions'},{'followers'})
        label=text(row['id'],100)
        if label in seen:raise Rejected('duplicate_post_id')
        seen.add(label)
        impressions=nonnegative(row['impressions']);interactions=nonnegative(row['interactions'])
        followers=row.get('followers')
        if followers is not None:followers=nonnegative(followers)
        result.append({'id':label,'engagement_rate_pct':round(100*interactions/impressions,4) if impressions else None,
                       'reach_multiple':round(impressions/followers,4) if followers else None,
                       'impressions':impressions,'interactions':interactions})
    result.sort(key=lambda row:(row['engagement_rate_pct'] is not None,row['engagement_rate_pct'] or 0),reverse=True)
    return {'posts':result,'formulas':{'engagement_rate_pct':'100 * interactions / impressions',
            'reach_multiple':'impressions / followers_at_publication'},
            'note':'Métricas calculadas somente com dados informados; nulo indica denominador ausente ou zero. Não acessa analytics do LinkedIn. Impressões não são pessoas únicas: o múltiplo não comprova alcance único, alcance fora da base ou distribuição a não seguidores.'}

def pdf_literal(value):
    value=value.translate(PUNCT)
    try:raw=value.encode('cp1252')
    except UnicodeEncodeError:raise Rejected('unsupported_pdf_characters') from None
    return raw.replace(b'\\',b'\\\\').replace(b'(',b'\\(').replace(b')',b'\\)')

def make_pdf(data):
    schema(data,{'slides'})
    slides=data['slides']
    if type(slides) is not list or not 1<=len(slides)<=12:raise Rejected('invalid_slides')
    streams=[]
    for index,slide in enumerate(slides,1):
        schema(slide,{'title','body'})
        title=text(slide['title'],100);body=text(slide['body'],1000)
        titles=textwrap.wrap(title,40);lines=[]
        for paragraph in body.splitlines():
            lines.extend(textwrap.wrap(paragraph,65) or [''])
        if len(titles)>2 or len(lines)>13:raise Rejected('slide_text_overflow')
        stream=b'q 0.035 0.075 0.14 rg 0 0 960 540 re f Q\n'
        stream+=b'q 0.2 0.85 0.65 rg 64 468 72 5 re f Q\n'
        for n,line in enumerate(titles):
            stream+=b'BT /F2 30 Tf 1 1 1 rg 64 '+str(425-n*36).encode()+b' Td ('+pdf_literal(line)+b') Tj ET\n'
        for n,line in enumerate(lines):
            stream+=b'BT /F1 20 Tf 0.88 0.92 0.96 rg 64 '+str(330-n*22).encode()+b' Td ('+pdf_literal(line)+b') Tj ET\n'
        footer=f'Rascunho para revisao | {index}/{len(slides)}'
        stream+=b'BT /F1 12 Tf 0.55 0.68 0.75 rg 64 28 Td ('+pdf_literal(footer)+b') Tj ET\n'
        streams.append(stream)
    objects=[b'<< /Type /Catalog /Pages 2 0 R >>',b'',
             b'<< /Type /Font /Subtype /Type1 /BaseFont /Courier /Encoding /WinAnsiEncoding >>',
             b'<< /Type /Font /Subtype /Type1 /BaseFont /Courier-Bold /Encoding /WinAnsiEncoding >>']
    kids=[]
    for stream in streams:
        page_id=len(objects)+1;content_id=page_id+1;kids.append(f'{page_id} 0 R')
        objects.append(f'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 960 540] /Resources << /Font << /F1 3 0 R /F2 4 0 R >> >> /Contents {content_id} 0 R >>'.encode())
        objects.append(b'<< /Length '+str(len(stream)).encode()+b' >>\nstream\n'+stream+b'endstream')
    objects[1]=('<< /Type /Pages /Count '+str(len(streams))+' /Kids ['+' '.join(kids)+'] >>').encode()
    output=bytearray(b'%PDF-1.4\n%\xe2\xe3\xcf\xd3\n');offsets=[0]
    for n,obj in enumerate(objects,1):
        offsets.append(len(output));output.extend(f'{n} 0 obj\n'.encode()+obj+b'\nendobj\n')
    xref=len(output);output.extend(f'xref\n0 {len(objects)+1}\n0000000000 65535 f \n'.encode())
    for offset in offsets[1:]:output.extend(f'{offset:010d} 00000 n \n'.encode())
    output.extend(f'trailer\n<< /Size {len(objects)+1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n'.encode())
    # Only a newly-created private temporary directory is writable by this helper.
    directory=Path(tempfile.mkdtemp(prefix='enfhase-carousel-'))
    target=directory/'carousel.pdf';target.write_bytes(output)
    return {'pdf_path':str(target),'pages':len(streams),'note':'PDF estático sem links, JavaScript, anexos ou publicação.'}

def dispatch(operation,data):
    if operation not in OPERATIONS:raise Rejected('operation_denied')
    validate_tree(data)
    if operation in {'clean_text','style_report'}:
        schema(data,{'text'});result=clean(data['text']) if operation=='clean_text' else style(data['text'])
    else:
        result={'profile_score':profile,'audit_posts':audit,'carousel_pdf':make_pdf,'review_draft':review}[operation](data)
    return {'result':result,'receipt':{'id':str(uuid.uuid4()),'operation':operation,'version':VERSION,
            'network_used':False,'persistence':'No durable audit journal; keep this receipt if needed.'}}

def unique_object(pairs):
    result={}
    for key,value in pairs:
        if key in result:raise Rejected('duplicate_json_key')
        result[key]=value
    return result

def main():
    try:
        if len(sys.argv)!=2 or sys.argv[1] not in OPERATIONS:raise Rejected('operation_denied')
        raw=sys.stdin.buffer.read(65537)
        if len(raw)>65536:raise Rejected('input_too_large')
        data=json.loads(raw,object_pairs_hook=unique_object,parse_constant=lambda _:(_ for _ in ()).throw(Rejected('invalid_number')))
        print(json.dumps(dispatch(sys.argv[1],data),ensure_ascii=True,allow_nan=False))
    except Exception as exc:
        error=str(exc) if isinstance(exc,Rejected) else 'invalid_request'
        print(json.dumps({'error':error}));raise SystemExit(2)

if __name__=='__main__':main()

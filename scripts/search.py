"""Dependency-free intent search, mirrored by web/search.js using search.json."""
import re
import unicodedata


def normalize(value):
    return unicodedata.normalize('NFKC', str(value)).lower().strip()


def contains(text, term):
    if len(term)==1:return term in text.split()
    if re.fullmatch(r'[a-z0-9][a-z0-9 ._-]*', term):
        return re.search(r'(?<![a-z0-9])'+re.escape(term)+r'(?![a-z0-9])', text) is not None
    return term in text


def occurrences(text, term):
    """Locate literal terms without consuming adjacent word boundaries."""
    if not term:return
    ascii_term=bool(re.fullmatch(r'[a-z0-9][a-z0-9 ._-]*',term))
    start=0
    while True:
        start=text.find(term,start)
        if start<0:return
        end=start+len(term)
        before=text[start-1] if start else ''
        after=text[end] if end<len(text) else ''
        if len(term)==1:
            valid=(not before or before.isspace()) and (not after or after.isspace())
        else:
            valid=not ascii_term or not (re.fullmatch(r'[a-z0-9]',before) or re.fullmatch(r'[a-z0-9]',after))
        if valid:yield start,end
        start+=1


def fields(asset, config):
    guide=asset.get('guidance',{})
    composition=asset.get('composition',{})
    words=[]
    for value in composition.values():
        words.extend([str(value), *config['composition_terms'].get(str(value),[])])
    return [(normalize(text),weight) for text,weight in [
        (asset['id'].split('/',1)[1],8),(asset['title'],12),(' '.join(asset['keywords']),6),
        (asset.get('use_case',guide.get('use_case','')),3),
        (asset.get('message',guide.get('message','')),7),
        (' '.join(config['kind_terms'][asset['kind']]),8),(' '.join(words),2),(asset.get('category',''),3)]]


def prepare(assets, config):
    """Use the same public fields for the compact index and full gallery rows."""
    documents=[(asset,fields(asset,config)) for asset in assets]
    groups=[[normalize(term) for term in group] for group in config['groups']]
    groups.extend([[normalize(term) for term in group] for group in config['kind_terms'].values()])
    aliases={term for group in groups for term in group}
    vocabulary=set()
    for asset in assets:
        vocabulary.add(normalize(asset['title']))
        vocabulary.update(normalize(word) for word in asset['keywords'])
        vocabulary.update(normalize(word) for word in re.split(r'[-/]',asset['id']))
    vocabulary={word for word in vocabulary if len(word)>=2 and word not in aliases}
    return dict(documents=documents,groups=groups,vocabulary=sorted(vocabulary),config=config,matches={})


def query_terms(query, prepared):
    query=normalize(query)
    candidates=[]
    for group in [*prepared['groups'],*[[word] for word in prepared['vocabulary']]]:
        spans={span for word in group for span in occurrences(query,word)}
        if spans:candidates.append((group,spans))
    spans={span for _,matches in candidates for span in matches}
    # A compound phrase expresses one topic. Count its fragments only when they
    # also occur independently elsewhere in the sentence.
    uncovered={span for span in spans if not any(other!=span and other[0]<=span[0] and span[1]<=other[1] for other in spans)}
    groups=[group for group,matches in candidates if matches & uncovered]
    generic={normalize(term) for term in prepared['config']['generic_terms']}
    specific=[group for group in groups if not all(word in generic for word in group)]
    return specific or groups


def interleave(entries, kind_order):
    result=[]
    kinds=[*kind_order,*sorted({asset['kind'] for asset in entries}-set(kind_order))]
    queues={kind:sorted((asset for asset in entries if asset['kind']==kind),key=lambda asset:asset['id']) for kind in kinds}
    while any(queues.values()):
        for kind in kinds:
            if queues[kind]:result.append(queues[kind].pop(0))
    return result


def rank(prepared, query, filters=None):
    filters=filters or {};normalized=normalize(query);terms=query_terms(query,prepared);buckets={}
    # These weights depend on the prepared library, not on filters or query
    # wording. Reuse them as users refine searches and when auditing all titles.
    columns=[]
    for group in terms:
        key=tuple(group)
        if key not in prepared['matches']:
            prepared['matches'][key]=[max((weight for text,weight in document if any(contains(text,word) for word in group)),default=0) for _,document in prepared['documents']]
        columns.append(prepared['matches'][key])
    matched=[list(values) for values in zip(*columns)] if columns else [[] for _ in prepared['documents']]
    # Concrete topics distinguish an asset; goals such as improvement are shared
    # by many subjects. Measure rarity across the library, before optional filters.
    rarity=[1000//(20+sum(bool(matches[i]) for matches in matched)) for i in range(len(terms))]
    broad=set(prepared['config']['broad_terms']);specific=any(not any(word in broad for word in group) for group in terms)
    factors=[1 if specific and any(word in broad for word in group) else 3 for group in terms]
    # A broadly applicable goal should not gain a large rarity bonus merely
    # because its particular wording appears in few descriptions.
    rarity=[min(rare,10) if factor==1 else rare for rare,factor in zip(rarity,factors)]
    for (asset,_),matches in zip(prepared['documents'],matched):
        if any(asset.get(key)!=value for key,value in filters.items() if key in ('kind','format','category')):continue
        if 'transparent' in filters and asset.get('transparent') is not filters['transparent']:continue
        if 'themeable' in filters and asset['render']['theme'] is not filters['themeable']:continue
        exact_id=normalized==normalize(asset['id']);exact_title=normalized==normalize(asset['title'])
        partial_title=len(normalized)>=2 and normalized in normalize(asset['title'])
        if normalized and not exact_id and not exact_title and not partial_title and not any(matches):continue
        score=sum(weight*rare*factor for weight,rare,factor in zip(matches,rarity,factors))+(2000000 if exact_id else 1000000 if exact_title else 12 if partial_title else 0)
        buckets.setdefault(score,[]).append(asset)
    ranked=[]
    for score in sorted(buckets,reverse=True):ranked.extend(interleave(buckets[score],prepared['config']['kind_order']))
    return ranked,[group[0] for group in terms]

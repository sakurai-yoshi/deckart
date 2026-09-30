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
    return dict(documents=documents,groups=groups,vocabulary=sorted(vocabulary),config=config)


def query_terms(query, prepared):
    query=normalize(query)
    groups=[group for group in prepared['groups'] if any(contains(query,word) for word in group)]
    matched_aliases=[word for group in groups for word in group if contains(query,word)]
    words=[word for word in prepared['vocabulary'] if contains(query,word) and not any(word in alias for alias in matched_aliases)]
    # A longer registered phrase carries more intent than its repeated fragments.
    words=[word for word in words if not any(word!=other and word in other for other in words)]
    groups.extend([[word] for word in words])
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
    matched=[[max((weight for text,weight in document if any(contains(text,word) for word in group)),default=0) for group in terms] for _,document in prepared['documents']]
    # Concrete topics distinguish an asset; goals such as improvement are shared
    # by many subjects. Measure rarity across the library, before optional filters.
    rarity=[1000//(20+sum(bool(matches[i]) for matches in matched)) for i in range(len(terms))]
    broad=set(prepared['config']['broad_terms']);specific=any(not any(word in broad for word in group) for group in terms)
    factors=[1 if specific and any(word in broad for word in group) else 3 for group in terms]
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

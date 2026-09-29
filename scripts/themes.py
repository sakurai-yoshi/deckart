"""Role-based SVG themes: one geometry, a brand accent, fixed semantic signals."""
import re
import xml.etree.ElementTree as ET

SOURCE_ROLES = {
    '#153A6B':'ink', '#2864F0':'accent', '#79A7ED':'mid',
    '#E7F0FF':'pale', '#F3F7FD':'faint', '#607590':'muted',
    '#FFFFFF':'paper', '#C58930':'caution', '#FFF0D7':'caution_pale',
    '#137D66':'positive', '#B5473A':'negative', '#526272':'series_secondary',
}
DEFAULT_ACCENT='#2864F0'
NEUTRALS={'ink':'#153A6B','muted':'#607590','paper':'#FFFFFF'}
SIGNALS={'positive':'#137D66','negative':'#B5473A','caution':'#A46A16','caution_pale':'#FFF0D7'}
SVG_NS='http://www.w3.org/2000/svg'
ET.register_namespace('',SVG_NS)
COORDINATES={'d','points','transform','viewBox','x','y','x1','y1','x2','y2','cx','cy','r','rx','ry','width','height','stroke-width','stroke-dasharray'}
NUMBER=re.compile(r'[-+]?(?:\d*\.\d+|\d+)(?:[eE][-+]?\d+)?')


def canonical_geometry(root):
    """Keep subpixel precision while removing platform-specific libm tail digits."""
    def coordinate(match):
        value=f'{float(match.group()):.6f}'.rstrip('0').rstrip('.')
        return '0' if value=='-0' else value
    for element in root.iter():
        for name in COORDINATES & element.attrib.keys():
            element.set(name,NUMBER.sub(coordinate,element.get(name)))
    return root


def rgb(value):
    if not isinstance(value,str) or not re.fullmatch(r'#[0-9a-fA-F]{6}',value):
        raise ValueError('accent must be a six-digit hex color such as #005BAC')
    return tuple(int(value[i:i+2],16) for i in (1,3,5))


def hex_color(channels):
    return '#'+''.join(f'{min(255,max(0,int(c+.5))):02X}' for c in channels)


def mix(color,other,weight):
    return hex_color(a*(1-weight)+b*weight for a,b in zip(rgb(color),rgb(other)))


def luminance(color):
    channels=[v/255 for v in rgb(color)]
    linear=[v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in channels]
    return sum(v*w for v,w in zip(linear,(.2126,.7152,.0722)))


def contrast(a,b='#FFFFFF'):
    high,low=sorted((luminance(a),luminance(b)),reverse=True)
    return (high+.05)/(low+.05)


def resolve_theme(accent=DEFAULT_ACCENT,monochrome=False):
    requested=hex_color(rgb(accent))
    if monochrome:
        colors={'ink':'#202A35','accent':'#202A35','mid':'#929BA6','pale':'#E8EBEE',
                'faint':'#F5F6F7','muted':'#596370','paper':'#FFFFFF',
                'positive':'#202A35','negative':'#202A35','caution':'#202A35',
                'caution_pale':'#E8EBEE','series_secondary':'#63707F'}
        return {'mode':'monochrome','colors':colors,'adjustments':[]}
    effective=requested
    # Preserve hue; use the first darker tone that supports white marks at 4.5:1.
    for step in range(1,256):
        if contrast(effective)>=4.5:break
        effective=mix(requested,'#000000',step/255)
    # The blue source keeps its individually reviewed tonal values.
    tones=({'mid':'#79A7ED','pale':'#E7F0FF','faint':'#F3F7FD'} if requested==DEFAULT_ACCENT
           else {'mid':mix(effective,'#FFFFFF',.68),'pale':mix(effective,'#FFFFFF',.9),'faint':mix(effective,'#FFFFFF',.965)})
    secondary=NEUTRALS['ink'] if contrast(effective,NEUTRALS['ink'])>=1.6 else '#63707F'
    colors={**NEUTRALS,**SIGNALS,**tones,'accent':effective,'series_secondary':secondary}
    assert contrast(colors['ink'],colors['mid'])>=4.5
    adjustments=[] if requested==effective else [f'Accent adjusted from {requested} to {effective} for white-mark contrast.']
    return {'mode':'brand','requested_accent':requested,'colors':colors,'adjustments':adjustments}


def annotate_roles(svg):
    root=canonical_geometry(ET.fromstring(svg))
    for element in root.iter():
        for paint in ('fill','stroke'):
            value=element.get(paint,'').upper()
            if value in SOURCE_ROLES:element.set('data-'+paint+'-role',SOURCE_ROLES[value])
    return ET.tostring(root,encoding='unicode')+'\n'


def apply_theme(svg,theme):
    root=ET.fromstring(svg)
    for element in root.iter():
        for paint in ('fill','stroke'):
            role=element.get('data-'+paint+'-role')
            if role:element.set(paint,theme['colors'][role])
    return ET.tostring(root,encoding='unicode')+'\n'


def theme_contract():
    return {
        'schema_version':1,
        'default':resolve_theme(),
        'modes':['brand','monochrome'],
        'input':{'accent':'#RRGGBB','monochrome':False},
        'roles':{
            'ink':'輪郭・本文・強い対比。ブランド色に連動しない。',
            'accent':'注目箇所・主経路。ブランド色を基に白とのコントラストを確保する。',
            'mid':'副要素・比較対象。inkと読み分けられる明度を保つ。',
            'pale':'補助面・非選択領域。', 'faint':'背景の淡い面。',
            'muted':'補助線・補足。','paper':'白い紙面・抜き。',
            'positive':'増加・肯定。符号や形状も併用する。',
            'negative':'減少・否定。符号や形状も併用する。',
            'caution':'注意・例外。記号や経路も併用する。',
            'caution_pale':'注意を示す淡い補助面。',
            'series_secondary':'グラフの第2系列。強調色と区別できる濃さを選び、区切り線も併用する。',
        },
        'rules':['Geometry is authored once; themes change paint attributes only.',
                 'Brand color does not replace semantic signal colors.',
                 'Monochrome uses shape, position and signs to retain meaning.',
                 'Resolved colors are explicit SVG attributes; no CSS variables or external styles are required.',
                 'The export metadata records requested color, resolved colors and adjustments.'],
    }

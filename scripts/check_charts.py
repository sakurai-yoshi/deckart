#!/usr/bin/env python3
"""Compare the 12 chart examples' exported SVG geometry with catalog values."""
import json
import math
from pathlib import Path
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
BLUE, INK, MID = '#2864F0', '#153A6B', '#79A7ED'
POSITIVE, NEGATIVE = '#137D66', '#B5473A'
TOKEN = re.compile(r'[A-Za-z]|[-+]?(?:\d*\.\d+|\d+\.?\d*)(?:[eE][-+]?\d+)?')
ARITY = {'M': 2, 'L': 2, 'A': 7, 'Z': 0}


def close(actual, expected, context, tolerance=0.0001):
    assert abs(actual-expected) <= tolerance, f'{context}: {actual} != {expected}'


def point(actual, expected, context):
    for a, e in zip(actual, expected):
        close(a, e, context)


def commands(d):
    """Parse the absolute move, line and circular arc commands used by marks."""
    tokens = TOKEN.findall(d)
    result = []
    while tokens:
        command = tokens.pop(0)
        if command not in ARITY:
            return []
        count = ARITY[command]
        result.append((command, [float(v) for v in tokens[:count]]))
        tokens = tokens[count:]
    return result


def arc(start, args):
    """Recover a circular SVG arc's center and signed angular extent."""
    rx, ry, rotation, large, sweep, x, y = args
    close(rx, ry, 'Circular arc radii')
    close(rotation, 0, 'Arc rotation')
    dx, dy = (start[0]-x)/2, (start[1]-y)/2
    distance = dx*dx+dy*dy
    assert distance > 0 and distance <= rx*rx+0.0001, 'Invalid arc chord'
    sign = -1 if large == sweep else 1
    factor = sign*math.sqrt(max(0, rx*rx-distance)/distance)
    center = ((start[0]+x)/2+factor*dy, (start[1]+y)/2-factor*dx)
    first = math.atan2(start[1]-center[1], start[0]-center[0])
    last = math.atan2(y-center[1], x-center[0])
    extent = (last-first) % math.tau if sweep else -((first-last) % math.tau)
    return center, rx, first, extent, (x, y)


def annulus(element):
    c = commands(element.attrib['d'])
    assert [kind for kind, _ in c] == ['M', 'A', 'L', 'A', 'Z'], 'Annular mark path'
    outer = arc(c[0][1], c[1][1])
    inner = arc(c[2][1], c[3][1])
    point(inner[0], outer[0], 'Concentric inner and outer arcs')
    close(inner[3], -outer[3], 'Matching annular extents')
    assert 0 < inner[1] < outer[1], 'Inner radius must be smaller'
    for inner_point, outer_point in [(c[2][1], outer[4]), (inner[4], c[0][1])]:
        cross = ((inner_point[0]-outer[0][0])*(outer_point[1]-outer[0][1])
                 -(inner_point[1]-outer[0][1])*(outer_point[0]-outer[0][0]))
        close(cross, 0, 'Radial sector boundary', 0.001)
    return outer, inner


def polar(center, radius, angle):
    return center[0]+radius*math.cos(angle), center[1]+radius*math.sin(angle)


class Drawing:
    def __init__(self, element):
        self.elements = list(element)
        self.paths = self.tags('path')
        self.segments = [c for e in self.paths if len(c := commands(e.attrib['d'])) == 2
                         and [kind for kind, _ in c] == ['M', 'L']]

    def tags(self, tag):
        return [e for e in self.elements if e.tag.rsplit('}', 1)[-1] == tag]

    def bars(self):
        return [e for e in self.tags('rect') if float(e.attrib['width']) > 32
                and float(e.attrib['height']) > 32]

    def segment(self, start, end, context):
        assert any(all(abs(a-b) < 0.0001 for a, b in zip(c[0][1]+c[1][1], list(start)+list(end)))
                   for c in self.segments), context

    def axis(self, data, horizontal=False):
        p = data['plot']; x, y, w, h = (p[k] for k in ('x','y','width','height'))
        if horizontal:
            self.segment((x,y),(x,y+h),'Missing common zero axis')
            for tick in data['ticks']:
                tx = x+w*tick/data['domain'][1]
                self.segment((tx,y),(tx,y+h),'Horizontal tick geometry')
        else:
            self.segment((x,y+h),(x+w,y+h),'Missing common zero axis')
            for tick in data['ticks']:
                ty = y+h-h*tick/data['domain'][1]
                self.segment((x,ty),(x+w,ty),'Vertical tick geometry')


def bar_check(drawing, data, horizontal=False, grouped=False):
    drawing.axis(data, horizontal)
    p = data['plot']; maximum = data['domain'][1]
    bars = sorted(drawing.bars(), key=lambda e: float(e.attrib['y' if horizontal else 'x']))
    values = ([v for values in zip(*(s['values'] for s in data['series'])) for v in values]
              if grouped else data['series'][0]['values'])
    assert len(bars) == len(values), 'Bar count'
    thickness = float(bars[0].attrib['height' if horizontal else 'width'])
    for i, (e, value) in enumerate(zip(bars, values)):
        r = {k: float(e.attrib[k]) for k in ('x','y','width','height')}
        close(r['height' if horizontal else 'width'], thickness, 'Equal bar thickness')
        if horizontal:
            close(r['x'], p['x'], 'Horizontal zero origin')
            close(r['width'], p['width']*value/maximum, 'Horizontal value length')
        else:
            close(r['y']+r['height'], p['y']+p['height'], 'Vertical zero origin')
            close(r['height'], p['height']*value/maximum, 'Vertical value height')
        expected_color = (MID,BLUE)[i % 2] if grouped else BLUE
        assert e.attrib['fill'] == expected_color, 'Bar series order'


def line_check(drawing, data, slope=False):
    drawing.axis(data)
    p = data['plot']; maximum = data['domain'][1]
    if slope:
        paths = [e for e in drawing.paths if e.attrib.get('stroke-width') == '5']
        assert len(paths) == len(data['series']), 'Slope line count'
        x_positions = None
        for e, series, color in zip(paths, data['series'], (BLUE, INK, MID)):
            c = commands(e.attrib['d']); assert [k for k, _ in c] == ['M','L']
            pts = [v for _, v in c]
            current_x = [pt[0] for pt in pts]
            if x_positions is None: x_positions = current_x
            assert current_x == x_positions and current_x[0] < current_x[1], 'Aligned time positions'
            assert e.attrib['stroke'] == color, 'Slope series order'
            for (x,y), value in zip(pts, series['values']):
                close(y, p['y']+p['height']*(1-value/maximum), 'Slope value position')
                assert any(abs(float(q.attrib['cx'])-x)<0.0001 and abs(float(q.attrib['cy'])-y)<0.0001
                           and q.attrib['stroke']==color for q in drawing.tags('circle')), 'Slope endpoint marker'
    else:
        paths = [e for e in drawing.paths if e.attrib.get('stroke-width') == '6']
        assert len(paths) == 1, 'Line series count'
        pts = commands(paths[0].attrib['d'])
        values = data['series'][0]['values']
        assert [k for k, _ in pts] == ['M']+['L']*(len(values)-1), 'Straight line point count'
        circles = drawing.tags('circle'); assert len(circles) == len(values), 'Line marker count'
        for i, ((_, xy), value, marker) in enumerate(zip(pts,values,circles)):
            expected = (p['x']+p['width']*i/(len(values)-1), p['y']+p['height']*(1-value/maximum))
            point(xy, expected, 'Line data position')
            point((float(marker.attrib['cx']),float(marker.attrib['cy'])), expected, 'Line marker position')


def sector_check(drawing, data, donut=False):
    paths = [e for e in drawing.paths if 'A' in e.attrib['d']]
    values = data['series'][0]['values']; total = sum(values)
    close(total, data['total'], 'Part-to-whole total')
    common_center = None; common_radius = None
    start = math.radians(data['start_angle_degrees'])
    for value, color in zip(values,(BLUE,INK,MID)):
        pieces = []
        while paths and paths[0].attrib['fill']==color:
            pieces.append(paths.pop(0))
        assert pieces, 'Sector series order'
        expected_angle = math.tau*value/total
        angle = 0; area = 0
        for e in pieces:
            if donut:
                outer, inner = annulus(e)
                close(outer[1], data['outer_radius'], 'Donut outer radius')
                close(inner[1], data['inner_radius'], 'Donut inner radius')
                center, radius, _, extent, endpoint = outer
                first = commands(e.attrib['d'])[0][1]
                area += (radius**2-inner[1]**2)*extent/2
            else:
                c = commands(e.attrib['d']); assert [k for k, _ in c] == ['M','L','A','Z']
                center, radius, _, extent, endpoint = arc(c[1][1],c[2][1])
                point(c[0][1],center,'Pie wedge apex')
                first = c[1][1]
                area += radius**2*extent/2
            if common_center is None: common_center, common_radius = center, radius
            point(center, common_center, 'Common sector center')
            close(radius, common_radius, 'Common sector radius')
            assert extent > 0, 'Clockwise sector sweep'
            point(first,polar(center,radius,start+angle),'Contiguous sector start')
            angle += extent
            point(endpoint,polar(center,radius,start+angle),'Contiguous sector endpoint')
        close(angle,expected_angle,'Value-to-angle mapping')
        filled_radii = common_radius**2-(data['inner_radius']**2 if donut else 0)
        close(area,filled_radii*expected_angle/2,'Value-to-area mapping',.01)
        start += angle
    assert not paths, 'Unexpected extra sectors'
    close(start-math.radians(data['start_angle_degrees']),math.tau,'Complete circle')


def annular_run(elements, center, outer_radius, inner_radius, start, extent, context):
    """Validate contiguous pieces and their actual combined angle and filled area."""
    angle = 0; area = 0
    for element in elements:
        outer, inner = annulus(element)
        point(outer[0], center, context+' center')
        close(outer[1], outer_radius, context+' outer radius')
        close(inner[1], inner_radius, context+' inner radius')
        assert outer[3] > 0, context+' clockwise sweep'
        first = commands(element.attrib['d'])[0][1]
        point(first, polar(center, outer_radius, start+angle), context+' contiguous start')
        angle += outer[3]
        point(outer[4], polar(center, outer_radius, start+angle), context+' endpoint')
        area += (outer[1]**2-inner[1]**2)*outer[3]/2
    close(angle, extent, context+' total angle')
    close(area, (outer_radius**2-inner_radius**2)*extent/2, context+' total area', .01)


def radial_check(drawing, data, gauge=False):
    paths = [e for e in drawing.paths if 'A' in e.attrib['d']]
    value = data['series'][0]['values'][0]
    maximum = data['domain'][1] if gauge else data['total']
    ratio = value/maximum
    close(data['percentage'], ratio*100, 'Progress percentage')
    selected = [e for e in paths if e.attrib['fill']==BLUE]
    start = math.radians(data['start_angle_degrees'])
    sweep = math.pi if gauge else math.tau
    if gauge:
        tracks = [e for e in paths if e not in selected]
        assert tracks, 'Gauge full-scale track'
        track, track_inner = annulus(tracks[0])
        center, radius, inner_radius = track[0], track[1], track_inner[1]
        annular_run(tracks, center, radius, inner_radius, start, sweep, 'Gauge track')
        polygons=drawing.tags('polygon'); assert len(polygons)==1
        points=[float(v) for v in re.findall(r'[-+]?\d*\.?\d+(?:e[-+]?\d+)?',polygons[0].attrib['points'])]
        vertices=list(zip(points[::2],points[1::2]))
        tip=max(vertices,key=lambda pt: math.dist(pt,center))
        direction=math.atan2(tip[1]-center[1],tip[0]-center[0])
        close((direction-start-sweep*ratio+math.pi)%math.tau-math.pi,0,'Gauge needle value')
        for tick in data['ticks']:
            angle=start+sweep*tick/maximum
            assert any(abs((math.atan2(c[0][1][1]-center[1],c[0][1][0]-center[0])-angle+math.pi)%math.tau-math.pi)<0.0001
                       for c in drawing.segments),'Gauge tick angle'
    else:
        tracks=drawing.tags('circle'); assert len(tracks)==1
        track=tracks[0].attrib
        center=(float(track['cx']),float(track['cy']))
        radius=float(track['r'])+float(track['stroke-width'])/2
        inner_radius=float(track['r'])-float(track['stroke-width'])/2
        close(radius,data['outer_radius'],'Ring outer radius')
        close(inner_radius,data['inner_radius'],'Ring inner radius')
        close(sum(data['series'][0]['values']),maximum,'Ring part-to-whole total')
    annular_run(selected, center, radius, inner_radius, start, sweep*ratio, 'Progress arc')


def pictogram_check(drawing, data):
    people=[]
    for g in drawing.tags('g'):
        children=list(g)
        if [e.tag.rsplit('}',1)[-1] for e in children]==['circle','path']:
            people.append(g)
    assert len(people)==data['mark_count']==10, 'Person mark count'
    selected=sum(list(g)[0].attrib['fill']==BLUE for g in people)
    assert selected==data['selected_marks'], 'Selected person count'
    close(selected*data['value_per_mark'],data['series'][0]['values'][0],'Selected represented count')
    close(len(people)*data['value_per_mark'],data['total'],'Total represented count')
    close(selected/len(people)*100,data['percentage'],'Pictogram percentage')
    shape=list(people[0])[1].attrib['d']; positions=[]
    for g in people:
        head, body=list(g)
        assert body.attrib['d']==shape and body.attrib['fill']==head.attrib['fill'], 'Equal person shapes'
        assert head.attrib['r']=='14', 'Equal head size'
        transform=[float(v) for v in re.findall(r'[-+]?\d*\.?\d+',g.attrib['transform'])]
        assert transform[2:]==[1.0], 'Equal mark scale'
        positions.append(transform[:2])
    gap=positions[1][0]-positions[0][0]
    for i, pos in enumerate(positions): point(pos,(positions[0][0]+gap*i,positions[0][1]),'Even person spacing')


def stacked_check(drawing, data):
    bars=sorted(drawing.bars(),key=lambda e:(float(e.attrib['y']),float(e.attrib['x'])))
    p=data['plot']; assert len(bars)==len(data['categories'])*len(data['series']), 'Stack segment count'
    for i in range(len(data['categories'])):
        row=bars[i*3:(i+1)*3]; values=[s['values'][i] for s in data['series']]
        close(sum(values),100,'Normalized row total'); x=p['x']
        y=float(row[0].attrib['y']); height=float(row[0].attrib['height'])
        for e,value,color in zip(row,values,(BLUE,INK,MID)):
            r=e.attrib; close(float(r['x']),x,'Contiguous stack segment')
            close(float(r['y']),y,'Stack row alignment'); close(float(r['height']),height,'Stack thickness')
            close(float(r['width']),p['width']*value/100,'Stack value width')
            assert r['fill']==color, 'Stack series order'
            x+=float(r['width'])
        close(x,p['x']+p['width'],'Common full-length stack endpoint')
    for tick in data['ticks']:
        x=p['x']+p['width']*tick/100
        assert any(abs(c[0][1][0]-x)<0.0001 and abs(c[1][1][0]-x)<0.0001 for c in drawing.segments),'Stack tick geometry'


def waterfall_check(drawing,data):
    drawing.axis(data); p=data['plot']; scale=p['height']/data['domain'][1]; baseline=p['y']+p['height']
    bars=sorted(drawing.bars(),key=lambda e:float(e.attrib['x']))
    values=data['series'][0]['values']; assert len(bars)==len(values), 'Waterfall step count'
    close(values[0]+sum(values[1:-1]),values[-1],'Waterfall total reconciliation')
    running=0
    for i,(e,value,kind) in enumerate(zip(bars,values,data['step_types'])):
        before=0 if kind=='total' else running; after=value if kind=='total' else running+value
        low,high=sorted((before,after)); r=e.attrib
        close(float(r['y']),baseline-scale*high,'Waterfall upper boundary')
        close(float(r['height']),scale*(high-low),'Waterfall value height')
        assert r['fill']==(INK if kind=='total' else POSITIVE if value>=0 else NEGATIVE),'Waterfall sign color'
        close(after,data['running_totals'][i],'Waterfall running total')
        if i<len(bars)-1:
            drawing.segment((float(r['x'])+float(r['width']),baseline-scale*after),
                            (float(bars[i+1].attrib['x']),baseline-scale*after),'Waterfall connecting balance')
        running=after


CHECKS = {
    'progress_ring': radial_check,
    'semicircle_gauge': lambda drawing,data: radial_check(drawing,data,True),
    'pictogram': pictogram_check,
    'horizontal_bar': lambda drawing,data: bar_check(drawing,data,True),
    'vertical_bar': bar_check,
    'line': line_check,
    'pie': sector_check,
    'donut': lambda drawing,data: sector_check(drawing,data,True),
    'grouped_bar': lambda drawing,data: bar_check(drawing,data,grouped=True),
    'stacked_percent_bar': stacked_check,
    'waterfall': waterfall_check,
    'slope': lambda drawing,data: line_check(drawing,data,True),
}


def validate_charts(root=ROOT, records=None):
    root=Path(root)
    if records is None:
        rows=json.loads((root/'catalog.json').read_text(encoding='utf-8'))['assets']
        records=[json.loads((root/a['metadata_path']).read_text(encoding='utf-8')) for a in rows]
    charts=[a for a in records if a.get('kind')=='chart']
    assert len(charts)==12 and {a['data']['chart_type'] for a in charts}==set(CHECKS), 'Expected 12 chart examples'
    for a in charts:
        try:
            CHECKS[a['data']['chart_type']](Drawing(ET.parse(root/a['path']).getroot()),a['data'])
        except AssertionError as error:
            raise AssertionError(f"{a['id']}: {error}") from error
    return len(charts)


if __name__=='__main__':
    print(f'PASS: {validate_charts()} chart geometries match catalog sample data')

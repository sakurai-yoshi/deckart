"""Small SVG vocabulary shared by individually composed artwork."""
from html import escape
from math import atan2, cos, sin, pi
INK='#153A6B'
BLUE='#2864F0'
MID='#79A7ED'
PALE='#E7F0FF'
FAINT='#F3F7FD'
WHITE='#FFFFFF'
GRAY='#607590'
AMBER='#C58930'

def path(d,fill='none',stroke='none',sw=2,extra=''):
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round" {extra}/>'
def rect(x,y,w,h,fill=PALE,r=0,stroke='none',sw=2):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
def circle(x,y,r,fill=BLUE,stroke='none',sw=2):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
def ellipse(x,y,rx,ry,fill=PALE,stroke='none',sw=2):
    return f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
def line(x1,y1,x2,y2,stroke=INK,sw=3,dash=None):
    return path(f'M{x1} {y1}L{x2} {y2}',stroke=stroke,sw=sw,extra=f'stroke-dasharray="{dash}"' if dash else '')
def poly(points,fill=BLUE,stroke='none',sw=2):
    return f'<polygon points="{points}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"/>'
def group(body,x=0,y=0,scale=1):
    return f'<g transform="translate({x} {y}) scale({scale})">{body}</g>'
def arrow(x1,y1,x2,y2,stroke=BLUE,sw=5,head=16):
    a=atan2(y2-y1,x2-x1);bx=x2-head*cos(a);by=y2-head*sin(a);px=head*.46*sin(a);py=-head*.46*cos(a)
    return line(x1,y1,bx,by,stroke,sw)+poly(f'{x2},{y2} {bx+px},{by+py} {bx-px},{by-py}',stroke)
def check(x,y,scale=1,color=WHITE):
    return group(path('M0 12L10 22L32 0',stroke=color,sw=5),x,y,scale)
def slot(x,y,w,h,text,role='項目',align='center',color=INK):
    return dict(x=x,y=y,width=w,height=h,text=text,role=role,align=align,color=color)
def asset(name,category,title,description,keywords,body,labels=None,size=(1200,720)):
    return dict(id=name,category=category,title=title,description=description,keywords=keywords.split() if isinstance(keywords,str) else keywords,body=body,labels=labels or [],width=size[0],height=size[1])

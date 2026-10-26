"""Reusable navy star field for self-contained README SVG panels."""
import random
BG='#0B1431'
PANEL='#111F40'
BORDER='#31476B'

def starfield(width,height,prefix='space'):
    rng=random.Random(2407+width+height)
    g=prefix+'-gradient'; clip=prefix+'-clip'
    out=[f'<defs><linearGradient id="{g}" x2="1" y2="1"><stop stop-color="#08132D"/><stop offset=".55" stop-color="#111C46"/><stop offset="1" stop-color="#17224B"/></linearGradient><clipPath id="{clip}"><rect x=".5" y=".5" width="{width-1}" height="{height-1}" rx="12"/></clipPath></defs>',
         f'<rect x=".5" y=".5" width="{width-1}" height="{height-1}" rx="12" fill="url(#{g})" stroke="{BORDER}"/>',f'<g clip-path="url(#{clip})" pointer-events="none">']
    for i in range(max(25,width*height//2800)):
        x,y=rng.uniform(6,width-6),rng.uniform(6,height-6)
        color=['#8BBEFF','#C7D8FF','#B7A9FF'][i%3]
        r=rng.choice([.4,.55,.7,1.0]);opacity=rng.uniform(.12,.36)
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{color}" opacity="{opacity:.2f}"/>')
    for x,y in [(width*.91,height*.15),(width*.64,height*.82)]:
        out.append(f'<path d="M{x-4:.1f} {y:.1f}h8M{x:.1f} {y-4:.1f}v8" stroke="#94D6FF" stroke-width=".65" opacity=".42"/>')
    out.append('</g>')
    return ''.join(out)

"""Export a real-data 2D ↔ 3D skyline using the supplied component's camera maths.
SVG SMIL interpolates the same polygons; README rendering needs no JavaScript.
"""
from datetime import date, timedelta
from html import escape
from visual_theme import starfield
import json, math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PAL=['#161B22','#0E4429','#006D32','#26A641','#39D353']

def ease(t):
    t=max(0,min(1,t)); return 4*t*t*t if t<.5 else 1-(-2*t+2)**3/2

def project(x,y,z,t):
    e=ease(t); yaw=e*math.pi/4; elev=math.pi/2+(math.radians(34)-math.pi/2)*e
    return x*math.cos(yaw)-y*math.sin(yaw),(x*math.sin(yaw)+y*math.cos(yaw))*math.sin(elev)-z*math.cos(elev)

def rise(t,week,weeks,day):
    delay=(week/max(1,weeks-1))*.36+day/6*.06
    p=max(0,min(1,(t-delay)/.58));return 1-(1-p)**3

def txt(x,y,s,size=12,fill='#8B949E',weight='normal'):
    return f'<text x="{x}" y="{y}" fill="{fill}" font-size="{size}" font-weight="{weight}">{escape(str(s))}</text>'

def render(data,animated=True):
    start=date.fromisoformat(data['from']);start-=timedelta(days=(start.weekday()+1)%7)
    cells=[]
    for d in data['days']:
        delta=(date.fromisoformat(d['date'])-start).days
        cells.append(dict(d,week=delta//7,day=delta%7))
    weeks=max(c['week'] for c in cells)+1;maximum=max(c['count'] for c in cells) or 1
    def world(c,t):
        x,y=c['week']-weeks/2,c['day']-3.5
        h=(.4+(c['count']/maximum)**.85*7.2)*rise(t,c['week'],weeks,c['day']) if c['count'] else 0
        return [project(a,b,z,t) for a,b,z in [(x,y,h),(x+.78,y,h),(x+.78,y+.78,h),(x,y+.78,h),(x,y,0),(x+.78,y,0),(x+.78,y+.78,0),(x,y+.78,0)]]
    samples=[i/8 for i in range(9)]
    allpoints=[p for c in cells for t in samples for p in world(c,t)]
    allpoints += [project(c['week']-weeks/2,4.6,0,t) for c in cells if c['date'][8:]=='01' for t in samples]
    xmin,xmax=min(p[0] for p in allpoints),max(p[0] for p in allpoints)
    ymin,ymax=min(p[1] for p in allpoints),max(p[1] for p in allpoints)
    scale=min(1000/(xmax-xmin),320/(ymax-ymin))
    def screen(p): return 550+(p[0]-(xmin+xmax)/2)*scale,242+(p[1]-(ymin+ymax)/2)*scale
    def poly(c,t,indices): return ' '.join(f'{screen(world(c,t)[i])[0]:.2f},{screen(world(c,t)[i])[1]:.2f}' for i in indices)
    keys=[0,.12]+[.12+.22*i/8 for i in range(1,9)]+[.67]+[.67+.22*i/8 for i in range(1,9)]+[1]
    states=[0,0]+[i/8 for i in range(1,9)]+[1]+[1-i/8 for i in range(1,9)]+[0]
    out=['<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="550" viewBox="0 0 1100 550" role="img" aria-labelledby="t d">',
         '<title id="t">Subhajit2407 — contribution skyline</title>',
         '<desc id="d">Real public contribution days morph from a flat heatmap into an isometric skyline. Tower heights encode counts; summary statistics follow below.</desc>',
         '<style>text{font-family:JetBrains Mono,Consolas,monospace}</style>',
         starfield(1100,550,'skyline'),
         '<path d="M1 49h1098" stroke="#30363D"/>',txt(24,31,'// CONTRIBUTION SKYLINE',17,'#E6EDF3','bold'),
         txt(788,30,'2D → 3D / PUBLIC DATA',12,'#39D353'),txt(24,75,f'{data["from"]} → {data["to"]}   ·   Height = daily contribution count',11)]
    cells.sort(key=lambda c:(c['week']+c['day'],c['week']))
    for c in cells:
        color=PAL[c['level']]
        faces=[([0,1,2,3],color)]
        if c['count']:
            faces=[([1,2,6,5],PAL[max(1,c['level']-1)]),([2,3,7,6],PAL[max(1,c['level']-1)])]+faces
        for indices,fill in faces:
            out.append(f'<polygon points="{poly(c,1,indices)}" fill="{fill}" stroke="#0D1117" stroke-width=".55"><title>{c["date"]}: {c["count"]} contributions</title>')
            if animated:
                vals=';'.join(poly(c,t,indices) for t in states)
                out.append(f'<animate attributeName="points" values="{vals}" keyTimes="{";".join(f"{k:.4f}" for k in keys)}" dur="16s" repeatCount="indefinite"/>')
            out.append('</polygon>')
    seen=set()
    for c in sorted(cells,key=lambda c:c['date']):
        month=c['date'][:7]
        if month not in seen and c['date'][8:]=='01':
            positions=[screen(project(c['week']-weeks/2,4.6,0,state)) for state in states]
            p=screen(project(c['week']-weeks/2,4.6,0,1))
            label=txt(round(p[0]),round(p[1]),date.fromisoformat(c['date']).strftime('%b'),9)
            if animated:
                for axis,index in [('x',0),('y',1)]:
                    values=';'.join(f'{point[index]:.2f}' for point in positions)
                    label=label.replace('</text>',f'<animate attributeName="{axis}" values="{values}" keyTimes="{";".join(f"{k:.4f}" for k in keys)}" dur="16s" repeatCount="indefinite"/></text>')
            out.append(label);seen.add(month)
    out.extend([txt(24,433,'Less',10)])
    for i,color in enumerate(PAL):out.append(f'<rect x="{62+i*17}" y="423" width="12" height="12" rx="2" fill="{color}"/>')
    out+=[txt(153,433,'More',10),txt(655,433,'A year of work, one day at a time.',10),'<path d="M24 451h1052" stroke="#30363D"/>']
    s=data['stats']
    for i,(value,label,sub) in enumerate([(s['total'],'TOTAL CONTRIBUTIONS','Public calendar'),(s['current_streak'],'CURRENT STREAK','Consecutive days'),(s['longest_streak'],'LONGEST STREAK','In displayed period'),(s['best_day']['count'],'BUSIEST DAY',s['best_day']['date'])]):
        x=26+i*271
        out += [txt(x,476,label,10),txt(x,514,str(value),29,'#39D353','bold'),txt(x+70,510,sub,10)]
    out+=[txt(24,537,'Updated '+data['updated']+' UTC · Generated from GitHub public data · Static fallback available',9),'</svg>']
    return ''.join(out)+'\n'

if __name__=='__main__':
    d=json.loads((ROOT/'data/contributions.json').read_text())
    (ROOT/'assets/contributions.svg').write_text(render(d,True))
    (ROOT/'assets/contributions-static.svg').write_text(render(d,False))
    print('Generated animated skyline and static fallback from',len(d['days']),'real dates.')

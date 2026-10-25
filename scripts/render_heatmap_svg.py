"""Render an animated, self-contained SVG from validated calendar data."""
from datetime import date, timedelta
from html import escape
import json
import os
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
PALETTE = ['#161f28', '#0e4429', '#006d32', '#26a641', '#7ee787']

def text(x,y,s,size=12,fill='#8b949e',weight='normal'):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{weight}">{escape(str(s))}</text>'

def render(data, static=False):
    days, stats = data['days'], data['stats']
    start = date.fromisoformat(days[0]['date'])
    start -= timedelta(days=(start.weekday()+1)%7)
    content = ['<svg xmlns="http://www.w3.org/2000/svg" width="900" height="290" viewBox="0 0 900 290" role="img" aria-labelledby="title desc">',
        '<title id="title">Subhajit2407 — public contribution calendar</title>',
        f'<desc id="desc">{stats["total"]} public contributions from {data["from"]} to {data["to"]}. Longest streak in this period: {stats["longest_streak"]} days.</desc>',
        '<style>text{font-family:ui-monospace,SFMono-Regular,Consolas,monospace}.day{animation:reveal .45s both;animation-delay:var(--delay)}@keyframes reveal{from{opacity:0;transform:translateY(-5px)}to{opacity:1;transform:translateY(0)}}@media(prefers-reduced-motion:reduce){.day{animation:none}}</style>',
        '<rect x=".5" y=".5" width="899" height="289" rx="12" fill="#0d1117" stroke="#30363d"/>',
        '<path d="M1 43h898" stroke="#21262d"/>',
        '<circle cx="22" cy="22" r="4" fill="#f85149"/><circle cx="36" cy="22" r="4" fill="#d29922"/><circle cx="50" cy="22" r="4" fill="#3fb950"/>',
        text(70,26,'subhajit@github: ~/activity',12,'#c9d1d9'),text(735,26,'PUBLIC / LIVE',11,'#7ee787')]
    seen = set()
    for d in days:
        day = date.fromisoformat(d['date'])
        week, weekday = (day-start).days//7, (day.weekday()+1)%7
        x,y = 52+week*15.2, 83+weekday*15
        if day.strftime('%Y-%m') not in seen and day.day <= 7:
            content.append(text(x,70,day.strftime('%b'),10))
            seen.add(day.strftime('%Y-%m'))
        anim = '' if static else f' class="day" style="--delay:{(week+weekday)*.022:.3f}s"'
        content.append(f'<rect x="{x:.1f}" y="{y}" width="11" height="11" rx="2" fill="{PALETTE[d["level"]]}"{anim}><title>{d["date"]}: {d["count"]} contributions</title></rect>')
    for n, label in [(1,'Mon'),(3,'Wed'),(5,'Fri')]:
        content.append(text(18,92+n*15,label,9))
    content += [text(52,213,f'{data["from"]} → {data["to"]}',10),text(697,213,'Less',10)]
    for i,color in enumerate(PALETTE):
        content.append(f'<rect x="{730+i*16}" y="204" width="11" height="11" rx="2" fill="{color}"/>')
    content += [text(814,213,'More',10),'<path d="M22 228h856" stroke="#21262d"/>']
    for x,value,label in [(30,stats['total'],'contributions'),(258,stats['current_streak'],'current streak'),(482,stats['longest_streak'],'longest in period'),(718,stats['best_day']['count'],'best day')]:
        content += [text(x,256,value,22,'#7ee787','600'),text(x+len(str(value))*14+12,255,label,10)]
    content += [text(30,278,f'Public GitHub calendar · Updated {data["updated"]} UTC · Streaks in days',9),'</svg>']
    return ''.join(content)+'\n'

if __name__ == '__main__':
    data = json.loads((ROOT/'data/contributions.json').read_text())
    (ROOT/'contrib-heatmap.svg').write_text(render(data, os.environ.get('STATIC')=='1'))

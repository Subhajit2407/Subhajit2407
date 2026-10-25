"""Render verified profile facts as a neofetch-style animated SVG."""
from html import escape
import os
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def render(static=False):
    rows = [
        ('Name', 'Subhajit Talukder'),
        ('Now', 'B.Tech student · Jain University'),
        ('Focus', 'Frontend & interactive UI engineering'),
        ('Build', 'Useful products, thoughtful interfaces'),
        ('Stack', 'React · TypeScript · Next.js'),
        ('UI', 'Tailwind CSS · shadcn/ui · Framer Motion'),
        ('Tools', 'Vite · Git · GitHub'),
        ('Projects', 'MILES · Portfolio · CVita · Homie'),
        ('Web', 'subhajitdeveloper24.vercel.app'),
    ]
    out=['<svg xmlns="http://www.w3.org/2000/svg" width="530" height="390" viewBox="0 0 530 390" role="img" aria-labelledby="t d">',
         '<title id="t">Subhajit2407 — terminal profile</title><desc id="d">Verified biography, frontend stack, projects, and portfolio. Lines animate once, then remain visible.</desc>',
         '<style>text{font-family:Consolas,Menlo,monospace}.line{animation:print .45s both;animation-delay:var(--delay)}@keyframes print{from{opacity:0;transform:translateX(-5px)}to{opacity:1;transform:translateX(0)}}@media(prefers-reduced-motion:reduce){.line{animation:none}}</style>',
         '<rect x=".5" y=".5" width="529" height="389" rx="12" fill="#0d1117" stroke="#30363d"/>',
         '<text x="24" y="27" font-size="11" fill="#8b949e">$ neofetch --user Subhajit2407</text><path d="M1 43h528" stroke="#21262d"/>',
         '<text x="24" y="77" fill="#7ee787" font-size="19" font-weight="bold">subhajit@github</text>',
         '<text x="24" y="97" fill="#30363d" font-size="12">────────────────────────────────────────</text>']
    for i,(key,value) in enumerate(rows):
        attr = '' if static else f' class="line" style="--delay:{.18+i*.10:.2f}s"'
        out.append(f'<g{attr}><text x="24" y="{123+i*24}" fill="#7ee787" font-size="11">{key}</text><text x="102" y="{123+i*24}" fill="#c9d1d9" font-size="11">{escape(value)}</text></g>')
    for i,c in enumerate(['#161b22','#f85149','#7ee787','#e3b341','#58a6ff','#bc8cff','#56d4dd','#c9d1d9']):
        out.append(f'<rect x="{24+i*25}" y="350" width="24" height="12" fill="{c}"/>')
    out.append('<text x="24" y="378" fill="#8b949e" font-size="9">build → learn → iterate → ship</text></svg>')
    return ''.join(out)+'\n'

if __name__ == '__main__':
    (ROOT/'info-card.svg').write_text(render(os.environ.get('STATIC')=='1'))

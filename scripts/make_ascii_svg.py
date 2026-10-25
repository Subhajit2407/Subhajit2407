"""Make a monochrome, self-typing SVG from the user's existing GitHub avatar.
Only local regeneration needs Pillow; daily updates never install image libraries.
"""
from html import escape
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageOps
ROOT = Path(__file__).resolve().parents[1]
RAMP = ' .`:-=+*cs#%@'

def build(static=False):
    image = Image.open(ROOT/'assets/portrait-source.png').convert('RGB').resize((398,398))
    # A source-specific outline removes the window and patterned wall without an AI model.
    mask = Image.new('L', image.size, 0)
    ImageDraw.Draw(mask).polygon([(111,59),(152,34),(204,28),(262,42),(285,66),(294,117),
        (286,158),(280,202),(298,232),(346,256),(385,295),(397,398),(48,398),
        (57,323),(78,279),(124,244),(143,222),(143,202),(126,182),(116,154),(111,115)],fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(1))
    gray = ImageOps.autocontrast(image.convert('L'),cutoff=2)
    gray = ImageEnhance.Contrast(gray).enhance(1.35)
    gray = Image.composite(gray,Image.new('L',image.size,255),mask).crop((42,21,398,398))
    grid = gray.resize((88,59),Image.Resampling.LANCZOS)
    rows = [''.join(RAMP[min(len(RAMP)-1,round((255-grid.getpixel((x,y)))/255*(len(RAMP)-1)))] for x in range(88)) for y in range(59)]
    out=['<svg xmlns="http://www.w3.org/2000/svg" width="370" height="390" viewBox="0 0 370 390" role="img" aria-labelledby="t d">',
        '<title id="t">Subhajit Talukder — ASCII portrait</title><desc id="d">A monochrome ASCII rendering of Subhajit’s GitHub avatar, typed row by row.</desc>',
        '<style>text{font-family:Consolas,Menlo,monospace}.cursor{fill:#7ee787}@media(prefers-reduced-motion:reduce){.ascii-row{clip-path:none}}</style>',
        '<rect x=".5" y=".5" width="369" height="389" rx="12" fill="#0d1117" stroke="#30363d"/>',
        '<text x="22" y="27" fill="#8b949e" font-size="11">$ cat portrait.txt</text><path d="M1 43h368" stroke="#21262d"/>','<defs>']
    for y in range(59):
        a,b = y*.013, y*.013+.12
        animation = '' if static else f'<animate attributeName="width" values="0;0;322;322" keyTimes="0;{a:.3f};{b:.3f};1" dur="3s" fill="freeze"/>' if y else '<animate attributeName="width" values="0;322;322" keyTimes="0;.12;1" dur="3s" fill="freeze"/>'
        out.append(f'<clipPath id="row{y}"><rect x="23" y="{53+y*5.15:.2f}" width="322" height="6">{animation}</rect></clipPath>')
    out.append('</defs>')
    for y,line in enumerate(rows):
        out.append(f'<text class="ascii-row" xml:space="preserve" x="23" y="{58+y*5.15:.2f}" font-size="6" letter-spacing="0" fill="#c9d1d9" clip-path="url(#row{y})">{escape(line)}</text>')
    out += ['<text x="22" y="375" fill="#7ee787" font-size="10">subhajit2407 / rendered in characters</text>','</svg>']
    return ''.join(out)+'\n'

if __name__ == '__main__':
    (ROOT/'subhajit-ascii.svg').write_text(build(os.environ.get('STATIC')=='1'))

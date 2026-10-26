"""Generate reusable black-and-green README panels from checked profile facts."""
from html import escape
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets';OUT.mkdir(exist_ok=True)
ICONS=json.loads((ROOT/'data/tech-icons.json').read_text())
DATA=json.loads((ROOT/'data/dashboard.json').read_text())
BG='#0D1117';PANEL='#161B22';BORDER='#30363D';TEXT='#E6EDF3';MUTED='#8B949E';GREEN='#39D353'

def t(x,y,s,size=13,fill=TEXT,weight='normal',spacing=0):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{weight}" letter-spacing="{spacing}">{escape(str(s))}</text>'

def rect(x,y,w,h,fill=PANEL,rx=7):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{BORDER}"/>'

def svg(w,h,title,body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img"><title>{escape(title)}</title><style>text{{font-family:JetBrains Mono,Consolas,monospace}}</style>'+rect(.5,.5,w-1,h-1,BG,12)+body+'</svg>\n'

def icon(slug,x,y,size=25):
    if slug in ICONS:
        return f'<svg x="{x}" y="{y}" width="{size}" height="{size}" viewBox="0 0 24 24"><path fill="{GREEN}" d="{ICONS[slug]["path"]}"/></svg>'
    shapes={
      'database':'M3 6c0-5 18-5 18 0v12c0 5-18 5-18 0zm0 0c0 5 18 5 18 0M3 12c0 5 18 5 18 0',
      'api':'M8 5 1 12l7 7M16 5l7 7-7 7M14 3l-4 18',
      'auth':'M5 10V7a7 7 0 0 1 14 0v3M3 10h18v12H3zM12 14v4',
      'network':'M2 5h6v6H2zM16 13h6v6h-6zM8 8h10v5M5 11v7h11',
      'brain':'M12 3v18M12 6C4 0-2 10 5 12c-5 5 2 12 7 5M12 6c8-6 14 4 7 6 5 5-2 12-7 5',
      'test':'m3 12 6 6 12-13',
      'terminal':'m3 5 7 7-7 7M13 19h8',
      'box':'m12 2 10 5v10l-10 5-10-5V7zm0 10v10M2 7l10 5 10-5',
    }
    path=shapes.get(slug,shapes['api'])
    return f'<svg x="{x}" y="{y}" width="{size}" height="{size}" viewBox="0 0 24 24"><path d="{path}" fill="none" stroke="{GREEN}" stroke-width="1.5" stroke-linejoin="round" stroke-linecap="round"/></svg>'

def banner():
    b=''
    for x in range(720,1090,15):
        for y in range(14,306,15):
            if (x//15+y//15)%4==0:b+=f'<circle cx="{x}" cy="{y}" r="1" fill="{GREEN}" opacity=".16"/>'
    b+=f'<path d="M630 1 530 101h100l-65 65M1010 310l90-90M1 276l34-34" fill="none" stroke="{GREEN}" opacity=".22"/>'
    b+=t(30,33,'subhajit@github ~ $ whoami',13,GREEN)
    b+=t(28,101,'SUBHAJIT',57,TEXT,'bold',1)+t(28,159,'TALUKDER',57,GREEN,'bold',1)
    b+=t(31,193,DATA['role'],22,TEXT)+t(31,221,DATA['focus'],13,GREEN)
    b+=t(31,252,'Building scalable applications, real-time systems',12,MUTED)+t(31,272,'and thoughtful AI-powered products.',12,MUTED)
    b+=rect(694,48,375,226,BG,8)+t(714,76,'// CURRENTLY',15,TEXT,'bold')
    for i,line in enumerate(['Building and shipping useful products','Designing APIs & real-time systems','Exploring AI & LLM applications','Improving system design fundamentals','Open to thoughtful collaborations']):
        b+=f'<circle cx="718" cy="{102+i*34}" r="2" fill="{GREEN}"/>'+t(731,106+i*34,line,11,TEXT)
        if i<4:b+=f'<path d="M715 {118+i*34}h331" stroke="{BORDER}" opacity=".6"/>'
    return svg(1100,310,'Subhajit Talukder — Software Development Engineer',b)

def profile():
    rows=[('Name','Subhajit Talukder'),('Role','Software Development Engineer'),('Focus','Backend / Full Stack / AI'),('Education','JAIN University · B.Tech · 2027'),('Backend','Node.js · Express · REST · WebSockets'),('Data','PostgreSQL · MongoDB · Supabase'),('AI','OpenAI API · Claude API · LLMs'),('Interests','System design · testing · performance'),('Portfolio','subhajitdeveloper24.vercel.app')]
    b=t(23,27,'$ neofetch --user Subhajit2407',11,MUTED)+f'<path d="M1 43h528" stroke="{BORDER}"/>'+t(24,79,'subhajit@github',21,GREEN,'bold')
    for i,(label,value) in enumerate(rows):
        b+=t(24,117+i*25,label,11,GREEN)+t(105,117+i*25,value,11,TEXT)
    for i,c in enumerate([BG,PANEL,BORDER,'#0E4429','#006D32','#26A641',GREEN,TEXT]):b+=f'<rect x="{24+i*26}" y="350" width="25" height="11" fill="{c}"/>'
    b+=t(24,378,'create. iterate. build.',10,MUTED)
    return svg(530,390,'Engineering profile — Subhajit Talukder',b)

def stack():
    groups=[('LANGUAGES',[('JavaScript','javascript'),('TypeScript','typescript'),('Python','python'),('C++','cplusplus'),('SQL','database')]),
      ('BACKEND',[('Node.js','nodedotjs'),('Express.js','express'),('REST APIs','api'),('WebSockets','network'),('Auth','auth')]),
      ('FRONTEND',[('React','react'),('HTML5','html5'),('CSS3','css3'),('Responsive','box')]),
      ('DATABASES',[('PostgreSQL','postgresql'),('MongoDB','mongodb'),('Supabase','supabase')]),
      ('CLOUD & DEVOPS',[('AWS EC2','amazonwebservices'),('Docker','docker'),('Git','git'),('Actions','githubactions'),('CI/CD','network'),('Linux','linux'),('Vercel','vercel')]),
      ('AI ENGINEERING',[('OpenAI API','openai'),('Claude API','anthropic'),('LLMs','brain'),('Prompt Eng.','terminal'),('AI Agents','box')])]
    b=t(24,32,'// TECHNICAL STACK',17,TEXT,'bold')+t(738,31,'TOOLS FOR BUILDING USEFUL SYSTEMS',10,GREEN)
    for gi,(label,items) in enumerate(groups):
        gx,gy=22+(gi%3)*360,55+(gi//3)*214
        b+=rect(gx,gy,336,200,BG,7)+t(gx+14,gy+24,label,12,GREEN,'bold')
        for i,(name,slug) in enumerate(items):
            x=gx+12+(i%4)*79;y=gy+40+(i//4)*74
            b+=f'<rect x="{x}" y="{y}" width="73" height="64" rx="5" fill="{PANEL}"/>'+icon(slug,x+25,y+9,24)+t(x+6,y+51,name,8,TEXT)
    b+=f'<path d="M24 494h1052" stroke="{BORDER}"/>'+t(24,517,'ENGINEERING',11,GREEN,'bold')
    b+=t(160,517,'Data structures · Algorithms · OOP · DBMS · System design · Testing · Performance',10,TEXT)
    b+=t(24,542,'Practical tools. Strong fundamentals. Continuous learning.',10,MUTED)
    return svg(1100,560,'Technical stack — languages, backend, frontend, databases, cloud and AI',b)

def impact():
    b=t(24,32,'// ENGINEERING IMPACT',17,TEXT,'bold')
    for i,(value,label,sub) in enumerate([('100+','ACTIVE USERS','Nexio collaboration platform'),('30%','LOWER API RESPONSE TIME','Query & connection-pool optimization'),('3','DEPLOYED APPLICATIONS','Full-stack product delivery'),('AI + CI/CD','ENGINEERING WORKFLOW','Validation, testing and releases')]):
        x=22+i*270;b+=rect(x,54,254,133,BG,7)+t(x+15,97,value,30,GREEN,'bold')+t(x+15,124,label,10,TEXT,'bold')+t(x+15,151,sub,8,MUTED)
    return svg(1100,208,'Engineering impact — 100+ users, 30 percent reduction in API response time, three deployed applications',b)

def project(p):
    b=t(24,28,'// '+p['category'],10,GREEN)+t(24,66,p['name'],28,TEXT,'bold')
    b+=f'<path d="M24 82h482" stroke="{BORDER}"/>'
    for i,line in enumerate(p['description']):b+=t(24,111+i*23,line,11,TEXT)
    b+=t(24,172,p['tech'],9,MUTED)
    b+=f'<path d="M24 190h482" stroke="{BORDER}"/>'+t(24,215,p['highlight'],10,GREEN)
    return svg(530,240,p['name']+' — '+p['category'],b)

if __name__=='__main__':
    for name,content in [('banner.svg',banner()),('neofetch.svg',profile()),('tech-stack.svg',stack()),('impact.svg',impact())]: (OUT/name).write_text(content)
    (OUT/'projects').mkdir(exist_ok=True)
    for p in DATA['projects']:(OUT/'projects'/f'{p["id"]}.svg').write_text(project(p))
    portrait=(ROOT/'subhajit-ascii.svg').read_text().replace('#7ee787',GREEN)
    (OUT/'portrait.svg').write_text(portrait)
    print('Generated dashboard panels; preserved ASCII portrait character layout.')

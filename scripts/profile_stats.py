"""Render public GitHub data as local SVGs. Python standard library only."""
import collections
import datetime as dt
import html
import json
import os
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
USER = 'Subhajit2407'
BG, FG, MUTED, CYAN, VIOLET = '#0d1117', '#e6edf3', '#8b9eb3', '#67e8f9', '#a78bfa'

def graphql(query, variables):
    request = urllib.request.Request('https://api.github.com/graphql',
        data=json.dumps({'query': query, 'variables': variables}).encode(),
        headers={'Authorization': 'Bearer ' + os.environ['GH_TOKEN'],
                 'Content-Type': 'application/json', 'User-Agent': 'Subhajit2407-profile'})
    with urllib.request.urlopen(request, timeout=45) as response:
        result = json.load(response)
    if result.get('errors'):
        raise RuntimeError(json.dumps(result['errors']))
    return result['data']

def text(x, y, value, size=14, color=FG, weight='normal'):
    return f'<text x="{x}" y="{y}" fill="{color}" font-family="Segoe UI,Arial,sans-serif" font-size="{size}" font-weight="{weight}">{html.escape(str(value))}</text>'

def card(width, height, title, body, description):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="t d">'
            f'<title id="t">{html.escape(title)}</title><desc id="d">{html.escape(description)}</desc>'
            f'<rect x=".5" y=".5" width="{width-1}" height="{height-1}" rx="10" fill="{BG}" stroke="#303b50"/>'
            + text(22, 30, title, 16, CYAN, '600') + body + '</svg>')

def write(path, content):
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content + '\n')

def streaks(days, today):
    days = sorted(days, key=lambda day: day['date'])
    longest = current_run = 0
    previous = None
    for day in days:
        date = dt.date.fromisoformat(day['date'])
        if day['contributionCount']:
            current_run = current_run + 1 if previous == date - dt.timedelta(days=1) else 1
            longest = max(longest, current_run)
            previous = date
        else:
            current_run = 0
            previous = None
    by_date = {dt.date.fromisoformat(d['date']): d['contributionCount'] for d in days}
    cursor = today if by_date.get(today, 0) else today - dt.timedelta(days=1)
    current = 0
    while by_date.get(cursor, 0):
        current += 1
        cursor -= dt.timedelta(days=1)
    return current, longest

def render(user, repos, today):
    cal = user['contributionsCollection']['contributionCalendar']
    days = [day for week in cal['weeks'] for day in week['contributionDays']]
    period = f"{days[0]['date']} to {days[-1]['date']} (UTC)"
    updated = 'Updated ' + today.isoformat() + ' UTC'
    public = [r for r in repos if not r['isPrivate'] and not r['isFork']]
    stars = sum(r['stargazerCount'] for r in public)
    forks = sum(r['forkCount'] for r in public)
    rows = [('Public repositories (owned, non-fork)', len(public)), ('Stars across those repositories', stars),
            ('Forks across those repositories', forks), ('Contributions in displayed period', cal['totalContributions'])]
    body = ''
    for i, (label, value) in enumerate(rows):
        y = 63 + i * 29
        body += text(22, y, label, 12, MUTED) + text(375, y, f'{value:,}', 15, FG, '600')
    body += text(22, 193, updated, 10, MUTED)
    write('assets/stats/overview.svg', card(450, 210, 'GitHub / overview', body, period + '. Public data only.'))
    current, longest = streaks(days, today)
    active = sum(d['contributionCount'] > 0 for d in days)
    body = ''
    for x, val, label in [(75, current, 'Current streak'), (225, longest, 'Longest in period'), (375, active, 'Active days')]:
        body += f'<circle cx="{x}" cy="93" r="36" fill="none" stroke="#26384e" stroke-width="3"/>'
        body += text(x - len(str(val)) * 9, 103, val, 30, VIOLET, '600') + text(x - 56, 151, label, 12, MUTED)
    body += text(22, 178, 'Streaks count consecutive contribution days; today may be in progress.', 10, MUTED)
    body += text(22, 193, updated, 10, MUTED)
    write('assets/stats/streak.svg', card(450, 210, 'Contribution / rhythm', body, period))
    langs = collections.Counter()
    colors = {}
    for repo in public:
        for edge in repo['languages']['edges']:
            name = edge['node']['name']
            langs[name] += edge['size']
            colors[name] = edge['node']['color'] or CYAN
    top = langs.most_common(6)
    total = sum(langs.values())
    body = text(22, 52, 'Language bytes in owned public non-fork repositories', 11, MUTED)
    for i, (lang, value) in enumerate(top):
        x, y = 22 + (i % 2) * 220, 82 + (i // 2) * 44
        pct = 100 * value / total
        body += text(x, y, f'{lang}  {pct:.1f}%', 12)
        body += f'<rect x="{x}" y="{y+9}" width="190" height="5" rx="2" fill="#1c293b"/>'
        body += f'<rect x="{x}" y="{y+9}" width="{190*pct/100:.2f}" height="5" rx="2" fill="{colors[lang]}"/>'
    if not top:
        body += text(22, 100, 'No language data returned by GitHub.', 12, MUTED)
    body += text(22, 220, updated + ' · Language mix does not indicate proficiency.', 10, MUTED)
    write('assets/stats/languages.svg', card(480, 238, 'Languages / code composition', body, 'Top six language shares of all returned repository language bytes.'))
    # A true isometric chart: height and color encode each day's contribution count.
    body = text(22, 53, period + ' · Height = daily contributions', 11, MUTED)
    max_count = max((d['contributionCount'] for d in days), default=1) or 1
    for wi, week in enumerate(cal['weeks']):
        for day in week['contributionDays']:
            date = dt.date.fromisoformat(day['date'])
            di = (date.weekday() + 1) % 7
            x, y = 56 + wi*14 + di*8, 115 + di*10 - wi*.25
            count = day['contributionCount']
            h = 3 + 51 * count / max_count if count else 2
            level = min(3, max(0, round(3*count/max_count)))
            color = ['#1b3047','#276a92','#548dd1','#67e8f9'][level] if count else '#172233'
            p = lambda pts: ' '.join(f'{a:.2f},{b:.2f}' for a,b in pts)
            body += f'<g><title>{date}: {count} contributions</title>'
            body += f'<polygon points="{p([(x,y-h),(x+7,y+4-h),(x+14,y-h),(x+7,y-4-h)])}" fill="{color}"/>'
            body += f'<polygon points="{p([(x,y-h),(x+7,y+4-h),(x+7,y+4),(x,y)])}" fill="{color}" opacity=".7"/>'
            body += f'<polygon points="{p([(x+7,y+4-h),(x+14,y-h),(x+14,y),(x+7,y+4)])}" fill="{color}" opacity=".45"/></g>'
    body += text(22, 225, f"{cal['totalContributions']:,} contributions · {active} active days · {updated}", 12, MUTED)
    write('profile-3d-contrib/profile-night-cyan.svg', card(890, 248, 'Contribution / cityscape', body, 'Isometric daily GitHub contribution counts. ' + period))

def main():
    today = dt.datetime.now(dt.timezone.utc).date()
    query = '''query($login:String!, $from:DateTime!, $to:DateTime!) { user(login:$login) {
      contributionsCollection(from:$from,to:$to) { contributionCalendar { totalContributions weeks { contributionDays { date contributionCount } } } }
    } }'''
    user = graphql(query, {'login': USER, 'from': (today-dt.timedelta(days=364)).isoformat()+'T00:00:00Z',
                           'to': today.isoformat()+'T23:59:59Z'})['user']
    repos, cursor = [], None
    query = '''query($login:String!,$cursor:String) { user(login:$login) {
      repositories(first:100,after:$cursor,ownerAffiliations:OWNER,privacy:PUBLIC,isFork:false) {
        nodes { isPrivate isFork stargazerCount forkCount languages(first:100) { edges { size node { name color } } } }
        pageInfo { hasNextPage endCursor }
      }
    } }'''
    while True:
        data = graphql(query, {'login': USER, 'cursor': cursor})['user']['repositories']
        repos.extend(data['nodes'])
        if not data['pageInfo']['hasNextPage']:
            break
        cursor = data['pageInfo']['endCursor']
    render(user, repos, today)

if __name__ == '__main__':
    main()

"""Fetch the public GitHub calendar without credentials; fail closed on markup changes."""
import argparse
from collections import Counter
from datetime import date, datetime, timedelta, timezone
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import time
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
USER = 'Subhajit2407'

class CalendarParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.cells, self.labels = {}, {}
        self.tip_id, self.tip_text = None, []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get('data-date') and a.get('id') and a.get('data-level') is not None:
            self.cells[a['id']] = {'date': a['data-date'], 'level': int(a['data-level']),
                                   'count': int(a['data-count']) if 'data-count' in a else None}
        if tag == 'tool-tip' and a.get('for'):
            self.tip_id, self.tip_text = a['for'], []
    def handle_data(self, text):
        if self.tip_id:
            self.tip_text.append(text)
    def handle_endtag(self, tag):
        if tag == 'tool-tip' and self.tip_id:
            self.labels[self.tip_id] = ''.join(self.tip_text).strip()
            self.tip_id = None
    def days(self):
        days = []
        for cell_id, day in self.cells.items():
            if day['count'] is None:
                label = self.labels.get(cell_id, '')
                match = re.match(r'([\d,]+) contributions?\b', label)
                if label.startswith('No contributions'):
                    day['count'] = 0
                elif match:
                    day['count'] = int(match[1].replace(',', ''))
                else:
                    raise ValueError(f'Missing contribution count for {day["date"]}; refusing to invent data.')
            if day['count'] < 0 or not 0 <= day['level'] <= 4:
                raise ValueError('Invalid contribution cell')
            days.append(day)
        days.sort(key=lambda d: d['date'])
        if not 350 <= len(days) <= 371:
            raise ValueError(f'Expected a full-year calendar, received {len(days)} days')
        for before, after in zip(days, days[1:]):
            if date.fromisoformat(after['date']) - date.fromisoformat(before['date']) != timedelta(days=1):
                raise ValueError('Calendar contains missing or duplicate dates')
        return days

def summarize(days, today):
    by_date = {date.fromisoformat(d['date']): d['count'] for d in days}
    cursor = today if by_date.get(today, 0) else today - timedelta(days=1)
    current = 0
    while by_date.get(cursor, 0):
        current += 1
        cursor -= timedelta(days=1)
    run = longest = 0
    monthly = Counter()
    for day in days:
        run = run + 1 if day['count'] else 0
        longest = max(longest, run)
        monthly[day['date'][:7]] += day['count']
    best = max(days, key=lambda d: (d['count'], d['date']))
    return {'total': sum(d['count'] for d in days), 'current_streak': current,
            'longest_streak': longest, 'active_days': sum(d['count'] > 0 for d in days),
            'best_day': {'date': best['date'], 'count': best['count']},
            'monthly_totals': dict(sorted(monthly.items()))}

def fetch():
    req = Request(f'https://github.com/users/{USER}/contributions',
                  headers={'User-Agent': f'{USER}-profile-calendar', 'Accept-Language': 'en-US,en;q=0.9'})
    for attempt in range(3):
        try:
            with urlopen(req, timeout=45) as response:
                return response.read().decode('utf-8')
        except (OSError, TimeoutError):
            if attempt == 2:
                raise
            time.sleep(2 ** attempt)

def main():
    args = argparse.ArgumentParser()
    args.add_argument('--html', type=Path, help='Use a saved calendar for offline validation')
    options = args.parse_args()
    parser = CalendarParser()
    parser.feed(options.html.read_text() if options.html else fetch())
    days = parser.days()
    today = datetime.now(timezone.utc).date()
    last = date.fromisoformat(days[-1]['date'])
    if last > today or (today-last).days > 1:
        raise ValueError('Calendar is stale or contains future dates')
    result = {'username': USER, 'source': f'https://github.com/users/{USER}/contributions',
              'updated': today.isoformat(), 'from': days[0]['date'], 'to': days[-1]['date'],
              'days': days, 'stats': summarize(days, today)}
    target = ROOT / 'data/contributions.json'
    target.parent.mkdir(parents=True, exist_ok=True)
    temp = target.with_suffix('.tmp')
    temp.write_text(json.dumps(result, indent=2) + '\n')
    temp.replace(target)
    print(f'Validated {len(days)} public calendar days; {result["stats"]["total"]} contributions.')

if __name__ == '__main__':
    main()

import json,re,datetime as dt
from pathlib import Path
import requests
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]; H={'User-Agent':'Mozilla/5.0 SanctuaryDashboard/1.0'}

def get(url):
    r=requests.get(url,headers=H,timeout=25); r.raise_for_status(); return r

def world_boss():
    # Helltides exposes the same schedule feed used by community tools.
    # If it rejects automated requests, we keep the last known-good JSON.
    j=get('https://helltides.com/api/schedule').json()
    rows=j.get('world_boss') or j.get('worldBoss') or []
    out=[]
    for x in rows:
        raw=x.get('startTime') or x.get('start_time') or x.get('time')
        if raw is None: continue
        if isinstance(raw,(int,float)):
            # tolerate seconds or milliseconds
            if raw>10_000_000_000: raw=raw/1000
            t=dt.datetime.fromtimestamp(raw,dt.timezone.utc)
        else:
            z=str(raw).replace('Z','+00:00')
            t=dt.datetime.fromisoformat(z)
            if t.tzinfo is None: t=t.replace(tzinfo=dt.timezone.utc)
            t=t.astimezone(dt.timezone.utc)
        name=x.get('name') or x.get('boss') or x.get('bossName') or 'World Boss'
        loc=x.get('location') or x.get('zone') or x.get('region') or 'Sanctuary'
        if isinstance(name,dict): name=name.get('name','World Boss')
        if isinstance(loc,dict): loc=loc.get('name','Sanctuary')
        out.append({'time':t.isoformat().replace('+00:00','Z'),'name':str(name),'location':str(loc)})
    return sorted(out,key=lambda x:x['time'])

def tracker():
    items=[]
    try:
        s=BeautifulSoup(get('https://blizztrack.com/forums').text,'html.parser')
        for a in s.find_all('a',href=True):
            title=' '.join(a.stripped_strings)
            if len(title)>20 and ('d4' in a['href'].lower() or 'diablo' in title.lower()):
                url=a['href']; url=('https://blizztrack.com'+url) if url.startswith('/') else url
                items.append({'kind':'community','author':'Blizzard Staff','source':'Blizzard Tracker','published':dt.datetime.now(dt.timezone.utc).isoformat(),'title':title[:180],'summary':'Cập nhật từ Blizzard tracker.','url':url})
                if len(items)>=6: break
    except Exception: pass
    try:
        s=BeautifulSoup(get('https://news.blizzard.com/en-us/diablo4').text,'html.parser')
        for a in s.find_all('a',href=True):
            title=' '.join(a.stripped_strings)
            if len(title)>25 and '/article/' in a['href']:
                url=a['href']; url=('https://news.blizzard.com'+url) if url.startswith('/') else url
                items.append({'kind':'blizzard','author':'Blizzard Entertainment','source':'Blizzard News','published':dt.datetime.now(dt.timezone.utc).isoformat(),'title':title[:180],'summary':'Tin chính thức Diablo IV từ Blizzard.','url':url})
                if len([x for x in items if x['kind']=='blizzard'])>=6: break
    except Exception: pass
    # de-dupe
    seen=set(); clean=[]
    for x in items:
        if x['url'] not in seen: seen.add(x['url']); clean.append(x)
    return clean

def main():
    ep=ROOT/'data/events.json'; np=ROOT/'data/news.json'
    old=json.loads(ep.read_text()) if ep.exists() else {'world_boss':[]}
    try:
        wb=world_boss()
        if wb: old['world_boss']=wb
    except Exception as e: print('world boss refresh failed:',e)
    old['updated_at']=dt.datetime.now(dt.timezone.utc).isoformat().replace('+00:00','Z')
    ep.write_text(json.dumps(old,ensure_ascii=False,indent=2))
    try:
        n=tracker()
        if n: np.write_text(json.dumps(n,ensure_ascii=False,indent=2))
    except Exception as e: print('news refresh failed:',e)
if __name__=='__main__': main()

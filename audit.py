import csv
import sqlite3
from pathlib import Path
import logging

ROOT = Path(__file__).resolve().parent

def run():
    out = ROOT / 'output'
    out.mkdir(exist_ok=True)
    logging.basicConfig(filename=out/'audit.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s', force=True)
    with (ROOT/'data/providers.csv').open(newline='') as f:
        rows = list(csv.DictReader(f))
    exceptions, updates = [], []
    with sqlite3.connect(':memory:') as db:
        db.execute('CREATE TABLE providers (provider_id TEXT, name TEXT, state TEXT, status TEXT)')
        db.executemany('INSERT INTO providers VALUES (:provider_id,:name,:state,:status)', rows)
        duplicates = {r[0] for r in db.execute('SELECT provider_id FROM providers GROUP BY provider_id HAVING COUNT(*) > 1')}
        for r in rows:
            issues = []
            if not r['provider_id'].strip(): issues.append('MISSING_ID')
            if not r['name'].strip(): issues.append('MISSING_NAME')
            if r['provider_id'] in duplicates: issues.append('DUPLICATE_ID')
            if r['state'].strip().upper() not in {'AL','GA','TX','OH'}: issues.append('STATE_OUTSIDE_DEMO_NETWORK')
            if r['status'].strip().upper() not in {'ACTIVE','INACTIVE'}: issues.append('INVALID_STATUS')
            for issue in issues:
                exceptions.append({'provider_id':r['provider_id'],'issue':issue})
            if not issues:
                for field in ('state','status'):
                    new = r[field].strip().upper()
                    if new != r[field]:
                        updates.append({'provider_id':r['provider_id'],'field':field,'old_value':r[field],'new_value':new})
    for name, fields, records in [('exceptions.csv',['provider_id','issue'],exceptions),('correction_batch.csv',['provider_id','field','old_value','new_value'],updates)]:
        with (out/name).open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(records)
    logging.info('Processed %d records; %d exceptions; %d proposed corrections',len(rows),len(exceptions),len(updates))
    print(f'Processed {len(rows)} records; {len(exceptions)} exceptions; {len(updates)} proposed corrections')
    return exceptions, updates

if __name__ == '__main__':
    run()

"""Persist requested automatic capture ranges so an interrupted prefix is not complete."""
import json
from datetime import datetime, timezone


def save_capture_plan(sha, sections, total_pages, db_path=None):
    from .db import connect_db
    ranges = [[max(1,min(int(s['start_page']),total_pages)),
               max(1,min(int(s['end_page']),total_pages))] for s in sections]
    with connect_db(db_path) as conn:
        conn.execute('INSERT INTO app_state(key,value,updated_at) VALUES(?,?,?) '
                     'ON CONFLICT(key) DO UPDATE SET value=excluded.value,updated_at=excluded.updated_at',
                     ('capture_plan:'+sha,json.dumps(ranges),datetime.now(timezone.utc).isoformat()))


def assert_capture_plan_complete(sha, sections, db_path=None):
    from .db import connect_db
    with connect_db(db_path) as conn:
        row = conn.execute('SELECT value FROM app_state WHERE key=?',('capture_plan:'+sha,)).fetchone()
    if row is None:
        return  # Legacy/manual captures have no claim of automatic-plan completion.
    expected = {p for start,end in json.loads(row[0]) for p in range(start,max(start,end)+1)}
    actual = {part['physical_page'] for sec in sections for part in sec.selections}
    missing = sorted(expected-actual)
    if missing:
        raise ValueError('Automatic capture is incomplete; missing physical pages '
                         + ', '.join(map(str,missing))
                         + '. Preserve existing captures and use an explicit recapture to finish this plan.')

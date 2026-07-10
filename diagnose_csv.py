# -*- coding: utf-8 -*-
import csv, io, urllib.request

SHEET_ID = "1HPmYJb-GzbH7OVzxXJw5l6bSA89gK3Wd5aRn3KHrSX0"
URLS = {
    "gviz":   f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=data",
    "export": f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv",
}

out = io.StringIO()
def w(*a):
    print(*a, file=out)

for name, url in URLS.items():
    w("=" * 70)
    w(f"ENDPOINT: {name}")
    w("=" * 70)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        data = urllib.request.urlopen(req, timeout=30).read()
    except Exception as e:
        w("FETCH ERROR:", e); continue
    text = data.decode("utf-8")
    rows = list(csv.reader(io.StringIO(text)))
    w(f"bytes={len(data)}  parsed_rows={len(rows)}  cols_in_row0={len(rows[0]) if rows else 0}")
    w(f"field counts per row: {[len(r) for r in rows]}")
    w("\n-- ROW 0 (each field, full) --")
    for j, c in enumerate(rows[0]):
        w(f"  [{j}] {c!r}")
    if len(rows) > 1:
        w("\n-- ROW 1 (full) --")
        for j, c in enumerate(rows[1]):
            w(f"  [{j}] {c!r}")
    w("")

open(r"C:\Users\user\Downloads\웹사이트개발\2026-07-10\csv_report.txt", "w", encoding="utf-8").write(out.getvalue())
print("report written")

# -*- coding: utf-8 -*-
import csv, io, urllib.request

SID = "1HPmYJb-GzbH7OVzxXJw5l6bSA89gK3Wd5aRn3KHrSX0"
base = f"https://docs.google.com/spreadsheets/d/{SID}"
variants = {
    "gviz sheet=data":            f"{base}/gviz/tq?tqx=out:csv&sheet=data",
    "gviz sheet=data&headers=1":  f"{base}/gviz/tq?tqx=out:csv&headers=1&sheet=data",
    "gviz gid=0&headers=1":       f"{base}/gviz/tq?tqx=out:csv&headers=1&gid=0",
    "gviz tq=select*&headers=1":  f"{base}/gviz/tq?tqx=out:csv&headers=1&sheet=data&tq=" + urllib.parse.quote("select *"),
}
out = io.StringIO()
def w(*a): print(*a, file=out)
for name, url in variants.items():
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        data = urllib.request.urlopen(req, timeout=30).read()
        rows = list(csv.reader(io.StringIO(data.decode("utf-8"))))
        clean = (len(rows) == 33 and all(len(r) == 17 for r in rows)
                 and rows[1][0] == "PNU-2026-001")
        w(f"{'OK ' if clean else 'BAD'} | rows={len(rows):>2} | row1[0]={rows[1][0][:22]!r:24} | {name}")
    except Exception as e:
        w(f"ERR | {name} -> {e}")
open(r"C:\Users\user\Downloads\웹사이트개발\2026-07-10\gviz_variants_report.txt","w",encoding="utf-8").write(out.getvalue())
print("done")

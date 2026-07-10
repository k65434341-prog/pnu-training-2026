# -*- coding: utf-8 -*-
import csv, io, urllib.request
from collections import Counter, OrderedDict

SID = "1HPmYJb-GzbH7OVzxXJw5l6bSA89gK3Wd5aRn3KHrSX0"
url = f"https://docs.google.com/spreadsheets/d/{SID}/gviz/tq?tqx=out:csv&headers=1&sheet=data"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
data = urllib.request.urlopen(req, timeout=30).read().decode("utf-8")
rows = list(csv.reader(io.StringIO(data)))
header, records = rows[0], rows[1:]

out = io.StringIO()
def w(*a): print(*a, file=out)
w(f"courses: {len(records)}   columns: {len(header)}")
w("headers:", header)

facets = ["분야", "대상", "이수구분", "교육방식", "담당부서", "정원", "교육시간"]
idx = {h: i for i, h in enumerate(header)}
for f in facets:
    i = idx[f]
    c = Counter(r[i] for r in records)
    w(f"\n[{f}]  ({len(c)} distinct)")
    for k, n in c.most_common():
        w(f"   {n:>2}  {k}")

# code prefix -> 분야 mapping sanity
w("\n[code prefix vs 분야]")
for r in records:
    pass
w("\nsample 신청기간 / 교육기간 patterns:")
for r in records[:6]:
    w(f"   {r[idx['과정코드']]}: 기간={r[idx['교육기간']]!r}  신청={r[idx['신청기간']]!r}")

open(r"C:\Users\user\Downloads\웹사이트개발\2026-07-10\data_profile.txt","w",encoding="utf-8").write(out.getvalue())
print("done")

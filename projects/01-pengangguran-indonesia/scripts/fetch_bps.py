#!/usr/bin/env python3
# Script sederhana untuk mengakses BPS WebAPI v2 (Tenaga Kerja)
#
# SKEMA API:
# https://web-api.bps.go.id/v2/api/list/model/{model}/lang/{lang}/domain/{domain}/subject/{subj}/key/{API_KEY}/
# https://web-api.bps.go.id/v2/api/list/model/{model}/lang/{lang}/domain/{domain}/var/{var}/th/{th}/key/{API_KEY}/
#
# Param:
# model: var (list variabel di subjek), subject, data (data tabel)
# lang: ind
# domain: 0000 (nasional)
# th: 0 berarti semua tahun
#
# Dapatkan API key gratis di: https://webapi.bps.go.id/

import os, sys, json, csv
from urllib.request import urlopen, Request

HOST = "https://web-api.bps.go.id"
API_KEY = os.getenv("BPS_API_KEY") or os.getenv("BPS_APIKEY")

def get(url, api_key=None):
    if api_key and "/key/" not in url:
        url = url.rstrip("/") + "/key/" + api_key + "/"
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode("utf-8", "replace"))

def list_vars(subject=520, domain="0000", api_key=API_KEY):
    url = f"{HOST}/v2/api/list/model/var/lang/ind/domain/{domain}/subject/{subject}/"
    return get(url, api_key)

def fetch_data(var=543, th=0, domain="0000", lang="ind", api_key=API_KEY):
    url = f"{HOST}/v2/api/list/model/data/lang/{lang}/domain/{domain}/var/{var}/th/{th}/"
    return get(url, api_key)

def data_to_csv(data_json, out_path):
    try:
        d = data_json.get("data", data_json)
        vervar = {v["val"]: v.get("label") for v in d.get("vervar", [])}
        datacontent = d.get("datacontent", {})
        tahun = (d.get("tahun") or [{}])[0].get("label") or ""
        turtahun = (d.get("turtahun") or [{}])[0].get("label") or ""
        varinfo = (d.get("var") or [{}])[0]
        rows = []
        for k, val in datacontent.items():
            vcode = str(k)[:4]
            rows.append((vcode, vervar.get(str(vcode), vcode), tahun, turtahun, float(val)))
        rows.sort(key=lambda r: r[0])
        with open(out_path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["provinsi_kode", "provinsi", "tahun", "periode", "tpt"])
            w.writerows(rows)
        print("CSV saved:", out_path, "rows:", len(rows), "var:", varinfo.get("label"))
    except Exception as e:
        print("err", e)
        json.dump(data_json, open(out_path.replace(".csv", ".json"), "w", encoding="utf-8"), indent=2)

if __name__ == "__main__":
    if not API_KEY:
        print("BPS_API_KEY belum diset. Contoh: set BPS_API_KEY=xxx")
        sys.exit(1)
    args = sys.argv[1:]
    if not args:
        print("Gunakan: list-vars [subject] | data [var] [th=0]")
        sys.exit(1)
    cmd = args[0]
    if cmd == "list-vars":
        subj = int(args[1]) if len(args) > 1 else 520
        r = list_vars(subj, api_key=API_KEY)
        print(json.dumps(r, ensure_ascii=False, indent=2))
        print()
        print("URL didapat. Kalau status OK, bisa lanjut data <var> <th>")
    elif cmd == "data":
        var = int(args[1]) if len(args) > 1 else 543
        th = int(args[2]) if len(args) > 2 else 0
        r = fetch_data(var, th, api_key=API_KEY)
        out = f"projects/01-pengangguran-indonesia/data/raw/tpt_{var}_th{th}.csv"
        data_to_csv(r, out)
    else:
        print("cmd tak dikenal: list-vars/data")

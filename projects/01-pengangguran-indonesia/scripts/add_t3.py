import json

path='projects/01-pengangguran-indonesia/notebooks/01_cleaning.ipynb'
with open(path, encoding='utf-8') as f:
    nb=json.load(f)

md={'cell_type':'markdown','id':'t3-clean','metadata':{},'source':[
    '## Tahap 3 - Data Cleaning (provinsi - sampel 2026 Feb)',
    'Catatan: file ini adalah sampel dari payload SSR BPS. Struktur sudah rapi.',
    '- Cek duplikasi (kode provinsi)',
    "- Pisahkan baris total 'INDONESIA' (tidak dipakai untuk ranking provinsi)",
    '- Pastikan tipe numerik (tpt float)',
    '- Simpan ke data/clean/tpt_provinsi_clean.csv'
]}
code={'cell_type':'code','execution_count':None,'id':'t3-code','metadata':{},'outputs':[],'source':[
    'import pandas as pd',
    "df = pd.read_csv('../data/raw/tpt_provinsi_bps_embed.csv')",
    "print('shape:', df.shape, 'unik kode:', df['provinsi_kode'].nunique())",
    "df_clean = df[df['provinsi'] != 'INDONESIA'].copy()",
    "df_clean['tpt'] = pd.to_numeric(df_clean['tpt'], errors='coerce')",
    "df_clean.to_csv('../data/clean/tpt_provinsi_clean.csv', index=False)",
    'df_clean.head(5)'
]}
nb['cells'].append(md)
nb['cells'].append(code)
with open(path,'w',encoding='utf-8') as f:
    json.dump(nb,f,indent=1)
    f.write('\n')
print('done')

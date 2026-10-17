import json

path='projects/01-pengangguran-indonesia/notebooks/02_eda.ipynb'
nb={'cells':[],'metadata':{'kernelspec':{'display_name':'Python (Voiceover)','language':'python','name':'voiceover'},'language_info':{'name':'python','version':'3.14.8'}},'nbformat':4,'nbformat_minor':5}
md={'cell_type':'markdown','id':'eda1','metadata':{},'source':[
    '## Tahap 4 - EDA (provinsi, sampel 1 periode)',
    '**Keterbatasan:** Data hanya tersedia untuk Februari 2026 (1 periode). Tren multi-tahun belum bisa dianalisis; fokus pada ranking provinsi, distribusi, dan kesenjangan antar provinsi.'
]}
code={'cell_type':'code','execution_count':None,'id':'eda1c','metadata':{},'outputs':[],'source':[
    'import pandas as pd, numpy as np, matplotlib.pyplot as plt, seaborn as sns',
    "df = pd.read_csv('../data/clean/tpt_provinsi_clean.csv')",
    'df.head(5)'
]}
md2={'cell_type':'markdown','id':'eda2','metadata':{},'source':['### 4.1 Statistik deskriptif & ranking provinsi']}
code2={'cell_type':'code','execution_count':None,'id':'eda2c','metadata':{},'outputs':[],'source':[
    'df.describe()',
    '',
    '# Ranking tertinggi & terendah',
    "df.sort_values('tpt', ascending=False)[['provinsi','tpt']].head(5)",
    '',
    '# Bottom 5',
    "df.sort_values('tpt', ascending=True)[['provinsi','tpt']].head(5)"
]}
nb['cells']=[md,code,md2,code2]
with open(path,'w',encoding='utf-8') as f:
    json.dump(nb,f,indent=1)
    f.write('\n')
print('done')

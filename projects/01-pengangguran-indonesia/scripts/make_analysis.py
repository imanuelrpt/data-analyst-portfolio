import json

path='projects/01-pengangguran-indonesia/notebooks/03_analysis.ipynb'
nb={'cells':[],'metadata':{'kernelspec':{'display_name':'Python (Voiceover)','language':'python','name':'voiceover'},'language_info':{'name':'python','version':'3.14.8'}},'nbformat':4,'nbformat_minor':5}
md={'cell_type':'markdown','id':'a1','metadata':{},'source':['## Tahap 5 - Analisis lanjutan sederhana','Fokus: ranking, gap, distribusi. Keterbatasan: hanya 1 periode (Feb 2026).']}
code={'cell_type':'code','execution_count':None,'id':'a1c','metadata':{},'outputs':[],'source':[
    'import pandas as pd, numpy as np',
    "df=pd.read_csv('../data/clean/tpt_provinsi_clean.csv')",
    "df.sort_values('tpt',ascending=False)[['provinsi','tpt']]"
]}
md2={'cell_type':'markdown','id':'a2','metadata':{},'source':['### Gap & ringkasan']}
code2={'cell_type':'code','execution_count':None,'id':'a2c','metadata':{},'outputs':[],'source':[
    "print('Gap max-min:', df['tpt'].max()-df['tpt'].min())",
    "print('Rerata/median:', df['tpt'].mean().round(2), df['tpt'].median().round(2))",
    "df.describe()"
]}
nb['cells']=[md,code,md2,code2]
with open(path,'w',encoding='utf-8') as f:
    json.dump(nb,f,indent=1)
    f.write('\n')
print('done')

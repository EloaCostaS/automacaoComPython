import pandas as pd
import unicodedata
from rapidfuzz import process, fuzz

def limpar(col):
col = col.astype(str).str.lower().str.strip()
col = col.str.replace(r'\s+', ' ', regex=True)
col = col.apply(lambda x: unicodedata.normalize('NFKD', x).encode('ascii', 'ignore').decode('utf-8'))
return col

anuncios = pd.read_excel(
'Anuncios-2026_04_15-09_14.xlsx',
sheet_name='Anúncios',
usecols='E,G',
skiprows=2
)

anuncios.columns = ['produto', 'estoque_p1']
anuncios = anuncios.dropna(subset=['produto'])
anuncios['produto'] = limpar(anuncios['produto'])
anuncios['estoque_p1'] = pd.to_numeric(anuncios['estoque_p1'], errors='coerce')

fichas_dict = pd.read_excel(
'Fichas_tecnicas-2026_04_15-10_34.xlsx',
sheet_name=None
)

lista = []

for nome_aba, df in fichas_dict.items():
if nome_aba.lower() == 'ajuda':
continue

```
df = df.iloc[4:].reset_index(drop=True)
df = df.iloc[:, [3, 8]]
df.columns = ['sku', 'produto']

df = df.dropna()
df['produto'] = limpar(df['produto'])
df['sku'] = df['sku'].astype(str).str.strip()

lista.append(df)
```

fichas = pd.concat(lista, ignore_index=True)

fichas_validos = fichas.groupby('produto').filter(lambda x: x['sku'].nunique() == 1)
fichas_validos = fichas_validos.drop_duplicates('produto')

mapa_prod_sku = dict(zip(fichas_validos['produto'], fichas_validos['sku']))

anuncios['sku'] = anuncios['produto'].map(mapa_prod_sku)

anuncios['match_tipo'] = anuncios['sku'].apply(
lambda x: 'exato' if pd.notna(x) else 'pendente'
)

lista_produtos_fichas = fichas_validos['produto'].tolist()

def validar_match(produto, produto_match):
palavras_criticas = ['zero', 'light', 'diet', 'integral']

```
for p in palavras_criticas:
    if (p in produto) != (p in produto_match):
        return False

return True
```

def encontrar_sku_aproximado(produto):
match = process.extractOne(
produto,
lista_produtos_fichas,
scorer=fuzz.token_sort_ratio
)

```
if match:
    produto_match, score, _ = match

    if score >= 96 and validar_match(produto, produto_match):
        return mapa_prod_sku.get(produto_match)

return None
```

mask = anuncios['sku'].isna()

anuncios.loc[mask, 'sku'] = anuncios.loc[mask, 'produto'].apply(encontrar_sku_aproximado)

anuncios.loc[mask & anuncios['sku'].notna(), 'match_tipo'] = 'fuzzy'
anuncios.loc[anuncios['sku'].isna(), 'match_tipo'] = 'sem match'

deposito = pd.read_excel(
'DepositoAtualizado.xlsx',
usecols='B,H',
skiprows=1
)

deposito.columns = ['estoque_p3', 'sku']
deposito = deposito.dropna(subset=['sku'])

deposito['sku'] = deposito['sku'].astype(str).str.strip()
deposito['estoque_p3'] = pd.to_numeric(deposito['estoque_p3'], errors='coerce')

final = pd.merge(anuncios, deposito, on='sku', how='left')

def classificar(row):
if pd.isna(row['sku']):
return 'Produto sem SKU'
if pd.isna(row['estoque_p3']):
return 'SKU não encontrado no depósito'
if row['estoque_p1'] == row['estoque_p3']:
return 'Estoque correto'
return 'Diferença de estoque'

final['status'] = final.apply(classificar, axis=1)

print("\n📊 Resumo de matching:")
print(anuncios['match_tipo'].value_counts())

problemas = anuncios[anuncios['match_tipo'] == 'sem match']
problemas.to_excel('produtos_sem_sku.xlsx', index=False)

final.to_excel('resultado_conferencia.xlsx', index=False)

colunas_export = [
'produto',
'sku',
'estoque_p1',
'estoque_p3',
'match_tipo',
'status'
]

for col in colunas_export:
if col not in final.columns:
final[col] = None

exato = final[final['match_tipo'] == 'exato'][colunas_export]
fuzzy = final[final['match_tipo'] == 'fuzzy'][colunas_export]
sem_match = final[final['match_tipo'] == 'sem match'][colunas_export]

exato.to_excel('01_exato_completo.xlsx', index=False)
fuzzy.to_excel('02_fuzzy_revisar_completo.xlsx', index=False)
sem_match.to_excel('03_sem_match_completo.xlsx', index=False)

print("\n📁 Arquivos completos gerados:")
print("- 01_exato_completo.xlsx")
print("- 02_fuzzy_revisar_completo.xlsx")
print("- 03_sem_match_completo.xlsx")
print("\n✅ Processo finalizado com segurança (sem SKU inventado!)")

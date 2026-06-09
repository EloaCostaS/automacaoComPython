# =========================================================
# ARQUIVOS
# =========================================================

ARQUIVO_SHOPEE = 'mass_update_sales_info_1357391682_20260521211831.xlsx'
ARQUIVO_DEPOSITO = 'DepositoAtualizado.xlsx'

ARQUIVO_NAO_ENCONTRADOS = 'skus_nao_encontrados.xlsx'

# =========================================================
# CARREGAR DEPÓSITO (SKU -> ESTOQUE)
# =========================================================

deposito = pd.read_excel(
    ARQUIVO_DEPOSITO,
    header=None,
    skiprows=1,
    engine='calamine'
)

# Coluna B = estoque (1)
# Coluna H = sku (7)
deposito = deposito.iloc[:, [1, 7]]
deposito.columns = ['estoque', 'sku']

deposito['sku'] = (
    deposito['sku']
    .astype(str)
    .str.strip()
)

deposito['estoque'] = pd.to_numeric(
    deposito['estoque'],
    errors='coerce'
).fillna(0)

# remove duplicados
deposito = deposito.drop_duplicates(subset='sku')

# mapa sku -> estoque
mapa_estoque = dict(zip(deposito['sku'], deposito['estoque']))

# =========================================================
# ABRIR SHOPEE (EDITA ORIGINAL)
# =========================================================

wb = load_workbook(ARQUIVO_SHOPEE)
ws = wb.active

# =========================================================
# LISTA DE NÃO ENCONTRADOS
# =========================================================

nao_encontrados = []

# =========================================================
# PROCESSO
# =========================================================

for linha in range(7, ws.max_row + 1):

    try:
        sku_e = str(ws[f'E{linha}'].value).strip()
        sku_f = str(ws[f'F{linha}'].value).strip()

        # regra: se E > 6 caracteres usa F
        if len(sku_e) > 6:
            sku = sku_f
        else:
            sku = sku_e

        sku = str(sku).strip()

        if sku in ['', 'nan', 'None']:
            continue

        # busca estoque
        if sku in mapa_estoque:
            estoque = mapa_estoque[sku]
        else:
            estoque = 0
            nao_encontrados.append({
                'linha': linha,
                'sku': sku
            })

        # atualiza SOMENTE coluna I
        ws[f'I{linha}'] = estoque

    except Exception as e:
        nao_encontrados.append({
            'linha': linha,
            'sku': f'ERRO: {e}'
        })

# =========================================================
# SALVAR NA MESMA PLANILHA (ORIGINAL EDITADO)
# =========================================================

wb.save(ARQUIVO_SHOPEE)

# =========================================================
# EXPORTAR NÃO ENCONTRADOS
# =========================================================

pd.DataFrame(nao_encontrados).to_excel(
    ARQUIVO_NAO_ENCONTRADOS,
    index=False
)

# =========================================================
# RESUMO
# =========================================================

print("\n====================================")
print("✅ FINALIZADO COM SUCESSO")
print("====================================")

print(f"\n📦 SKUs não encontrados: {len(nao_encontrados)}")

print("\n📁 Arquivos gerados:")
print(f"- {ARQUIVO_NAO_ENCONTRADOS}")

print("\n✔ Arquivo Shopee atualizado diretamente")
print("✔ Apenas coluna I foi alterada")

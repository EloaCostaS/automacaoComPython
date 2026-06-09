import pandas as pd

# =========================================================
# ARQUIVOS
# =========================================================

ARQUIVO_SHOPEE = "mass_update_sales_info_1357391682_20260521211831.xlsx"
ARQUIVO_DEPOSITO = "DepositoAtualizado.xlsx"

# =========================================================
# DEPÓSITO
# =========================================================

deposito = pd.read_excel(
    ARQUIVO_DEPOSITO,
    header=None,
    skiprows=1,
    engine="calamine"
)

deposito = deposito.iloc[:, [1, 7]]
deposito.columns = ["estoque", "sku"]

deposito["sku"] = deposito["sku"].astype(str).str.strip()
deposito["estoque"] = pd.to_numeric(deposito["estoque"], errors="coerce").fillna(0)

mapa_estoque = dict(zip(deposito["sku"], deposito["estoque"]))

# =========================================================
# SHOPEE
# =========================================================

shopee = pd.read_excel(
    ARQUIVO_SHOPEE,
    header=None,
    engine="calamine"
)

# =========================================================
# CONFERÊNCIA REAL
# =========================================================

lista_erros = []

for i in range(6, len(shopee)):

    sku_e = str(shopee.iat[i, 4]).strip()
    sku_f = str(shopee.iat[i, 5]).strip()

    sku = sku_f if len(sku_e) > 6 else sku_e
    sku = str(sku).strip()

    if sku in ["", "nan", "None"]:
        continue

    estoque_shopee = shopee.iat[i, 8]

    # normaliza estoque
    try:
        estoque_shopee = float(estoque_shopee)
    except:
        estoque_shopee = 0

    if sku not in mapa_estoque:

        if estoque_shopee != 0:
            lista_erros.append((i + 1, sku, "DEVERIA SER 0 MAS NÃO É"))

        continue

    estoque_correto = float(mapa_estoque[sku])

    if estoque_shopee != estoque_correto:
        lista_erros.append((i + 1, sku, f"{estoque_shopee} != {estoque_correto}"))

# =========================================================
# RESULTADO CORRIGIDO
# =========================================================

print("\n==============================")
print("🔍 RELATÓRIO DE CONFERÊNCIA")
print("==============================")

print(f"\n❌ Total real de erros: {len(lista_erros)}")

print("\nExemplos de erros:")
for e in lista_erros[:20]:
    print(e)
    
print("\nDEBUG PRIMEIRAS LINHAS SHOPEE:\n")

for i in range(6, 15):
    print(
        "linha", i+1,
        "| E:", shopee.iat[i, 4],
        "| F:", shopee.iat[i, 5],
        "| I:", shopee.iat[i, 8]
    )

print("\nCHECK DEPÓSITO VS SHOPEE:\n")

for i in range(6, 15):

    sku_e = str(shopee.iat[i, 4]).strip()
    sku = sku_e

    print(
        "SKU:",
        sku,
        "| Shopee:",
        shopee.iat[i, 8],
        "| Depósito:",
        mapa_estoque.get(sku, "❌ NÃO ENCONTRADO")
    )
print("\n==============================")
print("✔ CONFERÊNCIA FINALIZADA")
print("==============================")

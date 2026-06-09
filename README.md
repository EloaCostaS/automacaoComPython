# automacaoComPython
# Automação de Conferência e Atualização de Estoque

## Visão Geral

Este projeto foi desenvolvido para automatizar processos de conferência e atualização de estoque entre o depósito e marketplaces.

A evolução ocorreu em três etapas:

1. Conferência de estoque no Mercado Livre.
2. Atualização automática de estoque na Shopee.
3. Validação da atualização realizada na Shopee.

O objetivo foi reduzir o tempo operacional e eliminar tarefas repetitivas realizadas manualmente.

---

# 1. Conferência de Estoque - Mercado Livre

## Problema Inicial

No início do processo, a conferência era realizada manualmente.

O fluxo era:

1. Exportar anúncios do Mercado Livre.
2. Exportar estoque do depósito.
3. Localizar o SKU de cada produto.
4. Comparar os estoques.
5. Corrigir divergências manualmente.

Com o volume de produtos existente, essa atividade consumia aproximadamente **3 semanas de trabalho**.

---

## Solução Desenvolvida

Foi criado um sistema de identificação automática de SKUs e comparação de estoques.

O script:

* Lê os anúncios do Mercado Livre.
* Lê as fichas técnicas contendo SKU dos produtos.
* Localiza automaticamente o SKU correspondente.
* Compara o estoque anunciado com o estoque do depósito.
* Gera relatórios organizados para análise.

---

## Processo de Identificação

### Match Exato

Primeiramente o sistema procura correspondências exatas entre o nome do anúncio e o nome cadastrado nas fichas técnicas.

Quando encontra:

* Produto recebe o status **Exato**.
* SKU é associado automaticamente.

---

### Match Aproximado (Fuzzy Match)

Quando não existe correspondência exata, é utilizada comparação textual.

Isso permite identificar produtos escritos de formas ligeiramente diferentes.

Exemplo:

* Martelo Unha 25mm
* Martelo Unha 25 mm

Para evitar erros:

* Apenas similaridades acima de 96% são aceitas.
* Palavras críticas devem coincidir exatamente.

Palavras protegidas:

* Zero
* Light
* Diet
* Integral

---

## Resultado

O sistema gera relatórios contendo:

* Produtos corretos.
* Produtos com estoque divergente.
* Produtos sem SKU.
* Produtos que necessitam revisão.

Arquivos gerados:

* resultado_conferencia.xlsx
* 01_exato_completo.xlsx
* 02_fuzzy_revisar_completo.xlsx
* 03_sem_match_completo.xlsx
* produtos_sem_sku.xlsx

---

## Ganho Operacional

Antes:

* Aproximadamente 3 semanas.
* Conferência totalmente manual.

Depois:

* Aproximadamente 1 semana.
* Localização automática das divergências.
* Correções ainda realizadas manualmente dentro do Mercado Livre.

O script não atualizava o marketplace. Seu objetivo era apenas apontar quais SKUs possuíam estoque incorreto.

---

# 2. Atualização Automática de Estoque - Shopee

## Evolução do Processo

Após automatizar a conferência do Mercado Livre, o próximo passo foi automatizar também a atualização dos estoques.

Ao invés de apenas identificar diferenças, o sistema passou a preencher automaticamente a planilha de atualização em massa da Shopee.

---

## Funcionamento

O script realiza:

1. Leitura da planilha do depósito.
2. Criação de um mapa SKU → Estoque.
3. Abertura da planilha exportada pela Shopee.
4. Localização dos SKUs.
5. Atualização automática dos estoques.

Para cada SKU:

* Se existir no depósito, recebe o estoque correto.
* Se não existir, recebe estoque zero.

Os SKUs não encontrados são registrados em um relatório separado.

---

## Segurança

O script altera apenas a coluna de estoque da planilha da Shopee.

Nenhuma outra informação do anúncio é modificada.

---

## Arquivos Gerados

* Planilha original da Shopee atualizada.
* skus_nao_encontrados.xlsx

---

## Processo Final

Após a execução:

1. A planilha já fica pronta para envio.
2. Basta acessar a Shopee.
3. Utilizar a função de atualização em massa.
4. Importar a própria planilha gerada pelo script.

Nenhuma correção manual é necessária na maioria dos casos.

---

## Ganho Operacional

Antes:

* Aproximadamente 3 semanas de conferência e atualização.

Depois:

* Aproximadamente 1 dia para concluir todo o processo.

A maior parte do trabalho passou a ser executada automaticamente.

---

# 3. Conferência da Atualização Shopee

## Objetivo

Após automatizar a atualização dos estoques, foi criado um segundo script para validar se a planilha gerada estava realmente correta.

Esse processo funciona como uma auditoria.

O script não altera arquivos.

Ele apenas verifica.

---

## Funcionamento

Para cada SKU presente na planilha:

1. Localiza o SKU.
2. Obtém o estoque presente na planilha da Shopee.
3. Obtém o estoque correspondente do depósito.
4. Compara os valores.

---

## Validações

### SKU Encontrado

O estoque da planilha deve ser exatamente igual ao estoque do depósito.

Caso exista diferença:

* O erro é registrado.

---

### SKU Não Encontrado

O estoque esperado é zero.

Caso exista qualquer valor diferente:

* O erro é registrado.

---

## Resultado

Ao final da execução são exibidos:

* Quantidade total de erros encontrados.
* Exemplos das divergências.
* Dados de depuração para conferência.
* Comparação direta entre Shopee e depósito.

---

## Objetivo da Conferência

Garantir que:

* O script de atualização funcionou corretamente.
* Nenhum SKU foi atualizado incorretamente.
* Os estoques enviados para a Shopee são exatamente os mesmos do depósito.

---

# Evolução do Projeto

| Etapa              | Processo                                 | Tempo Médio    |
| ------------------ | ---------------------------------------- | -------------- |
| Inicial            | Conferência totalmente manual            | ~3 semanas     |
| Mercado Livre      | Identificação automática de divergências | ~1 semana      |
| Shopee             | Atualização automática por planilha      | ~1 dia         |
| Conferência Shopee | Validação automática da atualização      | Alguns minutos |

---

# Resultado Final

O projeto evoluiu de uma operação totalmente manual para um fluxo automatizado capaz de:

* Identificar SKUs automaticamente.
* Comparar estoques.
* Gerar relatórios.
* Atualizar estoques em massa.
* Validar os resultados da atualização.

Isso reduziu drasticamente o tempo operacional, aumentou a confiabilidade das informações e diminuiu a necessidade de intervenção manual.


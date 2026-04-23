import requests

# Lista de títulos para monitorar: [Nome do Título, Preço Alvo]
MEUS_TITULOS = [
    ["Tesouro Prefixado com Juros Semestrais 2033", 963.016],
    ["Tesouro Prefixado com Juros Semestrais 2031", 1.054,29],
    ["Tesouro Prefixado com Juros Semestrais 2035", 899,71]
]

# Porcentagem de diferença para disparar o aviso (ex: -1.0 significa 1% mais barato que o alvo)
MARGEM_ALERTA = -1.0

def buscar_precos_tesouro():
    url = "https://www.tesourodireto.com.br/json/br/com/b3/tesourodireto/service/api/treasurybondprice/daily"
    try:
        response = requests.get(url)
        data = response.json()
        return data['response']['TrsuryBdTradgList']
    except Exception as e:
        print(f"Erro ao acessar dados: {e}")
        return []

def monitorar():
    lista_mercado = buscar_precos_tesouro()
    
    print("--- RELATÓRIO DE RESGATE ---")
    for item in lista_mercado:
        nome_mercado = item['TrsuryBd']['nm']
        # ALTERADO: Agora busca o preço de resgate (venda antecipada)
        preco_resgate = item['TrsuryBd']['untrRedmPric'] 
        
        for meu_titulo, preco_alvo in MEUS_TITULOS:
            if nome_mercado == meu_titulo:
                diff = ((preco_resgate - preco_alvo) / preco_alvo) * 100
                
                status = "DENTRO DO ALVO 🚨" if diff <= MARGEM_ALERTA else "Acima do alvo"
                
                print(f"Título: {nome_mercado}")
                print(f"  Preço de Resgate: R$ {preco_resgate:.2f} | Alvo: R$ {preco_alvo:.2f}")
                print(f"  Diferença: {diff:.2f}% | Status: {status}")
                print("-" * 20)

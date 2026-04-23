import requests

# Configure aqui seus títulos e valores de referência
MEUS_TITULOS = [
["Tesouro Prefixado com Juros Semestrais 2033", 963.016],
    ["Tesouro Prefixado com Juros Semestrais 2031", 1054.29],
    ["Tesouro Prefixado com Juros Semestrais 2035", 899.71]
]

def monitorar():
    url = "https://www.tesourodireto.com.br/json/br/com/b3/tesourodireto/service/api/treasurybondprice/daily"
    
    try:
        response = requests.get(url)
        data = response.json()
        lista_mercado = data['response']['TrsuryBdTradgList']
        
        print("--- MONITORAMENTO DE PREÇOS (RESGATE) ---")
        
        for item in lista_mercado:
            nome_mercado = item['TrsuryBd']['nm'].strip()
            preco_resgate = item['TrsuryBd']['untrRedmPric']
            
            for meu_titulo, preco_alvo in MEUS_TITULOS:
                if nome_mercado == meu_titulo.strip():
                    # Cálculo da diferença percentual
                    diff = ((preco_resgate - preco_alvo) / preco_alvo) * 100
                    
                    print(f"Título: {nome_mercado}")
                    print(f"  Preço Atual: R$ {preco_resgate:.2f}")
                    print(f"  Preço Alvo:  R$ {preco_alvo:.2f}")
                    print(f"  Diferença:   {diff:.2f}%")
                    print("-" * 30)
                    
    except Exception as e:
        print(f"Erro ao processar dados: {e}")

if __name__ == "__main__":
    monitorar()

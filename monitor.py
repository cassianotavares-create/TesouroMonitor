import requests

# COLAR API
API_KEY_PROXY = "99f7237f-e897-4ed3-9058-a086025aa43d"

# Configure aqui seus títulos e valores de referência
MEUS_TITULOS = [
["Tesouro Prefixado com Juros Semestrais 2033", 963.016],
    ["Tesouro Prefixado com Juros Semestrais 2031", 1054.29],
    ["Tesouro Prefixado com Juros Semestrais 2035", 899.71]
]

def monitorar():
    # URL da página de preços que contém os dados embutidos
    url = "https://www.tesourodireto.com.br/titulos/precos-e-taxas.htm"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers, timeout=20)
        
        if response.status_code != 200:
            print(f"Erro ao acessar site: {response.status_code}")
            return

        # O site do Tesouro coloca os dados dentro de uma variável JavaScript no HTML
        # Vamos tentar extrair os dados brutos se o JSON direto falhar
        conteudo = response.text
        
        # Tentativa de buscar a API interna atualizada
        api_url = "https://www.tesourodireto.com.br/json/br/com/b3/tesourodireto/service/api/treasurybondprice/daily"
        res_api = requests.get(api_url, headers=headers, timeout=20)
        
        if res_api.status_code == 200:
            data = res_api.json()
            lista_mercado = data['response']['TrsuryBdTradgList']
            
            print("--- MONITORAMENTO DE PREÇOS (RESGATE) ---")
            for item in lista_mercado:
                nome_mercado = item['TrsuryBd']['nm'].strip()
                preco_resgate = item['TrsuryBd']['untrRedmPric']
                
                for meu_titulo, preco_alvo in MEUS_TITULOS:
                    if nome_mercado == meu_titulo.strip():
                        diff = ((preco_resgate - preco_alvo) / preco_alvo) * 100
                        print(f"Título: {nome_mercado}")
                        print(f"  Preço Atual: R$ {preco_resgate:.2f}")
                        print(f"  Preço Alvo:  R$ {preco_alvo:.2f}")
                        print(f"  Diferença:   {diff:.2f}%")
                        print("-" * 30)
        else:
            print(f"A API retornou erro {res_api.status_code}. Provavelmente mercado fechado ou link alterado.")

    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    monitorar()

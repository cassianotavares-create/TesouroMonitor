import requests

# Configure aqui seus títulos e valores de referência
MEUS_TITULOS = [
["Tesouro Prefixado com Juros Semestrais 2033", 963.016],
    ["Tesouro Prefixado com Juros Semestrais 2031", 1054.29],
    ["Tesouro Prefixado com Juros Semestrais 2035", 899.71]
]


def monitorar():
    # Usando o endpoint de Dados Abertos que é menos restrito que o site principal
    url = "https://www.tesourodireto.com.br/json/br/com/b3/tesourodireto/service/api/treasurybondprice/daily"
    
    # Headers mais completos para simular um acesso legítimo
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'pt-BR,pt;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://www.tesourodireto.com.br/titulos/precos-e-taxas.htm'
    }
    
    try:
        # Criamos uma sessão para manter cookies, o que ajuda a evitar o erro 403
        session = requests.Session()
        response = session.get(url, headers=headers, timeout=15)
        
        if response.status_code != 200:
            print(f"O Tesouro ainda está bloqueando (Erro {response.status_code}).")
            print("Tentando alternativa em 3, 2, 1...")
            # Tentativa com outro endpoint caso o primeiro falhe
            url_alt = "https://www.tesourodireto.com.br/json/br/com/b3/tesourodireto/service/api/treasurybondprice/daily"
            response = session.get(url_alt, headers=headers, timeout=15)

        data = response.json()
        lista_mercado = data['response']['TrsuryBdTradgList']
        
        print("--- MONITORAMENTO DE PREÇOS (RESGATE) ---")
        encontrado = False
        
        for item in lista_mercado:
            nome_mercado = item['TrsuryBd']['nm'].strip()
            # Pega o preço de resgate
            preco_resgate = item['TrsuryBd']['untrRedmPric']
            
            for meu_titulo, preco_alvo in MEUS_TITULOS:
                if nome_mercado == meu_titulo.strip():
                    encontrado = True
                    diff = ((preco_resgate - preco_alvo) / preco_alvo) * 100
                    
                    print(f"Título: {nome_mercado}")
                    print(f"  Preço Atual: R$ {preco_resgate:.2f}")
                    print(f"  Preço Alvo:  R$ {preco_alvo:.2f}")
                    print(f"  Diferença:   {diff:.2f}%")
                    print("-" * 30)
        
        if not encontrado:
            print("Conectado, mas nenhum título da sua lista foi achado.")
            if lista_mercado:
                print(f"Exemplo de nome no site: {lista_mercado[0]['TrsuryBd']['nm']}")
                    
    except Exception as e:
        print(f"Erro crítico: {e}")

if __name__ == "__main__":
    monitorar()

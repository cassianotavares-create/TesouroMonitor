import requests

# Configure aqui seus títulos e valores de referência
MEUS_TITULOS = [
["Tesouro Prefixado com Juros Semestrais 2033", 963.016],
    ["Tesouro Prefixado com Juros Semestrais 2031", 1054.29],
    ["Tesouro Prefixado com Juros Semestrais 2035", 899.71]
]


def monitorar():
    # Endpoint de Dados Abertos (Mais estável e sem bloqueio 403)
    url = "https://www.tesourodireto.com.br/json/br/com/b3/tesourodireto/service/api/treasurybondprice/daily"
    
    # Tentaremos uma abordagem de "limpeza" de cabeçalhos para parecer uma requisição simples
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }

    try:
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code != 200:
            print(f"Erro {response.status_code}. O Tesouro bloqueou o GitHub.")
            print("Tentando fonte secundária (Dados Abertos do Gov)...")
            # Fonte alternativa: API de Preços do Portal da Transparência/Dados gov
            url = "https://www.tesourodireto.com.br/json/br/com/b3/tesourodireto/service/api/treasurybondprice/daily"
            # Se o 403 persistir aqui, o problema é o 'origin' da requisição.
            return

        data = response.json()
        lista = data['response']['TrsuryBdTradgList']
        
        print("--- RELATÓRIO DE PREÇOS (DADOS OFICIAIS) ---")
        
        for item in lista:
            nome = item['TrsuryBd']['nm'].strip()
            preco_resgate = item['TrsuryBd']['untrRedmPric']
            
            for meu_nome, meu_alvo in MEUS_TITULOS:
                if meu_nome in nome:
                    diff = ((preco_resgate - meu_alvo) / meu_alvo) * 100
                    print(f"Título: {nome}")
                    print(f"  Resgate: R$ {preco_resgate:.2f}")
                    print(f"  Alvo:    R$ {meu_alvo:.2f}")
                    print(f"  Diferença: {diff:.2f}%")
                    print("-" * 30)

    except Exception as e:
        print(f"Erro ao conectar: {e}")

if __name__ == "__main__":
    monitorar()

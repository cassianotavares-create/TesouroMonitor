import requests

# Configure aqui seus títulos e valores de referência
MEUS_TITULOS = [
["Tesouro Prefixado com Juros Semestrais 2033", 963.016],
    ["Tesouro Prefixado com Juros Semestrais 2031", 1054.29],
    ["Tesouro Prefixado com Juros Semestrais 2035", 899.71]
]


def monitorar():
    url = "https://www.tesourodireto.com.br/json/br/com/b3/tesourodireto/service/api/treasurybondprice/daily"
    
    # Cabeçalho para fingir que é um navegador real e evitar o bloqueio
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        
        # Verifica se o site bloqueou o acesso (Status 403 ou 500)
        if response.status_code != 200:
            print(f"O site do Tesouro recusou a conexão. Status: {response.status_code}")
            return

        data = response.json()
        lista_mercado = data['response']['TrsuryBdTradgList']
        
        print("--- MONITORAMENTO DE PREÇOS (RESGATE) ---")
        encontrado = False
        
        for item in lista_mercado:
            nome_mercado = item['TrsuryBd']['nm'].strip()
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
            print("Conectado com sucesso, mas os nomes dos títulos não bateram.")
            print("Primeiro título da lista no site para conferência:", lista_mercado[0]['TrsuryBd']['nm'])
                    
    except Exception as e:
        print(f"Erro ao processar dados: {e}")

if __name__ == "__main__":
    monitorar()

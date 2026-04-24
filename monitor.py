import pandas as pd
import requests
from io import StringIO

# CONFIGURAÇÃO: [Nome do Título, Seu Preço Alvo]
MEUS_TITULOS = [
   ["Tesouro Prefixado com Juros Semestrais 2033", 963.016],
    ["Tesouro Prefixado com Juros Semestrais 2031", 1.054,29],
    ["Tesouro Prefixado com Juros Semestrais 2035", 899,71]
]

def monitorar_com_calculo():
    # URL de Dados Abertos (CSV oficial do Governo/B3)
    url = "https://www.tesourotransparente.gov.br/ckan/dataset/df56aa42-484a-4a59-813d-78e936048fbf/resource/79607951-344d-4c3e-a89b-00898553257a/download/PrecoTaxaTesouroDireto.csv"
    
    try:
        print("Acessando base de dados da B3...")
        response = requests.get(url, timeout=30)
        
        if response.status_code == 200:
            # Lendo o CSV brasileiro (separador ';' e decimal ',')
            df = pd.read_csv(StringIO(response.text), sep=';', decimal=',')
            
            # Ajustando a data para pegar os valores mais recentes
            df['Data Referencia'] = pd.to_datetime(df['Data Referencia'], dayfirst=True)
            ultima_data = df['Data Referencia'].max()
            df_recente = df[df['Data Referencia'] == ultima_data]

            print(f"\n--- MONITORAMENTO DE PREÇOS (Ref: {ultima_data.strftime('%d/%m/%Y')}) ---")
            
            for meu_nome, preco_alvo in MEUS_TITULOS:
                # O CSV separa o nome do vencimento. Ex: 'Tesouro IPCA+' e '15/05/2029'
                # Vamos buscar por uma combinação que contenha o nome e o ano
                ano_vencimento = meu_nome.split()[-1]
                tipo_titulo = " ".join(meu_nome.split()[:-1])
                
                filtro = df_recente[
                    (df_recente['Tipo Titulo'].str.contains(tipo_titulo, case=False)) & 
                    (df_recente['Data Vencimento'].str.contains(ano_vencimento))
                ]
                
                if not filtro.empty:
                    preco_atual = filtro.iloc[0]['Preco Unitario']
                    # A conta que você pediu:
                    diff = ((preco_atual - preco_alvo) / preco_alvo) * 100
                    
                    print(f"📌 {meu_nome}")
                    print(f"   Preço Mercado: R$ {preco_atual:.2f}")
                    print(f"   Preço Alvo:    R$ {preco_alvo:.2f}")
                    print(f"   Diferença:     {diff:.2f}%")
                    print("-" * 35)
                else:
                    print(f"⚠️ {meu_nome} não encontrado na lista oficial.")
        else:
            print(f"Erro ao baixar arquivo: {response.status_code}")

    except Exception as e:
        print(f"Erro no script: {e}")
        print("\nCertifique-se de que a biblioteca 'pandas' está instalada:")
        print("No terminal: pip install pandas")

if __name__ == "__main__":
    monitorar_com_calculo()

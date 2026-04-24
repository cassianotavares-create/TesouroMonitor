import requests
from datetime import datetime

# Aqui usamos os códigos oficiais do Banco Central (SGS)
# 11 = Selic, 188 = IPCA (Exemplos de taxas)
# Como o BC fornece taxas e o Tesouro fornece preços, vamos focar no que o BC libera sem travas:
TITULOS_BC = [
    {"nome": "Taxa SELIC", "codigo": "11"},
    {"nome": "IPCA (Mensal)", "codigo": "433"},
    {"nome": "CDI", "codigo": "12"}
]

def monitorar_via_bacen():
    print(f"--- CONSULTA BANCO CENTRAL ({datetime.now().strftime('%d/%m/%Y %H:%M')}) ---")
    
    for titulo in TITULOS_BC:
        url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{titulo['codigo']}/dados/ultimos/1?formato=json"
        
        try:
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                dados = response.json()
                valor = dados[0]['valor']
                data = dados[0]['data']
                print(f"✅ {titulo['nome']}: {valor}% (Última atualização: {data})")
            else:
                print(f"❌ Erro ao acessar {titulo['nome']}")
        except Exception as e:
            print(f"Erro: {e}")

if __name__ == "__main__":
    monitorar_via_bacen()

import requests
import pandas as pd

def consultar_serie_sgs(cod_serie, i_date, f_date):
  
  # 1. Parâmetros da requisição
  base_url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{cod_serie}/dados"
  parameters = {
    "formato": "json", 
    "dataInicial": i_date, 
    "dataFinal": f_date}

  # 2. Requisição HTTP
  response = requests.get(base_url, params=parameters, timeout=10)

  # 3. O que fazer quando devolve vazio (período sem dados no SGS)
  if response.status_code == 404 and "Value(s) not found" in response.text:
    return pd.DataFrame()

  # 4. O que fazer quando a API falha (dispara erro se status for 4xx ou 5xx)
  response.raise_for_status()

  df = pd.DataFrame(response.json())

  df['codigo_serie'] = cod_serie


  # 5. Resposta em JSON (transforma em objeto do Python)
  return df


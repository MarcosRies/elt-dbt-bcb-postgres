from python_files.extract import consultar_serie_sgs
from python_files.load import carregar_dados, engine

if __name__ == "__main__":

    codigo_serie = 11
    data_inicio = "01/01/2026"
    data_fim = "31/12/2026"

    print(f"Iniciando pipeline ETL para a série {codigo_serie}...")

    dados_brutos = consultar_serie_sgs(codigo_serie, data_inicio, data_fim)

    if not dados_brutos.empty:
        linhas_afetadas = carregar_dados(dados_brutos, engine)
        print(f"{len(dados_brutos)} registros enviados ao banco.")
        print(f"{linhas_afetadas} linha(s) inserida(s) ou atualizada(s).")
    else:
        print("Nenhum registro válido retornado para carga.")

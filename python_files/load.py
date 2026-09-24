import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

# 1. Validação das variáveis de ambiente usando laço tradicional
variaveis_obrigatorias = ["DB_USER", "DB_PASSWORD", "DB_HOST", "DB_PORT", "DB_NAME"]
faltando = []

for var in variaveis_obrigatorias:
    if not os.getenv(var):
        faltando.append(var)

if faltando:
    raise RuntimeError(f"Faltam as seguintes variáveis no seu .env: {', '.join(faltando)}")

# 2. Conexão com os nomes corretos das variáveis
db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")

url = f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
engine = create_engine(url)


def carregar_dados(df, engine):
    """
    Executa a carga incremental usando Staging Table + UPSERT.
    Retorna o número de linhas efetivamente inseridas ou atualizadas.
    """
    # Garantia de DDL da tabela final
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE SCHEMA IF NOT EXISTS raw;

            CREATE TABLE IF NOT EXISTS raw.dados_sgs_raw (
                codigo_serie INT,
                data TEXT,
                valor TEXT,
                PRIMARY KEY (codigo_serie, data)
            );
        """))
        conn.commit()

    # Carga na Staging Table com tipos explícitos
    df.to_sql(
        name="stg_dados_sgs",
        con=engine,
        if_exists="replace",
        index=False,
        schema ="raw"
    )

    # UPSERT e captura das linhas realmente afetadas
    with engine.connect() as conn:
        resultado = conn.execute(text("""
            INSERT INTO raw.dados_sgs_raw (codigo_serie, data, valor)
            SELECT codigo_serie, data, valor FROM raw.stg_dados_sgs
            ON CONFLICT (codigo_serie, data)
            DO UPDATE SET valor = EXCLUDED.valor
            WHERE raw.dados_sgs_raw.valor IS DISTINCT FROM EXCLUDED.valor;
        """))
        
        linhas_afetadas = resultado.rowcount

        conn.execute(text("DROP TABLE IF EXISTS raw.stg_dados_sgs;"))
        conn.commit()

    return linhas_afetadas
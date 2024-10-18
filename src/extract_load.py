# import
import yfinance as yf
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# import das minhas variaveis de ambiente

load_dotenv()

DB_HOST = os.getenv('DB_HOST_PROD')
DB_PORT = os.getenv('DB_PORT_PROD')
DB_NAME = os.getenv('DB_NAME_PROD')
DB_USER = os.getenv('DB_USER_PROD')
DB_PASS = os.getenv('DB_PASS_PROD')
DB_SCHEMA = os.getenv('DB_SCHEMA_PROD')

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)

commodities = ['CL=F', 'GC=F', 'SI=F']

def buscar_dados_commodities(simbolo, periodo='5d', intervalo='1d'): # Busca os dados de uma Commoditi
    ticker = yf.Ticker(simbolo) # define qual ticker(símbolo da cotação) vai ser puxado
    dados = ticker.history(period=periodo, interval=intervalo)[['Close']] # Retorna um dataframe com os dados do Ticker no intervalo passado nos parametros da history
    dados['simbolo'] = simbolo # cria uma coluna com o símbolo do ticker.
    return dados

def buscar_todos_dados_commodities(commodities): # Percorre a função acima, busca diversas commodities e concatena tudo em um DF só.
    todos_dados = []
    for simbolo in commodities:
        dados = buscar_dados_commodities(simbolo)
        todos_dados.append(dados)
    return pd.concat(todos_dados)

def salvar_no_postgres(df, schema='public'):
    df.to_sql('commodities', engine, if_exists='replace', index=True, index_label='Date', schema = schema)
    

if __name__ == "__main__" :
    dados_concatenados = buscar_todos_dados_commodities(commodities)
    salvar_no_postgres(dados_concatenados,schema='public' )
# pegar a cotacao dos meus ativos

# concatenar os meus ativos (1..2..3) -> (1)

# Salvar no Banco de Dados
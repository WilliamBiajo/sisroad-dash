import os
import urllib.parse
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()


def get_engine():
    driver = os.getenv('SQLSERVER_DRIVER', 'ODBC Driver 18 for SQL Server')
    server = os.getenv('SQLSERVER_HOST', '127.0.0.1')
    port = os.getenv('SQLSERVER_PORT', '1433')
    database = os.getenv('SQLSERVER_DATABASE', 'master')
    user = os.getenv('SQLSERVER_USER', 'dbeaver')
    password = os.getenv('SQLSERVER_PASSWORD', '')
    trust_cert = os.getenv('SQLSERVER_TRUST_CERT', 'yes').lower() in ('1','true','yes')

    odbc = (
        f"DRIVER={{{driver}}};"
        f"SERVER={server},{port};"
        f"DATABASE={database};"
        f"UID={user};"
        f"PWD={password};"
        f"Encrypt=yes;"
        f"TrustServerCertificate={'yes' if trust_cert else 'no'};"
    )
    params = urllib.parse.quote_plus(odbc)
    return create_engine(f"mssql+pyodbc:///?odbc_connect={params}", pool_pre_ping=True)

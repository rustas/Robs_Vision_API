import os
from pydantic import BaseSettings
# BaseSettings
class Settings(BaseSettings):
    RV_API_SRV_URL: str
    RV_API_UID: str
    RV_API_PWD: str
    RV_API_DB: str
    RV_API_SK: str
    RV_API_ALG: str
    RV_API_TOKEN_TIMEOUT: int

    class Config:
        env_file = ".env"

settings = Settings()

# Azure connection
# db_driver = '{SQL Server}'
# db_srv = 'robsvision.database.windows.net,1433'
# db_user = 'dekasebp_sql_admin'
# db_pw = 'Heaton404'
# db_db = 'my_API_db'

# db_srv = 'localhost:1433'
# db_user = 'RV_sql_admin'
# db_pw = 'Heaton404'
# db_db = 'RV_API_db'
# db_driver = '{SQL Server}'
# db_port = '1433'
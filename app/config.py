from pydantic_settings import BaseSettings
from fastapi.templating import Jinja2Templates

class Settings(BaseSettings):
    sslrootcert : str
    database_protocol : str
    database_username : str
    database_password : str
    database_host : str
    database_port : str
    database_name : str
    database_connection_parameter : str
    github_client_id : str
    github_client_secret : str
    github_token_url :str
    github_redirect_url : str
    # secret_key : str
    # algorithm : str
    # access_token_expire_time : int

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        

settings = Settings()
settings.sslrootcert = settings.sslrootcert.replace("/n","\n")

# Configure Jinja2 templates
templates = Jinja2Templates(directory="app/templates")
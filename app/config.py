from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    sslrootcert : str
    database_protocol : str
    database_username : str
    database_password : str
    database_host : str
    database_port : str
    database_name : str
    database_connection_parameter : str
    # secret_key : str
    # algorithm : str
    # acess_token_expire_time : int

    class Config:
        env_file = ".env"
        

settings = Settings()
import secrets

class Config:
    SECRET_KEY = secrets.token_hex(16)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../filmes_avaliacoes.db'
    
    # Adicione a chave da API aqui
    API_KEY = '9eb0eb68'  # Substitua pela sua chave real

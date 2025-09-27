import os

# Ajuste: os.path.join(os.path.dirname(__file__), os.pardir) 
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

class Config:
   """Configurações base, comum para todos os ambientes."""
   # Chave padrão para desativar o rastreamento (boa prática)
   SQLALCHEMY_TRACK_MODIFICATIONS = False
   # A chave SQL_TRACK_MODIFICATIONS foi removida

class DevelopmentConfig(Config):
   """Configurações específicas para o ambiente de desenvolvimento."""
   DEBUG = True
   # URI aponta diretamente para a raiz do projeto
   SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'database.db')

class ProductionConfig(Config):
    """Configuração para o ambiente de produção."""
    DEBUG = False
    # URI aponta diretamente para a raiz do projeto
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'database.db')

config_by_name = {
   'development': DevelopmentConfig,
   'production': ProductionConfig
}
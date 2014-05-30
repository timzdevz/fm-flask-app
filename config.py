class Config:
    SECRET_KEY = 'jsA5!@z1'

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql://admin:adminpass@localhost/fastmonkeys"
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

config = {
    'development': DevelopmentConfig
}

from pydantic import AmqpDsn, PostgresDsn, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", env_prefix="POSTGRES_")

    user: str
    password: SecretStr
    db: str
    host: str
    port: int

    @property
    def db_url(self):
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.user,
            password=self.password.get_secret_value(),
            host=self.host,
            port=self.port,
            path=self.db,
        )


class RabbitMQSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", env_prefix="RABBITMQ_")

    user: str
    password: SecretStr
    host: str
    port: int

    @property
    def amqp_url(self):
        return AmqpDsn.build(
            username=self.user,
            password=self.password.get_secret_value(),
            host=self.host,
            port=self.port,
        )


class Settings(BaseSettings):

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    api_key: SecretStr

    webhook_timeout: int
    webhook_max_retries: int

    database_settings: DatabaseSettings = DatabaseSettings()
    rabbitmq_settings: RabbitMQSettings = RabbitMQSettings()


settings = Settings()
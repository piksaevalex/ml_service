import os
from pydantic import Field, SecretStr
from .base import BASE_DIRECTORY, AdvancedBaseSettings


class ServiceDatabaseSettings(AdvancedBaseSettings):
    """
    Этим именем мы явно даём понять, что данная база является для сервиса основной.
    В конфигурации данного класса мы дополнительно указываем префикс service_db,
    при помощи которого визуально объединяем эти энвы в группу.
    Префикс присоединяется спереди к имени атрибута,
    после чего ищет в списке соответствующую переменную:
        - service_db_host;
        - service_db_username;
        - service_db_name;
        - service_db_port;
    """
    host: str
    username: str
    password: SecretStr
    db_name: str = Field(..., env="ml_service_db_name")
    port: int = Field(default="5435")

    class Config:
        env_prefix = "ml_service_db_"
        secrets_dir = os.path.join(BASE_DIRECTORY, "secrets")

    @property
    def postgresql_url(self) -> str:
        """
        Это property (свойство) пригодится, когда будем подключаться к БД.
        """
        return f"postgresql://{self.username}:{self.password.get_secret_value()}@{self.host}:{self.port}/{self.db_name}"


service_database_settings = ServiceDatabaseSettings()

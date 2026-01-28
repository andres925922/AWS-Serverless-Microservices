from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    RABBITMQ_HOST: str = "localhost"
    RABBITMQ_PORT: int = 5672
    RABBITMQ_USER: str = "user"
    RABBITMQ_PASSWORD: str = "password"
    RABBITMQ_PROTOCOL: str = "amqp"

    RABBITMQ_QUEUE_NAME: str = "my_queue"
    RABBITMQ_EXCHANGE_NAME: str = "my_exchange"

    @property
    def RABBITMQ_URL(self) -> str:
        return f"{self.RABBITMQ_PROTOCOL}://{self.RABBITMQ_USER}:{self.RABBITMQ_PASSWORD}@{self.RABBITMQ_HOST}:{self.RABBITMQ_PORT}/"
    
settings = Settings()
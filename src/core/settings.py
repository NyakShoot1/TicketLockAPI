from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent


class DbSettings(BaseModel):
    user: str = "user"
    password: str = "password"
    host: str = "localhost"
    port: int = 5432
    name: str = "ticketlock"
    echo: bool = False

    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 30


class Setting(BaseSettings):
    api_v1_prefix: str = "/api/v1"

    db: DbSettings = DbSettings()
    auth_jwt: AuthJWT = AuthJWT()

    model_config = SettingsConfigDict(
        env_file=".env",
        env_nested_delimiter="__",
        env_prefix="DB_",
        extra="ignore"
    )


settings = Setting()

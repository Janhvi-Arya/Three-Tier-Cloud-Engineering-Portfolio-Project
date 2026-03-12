from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    app_name: str
    database_url: str
    app_secret: str
    admin_username: str
    admin_password: str
    customer_username: str
    customer_password: str


def get_settings(database_url: str | None = None) -> Settings:
    resolved_database_url = database_url or os.getenv(
        "DATABASE_URL",
        "sqlite+pysqlite:///./cloudops.db",
    )
    return Settings(
        app_name="CloudOps Dashboard",
        database_url=resolved_database_url,
        app_secret=os.getenv("APP_SECRET", "dev-secret-change-me"),
        admin_username=os.getenv("ADMIN_USERNAME", "admin"),
        admin_password=os.getenv("ADMIN_PASSWORD", "AdminPass123!"),
        customer_username=os.getenv("CUSTOMER_USERNAME", "customer"),
        customer_password=os.getenv("CUSTOMER_PASSWORD", "CustomerPass123!"),
    )

from pydantic_settings import BaseSettings
from pydantic import field_validator
import os
import sys


class Settings(BaseSettings):
    # -------------------- GENERAL --------------------
    ENV: str = "dev"   # dev | prod

    # -------------------- SUPABASE --------------------
    SUPABASE_URL: str = ""
    SUPABASE_KEY: str = ""
    SUPABASE_SERVICE_ROLE_KEY: str = ""

    # -------------------- SECURITY --------------------
    SUPABASE_JWT_SECRET: str = ""
    SECRET_KEY: str | None = None  # fallback for Flask sessions

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @field_validator("ENV")
    def validate_env(cls, v):
        allowed = {"dev", "prod"}
        if v not in allowed:
            raise ValueError(f"ENV must be one of {allowed}")
        return v

    @property
    def JWT_SECRET(self) -> str:
        if self.SUPABASE_JWT_SECRET:
            return self.SUPABASE_JWT_SECRET
        if self.SECRET_KEY:
            return self.SECRET_KEY
        raise RuntimeError("No JWT secret provided!")


settings = Settings()

# -------------------- REQUIRED KEYS (SAFE VALIDATION) --------------------
required = {
    "SUPABASE_URL": settings.SUPABASE_URL,
    "SUPABASE_KEY": settings.SUPABASE_KEY,
    "SUPABASE_SERVICE_ROLE_KEY": settings.SUPABASE_SERVICE_ROLE_KEY,
}

missing = [k for k, v in required.items() if not v]

if missing:
    msg = f"Missing environment variables: {', '.join(missing)}"
    print("[CONFIG ERROR]", msg, file=sys.stderr)
    raise RuntimeError(msg)

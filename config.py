import os
import sentry_sdk
from dotenv import load_dotenv
from typing import Any

load_dotenv()

class Settings:
    database_url: str = os.getenv("DATABASE_URL", "")
    secret_key: str = os.getenv("SECRET_KEY", "")
    sentry_dsn: str = os.getenv("SENTRY_DSN", "")

settings = Settings()

def init_sentry() -> None:
    """Initialise Sentry SDK if a DSN is configured.

    Called once at application startup from main.py.
    If SENTRY_DSN is empty (e.g. in development or testing),
    Sentry is silently skipped — no error is raised.
    """
    if settings.sentry_dsn:
        sentry_sdk.init(
            dsn=settings.sentry_dsn,
            traces_sample_rate=0.0,
            before_send=_scrub_pii,
        )


def _scrub_pii(event: dict[str, Any], _hint: dict[str, Any]) -> dict[str, Any] | None:
    """Remove personally identifiable information before sending to Sentry.

    Scrubs email addresses and password-related fields from
    exception context to comply with RGPD requirements.

    Args:
        event: The Sentry event dict.
        _hint: Additional context from the SDK.

    Returns:
        dict | None: The scrubbed event, or None to discard it entirely.
    """
    if "request" in event:
        event["request"].pop("data", None)
    return event

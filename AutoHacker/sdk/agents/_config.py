from typing_extensions import Literal

try:
    from openai import AsyncOpenAI
except ModuleNotFoundError as exc:
    class AsyncOpenAI:  # type: ignore[misc]
        """Placeholder type used when the optional openai dependency is absent."""

    _openai_import_error = exc
else:
    _openai_import_error = None

from .models import _openai_shared
from .tracing import set_tracing_export_api_key


def _require_openai() -> None:
    if _openai_import_error is not None:
        raise ModuleNotFoundError(
            "The optional 'openai' dependency is required for this feature. "
            "Install it with `pip install openai`."
        ) from _openai_import_error


def set_default_openai_key(key: str, use_for_tracing: bool) -> None:
    _require_openai()
    _openai_shared.set_default_openai_key(key)

    if use_for_tracing:
        set_tracing_export_api_key(key)


def set_default_openai_client(client: AsyncOpenAI, use_for_tracing: bool = True) -> None:
    _require_openai()
    _openai_shared.set_default_openai_client(client)

    if use_for_tracing:
        set_tracing_export_api_key(client.api_key)


def set_default_openai_api(api: Literal["chat_completions", "responses"]) -> None:
    if api == "chat_completions":
        _openai_shared.set_use_responses_by_default(False)
    else:
        _openai_shared.set_use_responses_by_default(True)

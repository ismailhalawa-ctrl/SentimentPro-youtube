from app.ai.interfaces.capability import AnalysisMode, Capability
from app.ai.interfaces.provider import AIProvider

_REGISTRY: dict[str, AIProvider] = {}


def register_provider(provider_id: str):
    def decorator(cls: type[AIProvider]) -> type[AIProvider]:
        _REGISTRY[provider_id] = cls()
        return cls

    return decorator


def resolve_provider(capability: Capability, mode: AnalysisMode, language: str) -> AIProvider:
    matches = [
        provider
        for provider in _REGISTRY.values()
        if provider.capability == capability
        and provider.mode == mode
        and language in getattr(provider, "languages", ())
    ]

    if not matches:
        raise LookupError(
            f"No provider registered for capability={capability.value!r} "
            f"mode={mode.value!r} language={language!r}."
        )

    for provider in matches:
        if provider.is_available():
            return provider

    return matches[0]


def get_registered_provider_ids() -> list[str]:
    return list(_REGISTRY.keys())

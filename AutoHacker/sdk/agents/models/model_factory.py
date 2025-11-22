"""
Model Provider Factory para CaiFramework

Este módulo proporciona una forma centralizada de obtener modelos LLM
basándose en variables de entorno, soportando múltiples providers:
- OpenAI / Anthropic (vía OpenAI-compatible API)
- Ollama (modelos locales)
- llama.cpp (modelos GGUF locales)
"""

import os
from typing import Optional

from openai import AsyncOpenAI

from cai.sdk.agents.models.interface import Model
from cai.sdk.agents.models.openai_chatcompletions import OpenAIChatCompletionsModel


def get_model_provider(
    model_name: Optional[str] = None,
    api_key: Optional[str] = None,
    agent_name: Optional[str] = None,
    agent_id: Optional[str] = None,
    agent_type: Optional[str] = None,
) -> Model:
    """
    Obtiene un modelo LLM basándose en las variables de entorno.
    
    Orden de prioridad para determinar el provider:
    1. OLLAMA=true → Usar Ollama
    2. LLAMACPP=true → Usar llama.cpp
    3. Por defecto → Usar OpenAI-compatible API
    
    Args:
        model_name: Nombre del modelo. Si no se proporciona, usa CAI_MODEL
        api_key: API key. Si no se proporciona, usa OPENAI_API_KEY
        agent_name: Nombre del agente (para tracking)
        agent_id: ID del agente (para parallel execution)
        agent_type: Tipo de agente (para registry)
    
    Returns:
        Model: Instancia del modelo configurado
        
    Environment Variables:
        OLLAMA: "true" para activar Ollama
        OLLAMA_API_BASE: URL base de Ollama (default: http://localhost:11434/v1)
        OLLAMA_MODEL: Modelo de Ollama (default: llama3.2)
        
        LLAMACPP: "true" para activar llama.cpp
        LLAMACPP_API_BASE: URL base de llama.cpp (default: http://localhost:8080/v1)
        LLAMACPP_MODEL: Modelo de llama.cpp (default: local-model)
        LLAMACPP_CONTEXT_SIZE: Tamaño del contexto (default: 4096)
        
        CAI_MODEL: Modelo por defecto si no hay override
        OPENAI_API_KEY: API key para OpenAI/Anthropic
    
    Examples:
        >>> # Usar con Ollama
        >>> os.environ["OLLAMA"] = "true"
        >>> os.environ["OLLAMA_MODEL"] = "llama3.2"
        >>> model = get_model_provider()
        
        >>> # Usar con llama.cpp
        >>> os.environ["LLAMACPP"] = "true"
        >>> model = get_model_provider()
        
        >>> # Usar con OpenAI (default)
        >>> model = get_model_provider("gpt-4")
    """
    
    # Determinar si usar Ollama
    use_ollama = os.getenv("OLLAMA", "").lower() == "true"
    
    # Determinar si usar llama.cpp
    use_llamacpp = os.getenv("LLAMACPP", "").lower() == "true"
    
    # Si ambos están activados, Ollama tiene prioridad
    if use_ollama and use_llamacpp:
        print("⚠️  Warning: Both OLLAMA and LLAMACPP are enabled. Using Ollama.")
        use_llamacpp = False
    
    # Provider: Ollama
    if use_ollama:
        from cai.sdk.agents.models.ollama_provider import OllamaProvider
        
        base_url = os.getenv("OLLAMA_API_BASE", "http://localhost:11434/v1")
        default_model = os.getenv("OLLAMA_MODEL", "llama3.2")
        
        # Si se proporciona un model_name, usarlo; sino usar el default
        model_to_use = model_name if model_name else default_model
        
        provider = OllamaProvider(base_url=base_url, model_name=model_to_use)
        model = provider.get_model()
        
        # Configurar metadata del agente si está disponible
        if hasattr(model, '_agent_name') and agent_name:
            model._agent_name = agent_name
        if hasattr(model, '_agent_id') and agent_id:
            model._agent_id = agent_id
        if hasattr(model, '_agent_type') and agent_type:
            model._agent_type = agent_type
            
        return model
    
    # Provider: llama.cpp
    if use_llamacpp:
        from cai.sdk.agents.models.llamacpp_provider import LlamaCppProvider
        
        base_url = os.getenv("LLAMACPP_API_BASE", "http://localhost:8080/v1")
        default_model = os.getenv("LLAMACPP_MODEL", "local-model")
        context_size = int(os.getenv("LLAMACPP_CONTEXT_SIZE", "4096"))
        
        # Si se proporciona un model_name, usarlo; sino usar el default
        model_to_use = model_name if model_name else default_model
        
        provider = LlamaCppProvider(
            base_url=base_url,
            model_name=model_to_use,
            context_size=context_size,
        )
        model = provider.get_model()
        
        # Configurar metadata del agente si está disponible
        if hasattr(model, '_agent_name') and agent_name:
            model._agent_name = agent_name
        if hasattr(model, '_agent_id') and agent_id:
            model._agent_id = agent_id
        if hasattr(model, '_agent_type') and agent_type:
            model._agent_type = agent_type
            
        return model
    
    # Provider por defecto: OpenAI-compatible (OpenAI, Anthropic, etc.)
    if not model_name:
        model_name = os.getenv("CAI_MODEL", "alias0")
    
    if not api_key:
        api_key = os.getenv("OPENAI_API_KEY", "sk-placeholder-key-for-local-models")
    
    return OpenAIChatCompletionsModel(
        model=model_name,
        openai_client=AsyncOpenAI(api_key=api_key),
        agent_name=agent_name,
        agent_id=agent_id,
        agent_type=agent_type,
    )


def get_current_provider_info() -> dict:
    """
    Obtiene información sobre el provider actualmente configurado.
    
    Returns:
        dict: Información del provider actual
        
    Example:
        >>> info = get_current_provider_info()
        >>> print(info)
        {
            'provider': 'ollama',
            'model': 'llama3.2',
            'base_url': 'http://localhost:11434/v1',
            'enabled': True
        }
    """
    use_ollama = os.getenv("OLLAMA", "").lower() == "true"
    use_llamacpp = os.getenv("LLAMACPP", "").lower() == "true"
    
    if use_ollama:
        return {
            "provider": "ollama",
            "model": os.getenv("OLLAMA_MODEL", "llama3.2"),
            "base_url": os.getenv("OLLAMA_API_BASE", "http://localhost:11434/v1"),
            "enabled": True,
        }
    
    if use_llamacpp:
        return {
            "provider": "llamacpp",
            "model": os.getenv("LLAMACPP_MODEL", "local-model"),
            "base_url": os.getenv("LLAMACPP_API_BASE", "http://localhost:8080/v1"),
            "context_size": os.getenv("LLAMACPP_CONTEXT_SIZE", "4096"),
            "enabled": True,
        }
    
    return {
        "provider": "openai-compatible",
        "model": os.getenv("CAI_MODEL", "alias0"),
        "enabled": True,
    }


def print_provider_info():
    """
    Imprime información sobre el provider configurado.
    
    Útil para debugging y verificación de configuración.
    """
    info = get_current_provider_info()
    
    print("\n" + "="*60)
    print("  Model Provider Configuration")
    print("="*60)
    
    provider_emoji = {
        "ollama": "🦙",
        "llamacpp": "🦜",
        "openai-compatible": "🤖"
    }
    
    emoji = provider_emoji.get(info["provider"], "🤖")
    
    print(f"\n{emoji} Provider: {info['provider'].upper()}")
    print(f"📦 Model: {info['model']}")
    
    if "base_url" in info:
        print(f"🔗 Base URL: {info['base_url']}")
    
    if "context_size" in info:
        print(f"📏 Context Size: {info['context_size']}")
    
    print(f"✅ Enabled: {info['enabled']}")
    print("="*60 + "\n")


# Alias para compatibilidad
create_model = get_model_provider

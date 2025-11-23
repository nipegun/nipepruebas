"""
PHAH - Plataforma de Hacking de Penetración Automatizada
Módulos principales para pruebas de penetración automatizadas con IA
"""

from .ollama_client import OllamaClient
from .pentester import AutoPentester
from .report_generator import ReportGenerator

__all__ = ['OllamaClient', 'AutoPentester', 'ReportGenerator']

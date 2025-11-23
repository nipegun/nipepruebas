#!/usr/bin/env python3
"""
Ejecutor de Comandos para PHAH
Ejecuta comandos del sistema y captura la salida
Similar al generic_linux_command de CaiFramework
"""

import subprocess
import asyncio
import shlex
from typing import Optional, Tuple
from datetime import datetime


class CommandExecutor:
  """Ejecuta comandos del sistema y captura la salida"""

  def __init__(self, timeout: int = 120, verbose: bool = True):
    """
    Inicializa el ejecutor de comandos

    Args:
      timeout: Tiempo de espera por defecto en segundos
      verbose: Mostrar comandos antes de ejecutarlos
    """
    self.timeout = timeout
    self.verbose = verbose
    self.command_history = []

  async def execute(
    self,
    command: str | list[str],
    timeout: Optional[int] = None,
    shell: bool = True
  ) -> Tuple[int, str, str]:
    """
    Ejecuta un comando de forma asíncrona

    Args:
      command: Comando a ejecutar (cadena o lista)
      timeout: Tiempo de espera del comando (usa el valor por defecto si es None)
      shell: Si se debe usar ejecución de shell

    Returns:
      Tupla de (código_retorno, stdout, stderr)
    """
    # Convertir lista a cadena si es necesario
    if isinstance(command, list):
      command = " ".join(str(part) for part in command)

    # Usar timeout por defecto si no se especifica
    if timeout is None:
      timeout = self.timeout

    # Registrar comando en el historial
    timestamp = datetime.now().isoformat()
    self.command_history.append({
      "timestamp": timestamp,
      "command": command
    })

    # Mostrar comando si verbose está activado
    if self.verbose:
      print(f"\n[{timestamp}] Ejecutando: {command}")

    try:
      # Ejecutar comando
      if shell:
        process = await asyncio.create_subprocess_shell(
          command,
          stdout=subprocess.PIPE,
          stderr=subprocess.PIPE
        )
      else:
        args = shlex.split(command)
        process = await asyncio.create_subprocess_exec(
          *args,
          stdout=subprocess.PIPE,
          stderr=subprocess.PIPE
        )

      # Esperar finalización con timeout
      try:
        stdout, stderr = await asyncio.wait_for(
          process.communicate(),
          timeout=timeout
        )
        return_code = process.returncode
      except asyncio.TimeoutError:
        process.kill()
        await process.wait()
        return -1, "", f"El comando agotó el tiempo de espera después de {timeout} segundos"

      # Decodificar salida
      stdout_str = stdout.decode('utf-8', errors='replace')
      stderr_str = stderr.decode('utf-8', errors='replace')

      return return_code, stdout_str, stderr_str

    except Exception as e:
      return -1, "", f"Error al ejecutar el comando: {str(e)}"

  async def execute_and_get_output(
    self,
    command: str | list[str],
    timeout: Optional[int] = None
  ) -> str:
    """
    Ejecuta comando y devuelve la salida combinada

    Args:
      command: Comando a ejecutar
      timeout: Tiempo de espera del comando

    Returns:
      Salida combinada de stdout y stderr
    """
    return_code, stdout, stderr = await self.execute(command, timeout)

    # Combinar salida
    output_parts = []

    if stdout:
      output_parts.append(stdout)

    if stderr:
      if output_parts:
        output_parts.append("\n--- STDERR ---\n")
      output_parts.append(stderr)

    if return_code != 0:
      output_parts.append(f"\n[Código de salida: {return_code}]")

    return "".join(output_parts)

  async def execute_multiple(
    self,
    commands: list[str],
    stop_on_error: bool = False
  ) -> list[Tuple[int, str, str]]:
    """
    Ejecuta múltiples comandos secuencialmente

    Args:
      commands: Lista de comandos a ejecutar
      stop_on_error: Detener ejecución si un comando falla

    Returns:
      Lista de tuplas (código_retorno, stdout, stderr)
    """
    results = []

    for command in commands:
      result = await self.execute(command)
      results.append(result)

      # Detener si el comando falló y stop_on_error está activo
      if stop_on_error and result[0] != 0:
        break

    return results

  def get_history(self) -> list:
    """Obtener historial de ejecución de comandos"""
    return self.command_history.copy()

  def clear_history(self):
    """Limpiar historial de ejecución de comandos"""
    self.command_history = []


# Envoltorio síncrono para uso simple
class SyncCommandExecutor:
  """Envoltorio síncrono para CommandExecutor"""

  def __init__(self, timeout: int = 120, verbose: bool = True):
    self.executor = CommandExecutor(timeout=timeout, verbose=verbose)

  def execute(
    self,
    command: str | list[str],
    timeout: Optional[int] = None,
    shell: bool = True
  ) -> Tuple[int, str, str]:
    """Ejecutar comando de forma síncrona"""
    return asyncio.run(self.executor.execute(command, timeout, shell))

  def execute_and_get_output(
    self,
    command: str | list[str],
    timeout: Optional[int] = None
  ) -> str:
    """Ejecutar comando y obtener salida de forma síncrona"""
    return asyncio.run(self.executor.execute_and_get_output(command, timeout))

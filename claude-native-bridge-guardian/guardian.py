#!/usr/bin/env -S PYTHONDONTWRITEBYTECODE=1 python3

# Pongo a disposición pública este script bajo el término de "software de dominio público".
# Puedes hacer lo que quieras con él porque es libre de verdad; no libre con condiciones como las licencias GNU y otras patrañas similares.
# Si se te llena la boca hablando de libertad entonces hazlo realmente libre.
# No tienes que aceptar ningún tipo de términos de uso o licencia para utilizarlo o modificarlo porque va sin CopyLeft.

# ----------
# Script de NiPeGun para x
#
# Ejecución remota (puede requerir permisos sudo):
#   curl -sL https://raw.githubusercontent.com/nipegun/nipepruebas/refs/heads/main/claude-native-bridge-guardian/guardian.py | python3 - "Cadena"
#
# Bajar y editar directamente el archivo en nano
#   curl -sL https://raw.githubusercontent.com/nipegun/nipepruebas/refs/heads/main/claude-native-bridge-guardian/guardian.py | nano -
# ----------

# ------ Inicio del bloque de instalación de dependencias de paquetes python ------

# Definir los paquetes python que necesita este script siguiendo la convención de ciccionario: nombre_del_modulo -> nombre_paquete_pip (para casos donde difieren)
dPaquetesPython = {
  "flask": "flask",
  "paramiko": "paramiko==2.4.1",
  "requests": "requests",
  "PIL": "Pillow",
  "nmap": "python-nmap"
}

import importlib.util
import subprocess
import sys

cNombreDelPaqueteApt = "python3-pip"

def fPaqueteAptEstaInstalado(pNombreDelPaqueteApt):
  """Verifica si un paquete apt está instalado."""
  vResultado = subprocess.run(
    ["dpkg", "-s", pNombreDelPaqueteApt],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
  )
  return vResultado.returncode == 0

def fInstalarPaqueteApt(pNombreDelPaqueteApt):
  """Instala un paquete mediante apt."""
  print(f"[*] Instalando paquete apt: {pNombreDelPaqueteApt}")
  try:
    subprocess.run(
      ["sudo", "apt-get", "-y", "update"],
      check=True
    )
    subprocess.run(
      ["sudo", "apt-get", "-y", "install", pNombreDelPaqueteApt],
      check=True
    )
    print(f"[✓] {pNombreDelPaqueteApt} instalado correctamente")
  except subprocess.CalledProcessError as e:
    print(f"[✗] Error instalando {pNombreDelPaqueteApt}: {e}")
    sys.exit(1)

def fModuloPythonEstaInstalado(pNombreDelModulo):
  """Verifica si un módulo Python está disponible."""
  return importlib.util.find_spec(pNombreDelModulo) is not None

def fInstalarPaquetePython(pNombreDelPaquete):
  """Instala un paquete Python mediante pip."""
  print(f"[*] Instalando paquete Python: {pNombreDelPaquete}")
  try:
    subprocess.run(
      [
        sys.executable,
        "-m", "pip", "install",
        pNombreDelPaquete,
        "--break-system-packages"
      ],
      check=True
    )
    print(f"[✓] {pNombreDelPaquete} instalado correctamente")
  except subprocess.CalledProcessError as e:
    print(f"[✗] Error instalando {pNombreDelPaquete}: {e}")
    return False
  return True

def fComprobarEInstalarPaquetes(pdPaquetesPython):
  """Comprueba e instala los paquetes Python necesarios."""
  aErrores = []
  for vNombreModulo, vNombrePip in pdPaquetesPython.items():
    if fModuloPythonEstaInstalado(vNombreModulo):
      print(f"[✓] {vNombrePip} ya está instalado")
    else:
      if not fInstalarPaquetePython(vNombrePip):
        aErrores.append(vNombrePip)
  return aErrores

print("=== Comprobando dependencias ===\n")

if not fPaqueteAptEstaInstalado(cNombreDelPaqueteApt):
  fInstalarPaqueteApt(cNombreDelPaqueteApt)
else:
  print(f"[✓] {cNombreDelPaqueteApt} ya está instalado")

print()

aErrores = fComprobarEInstalarPaquetes(dPaquetesPython)

print("\n=== Resumen ===")
if aErrores:
  print(f"[!] Paquetes con errores: {', '.join(aErrores)}")
  sys.exit(1)
else:
  print("[✓] Todas las dependencias instaladas correctamente")

# ------ Fin del bloque de instalación de dependencias. A partir de aquí va el código real del script ------

import argparse
import hashlib
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

cNativeMessagingPaths = [
  "/etc/opt/chrome/native-messaging-hosts",
  "/etc/chromium/native-messaging-hosts",
  "/usr/lib/chromium/native-messaging-hosts",
  "/usr/lib/mozilla/native-messaging-hosts",
  str(Path.home() / ".config/google-chrome/NativeMessagingHosts"),
  str(Path.home() / ".config/chromium/NativeMessagingHosts"),
  str(Path.home() / ".config/BraveSoftware/Brave-Browser/NativeMessagingHosts"),
  str(Path.home() / ".config/microsoft-edge/NativeMessagingHosts"),
  str(Path.home() / ".mozilla/native-messaging-hosts"),
]

cSuspiciousPatterns = [
  "anthropic",
  "claude",
  "com.anthropic",
]

cAuditKey = "claude_native_bridge_watch"


def fRun(vCommand):
  return subprocess.run(
    vCommand,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
  )


def fIsRoot():
  return os.geteuid() == 0


def fIsSuspiciousFile(vPath):
  vName = str(vPath).lower()

  if any(vPattern in vName for vPattern in cSuspiciousPatterns):
    return True

  try:
    vContent = Path(vPath).read_text(errors="ignore").lower()
  except Exception:
    return False

  return any(vPattern in vContent for vPattern in cSuspiciousPatterns)


def fUninstall():
  print("[+] Searching for Claude/Anthropic Native Messaging entries...")

  vRemoved = 0

  for vDirectory in cNativeMessagingPaths:
    vPathDirectory = Path(vDirectory)

    if not vPathDirectory.exists():
      continue

    for vFile in vPathDirectory.glob("*.json"):
      if fIsSuspiciousFile(vFile):
        print(f"[+] Removing: {vFile}")
        vFile.unlink()
        vRemoved += 1

  print(f"[+] Files removed: {vRemoved}")


def fEnsureAuditdInstalled():
  if shutil.which("auditctl") and shutil.which("ausearch"):
    return True

  print("[-] auditctl/ausearch not found.")
  print("[i] Install auditd with:")
  print("    apt update && apt install -y auditd audispd-plugins")
  return False


def fCreateDirectories():
  for vDirectory in cNativeMessagingPaths:
    try:
      Path(vDirectory).mkdir(parents=True, exist_ok=True)
    except Exception as vError:
      print(f"[-] Failed to create {vDirectory}: {vError}")


def fRemovePreviousAuditRules():
  vRules = fRun(["auditctl", "-l"]).stdout.splitlines()

  for vRule in vRules:
    if cAuditKey not in vRule:
      continue

    vParts = vRule.split()
    if "-w" not in vParts:
      continue

    vPath = vParts[vParts.index("-w") + 1]

    fRun(["auditctl", "-W", vPath, "-k", cAuditKey])


def fEnableAuditMonitoring():
  if not fIsRoot():
    print("[-] This script requires root to configure auditd.")
    sys.exit(1)

  if not fEnsureAuditdInstalled():
    sys.exit(1)

  fCreateDirectories()
  fRemovePreviousAuditRules()

  print("[+] Enabling auditd rules...")

  for vDirectory in cNativeMessagingPaths:
    if Path(vDirectory).exists():
      vResult = fRun([
        "auditctl",
        "-w",
        vDirectory,
        "-p",
        "wa",
        "-k",
        cAuditKey
      ])

      if vResult.returncode == 0:
        print(f"[+] Monitoring: {vDirectory}")
      else:
        print(f"[-] Error monitoring {vDirectory}: {vResult.stderr.strip()}")


def fShowAuditEvents():
  vResult = fRun([
    "ausearch",
    "-k",
    cAuditKey,
    "-i"
  ])

  if vResult.returncode != 0:
    print("[-] No auditd events yet.")
    return

  print(vResult.stdout)


def fHashFile(vPath):
  vHash = hashlib.sha256()

  with open(vPath, "rb") as vFile:
    for vBlock in iter(lambda: vFile.read(65536), b""):
      vHash.update(vBlock)

  return vHash.hexdigest()


def fSnapshot():
  vSnapshot = {}

  for vDirectory in cNativeMessagingPaths:
    vPathDirectory = Path(vDirectory)

    if not vPathDirectory.exists():
      continue

    for vFile in vPathDirectory.glob("*.json"):
      try:
        vSnapshot[str(vFile)] = fHashFile(vFile)
      except Exception:
        pass

  return vSnapshot


def fMonitor(vInterval):
  print("[+] Starting reinstallation monitor...")
  print("[i] To identify the process that wrote the file, run:")
  print(f"    ausearch -k {cAuditKey} -i")

  vPreviousSnapshot = fSnapshot()

  while True:
    time.sleep(vInterval)

    vCurrentSnapshot = fSnapshot()

    for vPath, vHash in vCurrentSnapshot.items():
      if vPath not in vPreviousSnapshot:
        print(f"[!] New Native Messaging Host detected: {vPath}")

        if fIsSuspiciousFile(vPath):
          print(f"[!] Looks related to Claude/Anthropic. Removing: {vPath}")
          try:
            Path(vPath).unlink()
          except Exception as vError:
            print(f"[-] Failed to remove {vPath}: {vError}")

      elif vPreviousSnapshot[vPath] != vHash:
        print(f"[!] Native Messaging Host modified: {vPath}")

        if fIsSuspiciousFile(vPath):
          print(f"[!] Looks related to Claude/Anthropic. Removing: {vPath}")
          try:
            Path(vPath).unlink()
          except Exception as vError:
            print(f"[-] Failed to remove {vPath}: {vError}")

    vPreviousSnapshot = fSnapshot()


def fMain():
  vParser = argparse.ArgumentParser(
    description="Uninstall and monitor Claude/Anthropic Native Messaging Hosts."
  )

  vParser.add_argument(
    "--uninstall",
    action="store_true",
    help="Remove existing Claude/Anthropic entries."
  )

  vParser.add_argument(
    "--enable-auditd",
    action="store_true",
    help="Enable auditd rules to detect who reinstalls it."
  )

  vParser.add_argument(
    "--events",
    action="store_true",
    help="Show auditd events."
  )

  vParser.add_argument(
    "--monitor",
    action="store_true",
    help="Continuously monitor and remove if it reappears."
  )

  vParser.add_argument(
    "--interval",
    type=int,
    default=2,
    help="Monitoring interval in seconds."
  )

  vArgs = vParser.parse_args()

  if vArgs.uninstall:
    fUninstall()

  if vArgs.enable_auditd:
    fEnableAuditMonitoring()

  if vArgs.events:
    fShowAuditEvents()

  if vArgs.monitor:
    fMonitor(vArgs.interval)

  if not any([
    vArgs.uninstall,
    vArgs.enable_auditd,
    vArgs.events,
    vArgs.monitor
  ]):
    vParser.print_help()


if __name__ == "__main__":
  fMain()

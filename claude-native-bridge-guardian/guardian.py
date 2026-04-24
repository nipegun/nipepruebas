#!/usr/bin/env -S PYTHONDONTWRITEBYTECODE=1 python3

# I make this script publicly available under the term "public domain software."
# You can do whatever you want with it because it is truly free—unlike so-called "free" software with conditions, like the GNU licenses and other similar nonsense.
# If you're so eager to talk about freedom, then make it truly free.
# You don't have to accept any terms of use or license to use or modify it, because it comes with no CopyLeft.

# ----------
# # NiPeGun's script to remove and monitor Claude/Anthropic Native Messaging Hosts
#
# Remote execution (may require sudo privileges):
#   curl -sL https://raw.githubusercontent.com/nipegun/nipepruebas/refs/heads/main/claude-native-bridge-guardian/guardian.py | sudo python3 - --uninstall --enable-auditd
#
# Download and edit the file directly in nano:
#   curl -sL https://raw.githubusercontent.com/nipegun/nipepruebas/refs/heads/main/claude-native-bridge-guardian/guardian.py | nano -
# ----------

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

  print("[*] auditctl/ausearch not found. Installing auditd...")

  if not fIsRoot():
    print("[-] You need root privileges to install packages.")
    sys.exit(1)

  try:
    subprocess.run(
      ["apt-get", "update"],
      check=True
    )
    subprocess.run(
      ["apt-get", "-y", "install", "auditd", "audispd-plugins"],
      check=True
    )
  except subprocess.CalledProcessError as vError:
    print(f"[-] Failed to install auditd: {vError}")
    return False

  # Verify again after installation
  if shutil.which("auditctl") and shutil.which("ausearch"):
    print("[+] auditd installed successfully")
    return True

  print("[-] auditd installation completed but binaries not found")
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

# Claude Native Bridge Guardian

Tool to detect, remove, and monitor unauthorized Native Messaging Hosts related to Claude / Anthropic on Linux systems.

---

## What this does

This script focuses on one specific surface: **Native Messaging Hosts** used by Chromium-based browsers and Firefox.

It provides three capabilities:

- **Uninstall** suspicious Native Messaging entries (Claude / Anthropic related)
- **Monitor in real time** if they reappear
- **Identify which process recreated them** using `auditd`

---

## Why this matters

Native Messaging allows a browser extension to communicate with local binaries.

This is legitimate, but:

- It modifies system/browser configuration
- It creates a communication bridge between browser and local system
- It may be installed without clear user awareness

This script treats that surface as something to **control and audit**.

---

## Features

- Recursive detection across common browser paths
- Content-based detection (not only filename)
- Automatic removal of suspicious entries
- Real-time monitoring loop
- `auditd` integration to trace the exact process responsible
- Lightweight (no external Python dependencies)

---

## Requirements

- Python 3
- Linux system (tested on Debian)
- Root privileges (required for auditd features)

Optional but recommended:

- `auditd`
- `audispd-plugins`

Install auditd if needed:

```
apt update && apt install -y auditd audispd-plugins
```

---

## Installation

```
git clone <your-repo>
cd <your-repo>
chmod +x claude-native-bridge-guardian.py
```

---

## Usage

### 1. Remove existing entries

```
sudo ./claude-native-bridge-guardian.py --uninstall
```

---

### 2. Enable monitoring with auditd

```
sudo ./claude-native-bridge-guardian.py --enable-auditd
```

This will:

- Add audit rules on Native Messaging directories
- Track file creation and modification events

---

### 3. Monitor in real time

```
sudo ./claude-native-bridge-guardian.py --monitor
```

Behavior:

- Detects new or modified `.json` files
- Checks if they match suspicious patterns
- Automatically deletes them if needed

---

### 4. Identify who recreated the file

```
sudo ./claude-native-bridge-guardian.py --events
```

Or directly:

```
sudo ausearch -k claude_native_bridge_watch -i
```

This shows:

- Executable path
- PID
- User
- Timestamp

---

## Detection logic

A file is considered suspicious if:

- Its name contains:
  - `anthropic`
  - `claude`
  - `com.anthropic`

OR

- Its content contains those strings

---

## Monitored paths

Typical locations:

```
/etc/opt/chrome/native-messaging-hosts
/etc/chromium/native-messaging-hosts
/usr/lib/chromium/native-messaging-hosts
/usr/lib/mozilla/native-messaging-hosts
~/.config/*/NativeMessagingHosts
~/.mozilla/native-messaging-hosts
```

---

## Security model

This tool does **not assume malware**.

Instead, it assumes:

- Any silent system integration should be visible
- Any persistent bridge should be auditable
- Any reinstallation should be attributable

---

## Limitations

- Requires root for full functionality
- Relies on `auditd` for process attribution
- Pattern-based detection (can be bypassed if renamed/obfuscated)
- Does not inspect binary behavior, only registration files

---

## Recommended workflow

1. Run uninstall
2. Enable auditd monitoring
3. Leave monitor running
4. If something reappears → inspect with `ausearch`

---

## Disclaimer

This tool is intended for auditing and defensive analysis.

It does not prove malicious behavior by itself. It simply exposes and controls a system integration point.

---

## License

Public domain / do whatever you want.

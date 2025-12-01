#!/bin/bash

vRuta="$(pwd)"

python3 -m pip install Flask --break-system-packages

nohup python3 "$vRuta/01-BrokenAccessControl.py" >/dev/null 2>&1 &
nohup python3 "$vRuta/02-SecurityMisconfiguration.py" >/dev/null 2>&1 &
nohup python3 "$vRuta/03-Injection.py" >/dev/null 2>&1 &
nohup python3 "$vRuta/04-InsecureDesign.py" >/dev/null 2>&1 &
nohup python3 "$vRuta/05-SecurityMisconfiguration.py" >/dev/null 2>&1 &
nohup python3 "$vRuta/06-VulnerableAndOutdatedComponents.py" >/dev/null 2>&1 &
nohup python3 "$vRuta/07-IdentificationAndAuthenticationFailures.py" >/dev/null 2>&1 &
nohup python3 "$vRuta/08-SoftwareAndDataIntegrityFailures.py" >/dev/null 2>&1 &
nohup python3 "$vRuta/09-LoggingAndMonitoringFailures.py" >/dev/null 2>&1 &
nohup python3 "$vRuta/10-SSRF.py" >/dev/null 2>&1 &

# 📦 Guía de Instalación de PHAH

## Prerequisitos

1. **Ollama** - Ejecutándose localmente
2. **Python 3.8+**
3. **Herramientas de pentesting** (nmap, nikto, etc.)

---

## Pasos de Instalación

### 1. Instalar Ollama

```bash
# Instalar Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Iniciar servidor Ollama
ollama serve

# En otra terminal, descargar el modelo
ollama pull llama3.2
```

### 2. Configurar PHAH

#### Opción A: Usando Entorno Virtual (Recomendado)

```bash
# Navegar al directorio PHAH
cd /home/nipegun/Git/pruebas/PHAH

# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual
source venv/bin/activate

# Instalar dependencias de Python
pip install -r requirements.txt

# Hacer phah.py ejecutable
chmod +x phah.py

# Probar instalación
python phah.py --list-services
```

#### Opción B: Usando Entorno Virtual Existente

Si ya tienes un entorno virtual (como el de CaiFramework):

```bash
# Activar tu entorno virtual existente
source /home/nipegun/PythonVirtualEnvironments/CaiFramework/bin/activate

# Navegar a PHAH
cd /home/nipegun/Git/pruebas/PHAH

# Instalar dependencias
pip install -r requirements.txt

# Probar
python phah.py --list-services
```

#### Opción C: Instalación en el Sistema (No Recomendado)

```bash
# Solo si entiendes los riesgos
pip install -r requirements.txt --break-system-packages

# O instalar paquetes del sistema
sudo apt install python3-httpx
```

### 3. Instalar Herramientas de Pentesting (Opcional pero Recomendado)

```bash
# Herramientas básicas
sudo apt update
sudo apt install -y nmap curl netcat-traditional

# Herramientas de pruebas web
sudo apt install -y nikto dirb gobuster whatweb

# Herramientas SMB/Samba
sudo apt install -y smbclient enum4linux

# Herramientas adicionales (opcionales)
sudo apt install -y hydra sqlmap wpscan ssh-audit
```

---

## Verificación

### 1. Comprobar Ollama

```bash
# Comprobar que Ollama está ejecutándose
curl http://localhost:11434/api/tags

# Verificar que el modelo está disponible
ollama list | grep llama3.2
```

### 2. Comprobar PHAH

```bash
# Activar entorno virtual (si lo usas)
source venv/bin/activate  # o la ruta de tu venv

# Listar servicios disponibles
python phah.py --list-services

# Salida esperada:
# ╔════════════════════════════════════════════════════════════════╗
# ║              PHAH - Servicios Disponibles                      ║
# ╚════════════════════════════════════════════════════════════════╝
#
#   web             - Pruebas de aplicaciones web (HTTP/HTTPS)     [Puertos: 80, 443, 8080, 8443]
#   ssh             - Evaluación de seguridad del servicio SSH     [Puertos: 22]
#   ...
```

### 3. Comprobar Herramientas

```bash
# Comprobar si las herramientas están instaladas
which nmap
which curl
which smbclient

# Comprobar versiones
nmap --version
```

---

## Ejecutar PHAH

### Con Entorno Virtual

```bash
# Siempre activar el venv primero
source venv/bin/activate  # o la ruta de tu venv

# Ejecutar PHAH
python phah.py -service web -target https://ejemplo.com
```

### Script de Ejecución Rápida

Crear un script auxiliar `run_phah.sh`:

```bash
#!/bin/bash
cd /home/nipegun/Git/pruebas/PHAH
source venv/bin/activate
python phah.py "$@"
```

Hacerlo ejecutable:

```bash
chmod +x run_phah.sh

# Usarlo:
./run_phah.sh -service web -target https://ejemplo.com
```

---

## Solución de Problemas

### Problema: "ModuleNotFoundError: No module named 'httpx'"

**Solución**: Activar entorno virtual e instalar dependencias

```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Problema: "externally-managed-environment"

**Solución**: Usar un entorno virtual (Opción A o B arriba)

### Problema: "Connection refused" a Ollama

**Solución**: Iniciar servidor Ollama

```bash
# Terminal 1: Iniciar Ollama
ollama serve

# Terminal 2: Ejecutar PHAH
source venv/bin/activate
python phah.py -service web -target ejemplo.com
```

### Problema: "Model not found"

**Solución**: Descargar el modelo

```bash
ollama pull llama3.2

# O usar un modelo diferente
python phah.py -service web -target ejemplo.com -model mistral
```

### Problema: "Command not found: nmap"

**Solución**: Instalar herramientas de pentesting

```bash
sudo apt install nmap
```

---

## Desinstalación

```bash
# Eliminar entorno virtual
rm -rf venv

# Eliminar directorio PHAH
cd /home/nipegun/Git/pruebas
rm -rf PHAH
```

---

## Próximos Pasos

Una vez instalado:

1. Lee `QUICK_START.md` para ejemplos de uso
2. Lee `README.md` para documentación completa
3. Prueba un test básico:
   ```bash
   source venv/bin/activate
   python phah.py -service web -target https://ejemplo.com
   ```

---

**¡Instalación Completa! ¡Listo para hackear (solo objetivos autorizados)! 🔐**

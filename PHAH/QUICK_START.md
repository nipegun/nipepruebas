# 🚀 PHAH - Guía de Inicio Rápido

## Comprobación de Prerequisitos

```bash
# 1. Comprobar que Ollama está ejecutándose
curl http://localhost:11434/api/tags

# 2. Comprobar que el modelo está disponible
ollama list | grep llama3.2

# Si no está disponible:
ollama pull llama3.2
```

## Instalación

```bash
cd /home/nipegun/Git/pruebas/PHAH

# Instalar dependencias
pip install -r requirements.txt

# Hacer ejecutable
chmod +x phah.py
```

## Ejemplos Rápidos

### 1. Listar Servicios Disponibles

```bash
python phah.py --list-services
```

### 2. Prueba de Aplicación Web (Sin Reporte)

```bash
# Probar un sitio web - salida solo en terminal
python phah.py -service web -target https://ejemplo.com

# Probar con puerto personalizado
python phah.py -service web -target https://ejemplo.com -port 8080
```

### 3. Prueba de Aplicación Web (Con Reporte)

```bash
# Generar reportes completos (HTML, MD, JSON)
python phah.py -service web -target https://ejemplo.com -report
```

### 4. Evaluación de Seguridad SSH

```bash
# Puerto por defecto 22
python phah.py -service ssh -target 192.168.1.10

# Puerto personalizado con reporte
python phah.py -service ssh -target 192.168.1.10 -port 2222 -report
```

### 5. Pruebas Samba/SMB

```bash
# Probar servicios SMB
python phah.py -service samba -target 192.168.1.10 -report
```

### 6. Prueba de Seguridad FTP

```bash
# Prueba FTP básica
python phah.py -service ftp -target ftp.ejemplo.com

# Con puerto personalizado
python phah.py -service ftp -target 192.168.1.10 -port 2121
```

## Plantilla de Comando

```bash
python phah.py \
  -service <SERVICIO> \
  -target <OBJETIVO> \
  [-port <PUERTO>] \
  [-report] \
  [-model <MODELO>] \
  [-quiet]
```

## Servicios Comunes

| Ejemplo de Comando | Descripción |
|-------------------|-------------|
| `-service web -target https://sitio.com` | Pruebas de aplicaciones web |
| `-service ssh -target 192.168.1.10` | Auditoría de seguridad SSH |
| `-service samba -target 192.168.1.10` | Pruebas SMB/Samba |
| `-service ftp -target ftp.sitio.com` | Pruebas FTP |
| `-service mysql -target 192.168.1.10` | Pruebas MySQL |

## Ejemplos de Salida

### Salida en Terminal (Sin Reporte)

```
╔═══════════════════════════════════════════════════════════════════╗
║                       PHAH                                        ║
║        Plataforma de Hacking de Penetración Automatizada         ║
╚═══════════════════════════════════════════════════════════════════╝

📋 Configuración:
   Servicio:      WEB
   Objetivo:      https://ejemplo.com
   Puerto:        443
   Modelo:        llama3.2
   Reporte:       No

[20:15:30] [PHAH] Iniciando prueba de penetración automatizada
[20:15:31] [IA] Inicializando pentester de IA...
[20:15:35] [CMD] Ejecutando: nmap -sV -p 443 ejemplo.com
...
```

### Con Reportes

Los reportes se guardan en el directorio `reports/`:

```
reports/
├── phah_web_ejemplo.com_20231122_201530.html
├── phah_web_ejemplo.com_20231122_201530.md
└── phah_web_ejemplo.com_20231122_201530.json
```

## Solución de Problemas

### "Connection refused" a Ollama

```bash
# Iniciar Ollama
ollama serve

# En otra terminal, verificar
curl http://localhost:11434/api/tags
```

### "Model not found"

```bash
# Descargar el modelo
ollama pull llama3.2

# O probar con otro modelo
python phah.py -service web -target ejemplo.com -model mistral
```

### "Command not found" (nmap, etc.)

```bash
# Instalar herramientas de pentesting
sudo apt update
sudo apt install nmap nikto curl smbclient enum4linux
```

## Consejos

1. **Comienza con objetivos pequeños**: Prueba primero en tus propios sistemas
2. **Usa modo silencioso** para salida menos verbosa: `-quiet`
3. **Diferentes modelos** para diferentes tareas:
   - `llama3.2` - Propósito general (por defecto)
   - `mistral` - Ejecución más rápida
   - `codellama` - Mejor para análisis de código
   - `qwen2.5` - Reportes detallados

4. **Obtén siempre autorización** antes de probar objetivos externos

## Próximos Pasos

- Lee el README.md completo para documentación detallada
- Revisa el directorio prompts/ para metodologías de prueba específicas por servicio
- Revisa los reportes generados en el directorio reports/
- Personaliza los prompts según tus necesidades específicas

---

**¡Feliz Hacking (Autorizado)! 🔐**

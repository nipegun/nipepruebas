"""
Servicios PHAH
Módulos de pruebas de penetración específicos por servicio
"""

# Puertos por defecto de servicios
SERVICE_PORTS = {
  'web': [80, 443, 8080, 8443],
  'ssh': [22],
  'samba': [139, 445],
  'smb': [139, 445],
  'ftp': [21],
  'mysql': [3306],
  'postgresql': [5432],
  'rdp': [3389],
  'dns': [53],
  'smtp': [25, 465, 587],
  'pop3': [110, 995],
  'imap': [143, 993],
  'telnet': [23],
  'vnc': [5900],
  'mongodb': [27017],
  'redis': [6379],
  'elasticsearch': [9200],
}

def get_default_ports(service: str) -> list:
  """
  Obtener puertos por defecto para un servicio

  Args:
    service: Nombre del servicio

  Returns:
    Lista de puertos por defecto
  """
  return SERVICE_PORTS.get(service.lower(), [])

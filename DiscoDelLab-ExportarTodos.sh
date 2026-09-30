#!/bin/bash

# Carpeta donde guardar
  vCarpetaCyberSecLab="/Particiones/Datos/CyberSecLab"

# Carpeta de imagenes de PVE
  vCarpetaDeIMGs="/Particiones/local-lvm/images"

# Crear la carpeta donde guardar (En el caso de que no esté creada)
  mkdir -p "$vCarpetaCyberSecLab"

# CopSeg OpenWrtLab
  rm -v -f "$vCarpetaCyberSecLab"/openwrtlab.vmdk
  qemu-img convert -O vmdk "$vCarpetaDeIMGs"/1000/vm-1000-disk-0/disk.raw "$vCarpetaCyberSecLab"/openwrtlab.vmdk

# CopSeg Kali
  rm -v -f "$vCarpetaCyberSecLab"/kali.vmdk
  qemu-img convert -O vmdk "$vCarpetaDeIMGs"/1002/vm-1002-disk-0/disk.raw "$vCarpetaCyberSecLab"/kali.vmdk

# CopSeg Sift
  rm -v -f "$vCarpetaCyberSecLab"/sift.vmdk
  qemu-img convert -O vmdk "$vCarpetaDeIMGs"/1003/vm-1003-disk-0/disk.raw "$vCarpetaCyberSecLab"/sift.vmdk

# CopSeg WindServer22
  rm -v -f "$vCarpetaCyberSecLab"/winserver22.vmdk
  qemu-img convert -O vmdk "$vCarpetaDeIMGs"/1004/vm-1004-disk-0/disk.raw "$vCarpetaCyberSecLab"/winserver22.vmdk

# CopSeg Win11Pro
  rm -v -f "$vCarpetaCyberSecLab"/win11pro.vmdk
  qemu-img convert -O vmdk "$vCarpetaDeIMGs"/1005/vm-1005-disk-0/disk.raw "$vCarpetaCyberSecLab"/win11pro.vmdk

# CopSeg Debian12
  rm -v -f "$vCarpetaCyberSecLab"/debian12.vmdk
  qemu-img convert -O vmdk "$vCarpetaDeIMGs"/1006/vm-1006-disk-0/disk.raw "$vCarpetaCyberSecLab"/debian12.vmdk

# CopSeg Ubuntu24
  rm -v -f "$vCarpetaCyberSecLab"/ubuntu24.vmdk
  qemu-img convert -O vmdk "$vCarpetaDeIMGs"/1007/vm-1007-disk-0/disk.raw "$vCarpetaCyberSecLab"/ubuntu24.vmdk

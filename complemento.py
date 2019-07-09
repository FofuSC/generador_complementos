from xml.dom.minidom import parse
import base64
from M2Crypto import RSA
from lxml import etree as ET
import hashlib
import subprocess

print("""
---------------------------------------------------------------------
| AL HACER USO DE ESTE SCRIPT DEBE TOMAR EN CUENTA QUE LAS RUTAS DE |
|  LOS ARCHIVOS NO DEBE IR ENTRE COMILLAS Y QUE EL XML DEL CUAL SE  |
| QUIERE EXTRAER LOS COMPLEMENTOS DEBE ESTAR PREVIAMENTE MODIFICADO |
---------------------------------------------------------------------\n""")

get_serial = ""
get_certificado = ""
get_sello = ""

ruta_cadena = raw_input("Archivo Cadena Original: ")
ruta_cer = raw_input("Archivo CER: ")
ruta_xml = raw_input("Archivo XML: ")
ruta_pem = raw_input("Archivo KEY.PEM: ")

certificado = subprocess.check_output('openssl x509 -inform DER -in ' + str(ruta_cer), shell=True).replace("\n", "")
serial = subprocess.check_output('openssl x509 -inform DER -in ' + str(ruta_cer) + ' -noout -serial', shell=True)

indice = 7
while indice < len(serial):
	if indice % 2 == 0:
		get_serial += serial[indice]
	indice += 1

indice = 27
while indice < len(certificado) - 25:
	get_certificado += certificado[indice]
	indice += 1

def generar_sello( nombre_archivo, llave_pem ):
	file = open(nombre_archivo, 'r')
	comprobante = file.read()
	file.close()
	xdoc = ET.fromstring(comprobante)
	xsl_root = ET.parse(ruta_cadena)
	xsl = ET.XSLT(xsl_root)
	cadena_original = xsl(xdoc)

	keys = RSA.load_key(llave_pem)
	digest = hashlib.new('sha256', str(cadena_original).encode()).digest()
	get_sello = base64.b64encode(keys.sign(digest, "sha256"))

	print("-------------------- SELLO --------------------")
	print(get_sello)

generar_sello( ruta_xml, ruta_pem )

print("----------------- CERTIFICADO -----------------")
print(get_certificado)

print("------------------- SERIAL -------------------")
print(get_serial)
# Ejecutar pip install qrcode para instalar la librería
import qrcode
import qrcode.constants

# modifca estos parametros para generar un QR con los datos de tu red
data = {
    "s": "casa", # SSID de la red (nombre de la red)
    "t": "WPA2", # tipo de seguridad (WPA, WPA2, WEP)
    "p": "12345678" # contraseña de la red
}

wifi = f"WIFI:S:{data['s']};T:{data['t']};P:{data['p']};;"
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)

qr.add_data(wifi)
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")

# Guarda la imagen en la carpeta que desees
img.save(r"C:\Users\risse\Downloads\Automating_DailyTasks\QR_WIFI\img_qr\wifi.png")

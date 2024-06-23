import network
import camera
import socket
import time

ssid = 'HWA16'
password = 'hwahwa16'

wlan = network.WLAN(network.STA_IF)
wlan.active(False)
wlan.active(True)
wlan.connect(ssid,password)
print('connecting to network...')
while not wlan.isconnected():
    print('still connecting')
    time.sleep(1)
print('Connected wifi: ',wlan.ifconfig()[0])
esp32 = wlan.ifconfig()[0]

try:
    camera.init(0, format=camera.JPEG, fb_location=camera.PSRAM)
except Exception as e:
    camera.deinit()
    camera.init(0, format=camera.JPEG, fb_location=camera.PSRAM)

camera.flip(0)
camera.mirror(1)
camera.framesize(camera.FRAME_HVGA)
camera.speffect(camera.EFFECT_NONE)
camera.whitebalance(camera.WB_HOME)
camera.saturation(0)
camera.brightness(0)
camera.contrast(0)
camera.quality(10)

server = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
server.bind((esp32,12345))

try:

    while(True):
        buf = camera.capture()
        server.sendto(buf,('192.168.0.198',20000))
        time.sleep(0.4)
        server.sendto(buf,('192.168.0.122',9090))
        print('已發送')
    camera.deinit()

except Exception as e:
    print(e)
finally:
    camera.deinit()
import time
from utime import sleep
from machine import Pin, SoftI2C, SoftSPI, Timer, UART  #匯入模組
from esp8266_i2c_lcd import I2cLcd
import max7219
import network
import socket

#改IP

# 連接wifi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected(): # 連接網路
    print('connecting to network...')
    wlan.connect("LJPhone", "ihateesp32")   #wifi名字、密碼

    while not wlan.isconnected():
        pass
print('網路配置:', wlan.ifconfig())

s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM,0)
s.bind(('192.168.214.54',22000)) #IP
s.settimeout(0.1)

#UART setting
# uart = UART(1, baudrate=115200, tx=17, rx=16)
# def read_from_uart():
#     if uart.any():
#         data = uart.read()
#         return data.decode('utf-8')
#     return None

#lcd1602 setting
DEFAULT_I2C_ADDR = 0x27
i2c = SoftI2C(scl=Pin(22), sda=Pin(21),freq=100000)#建立SoftI2C類別物件
lcd = I2cLcd(i2c, DEFAULT_I2C_ADDR, 2, 16)

#max7219 setting
spi = SoftSPI(sck=27, mosi=12, miso=13) #mosi=DIN sck=clk miso需輸入port但不接線
cs = Pin(14, Pin.OUT) #cs=cs
door = max7219.Matrix8x8(spi, cs, 1)
door.init() #初始化
door.brightness(1) #亮度0-15

#button setting
button=[18, 19, 17, 35, 23, 34, 39, 2, 36]
for i in range(9):
    button[i]=Pin(button[i], Pin.IN, Pin.PULL_UP)
button_state=[0,0,0,0,0,0,0,0,0] #0-4 1-5F 5close 6open 7openlong 8emgc
floor_now=1 #初始一樓 1-5
direct=0 #0停止 1上樓 2下樓 3開關門
task = []
isPlay=False

#初始狀態關門
door.fill_rect(0,0,8,8,1)
door.show()
sleep(1)

def lcd_renew(floor_now,direct): #電梯內面板
    sentence= "　　     "+str(floor_now)+"F     　　\n"
    lcd.clear() #清除螢幕
    lcd.putstr(sentence) #第一行
    if direct ==3:
        lcd.putstr("　　  |      |  　　") #第二行
    elif direct ==2:
        lcd.putstr("　　  v      v  　　") #第二行
    elif direct ==1:
        lcd.putstr("　　  ^      ^  　　") #第二行
    else:
        lcd.putstr("　　  -      -  　　") #第二行

def door_open(): #開門
    door.vline(4,0,8,0)
    door.vline(3,0,8,0)
    door.show()
    sleep(0.5)
    door.vline(2,0,8,0)
    door.vline(5,0,8,0)
    door.show()
    sleep(0.5)
    door.vline(1,0,8,0)
    door.vline(6,0,8,0)
    door.show()

def door_close(): #關門
    door.vline(1,0,8,1)
    door.vline(6,0,8,1)
    door.show()
    sleep(0.5)
    door.vline(2,0,8,1)
    door.vline(5,0,8,1)
    door.show()
    sleep(0.5)
    door.vline(4,0,8,1)
    door.vline(3,0,8,1)
    door.show()

def opendoor(time): #0 open -30 openlong
    door_open()
    q=time
    while q<30:
        if button_state[5] ==1:
            button_state[5] = 0
            door_close()
            q=30
        elif button_state[6] ==1:
            button_state[6] = 0
            q=0
        elif button_state[7] ==1:
            button_state[7] = 0
            q=-30
        else:
            q+=1
            sleep(0.1)
    door_close()
#Timer check check if button push & emgc
def timer_callback(t):
    global floor_now, direct, isPlay
    if isPlay==False:
        # Face recogition
        try:

            received_data, IP=s.recvfrom(1024)
            if received_data.decode() =="ok":
                print(received_data.decode())
                isPlay=True
        except:
            pass

    elif isPlay:
        ## button can work
        for j in range(5):
            F = j+1
            if button[j].value()==1:
                button_state[j]=1
                print(j,"button pushed")
            if button_state[j]==1 and not task and F!= floor_now:
                task.append(F)
                print(task)
                if F > floor_now:
                    direct = 1
                else :
                    direct =2
            elif button_state[j]==1 and F > floor_now and direct ==1 and F != task[-1]:
                task.append(F)
                task.sort()
                print(task)
            elif button_state[j]==1 and F < floor_now and direct ==2 and F != task[0]:
                task.append(F)
                task.sort(reverse=True)
                print(task)
            button_state[j]=0
    for j in range (5,9):
        if button[j].value()==1:
            button_state[j]=1
            print(j,"button pushed")
    if button_state[8]==1:
        print("Emergency ", floor_now, "F now") #EMGC
        msg = '有人現在被困在'+str(floor_now)+'F, 請盡速救援!!\n'
        s.sendto(msg,('192.168.214.187',25000)) #IP
        button_state[8]=0


# 設置定時器
timer = Timer(-1)
timer.init(period=300, mode=Timer.PERIODIC, callback=timer_callback)
lcd_renew(floor_now,direct)

while True:
    if task and direct ==1:
        while floor_now < task[0]:
            floor_now+=1
            lcd_renew(floor_now,direct)
            sleep(2)
        direct = 3
        lcd_renew(floor_now,direct)
        opendoor(0)
        task.pop(0)
        if not task :
            direct=0
            lcd_renew(floor_now,direct)
        else :
            direct =1
    elif task and direct==2:
        while floor_now > task[0]:
            floor_now-=1
            lcd_renew(floor_now,direct)
            sleep(2)
        direct = 3
        lcd_renew(floor_now,direct)
        opendoor(0)
        task.pop(0)
        if not task :
            direct=0
            lcd_renew(floor_now,direct)
        else :
            direct =2
    elif button_state[5] ==1:
        button_state[5] =0
    elif button_state[6] ==1:
        direct=3
        lcd_renew(floor_now,direct)
        opendoor(0)
        button_state[6] =0
        direct=0
        lcd_renew(floor_now,direct)
    elif button_state[7] ==1:
        direct=3
        lcd_renew(floor_now,direct)
        opendoor(-50)
        button_state[7] =0
        direct=0
        lcd_renew(floor_now,direct)
    else:
        sleep(0.1)

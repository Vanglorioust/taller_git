#Jose Baza - Leonardo Salgado 
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


from pyfirmata import Arduino, util
from tkinter import *
from PIL import Image
from PIL import ImageTk
import time
cont=0
prom=0

placa = Arduino ('COM3')
it = util.Iterator(placa)
it.start()
a_0 = placa.get_pin('a:0:i')
led1 = placa.get_pin('d:3:p')
led2 = placa.get_pin('d:5:p')
led3 = placa.get_pin('d:6:p')
led4 = placa.get_pin('d:9:p')
led5 = placa.get_pin('d:10:p')
led6 = placa.get_pin('d:11:p')
led7 = placa.get_pin('d:12:p')
time.sleep(0.5)
ventana = Tk()
ventana.geometry('1090x545')
ventana.title("UI para sistemas de control")

# Fetch the service account key JSON file contents
cred = credentials.Certificate('key/key.json')
# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://taller-git.firebaseio.com/'
})


marco1 = Frame(ventana, bg="gray", highlightthickness=1, width=1280, height=800, bd= 5)
marco1.place(x = 0,y = 0)
b=Label(marco1,text="")
img = Image.open("D:/Perfil Raul Henao/Desktop/pu/AI")
img = img.resize((150,150), Image.ANTIALIAS)
photoImg=  ImageTk.PhotoImage(img)
b.configure(image=photoImg)
b.place(x = 760,y = 20)

valor= Label(marco1, bg='cadet blue1', font=("Arial Bold", 15), fg="white", width=5)
variable=StringVar()
valor2= Label(marco1, bg='cadet blue1', font=("Arial Bold", 15), fg="white", width=5)
adc_data=StringVar()

def adc_read():
    global prom
    i=0
    prom=0
    while i<15:
        i=i+1
        x=a_0.read()
        print(x)
        adc_data.set(x)
        prom=x+prom
        ventana.update()
        time.sleep(0.1)
    prom=prom/15
    print("El promedio es ",prom)
    ref = db.reference('sensor')
    ref.update({
        'sensor1/adc': prom
    })
def Leds_on():

    led5.write(1)
    
    led6.write(1)
    
    led7.write(1)
    
    ref = db.reference("sensor")
    
    ref.update({
                  'sensor1/led10': 'ON',
                  'sensor1/led11': 'ON',
                  'sensor1/led12': 'ON'
                    
         })
def Leds_off():

    led5.write(0)
    
    led6.write(0)
    
    led7.write(0)
    
    ref = db.reference("sensor")
    
    ref.update({
                  'sensor1/led10': 'OFF',
                  'sensor1/led11': 'OFF',
                  'sensor1/led12': 'OFF'
                    
         })
def update_label():
    global cont
    if cont>4:
        cont=cont-2
        ref = db.reference("sensor")
        ref.update({
                    'sensor1': {
                        'valor': cont,

                }
             })
    if cont==4:
        cont=cont-2
        ref = db.reference("sensor")
        ref.update({
                    'sensor1': {
                        'valor': 0,
                 }
             })
    if cont==2:
        cont=cont-2
        ref = db.reference("sensor")
        ref.update({
                    'sensor1': {
                        'valor': 0,
                 }
             })   
    variable.set(cont)

    
  

valor.configure(textvariable=variable)
valor.place(x=20, y=90)
start_button=Button(marco1,text="cont",command=update_label)
start_button.place(x=240, y=150)

valor2.configure(textvariable=adc_data)
valor2.place(x=130, y=90)

prom_15=Button(marco1,text="prom_15",command=adc_read)
prom_15.place(x=10, y=160)

leds_on=Button(marco1,text="LEDS_ON",command=Leds_on)
leds_on.place(x=80, y=160)

save_button=Button(marco1,text="LEDS_OFF",command=Leds_off)
save_button.place(x=170, y=160)





ventana.mainloop()

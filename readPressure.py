import serial

ser = serial.Serial("COM3", baudrate= 115200, timeout=2.5)
while ser.isOpen():
    ser.flush()
    try:
        incoming = ser.readline().decode("UTF-8")
        print(incoming)
    except Exception as e:
        print(e)
        pass    
ser.close()

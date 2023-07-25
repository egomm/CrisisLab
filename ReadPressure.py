import serial
import matplotlib.pyplot as plt

ser = serial.Serial("COM4", baudrate=115200, timeout=2.5)

MAX = 20
# You probably won't need this if you're embedding things in a tkinter plot...
plt.ion()

x = [0]
y = [0]


fig, ax = plt.subplots(figsize=(10, 8))
line1, = ax.plot(x, y)
ax.set_xlim(0, MAX)
ax.set_ylim(50000, 120000)

i = 0
while ser.isOpen():
    ser.flush()
    try:
        incoming = ser.readline().decode("UTF-8").rstrip()
        print('"' + incoming + '"', incoming.isnumeric())
        if incoming.isnumeric():
            incoming = float(incoming)
            print(incoming)
            x.append(x[-1] + 1)
            y.append(incoming)

            if (i >= MAX):
                x.pop(0)
                y.pop(0)
                ax.set_xlim(x[0], x[-1])

            line1.set_xdata(x)
            line1.set_ydata(y)

            fig.canvas.draw()
            fig.canvas.flush_events()

            i += 1
    except Exception as e:
        print(e)
        continue
    
ser.close()
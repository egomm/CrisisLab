import serial
import matplotlib.pyplot as plt

ser = serial.Serial("COM4", baudrate=115200, timeout=2.5)

MIN = 3
MAX = 20
plt.ion()

fig, ax = plt.subplots(figsize=(10, 8))

i = 0
while ser.isOpen():
    ser.flush()
    try:
        incoming = ser.readline().decode("UTF-8").rstrip()
        print(incoming)

        if i == MIN:
            incoming = float(incoming)
            x = [0]
            y = [incoming]
            ax.set_xlim(0, MAX)
            ax.set_ylim(incoming - incoming * 0.1, incoming + incoming * 0.1)
            line1, = ax.plot(x, y)

        if i > MIN:
            incoming = float(incoming)

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
        print("Error:")
        print(e)
        continue
    
ser.close()
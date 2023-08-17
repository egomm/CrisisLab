import serial
import matplotlib.pyplot as plt

ser = serial.Serial("COM4", baudrate=115200, timeout=2.5)

MIN = 2
MAX = 20
plt.ion()
plt.title("Tsunami Detector")

ROU = 1.0
GRA = 9.81

fig, axis = plt.subplots(1, 2)
fig.canvas.manager.full_screen_toggle()
fig.subplots_adjust(wspace=0.4)

ax = axis[0]
ax.set_title("Pressure Against Time")
ax.set_xlabel("Time(s)")
ax.set_ylabel("Pressure(Pa)")

ax2 = axis[1]
ax2.set_title("Height Against Time")
ax2.set_xlabel("Time(s)")
ax2.set_ylabel("Height(m)")

i = 0
while ser.isOpen():
    ser.flush()
    try:
        incoming = ser.readline().decode("UTF-8").rstrip()
        print(incoming)

        # Init the graph when the value is stablized.
        if i == MIN:
            incoming = float(incoming)
            x = [0]
            y = [incoming]
            ax.set_xlim(0, MAX)
            ax.set_ylim(incoming - incoming * 0.3, incoming + incoming * 0.3)
            line1, = ax.plot(x, y)

            height = incoming / (ROU * GRA)
            y2 = [height]
            ax2.set_xlim(0, MAX)
            ax2.set_ylim(height - height * 0.3, height + height * 0.3)
            line2, = ax2.plot(x, y)

        # Update the graph and plot it.
        if i > MIN:
            incoming = float(incoming)
            height = incoming / (ROU * GRA)

            x.append(x[-1] + 1)
            y.append(incoming)
            y2.append(height)

            if (i >= MAX):
                x.pop(0)
                y.pop(0)
                y2.pop(0)
                ax.set_xlim(x[0], x[-1])
                ax2.set_xlim(x[0], x[-1])

            line1.set_xdata(x)
            line1.set_ydata(y)
            ax.set_ylim(incoming - incoming * 0.3, incoming + incoming * 0.3)

            line2.set_xdata(x)
            line2.set_ydata(y2)
            ax2.set_ylim(height - height * 0.3, height + height * 0.3)

            fig.canvas.draw()
            fig.canvas.flush_events()

        i += 1
    except Exception as e:
        print("Error:")
        print(e)
        continue
    
ser.close()
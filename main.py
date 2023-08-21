import serial
import matplotlib.pyplot as plt
import time
import math
import threading
from func import send_email, find_port


COM_PORT = find_port()
if COM_PORT is not None:
    ser = serial.Serial(COM_PORT, baudrate=115200, timeout=2.5)
else:
    exit()

# Define the constants
MIN = 2
MAX = 20
# The base may change depending on the room/air
BASE = 101000

ROU = 1000 # Density in kg/m^3
GRA = 9.81

WARNING_HEIGHT = 20 
# Email addresses to alert
RECIPIENTS = []

# Initialize the graph
plt.ion()
plt.title("Tsunami Detector")
fig, axis = plt.subplots(1, 2)
fig.canvas.manager.full_screen_toggle()
fig.subplots_adjust(wspace=0.4)

ax = axis[0]
ax.set_title("Pressure Against Time")
ax.set_xlabel("Time (s)")
ax.set_ylabel("Pressure (Pa)")

ax2 = axis[1]
ax2.set_title("Height Against Time")
ax2.set_xlabel("Time (s)")
ax2.set_ylabel("Height (cm)")

last_time = 0
start_time = time.time()
i = 0
while True:
    if ser.isOpen():
        ser.flush()
        try:
            # Receive the incoming graph
            incoming = float(ser.readline().decode("UTF-8").rstrip())
            # Multiply by 100 to convert to cm
            height = max(100 * (incoming - BASE) / (ROU * GRA), 0)

            # Initialize the graph when the value is stabilized.
            if i == MIN:
                x = [0]
                y = [incoming]
                ax.set_xlim(0, MAX)
                ax.set_ylim(incoming - incoming * 0.3, incoming + incoming * 0.3)
                line1, = ax.plot(x, y)

                y2 = [height]
                ax2.set_xlim(0, MAX)
                ax2.set_ylim(height - height * 0.3, height + height * 0.3)
                line2, = ax2.plot(x, y2)

                figtext = ax2.text(0.95, 0.01, "Amplitude: 0cm",
                verticalalignment='bottom', horizontalalignment='right',
                transform=ax2.transAxes, fontsize=12)

            # Update the graph and plot it.
            if i > MIN:
                x.append(x[-1] + 0.25)
                y.append(incoming)
                y2.append(height)

                amplitude = (max(y2) - min(y2)) / 2
                text = "Amplitude: " + str(round(amplitude, 3)) + "cm"
                figtext.set_text(text)

                # Send warning email if height is larger
                if (amplitude) > WARNING_HEIGHT:
                    # Limit emails to every 10 minutes
                    if time.time() - last_time > 600:
                        last_time = time.time()
                        t = threading.Thread(target=send_email, args=[RECIPIENTS, height])
                        t.run()

                if x[-1] >= MAX:
                    x.pop(0)
                    y.pop(0)
                    y2.pop(0)
                    ax.set_xlim(x[0], x[-1])
                    ax2.set_xlim(x[0], x[-1])

                line1.set_xdata(x)
                line1.set_ydata(y)
                ax.set_ylim(min(y) - max(y) * 0.3, max(y) + max(y) * 0.3)
                #ax.set_ylim(incoming - incoming * 0.3, incoming + incoming * 0.3)

                line2.set_xdata(x)
                line2.set_ydata(y2)
                ax2.set_ylim(min(y2) - max(y2) * 0.3, max(y2) + max(y2) * 0.3)
                #display_max_height = max(y2) # Changed this as y2 is already the dataset(within MAX)
                #if display_max_height == 0:
                #    display_max_height = 10
                #ax2.set_ylim(0, math.ceil(display_max_height / 20) * 20)
                fig.canvas.draw()
                fig.canvas.flush_events()

            i += 0.25
        except Exception as e:
            print("Error:")
            print(e)
            continue

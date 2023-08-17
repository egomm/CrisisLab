import matplotlib.pyplot as plt
import random

MAX = 20

# You probably won't need this if you're embedding things in a tkinter plot...
plt.ion()

x = [0]
y = [0]


fig, ax = plt.subplots(figsize=(10, 8))
line1, = ax.plot(x, y)
ax.set_xlim(0, MAX)
ax.set_ylim(0, 1)

i = 0
while True:
    x.append(x[-1] + 1000)
    y.append(random.random())

    if (i >= MAX):
        x.pop(0)
        y.pop(0)
        ax.set_xlim(x[0], x[-1])

    line1.set_xdata(x)
    line1.set_ydata(y)


    fig.canvas.draw()
    fig.canvas.flush_events()

    i += 1
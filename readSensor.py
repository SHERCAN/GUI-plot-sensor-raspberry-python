#import Adafruit_ADS1x15
from random import choice
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from csv import writer


class ReadSensor:
    def __init__(self):
        self.t = 0
        self.limitXMax = 200
        self.limitYMax = 40000
        self.limitXMin = 0
        self.limitYMin = -40000
        self.ale = []
        self.plt = plt
        self.fig, self.ax = self.plt.subplots()
        self.ax.set_title('EKG')
        self.ax.set_xlabel('Tiempo')
        self.ax.set_ylabel('Amplitud')
        self.ax.set_ylim(self.limitYMin, self.limitYMax)
        self.ax.set_xlim(self.limitXMin, self.limitXMax)
        self.line, = self.ax.plot([], [], lw=2)
        self.ax.grid()
        self.xdata, self.ydata = [], []
        self.ani = None

    def animation(self, interval: int):
        self.ani = FuncAnimation(
            self.fig, self.run, self.data_gen, interval=interval, init_func=self.init)

    def valor(self):
        # La función de lectura del sensor se pone dentro de esta función se debe agregar al atibuto ale en una lista
        self.ale.append(choice(range(self.limitYMin, self.limitYMax)))
        # int((adc.read_adc(0, gain=16, data_rate=860)))

    def data_gen(self):
        self.valor()
        for cnt in self.ale:
            self.t += 1
            y = cnt
            yield self.t, y

    def init(self):
        self.ax.set_ylim(self.limitYMin, self.limitYMax)
        self.ax.set_xlim(self.limitXMin, self.limitXMax)
        del self.xdata[:]
        del self.ydata[:]
        self.line.set_data(self.xdata, self.ydata)
        return self.line,

    def run(self, data):
        x, y = data
        self.xdata.append(x)
        self.ydata.append(y)
        _, xmax = self.ax.get_xlim()

        if x >= xmax:
            self.ax.set_xlim(xmax+1-self.limitXMax, x)
            self.ax.figure.canvas.draw()
        self.line.set_data(self.xdata, self.ydata)
        self.valor()
        return self.line,

    def pauseAnimation(self, event):
        if event:
            self.ani.event_source.stop()
        else:
            self.ani.event_source.start()

    def exportData(self, name, breed, age):
        name = name+'_'+breed+'_'+age+'.csv'
        with open(name, 'w', newline='') as f:
            write = writer(f)
            write.writerows(zip(self.xdata, self.ydata))

#import Adafruit_ADS1x15
from random import choice
from threading import Thread
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from csv import writer
from time import sleep
import sys
from numpy import array,concatenate,arange,linspace,pi,sin

class ReadSensor:
    def __init__(self):
        self.t = None
        self.y = None
        self.limitXMax = 200
        self.limitYMax = 40000
        self.limitXMin = 0
        self.limitYMin = -40000
        self.ale = array([0])
        self.plt = plt
        self.fig, self.ax = self.plt.subplots()
        self.ax.set_title('EKG')
        self.ax.set_xlabel('Tiempo')
        self.ax.set_ylabel('Amplitud')
        self.ax.set_ylim(self.limitYMin, self.limitYMax)
        self.ax.set_xlim(self.limitXMin, self.limitXMax)
        self.line, = self.ax.plot([], [], lw=2)
        self.ax.grid()
        self.xdata, self.ydata = array([0]), array([0])
        self.hilo = None
        self.ani = None
        self.finish=False
        self.pause= True

    def animation(self, interval: int):
        self.hilo=Thread(target=self.valor)
        self.hilo.start()
        self.ani = FuncAnimation(self.fig, self.run, interval=interval, init_func=self.init,blit=True)

    def valor(self):
        while True:
            if self.pause:
                sleep(0.002)
                # La función de lectura del sensor se pone dentro de esta función se debe agregar al atibuto ale en una lista
                self.ale=array([choice(range(self.limitYMin, self.limitYMax))])
                # int((adc.read_adc(0, gain=16, data_rate=860)))
                self.xdata=concatenate((self.xdata, array([self.xdata[-1]+1])))
                self.ydata=concatenate((self.ydata, self.ale.copy()))
                self.ale=array([])
                
            if self.finish:
                print(len(self.xdata))
                print(len(self.ydata))
                break
        #sys.exit()
                
    def init(self):
        self.ax.set_ylim(self.limitYMin, self.limitYMax)
        self.ax.set_xlim(self.limitXMin, self.limitXMax)
        self.line.set_data(self.xdata, self.ydata)
        return self.line,

    def run(self,i):
        _, xmax = self.ax.get_xlim()
        if self.xdata[-1] >= xmax:
            self.ax.set_xlim(xmax+1-self.limitXMax, self.xdata[-1])
            self.ax.figure.canvas.draw()
        self.line.set_data(self.xdata, self.ydata)
        return self.line,

    def pauseAnimation(self, event):
        if event:
            self.pause= False
            self.ani.event_source.stop()
        else:
            self.ani.event_source.start()
            self.pause= True

    def exportData(self, name, breed, age):
        name = name+'_'+breed+'_'+age+'.csv'
        with open(name, 'w', newline='') as f:
            write = writer(f)
            write.writerows(zip(self.xdata, self.ydata))

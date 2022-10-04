from tkinter import Tk, Label, Button, Entry, Frame, RAISED
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from readSensor import ReadSensor
from time import sleep

class Window:
    def __init__(self):
        self.root = Tk()
        self.root.title('EKG CANINO')
        self.root.geometry('790x520')
        self.namePet = ''
        self.breedPet = ''
        self.agePet = ''
        self.pause = False
        self.control = False
        self.Window1()
        self.read = None

    def Window1(self):
        widthTk = 50
        self.root.resizable(height=0, width=0)
        self.frame = Frame(
            master=self.root, relief=RAISED, borderwidth=1)
        self.frame.grid(row=0, column=0)
        f_title = Label(master=self.frame,
                        text='EKG CANINO', font=('Arial', 20))
        f_title.grid(row=0, column=1, columnspan=3, sticky="w")
        f_name = Label(master=self.frame, text='Nombre de la mascota:')
        f_name.grid(row=1, column=0, sticky="w")
        self.f_name_in = Entry(
            master=self.frame, text='Nombre de la mascota', width=widthTk)
        self.f_name_in.grid(row=1, column=1, columnspan=2, sticky="w")
        s_breed = Label(master=self.frame, text='Raza:')
        s_breed.grid(row=2, column=0, sticky="w")
        self.s_breed_in = Entry(master=self.frame, text='Raza', width=widthTk)
        self.s_breed_in.grid(row=2, column=1, columnspan=2, sticky="w")
        s_age = Label(master=self.frame, text='Edad:')
        s_age.grid(row=3, column=0, sticky="w")
        self.s_age_in = Entry(master=self.frame, text='Edad', width=widthTk)
        self.s_age_in.grid(row=3, column=1, columnspan=2, sticky="w")
        ch_enc = Button(master=self.frame, text='INICIO',
                        width=widthTk-30, bg='blue', activebackground='red', fg='white', activeforeground='white', command=lambda: self.clear_window(1))
        ch_enc.grid(row=1, column=3, sticky='w')
        ch_dec = Button(master=self.frame, text='CANCELAR',
                        width=widthTk-30, bg='blue', activebackground='red', fg='white', activeforeground='white', command=self.quit)
        ch_dec.grid(row=2, column=3, sticky='w')
        self.root.mainloop()

    def Window2(self):
        self.read = ReadSensor()
        widthTk = 50
        self.root.resizable(height=0, width=0)
        self.frame = Frame(
            master=self.root, relief=RAISED, borderwidth=1)
        self.frame.grid(row=0, column=0)
        canvas = FigureCanvasTkAgg(self.read.fig, master=self.frame)
        canvas.get_tk_widget().grid(column=3, row=1, columnspan=2, rowspan=4)
        self.read.animation(1)
        f_title = Label(master=self.frame,
                        text='EKG CANINO', font=('Arial', 20))
        f_title.grid(row=0, column=3, columnspan=3)
        f_pause = Button(master=self.frame, text='PAUSA O REANUDA', width=widthTk-30, bg='blue',
                         activebackground='red', fg='white', activeforeground='white', command=self.pauseAnimation)
        f_pause = f_pause.grid(row=1, column=1, columnspan=1, sticky="w")
        f_export = Button(master=self.frame, text='EXPORTAR DATOS', width=widthTk-30, bg='blue',
                          activebackground='red', fg='white', activeforeground='white', command=self.sendData)
        f_export = f_export.grid(row=2, column=1, columnspan=1, sticky="w")
        f_finish = Button(master=self.frame, text='FINALIZA', width=widthTk-30, bg='blue',
                          activebackground='red', fg='white', activeforeground='white', command=lambda: self.clear_window(2))
        f_finish = f_finish.grid(row=3, column=1, columnspan=1, sticky="w")
        self.root.mainloop()
    def quit(self):
        try:
            self.read.finish=True
            sleep(1)
            self.read.hilo.join()
            del self.read.hilo
        except:
            pass
        self.root.destroy()

    def clear_window(self, wd):
        if wd == 1:
            self.namePet = self.f_name_in.get()
            self.breedPet = self.s_breed_in.get()
            self.agePet = self.s_age_in.get()
            for l in self.root.winfo_children():
                l.destroy()
            self.Window2()
        else:
            for l in self.root.winfo_children():
                l.destroy()
            self.Window1()

    def pauseAnimation(self):
        self.pause = not self.pause
        self.read.pauseAnimation(self.pause)

    def sendData(self):
        self.read.exportData(self.namePet, self.breedPet, self.agePet)


if __name__ == '__main__':
    app = Window()

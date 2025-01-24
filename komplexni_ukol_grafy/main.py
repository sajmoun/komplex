#!/usr/bin/env python3

from os.path import basename, splitext
import tkinter as tk

# from tkinter import ttk


class MyEntry(tk.Entry):
    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)

        if not "textvariable" in kw:
            self.variable = tk.StringVar()
            self.config(textvariable=self.variable)
        else:
            self.variable = kw["textvariable"]

    @property
    def value(self):
        return self.variable.get()

    @value.setter
    def value(self, new: str):
        self.variable.set(new)


class About(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent, class_=parent.name)
        self.config()

        btn = tk.Button(self, text="Konec", command=self.close)
        btn.pack()
    

    def close(self):
        self.destroy()


class Application(tk.Tk):
    name = "Grafy funkcí"

    def __init__(self):
        super().__init__(className=self.name)
        self.title(self.name)

        self.fce_var = ""

        #Label1
        self.lbl = tk.Label(self, text="Graf").pack()

        #Frames
        self.frame1 = tk.Frame(self, height=2, bd=1, relief="sunken")
        self.frame1.pack()

        self.frame2 = tk.Frame(self, height=2, bd=1, relief="sunken")
        self.frame2.pack()

        self.frame3 = tk.Frame(self, height=2, bd=1, relief="sunken")
        self.frame3.pack()

        #Frame 1
        self.rbtn1 = tk.Radiobutton(self.frame1, text="sin", variable=self.fce_var, value=0)
        self.rbtn1.grid(row=0, column=0, sticky="w")


        self.rbtn2 = tk.Radiobutton(self.frame1, text="cos", variable=self.fce_var, value=1)
        self.rbtn2.grid(row=1, column=0, sticky="w")


        self.rbtn3 = tk.Radiobutton(self.frame1, text="log", variable=self.fce_var, value=2)
        self.rbtn3.grid(row=2, column=0, sticky="w")


        #Buttons

        self.btngraf1 = tk.Button(self.frame1, text="Graf", height=2, bd=2, width=10, pady=12 ).grid(row=0, column=2, rowspan=3, sticky="e")

        #Entry
        self.entry_od = tk.Entry(self.frame1, )


        self.bind("<Escape>", self.quit)
        self.btn = tk.Button(self, text="Quit", command=self.quit)
        self.btn.pack()

    def about(self):
        pass

    def quit(self, event=None):
        super().quit()


app = Application()
app.mainloop()

import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import tkinter.filedialog as fdialog  # Importujeme tkFileDialog pro výběr souboru

class GrafickaAplikace:
    def __init__(self, root):
        self.root = root
        self.root.title("Graf funkce")
        self.root.bind("<Escape>", self.zavri_aplikaci)
        
        # main frame
        self.frame_funkce = tk.LabelFrame(root, text="Generuj graf funkce")
        self.frame_funkce.pack(padx=10, pady=5, fill=tk.X)

        self.frame_soubor = tk.LabelFrame(root, text="Generuj graf z textových dat")
        self.frame_soubor.pack(padx=10, pady=5, fill=tk.X)

        self.frame_popisky = tk.LabelFrame(root, text="Popisky os")
        self.frame_popisky.pack(padx=10, pady=5, fill=tk.X)

        # fukce vyber
        self.funkce_var = tk.StringVar(value="sin")
        self.radio_sin = tk.Radiobutton(self.frame_funkce, text="sin", variable=self.funkce_var, value="sin")
        self.radio_sin.pack(anchor=tk.W)
        self.radio_log = tk.Radiobutton(self.frame_funkce, text="log", variable=self.funkce_var, value="log")
        self.radio_log.pack(anchor=tk.W)
        self.radio_exp = tk.Radiobutton(self.frame_funkce, text="exp", variable=self.funkce_var, value="exp")
        self.radio_exp.pack(anchor=tk.W)
        
        # max a min hodnoty
        self.od_label = tk.Label(self.frame_funkce, text="Od:")
        self.od_label.pack(side=tk.LEFT, padx=5, pady=2)
        self.min_entry = tk.Entry(self.frame_funkce, width=10)
        self.min_entry.pack(side=tk.LEFT, padx=5, pady=2)
        
        self.do_label = tk.Label(self.frame_funkce, text="Do:")
        self.do_label.pack(side=tk.LEFT, padx=5, pady=2)
        self.max_entry = tk.Entry(self.frame_funkce, width=10)
        self.max_entry.pack(side=tk.LEFT, padx=5, pady=2)
        
        self.generuj_button = tk.Button(self.frame_funkce, text="Vytvoř graf", command=self.generuj_graf)
        self.generuj_button.pack(side=tk.RIGHT, padx=5, pady=2)

        # nahrani ze souboru
        self.soubor_entry = tk.Entry(self.frame_soubor, width=30)
        self.soubor_entry.pack(side=tk.LEFT, padx=5, pady=2)
        
        self.vyber_button = tk.Button(self.frame_soubor, text="Vyber soubor", command=self.vyber_soubor)
        self.vyber_button.pack(side=tk.LEFT, padx=5, pady=2)
        
        self.generuj_soubor_button = tk.Button(self.frame_soubor, text="Vytvoř graf", command=self.fceSoubor)
        self.generuj_soubor_button.pack(side=tk.RIGHT, padx=5, pady=2)

        # osy
        self.x_label = tk.Label(self.frame_popisky, text="osa X")
        self.x_label.pack(side=tk.LEFT, padx=5, pady=2)
        self.x_entry = tk.Entry(self.frame_popisky, width=15)
        self.x_entry.pack(side=tk.LEFT, padx=5, pady=2)

        self.y_label = tk.Label(self.frame_popisky, text="osa Y")
        self.y_label.pack(side=tk.LEFT, padx=5, pady=2)
        self.y_entry = tk.Entry(self.frame_popisky, width=15)
        self.y_entry.pack(side=tk.LEFT, padx=5, pady=2)

        # cesta k souboru
        self.souborVar = tk.StringVar()

    def generuj_graf(self):
        try:
            # je od do vyplneno?
            if not self.min_entry.get() or not self.max_entry.get():
                raise ValueError("Hodnoty od do nemohou být prázdné!")
            
            min_x = float(self.min_entry.get())
            max_x = float(self.max_entry.get())
            x_label = self.x_entry.get()
            y_label = self.y_entry.get()
            
            if min_x >= max_x:
                raise ValueError("Minimální hodnota musí být menší než maximální.")
            
            x = np.linspace(min_x, max_x, 500)
            funkce = self.funkce_var.get()
            
            if funkce == "sin":
                y = np.sin(x)
            elif funkce == "log":
                x = x[x > 0]  # Logaritmus pouze pro kladné hodnoty
                if len(x) == 0:
                    raise ValueError("Interval neobsahuje platné hodnoty pro logaritmus.")
                y = np.log(x)
            elif funkce == "exp":
                y = np.exp(x)
            
            self.vytvor_nove_okno(x, y, x_label, y_label, f"Graf funkce {funkce}")
        except ValueError as e:
            messagebox.showerror("Chyba", str(e))

    def vyber_soubor(self):
        cesta = fdialog.askopenfilename(title='Vyberte soubor')    
        if cesta != '':
            self.souborVar.set(cesta)
            self.soubor_entry.delete(0, tk.END)
            self.soubor_entry.insert(0, cesta)

    def fceSoubor(self):
        try:
            cesta = self.souborVar.get()
            with open(cesta, 'r') as f:
                x = []
                y = []
                while True:
                    radek = f.readline()
                    if radek == '':
                        break
                    cisla = radek.split()
                    if len(cisla) == 2:
                        x.append(float(cisla[0]))
                        y.append(float(cisla[1]))
            
            if not x or not y:
                raise ValueError("Soubor neobsahuje platná data pro vykreslení grafu.")
            
            self.vytvor_nove_okno(x, y, self.x_entry.get(), self.y_entry.get(), "Graf z dat v souboru")
        except Exception as e:
            messagebox.showerror("Chybný formát souboru", f"Graf se nepodařilo vytvořit,\nzkontrolujte formát souboru. Chyba: {e}")

    def vytvor_nove_okno(self, x, y, x_label, y_label, title):
        nove_okno = tk.Toplevel(self.root)
        nove_okno.title(title)
        nove_okno.bind("<Escape>", self.zavri_aplikaci)
        
        fig, ax = plt.subplots()
        ax.plot(x, y)
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.set_title(title)
        
        canvas = FigureCanvasTkAgg(fig, master=nove_okno)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        canvas.draw()

    def zavri_aplikaci(self, event=None):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    aplikace = GrafickaAplikace(root)
    root.mainloop()

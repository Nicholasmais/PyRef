from tkinter import Button, Entry, Frame, Scale, Tk, mainloop, DoubleVar
from tkinter.filedialog import askopenfilename, asksaveasfilename
from pandas import read_csv, DataFrame
from numpy import tanh, pi, absolute, log10
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from matplotlib.ticker import MultipleLocator

matplotlib.use("TkAgg")


def abre():
    global filename, line, a, dadosxy
    filename = askopenfilename(initialdir="/",
                                   title="Select A File",
                                   filetype=(("csv files", "*.csv",),("txt files",".txt"), ("all files", "*.*")))

    btn2.config(state='active')
    btn.config(state='active')
    btn_lim_superior.config(state='active')
    btn_lim_inferior.config(state='active')
    slider.config(state='active')
    salvar.config(state='active')
    dadosxy = refletividade(.004)
    fi.clf()
    a = fi.add_subplot(111)

    line, = a.plot(dadosxy[0], dadosxy[1])
    a.set_ylim(-30, 0)
    a.grid()
    a.axes.format_coord = lambda x, y: ""
    tick = MultipleLocator(base=0.5)
    a.xaxis.set_major_locator(tick)
    a.set_ylabel('Refletividade (dB)', fontsize=15)
    a.set_xlabel('Frequência (GHz)', fontsize=15)
    fi.canvas.draw_idle()


def refletividade(t):
    global frequency, rl
    arquivo = read_csv(f"{filename}")

    try:
        frequency = arquivo['frequency'].values[:]
    
    except KeyError:
        arquivo = read_csv(f"{filename}", sep=";")
        frequency = arquivo['frequency'].values[:]

    er = arquivo[["e'","e''"]].values[:]
    er = er[:,0] - 1j*er[:,1]
    ur = arquivo[["u'","u''"]].values[:]
    ur = ur[:,0] - 1j*ur[:,1]
    
    c = 299792458

    zin = ((ur / er) ** (1 / 2)) * tanh(1j*2*pi*frequency*t/c*((ur * er) ** (1 / 2)))
    rl = 20 * log10(absolute((zin-1)/(zin+1)))

    return [frequency/1000000000, rl]


def salvar():
    try:
        dados_csv = DataFrame(zip(frequency,rl), columns=["Frequency (Hz)","Reflectivity (dB)"])

    except NameError:
        return

    directory = asksaveasfilename(defaultextension=".csv", filetypes=[("csv",".*csv")])
    dados_csv.to_csv(f"{directory}",index=False)
    
    return


janela = Tk()
janela.state("zoomed")
janela.title("PyRef v1.0")
janela.iconbitmap("favicon.ico")

janela.minsize(500, 575)

frame_grafico = Frame(janela, bd=5, bg='black', relief='ridge')
frame_grafico.pack(expand=True, fill='both')

fi = Figure(figsize=(5, 4), dpi=100)

canvas = FigureCanvasTkAgg(fi, master=frame_grafico)
canvas.draw()
canvas.get_tk_widget().pack(side='top', fill='both', expand=1)
canvas._tkcanvas.pack(side='top', fill='both', expand=1)

frame_esquerda = Frame(janela)
frame_esquerda.pack(side='left', fill='both', expand=True)
frame_direita = Frame(janela)
frame_direita.pack(side='right', fill='both', expand=True)


def update(var):
    pos = slider.get()
    entryEsp.delete(0, 'end')
    entryEsp.insert(0, ("%.3f" % pos))
    dadosxy = refletividade(pos / 1000)
    line.set_data(dadosxy[0], dadosxy[1])
    fi.canvas.draw_idle()


botao = Button(frame_direita, text='Abrir arquivo', bd=5, relief='ridge', command=abre)
botao.config(highlightbackground='black', highlightcolor='black')
botao.pack()

salvar = Button(frame_direita,text="Salvar csv", bd=5, relief='ridge', command=salvar)
salvar.config(highlightbackground='black', highlightcolor='black', state='disabled')
salvar.pack()

frame_slider = Frame(frame_direita, bg='black', bd=5, relief='ridge', width=300, height=400)
frame_slider.pack(expand=True)

slider_var = DoubleVar()
slider_var.set(4)
slider = Scale(frame_slider, from_=2, to=8, length=270, orient='horizontal', tickinterval=1,
               resolution=.1, command=update, variable = slider_var)
slider.pack()
slider.config(state='disabled')

frame_esp = Frame(frame_esquerda, bd=5, bg='black', relief='ridge')
frame_esp.pack()

entryEsp = Entry(frame_esp, width=10)
entryEsp.pack(side="left", fill='both')


def atualiza_plot():
    pos = float(entryEsp.get())
    slider.set(pos)
    update(slider.get())


btn = Button(frame_esp, text="Espessura", width=20, command=atualiza_plot)
btn.pack(side="right", fill='x')
btn.config(state='disabled')

frame_lim_superior = Frame(frame_esquerda, bd=5, bg='black', relief='ridge')
frame_lim_superior.pack()

frame_lim_inferior = Frame(frame_esquerda, bd=5, bg='black', relief='ridge')
frame_lim_inferior.pack()

asd = NavigationToolbar2Tk(canvas, frame_slider)
asd.config(width=270)
asd.pack()

ymin = Entry(frame_lim_inferior, width=10)
ymin.pack(side='left', fill='both')
ymin.insert(0, '-30')

frame_nome = Frame(frame_esquerda, bd=6, bg='black', relief='ridge', width=270)
frame_nome.pack()

nome = Entry(frame_nome, width=40)
nome.pack()
nome.insert(0, "Exemplo")


def atualiza_axis():
    a.set_ylim(ymin=-absolute(float(ymin.get())))
    fi.canvas.draw_idle()


def atualiza_axiss():
    a.set_ylim(ymax=-absolute(float(ymax.get())))
    fi.canvas.draw_idle()


btn_lim_inferior = Button(frame_lim_inferior,
                          text="Limite inferior", width=20, command=atualiza_axis)
btn_lim_inferior.pack(side="right", fill='x')
btn_lim_inferior.config(state='disabled')

ymax = Entry(frame_lim_superior, width=10)
ymax.pack(side='left', fill='both')
ymax.insert(0, '0')

btn_lim_superior = Button(frame_lim_superior, text='Limite Superior', width=20, command=atualiza_axiss)
btn_lim_superior.pack(side='left', fill='both')
btn_lim_superior.config(state='disabled')


def nomeup():
    a.set_title(str(nome.get()), fontsize=15)
    fi.canvas.draw_idle()


btn2 = Button(frame_nome, text='Alterar título', command=nomeup)
btn2.pack(fill='x')
btn2.config(state='disabled')

mainloop()

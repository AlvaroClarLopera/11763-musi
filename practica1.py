import cv2
import logging
import pydicom
import copy as cp
import pandas as pd
import numpy as np
import os
from matplotlib import pyplot as plt


from tkinter import *
from tkinter import ttk
from tkinter import filedialog

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

global row,col,val
global val_corte
global imageDICOM
global directory
global filename
row = 0
col = 0
val = 0
import os
colorFondo = "#000040"
colorLletra = "#FFF"
scale = 1
offset = [0, 0]
current_scale = [offset[0], offset[1], scale, scale]

def load_images():
    global imageDICOM
    global val_corte
    global directory
    global filename
    val_corte = 0
    directory = "imagenes_dicom/"
    filename = filedialog.askopenfilename(initialdir=directory,title = "Select file")
    #filename = "000000.dcm"
    logging.info("Se ha cargado el archivo DICOM en "+str(filename))
    imageDICOM = pydicom.dcmread(filename)
    #directory = "imagenes_dicom/"
    #filename = "40826324_s1_CT_FB_masked.dcm"
    #imageDICOM = pydicom.read_file(directory+filename)
    # directory = "imagenes_dicom/"
    # filename = "PMD8540804318002412548_s04_T1_REST_Frame_1__PCARDM1.dcm"
    # imageDICOM = pydicom.read_file(directory+filename)
    image = imageDICOM.pixel_array
    if len(imageDICOM.pixel_array.shape) > 2:
        image = imageDICOM.pixel_array[val_corte]
    else:
        image = imageDICOM.pixel_array
        # df = pd.DataFrame(imageDICOM.values())
        # #print(df[0])
        # df[0] = df[0].apply(
        #     lambda x: pydicom.dataelem.DataElement_from_raw(x) if isinstance(x, pydicom.dataelem.RawDataElement) else x)
        # df['name'] = df[0].apply(lambda x: x.name)
        # df['value'] = df[0].apply(lambda x: x.value)
        # df = df[['name', 'value']]
    #print(imageDICOM.values())


def quit():
    exit(1)

def view_DICOM_headers():
    global tree
    global filename
    global imageDICOM
    global names
    global values
    global firstView
    ventanaH = Tk()
    ventanaH.resizable(0, 0)
    ventanaH.title("Cabeceras DICOM")
    ventanaH.geometry("1000x640")
    ventanaH.configure(background=colorFondo)
    column_names = ["name","value"]
    #imageDICOM = pydicom.dcmread(filename)
    logging.info("Se han consultado las cabecaras DICOM del archivo "+str(filename))
    df = pd.DataFrame(columns=column_names)
    if firstView == True:
        firstView = False
        names = []
        values = []
        for v in imageDICOM.values():
            if type(v) == pydicom.dataelem.RawDataElement:
                values.append(pydicom.dataelem.DataElement_from_raw(v).value)
            else:
                values.append(v)
        for n in imageDICOM:
            names.append(n.name)
    #print(len(names))
    df.insert(0,"name",names,allow_duplicates=True)
    df.insert(1,"value",values,allow_duplicates=True)

    tree = ttk.Treeview(ventanaH, height=40)
    vsb = ttk.Scrollbar(ventanaH, orient="vertical", command=tree.yview)
    vsb.place(x=980, y=0, height=640)

    tree.configure(yscrollcommand=vsb.set)
    df_col = df.columns.values

    counter = len(df)
    tree["columns"] = ("name", "value")
    rowLabels = df.index.tolist()

    for x in range(len(df_col)):
        tree.column(df_col[x], width=400)
        tree.heading(df_col[x], text=df_col[x])
        for i in range(counter):
            if x == 0:
                tree.insert('', i, text=rowLabels[i], values=df.iloc[i, :].tolist())

    tree.pack()

    #mainloop()

def callback(event):
    global row
    global col
    global val

    val = image[h-event.y][event.x]
    row = h-event.y
    col = event.x
    Label(ventanaV, text="              ",bg=colorFondo).place(x=1100,y=10)
    Label(ventanaV, text="              ",bg=colorFondo).place(x=1100,y=60)
    Label(ventanaV, text="              ",bg=colorFondo).place(x=1100,y=110)

    Label(ventanaV, text=row).place(x=1100,y=10)

    Label(ventanaV,text=col).place(x=1100,y=60)

    Label(ventanaV,text=val).place(x=1100,y=110)



def createViewerInterface():
    global firstView
    global ventanaV
    global fig
    global frame
    ventanaV = Tk()
    firstView = True
    ventanaV.resizable(0, 0)
    ventanaV.title("Practica 1")
    ventanaV.geometry("1280x720")
    ventanaV.configure(background=colorFondo)
    global image
    if len(imageDICOM.pixel_array.shape) > 2:
        image = imageDICOM.pixel_array[0]
    else:
        image = imageDICOM.pixel_array
    #image = cv2.imread('mandril_color.tif')

    my_dpi = 100  # Good default - doesn't really matter

    # Size of output in pixels
    global w,h
    w = image.shape[0]
    h = image.shape[1]
    fig = plt.figure(figsize=(w/my_dpi, h/my_dpi), dpi=my_dpi)
    plt.imshow(image)  # later use a.set_data(new_data)
    plt.gca().set_axis_off()
    plt.margins(0, 0)
    plt.subplots_adjust(top=1, bottom=0, right=1, left=0,
                        hspace=0, wspace=1)

    frame = Frame(ventanaV)


    left_arrow = cv2.imread("igu_data/left_arrow.png")
    #left_arrow = cv2.resize(left_arrow,(40,40), interpolation=cv2.INTER_AREA)
    right_arrow = cv2.imread("igu_data/right_arrow.png")
    #right_arrow = cv2.resize(right_arrow,(40,40), interpolation=cv2.INTER_AREA)
    #cv2.imwrite("igu_data/left_arrow.png",left_arrow)
    #cv2.imwrite("igu_data/right_arrow.png",right_arrow)

    # a tk.DrawingArea
    global canvas
    canvas = FigureCanvasTkAgg(fig, master=ventanaV)
    canvas.draw()
    frame.pack(side=TOP, fill=X)
    canvas.get_tk_widget().pack(side=TOP, expand=1)

    toolbar = NavigationToolbar2Tk(canvas, frame)
    toolbar.config(background=colorFondo)
    toolbar._message_label.config(background=colorFondo)
    toolbar.update()

    fig.canvas.callbacks.connect('button_press_event', callback)

    Label(ventanaV, text="Fila", bg=colorFondo,
          fg=colorLletra).place(x=1000, y=10)

    Label(ventanaV, text="Columna", bg=colorFondo,
          fg=colorLletra).place(x=1000, y=60)

    Label(ventanaV, text="Valor del pixel", bg=colorFondo,
          fg=colorLletra).place(x=1000, y=110)

    scale = Scale(ventanaV, from_=0, to=100, orient=HORIZONTAL, showvalue = 50,command=ajustarContraste)
    scale.place(x=1000,y=250)
    scale.set(50)
    Label(ventanaV, text="Ajustar contraste", bg="#000000", fg="white").place(x=1000, y=220)

    Button(ventanaV, text="Ver cabecera DICOM", command=view_DICOM_headers, bg="#000000", fg="white").place(x=470, y=20)
    Button(ventanaV, text="Salir", command=quit, bg="#000000", fg="white").place(x=780, y=20)

    lArrow = PhotoImage(file="igu_data/left_arrow.png", master=ventanaV)
    rArrow = PhotoImage(file="igu_data/right_arrow.png", master=ventanaV)

    Button(ventanaV, width=40, height=40, image=lArrow, command=lambda :cambiarCorte(-1),fg="white").place(x=600, y=50)
    Button(ventanaV, width=40, height=40, image=rArrow, command=lambda :cambiarCorte(1),fg="white").place(x=650, y=50)
    mainloop()

def createMainInterface():
    logging.basicConfig(filename='app.log', filemode='w', format='%(asctime)s - %(message)s', level=logging.INFO)
    logging.info("Se ha iniciado una nueva sesión")
    colorFondo = "#000040"
    ventana = Tk()
    ventana.resizable(0, 0)
    ventana.title("Practica 1")
    ventana.geometry("400x250")
    ventana.configure(background=colorFondo)
    Label(ventana, text="Visualizador \n de imágenes médicas DICOM",font=(None, 20), bg=colorFondo, fg=colorLletra).place(x=10, y=10)
    Button(ventana, text="Cargar imagen", command=load_images, bg="#000000", fg="white").place(x=10, y=200)
    Button(ventana, text="Visualizar", command=createViewerInterface, bg="#000000", fg="white").place(x=160, y=200)
    Button(ventana, text="Salir", command=quit, bg="#000000", fg="white").place(x=310, y=200)
    mainloop()

def ajustarContraste(val):
    global w, h
    global image
    global imageC
    my_dpi = 100  # Good default - doesn't really matter
    vali = int(val)
    alpha = vali / 50

    #print("Alpha = "+str(alpha))
    #print("Beta = "+str(beta))
    #imageC = cp.deepcopy(image)
    # print("Por defecto: "+str(image[196][260]))
    max_act = np.amax(image)
    min_act = np.amin(image)
    # print("Max: "+str(max_act))
    # print("Min: "+str(min_act))
    #print("Alpha: "+str(alpha))
    newmax = int(max_act* alpha * 30)
    if min_act < 0:
        newmin = int(min_act * alpha * 30)
    else:
        newmin = int(min_act / (alpha * 30 + 0.000001))

    imageC = cp.deepcopy(image)
    # print("newmax: "+str(newmax))
    # print("newmin: "+str(newmin))
    imageC[:,:] = (((newmax - newmin) * ((image[:,:] - min_act) / (max_act - min_act))) + newmin)
    # print(imageC[196][260])
    logging.info("Se ha ajustado el contraste a un valor alpha "+str(alpha))
    w = imageC.shape[0]
    h = imageC.shape[1]
    plt.imshow(imageC,cmap=plt.cm.bone)  # later use a.set_data(new_data)
    plt.gca().set_axis_off()
    plt.margins(0, 0)
    plt.subplots_adjust(top=1, bottom=0, right=1, left=0,
                        hspace=0, wspace=1)


    # a tk.DrawingArea
    canvas.figure = fig
    canvas.draw()
    frame.pack(side=TOP, fill=X)
    canvas.get_tk_widget().pack(side=TOP, expand=1)

def cambiarCorte(valor):
    global val_corte
    global image
    global filename
    global directory
    # print(imageDICOM.pixel_array.shape)
    if len(imageDICOM.pixel_array.shape) > 2:
        if valor == -1: #anterior corte
            val_corte -= 1
            if val_corte < 0:
                val_corte = imageDICOM.pixel_array.shape[2] - 1
        else: #siguiente corte
            val_corte += 1
            if val_corte > imageDICOM.pixel_array.shape[2] - 1:
                val_corte = 0
        imagep = imageDICOM.pixel_array[val_corte]
        image = cp.deepcopy(imagep)
    else:
        if "imagenes_dicom/0-27993/" in filename:
            if valor == -1: #anterior corte
                val_corte -= 1
                if val_corte < 0:
                    val_corte = 117
            else: #siguiente corte
                val_corte += 1
                if val_corte > 117:
                    val_corte = 0
            cont = 0
            directory = "imagenes_dicom/0-27993/"
            for fname in os.listdir(directory):
                imageDICOMp = pydicom.dcmread(directory+fname)
                if cont == val_corte:
                    break
                cont += 1
            imagep = imageDICOMp.pixel_array
            image = cp.deepcopy(imagep)
    logging.info("Se ha cambiado de corte. Actualmente se visualiza el corte nº "+str(val_corte+1))
    plt.imshow(image, cmap=plt.cm.bone)  # later use a.set_data(new_data)
    plt.gca().set_axis_off()
    plt.margins(0, 0)
    plt.subplots_adjust(top=1, bottom=0, right=1, left=0,
                        hspace=0, wspace=1)

    # a tk.DrawingArea
    canvas.figure = fig
    canvas.draw()
    frame.pack(side=TOP, fill=X)
    canvas.get_tk_widget().pack(side=TOP, expand=1)


createMainInterface()
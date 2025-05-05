#Importación de librerías 
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import numpy as np

#Definición de variables globales

#Valores de entrada
x0=1 

#indice de filas de los vectores
fila_vectores = 1

#Arrays de grupos de entradas,pesos y salidas
r_vars=[]
x_vars=[]
w_vars=[]

#Error 
error_calculo = False
error_lectura = False

#----------------------------------FUNCIONALIDAD DEL PERCEPTRÓN--------------------------------------------------------

#Función de activación sigmoidal
def activacion_sigmoidal(suma):
    v = 1 / (1 + np.exp(-suma))
    return v

#Función de activación escalonado
def activacion_escalonado(suma):
    if suma<=0:
        v=0
    else:
        v=1

    return v

    
#Suma producto de pesos con entradas
def sumaproducto(index):
    global x_vars,w_vars,x0,sesgo,error_calculo
    suma = 0 
    try: 
        for i in range(0,len(w_vars)):
            suma+=float(w_vars[i])*float(x_vars[i][index].get())
        suma+=float(sesgo)*x0
    except:
        error_calculo = True

    return suma


#Función principal de la ejecución del perceptrón
def perceptron(index):    
    global sesgo,fuente_activacion
    suma = sumaproducto(index)
    if fuente_activacion.get() == "escalonada":
        v = activacion_escalonado(suma)
    else:
        v = activacion_sigmoidal(suma)
    return v

#----------------------------------FUNCIONALIDAD DE LA INTERFAZ GRÁFICA--------------------------------------------------------

#---Funciones para lectura de archivos---

#Lectura de pesos de entrada
def readConfig():
    global x_vars, w_vars
    archive = open('config.txt')
    content = archive.read()
    archive.close()
    pesos=[]
    iterador=1
    datos = content.split(',')
    for peso in datos:
        if iterador!=1:
            pesos.append(peso)
            w_vars.append(peso)    
        else:
            sesgo=peso
        iterador+=1

    return sesgo, pesos

#Resetea el array dejando los arrays vacios
def resetArray():
    global pesosretornado,x_vars
    x_vars = [[] for _ in range(len(pesosretornado))]

#Función para leer los archivos de entrada
def LectorEntrada():
    archivo = filedialog.askopenfilename(
        title="Seleccionar archivo de entradas",
        filetypes=(("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*"))
    )
    if archivo:  
        with open(archivo, 'r') as archive:
            contenido = archive.readlines()
        datos = []
        for linea in contenido:
            linea_datos = linea.strip().split(',')
            datos.append([int(x) for x in linea_datos])
    
    return datos

#---Funciones correspondientes al cambio de tipo de entrada---

#Posterior a leer el archivo de entradas, se le asigna los valores y los vectores
def asignar_entrada_archivo():
    global x_vars
    datos=LectorEntrada()
    error = False
    for j in range(0,len(datos)):
        if j!=0:
            agregar_vector()
        if len(datos[j]) != len(w_vars):
            print()
            error_lectura = True
            error = True
        else:
            error_lectura = False

        if error_lectura == False:
            for i in range(0,len(datos[0])): 
                x_vars[i][j].set(datos[j][i])
        
    if error == True:
        messagebox.showwarning("Advertencia", "La cantidad de pesos no cuadra con las dimensiones del vector.")

    

#Acciones a realizar al cambiar el tipo de entrada, ya sea por archivo o teclado
def asignadorEntrada():
    if fuente_entrada.get() == "archivo":
        borrar_entries()
        asignar_entrada_archivo()  
        agregar_vector_btn.config(state="disabled")
    else:
        borrar_entries()
        agregar_vector_btn.config(state="normal")




#---Funciones correspondientes a la administración de los vectores---

#Agrega 1 vector
def agregar_vector():
    global fila_vectores,fuente_entrada    
    
    #label x1
    x1_label = tk.Label(minisec1, text=f"x1:", font=("Arial", 10))
    x1_label.grid(row=fila_vectores, column=0, sticky="w",padx=10, pady=(13, 0))

    #Entry x1 dependiendo de los casos
    x1var = tk.StringVar()
    if fuente_entrada.get() == "archivo":   
        x1_entry = tk.Entry(minisec1, textvariable=x1var, justify="center", width="70", state="readonly")
    else:
        x1_entry = tk.Entry(minisec1, textvariable=x1var, justify="center", width="70")
    x1_entry.grid(row=fila_vectores, column=1, sticky="w",padx=10, pady=(13, 0))

    #Entry de la salida
    rvar = tk.StringVar()
    r_entry = tk.Entry(minisec1, textvariable=rvar, justify="center", width="40", state="readonly")
    r_entry.grid(row=fila_vectores, column=2, rowspan=len(pesosretornado), sticky="ns",padx=10, pady=(13, 0))
    
    #Inserción a sus listas asociadas
    x_vars[0].append(x1var)
    r_vars.append(rvar)

    fila_vectores += 1

    #Entry xn dependiendo de los casos
    for n_vectores in range(0,len(pesosretornado)):

        if n_vectores > 0 : 
            #label xn
            xn_label = tk.Label(minisec1, text=f"x"+str(n_vectores+1)+":", font=("Arial", 10))
            xn_label.grid(row=fila_vectores, column=0,padx=10, sticky="w")

            xnvar = tk.StringVar()
            if fuente_entrada.get() == "archivo":   
                xn_entry = tk.Entry(minisec1, textvariable=xnvar, justify="center", width="70",state="readonly")
            else:
                xn_entry = tk.Entry(minisec1, textvariable=xnvar, justify="center", width="70")
            xn_entry.grid(row=fila_vectores, column=1,padx=10, sticky="w")

            x_vars[n_vectores].append(xnvar)

            fila_vectores += 1

#Calcula la salida del perceptrón
def calculo_vectores():
    #Definición de variables globales
    global x_vars,r_vars,error_calculo

    #Aplica la función perceptrón para cada una de los vectores que se tenga y actualiza los entry de las salidas
    for i in range(0,len(r_vars)):
        v = perceptron(i)
        if error_calculo == False:
            r_vars[i].set(v)
        error_calculo = False

#Función que borra las entradas en caso de que se cambie de tipo de entrada
def borrar_entries():

    global x_vars

    #Borra todos los los widgets de la seccion de los vectores y los valores de los arrays que conservan lso valores de entrada y resultados
    for xn in x_vars:
        for entry in xn:
            entry.set("")
    for entry in r_vars:
        entry.set("") 
    for widget in minisec1.winfo_children():
        widget.destroy()   
    x_vars = [[] for _ in range(len(pesosretornado))]
    r_vars.clear()
    resetArray()

    #Creación de label "Vectores" y "Salidas" y le añade 1 vector
    vector = tk.Label(minisec1, text="Vectores",font=("Arial", 13,"bold","underline"), pady=10)
    vector.grid(row=0, column=0, sticky="n", columnspan=2)
    resultados = tk.Label(minisec1, text="Salidas",font=("Arial", 13,"bold","underline"), pady=10)
    resultados.grid(row=0, column=2, sticky="n")
    agregar_vector()

#Mostrar pesos
def mostrarPesos():
    for index in range(0,len(pesosretornado)):
        valor_wn=tk.StringVar()
        wn=tk.Label(peso_antes_label,text="w"+str(index+1))
        wn.grid(row=0,column=index+1)
        wn_entry=tk.Entry(peso_antes_label,textvariable=valor_wn, state="readonly",justify="center",width=15)
        wn_entry.grid(row=1,column=index+1)
        valor_wn.set(pesosretornado[index])

    for widget in peso_antes_label.winfo_children():
        widget.grid_configure(padx=10,pady=5)

#----------------------------------INTERFAZ GRÁFICA--------------------------------------------------------

#Creación inicial de la ventana principal
window = tk.Tk()
window.title("Perceptrón simple")

#Frame principal que contiene la ventana principal
frame = tk.Frame(window) 
frame.pack()

#Sección 1 que contiene el frame principal
sec1 = tk.Label(frame,text="")
sec1.grid(row=0,column=0)

#Tipo de entrada
entrada_label=tk.LabelFrame(sec1, text="Tipo de entrada")
entrada_label.grid(row=0,column=0)
fuente_entrada = tk.StringVar()
entrada_teclado=tk.Radiobutton(entrada_label,text="Teclado", variable=fuente_entrada, value="teclado",command=asignadorEntrada)
entrada_archivo=tk.Radiobutton(entrada_label,text="Archivo", variable=fuente_entrada, value="archivo",command=asignadorEntrada)
entrada_teclado.grid(row=0,column=0)
entrada_archivo.grid(row=1,column=0)
fuente_entrada.set("teclado")

#Función de activación
fun_activacion_label=tk.LabelFrame(sec1,text="Función de activación")
fun_activacion_label.grid(row=0,column=1)
fuente_activacion = tk.StringVar()
funcion_escalonada=tk.Radiobutton(fun_activacion_label,text="Escalonada",variable=fuente_activacion,value="escalonada")
funcion_sigmoidal=tk.Radiobutton(fun_activacion_label,text="Sigmoidal",variable=fuente_activacion,value="sigmoidal")
funcion_escalonada.grid(row=0,column=0)
funcion_sigmoidal.grid(row=1,column=0)
fuente_activacion.set("escalonada")

#Sección 2 que contiene el frame principal
sec2 = tk.Label(frame)
sec2.grid(row=1,column=0)

#Label Frame de pesos asociados
peso_antes_label = tk.LabelFrame(sec1,text="Pesos asociados", labelanchor="n")
peso_antes_label.grid(row=0,column=2)

#w0 original
valor_w0_viejo=tk.StringVar()
w0_viejo=tk.Label(peso_antes_label,text="w₀")
w0_viejo.grid(row=0,column=0)
w0_viejo_entry=tk.Entry(peso_antes_label,textvariable=valor_w0_viejo, state="readonly",justify="center",width=15)
w0_viejo_entry.grid(row=1,column=0)
valor_w0_viejo.set("")

#Sección 2 que contiene el frame principal
sec2 = tk.Label(frame)
sec2.grid_columnconfigure(0, weight=3)
sec2.grid_columnconfigure(1, weight=1)
sec2.grid(row=2, column=0, sticky="w")  

#Sub-sección que contiene la sección 2
minisec1 = tk.Label(sec2)
minisec1.grid(row=0, column=0, sticky="w")  

#Componente de vector X1 entry y label
x1_label = tk.Label(minisec1, text="x₁:",font=("Arial", 10))
x1_label.grid(row=1, column=0, sticky="w", pady=(13, 0))
x1var = tk.StringVar()
x1_entry = tk.Entry(minisec1, textvariable=x1var, justify="center",width="70")
x1_entry.grid(row=1, column=1, sticky="w", pady=(13, 0))

#Salida del perceptrón entry y label
r1var = tk.StringVar()
r1_entry = tk.Entry(minisec1, textvariable=r1var, justify="center",width="40",state="readonly")
r1_entry.grid(row=1, column=2, rowspan=2,sticky="ns", pady=(13, 0))

#Componente de vector X2 entry y label
x2_label = tk.Label(minisec1, text="x₂:",font=("Arial", 13))
x2_label.grid(row=2, column=0, sticky="w")
x2var = tk.StringVar()
x2_entry = tk.Entry(minisec1, textvariable=x2var, justify="center",width="70")
x2_entry.grid(row=2, column=1, sticky="w")

#Sección 3 que contiene el frame principal
sec3 = tk.Label(frame)
sec3.grid(row=3, column=0, sticky="n")  

#Botón de agregar vector
agregar_vector_btn = tk.Button(sec3, text="Agregar Vector", bg="white", width="60", command=agregar_vector)
agregar_vector_btn.grid(row=0, column=0, sticky="n")

#Botón de calcular salidas
calcular = tk.Button(sec3,text="Calcular Salidas",bg="white",width="30",command=calculo_vectores)
calcular.grid(row=0,column=1,sticky="n")


#Padding de los widgets
for widget in peso_antes_label.winfo_children():
    widget.grid_configure(padx=10,pady=5)

for widget in sec1.winfo_children():
    widget.grid_configure(padx=10,pady=5)

for widget in sec2.winfo_children():
    widget.grid_configure(padx=10,pady=5)

for widget in sec3.winfo_children():
    widget.grid_configure(padx=10,pady=5)

for widget in frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

for widget in minisec1.winfo_children():
    widget.grid_configure(padx=10,pady=1)

#Scrollbar vertical para permitir múltiples vectores 
canvas = tk.Canvas(sec2)
scrollbar = tk.Scrollbar(sec2, orient="vertical", command=canvas.yview)
minisec1 = tk.Frame(canvas)

minisec1.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=minisec1, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)
canvas.grid(row=0, column=0, sticky="nsew")
scrollbar.grid(row=0, column=1, sticky="ns")


#Lectura y asignación de pesos iniciales
sesgo, pesosretornado = readConfig()
x_vars = [[] for _ in range(len(pesosretornado))]
valor_w0_viejo.set(sesgo)
mostrarPesos()
resetArray()

#Label vector
vector = tk.Label(minisec1, text="Vectores",font=("Arial", 13,"bold","underline"), pady=10)
vector.grid(row=0, column=0, sticky="n", columnspan=2)

#Label salidas
resultados = tk.Label(minisec1, text="Salidas",font=("Arial", 13,"bold","underline"), pady=10)
resultados.grid(row=0, column=2, sticky="n")

#Adicón del vector incial
agregar_vector()


#Loop de la ventana creada
window.mainloop()
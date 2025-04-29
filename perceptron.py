#Importación de librerías 
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import numpy as np

#Definición de variables globales


#factor de aprendizaje
aprendizaje=0.2

#Pesos
sesgo = 0
w1 = 0
w2 = 0

#Valores de entrada
x0=1 
x1 = 0 
x2 = 0 

#Matriz de operaciones binarias or y and
matriz_or=[[0,0,1,1],[0,1,0,1],[0,1,1,1]]
matriz_and=[[0,0,1,1],[0,1,0,1],[0,0,0,1]]

#Array de comparación en caso de error, si el array=[0,0,0,0] quiere decir que ya no hay error
array_error=[]

#indice de filas de los vectores
fila_vectores = 1

#Arrays de grupos de entradas y respuestas
x1_vars=[]
r_vars=[]
x2_vars=[]

#Booleano para revisar si ha cambiado la función de activación o la operación binaria
cambio=False

#Booleano para verificar si se ha actualizado los pesos para ver si se ha aprendido antes y no volver a hacer las iteraciones
aprendido=False

#----------------------------------FUNCIONALIDAD DEL PERCEPTRÓN--------------------------------------------------------

#Función de activación sigmoidal
def activacion_sigmoidal(suma):
    salida = 1 / (1 + np.exp(-suma))
    if salida > 0.5:
        v = 1 
    else:
        v = 0
    return v 

#Función de activación escalonado
def activacion_escalonado(suma):
    if suma<=0:
        v=0
    else:
        v=1;

    return v;

#Suma producto de pesos con entradas
def sumaproducto(wa,wb,xa,xb,bias):
    suma=wa*xa+wb*xb+bias*x0
    return suma

#Actualización de pesos a un peso válido mediante iteraciones con un factor de aprendiazaje de 0.2
def actualizacion_pesos(matriz,v,i):
        
        global w1, w2, sesgo
        error = matriz[2][i]-v #error = resultado esperado (yn) - resultado obtenido

        #wn = wn + factor de aprendizaje * xn * error 
        w1=w1+aprendizaje*matriz[0][i]*error
        w2=w2+aprendizaje*matriz[1][i]*error 
        sesgo=sesgo+aprendizaje*x0*error

        #Se le añade el numero error al array
        array_error.append(error)

#Aprendizaje del perceptrón para la actualización de pesos 
def aprender(wa,wb,bias,matriz):

    #Definición de variables globales y temporales
    global w1, w2, sesgo,array_error,fuente_activacion
    w1=wa
    w2=wb
    sesgo = bias
    sinAprender=True
    
    #Bucle para para llenar el array de error para verificar posteriormente si array_error=[0,0,0,0] 
    while sinAprender:
        #simula la operacion binaria con todos los valores posibles de entrada
        for i in range(0,4):
            suma = sumaproducto(w1,w2,matriz[0][i],matriz[1][i],sesgo)
            if fuente_activacion.get() == "escalonada": 
                v = activacion_escalonado(suma)
            else: 
                v = activacion_sigmoidal(suma)
            actualizacion_pesos(matriz,v,i)
            if len(array_error) == 4:
                #condicinal si el array error = [0,0,0,0] entonces ya aprendio y no hace falta realizar mas iteraciones
                if all(x==0 for x in array_error):
                    sinAprender=False
                else:
                    array_error=[]
    
    #Asignación de valores w0,w1,w2 nuevos post-aprendizaje
    valor_w1_nuevo.set(w1)
    valor_w2_nuevo.set(w2)
    valor_w0_nuevo.set(sesgo)

#Función principal de la ejecución del perceptrón
def perceptron(xa,xb):    
    global x1, x2,fuente_activacion
    x1=xa
    x2=xb
    suma = sumaproducto(w1,w2,x1,x2,sesgo)
    if fuente_activacion.get() == "escalonada":
        v = activacion_escalonado(suma)
    else:
        v = activacion_sigmoidal(suma)
    return v

#----------------------------------FUNCIONALIDAD DE LA INTERFAZ GRÁFICA--------------------------------------------------------

#---Funciones para lectura de archivos---

#Lectura de pesos de entrada
def readConfig():
    archive = open('config.txt')
    content = archive.read()
    archive.close()
    pesos=[]
    iterador=1
    datos = content.split(',')
    for peso in datos:
        if iterador!=1:
            pesos.append(peso)
        else:
            sesgo=peso
        iterador+=1

    return sesgo, pesos

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
    datos=LectorEntrada()
    i=0
    for x in datos:
        if i!=0:
            agregar_vector()
        x1_vars[i].set(x[0])
        x2_vars[i].set(x[1])
        i+=1

#Acciones a realizar al cambiar el tipo de entrada, ya sea por archivo o teclado
def asignadorEntrada():
    if fuente_entrada.get() == "archivo":
        borrar_entries()
        asignar_entrada_archivo()  
        agregar_vector_btn.config(state="disabled")
    else:
        borrar_entries()
        agregar_vector_btn.config(state="normal")

#Cambio de booleano al realizar un cambio de funcion de aplicación o operación binaria
def cambiador():
    global cambio 
    cambio = True


#---Funciones correspondientes a la administración de los vectores---

#Agrega 1 vector
def agregar_vector():
    global fila_vectores,fuente_entrada    
    
    #label x1
    x1_label = tk.Label(minisec1, text=f"x₁:", font=("Arial", 10))
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
    r_entry.grid(row=fila_vectores, column=2, rowspan=2, sticky="ns",padx=10, pady=(13, 0))

    #Inserción a sus listas asociadas
    x1_vars.append(x1var)
    r_vars.append(rvar)

    fila_vectores += 1

    #label x2
    x2_label = tk.Label(minisec1, text=f"x₂:", font=("Arial", 10))
    x2_label.grid(row=fila_vectores, column=0,padx=10, sticky="w")

    #Entry x2 dependiendo de los casos
    x2var = tk.StringVar()
    if fuente_entrada.get() == "archivo":   
        x2_entry = tk.Entry(minisec1, textvariable=x2var, justify="center", width="70",state="readonly")
    else:
        x2_entry = tk.Entry(minisec1, textvariable=x2var, justify="center", width="70")
    x2_entry.grid(row=fila_vectores, column=1,padx=10, sticky="w")

    x2_vars.append(x2var)

    fila_vectores += 1

#Calcula la salida del perceptrón
def calculo_vectores():
    #Definición de variables globales
    global x1_vars,r_vars,x2_vars,sesgoretornado,pesosretornado,aprendido,cambio,array_error
    error = False

    #Condicionales para verificar que tipo de operación de binaria es
    if aprendido == False or cambio == True:
        if fuente_op.get() == "and":
            aprender(int(pesosretornado[0]),int(pesosretornado[1]),int(sesgoretornado),matriz_and)
        else:
            aprender(int(pesosretornado[0]),int(pesosretornado[1]),int(sesgoretornado),matriz_or)
        aprendido = True
        cambio = False
        array_error=[]
    
    #Aplica la función perceptrón para cada una de los vectores que se tenga y actualiza los entry de las salidas
    for i in range(0,len(x1_vars)):
        if x1_vars[i].get() == "1" or x1_vars[i].get() == "0":
            if x2_vars[i].get() == "1" or x2_vars[i].get() == "0":
                v = perceptron(int(x1_vars[i].get()),int(x2_vars[i].get()))
                r_vars[i].set(v)
            else:
                error=True    
        else:
            error=True  

    if error == True:
        #En caso de haber un error con el formato, desplega un mensaje en pantalla
        messagebox.showwarning("Advertencia", "Solo puedes ingresar 0 o 1, puede que tengas celdas vacías.")

    error=False

#Función que borra las entradas en caso de que se cambie de tipo de entrada
def borrar_entries():
    #Borra todos los los widgets de la seccion de los vectores y los valores de los arrays que conservan lso valores de entrada y resultados
    for entry in x1_vars:
        entry.set("")  
    for entry in x2_vars:
        entry.set("")  
    for entry in r_vars:
        entry.set("") 
    for widget in minisec1.winfo_children():
        widget.destroy()   
    x1_vars.clear()  
    x2_vars.clear()  
    r_vars.clear()

    #Creación de label "Vectores" y "Salidas" y le añade 1 vector
    vector = tk.Label(minisec1, text="Vectores",font=("Arial", 13,"bold","underline"), pady=10)
    vector.grid(row=0, column=0, sticky="n", columnspan=2)
    resultados = tk.Label(minisec1, text="Salidas",font=("Arial", 13,"bold","underline"), pady=10)
    resultados.grid(row=0, column=2, sticky="n")
    agregar_vector()

#----------------------------------INTERFAZ GRÁFICA--------------------------------------------------------

#Creación inicial de la ventana principal
window = tk.Tk()
window.title("Perceptrón - Aprendizaje de las operaciones binarias AND y OR")

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
funcion_escalonada=tk.Radiobutton(fun_activacion_label,text="Escalonada",variable=fuente_activacion,value="escalonada",command=cambiador)
funcion_sigmoidal=tk.Radiobutton(fun_activacion_label,text="Sigmoidal",variable=fuente_activacion,value="sigmoidal",command=cambiador)
funcion_escalonada.grid(row=0,column=0)
funcion_sigmoidal.grid(row=1,column=0)
fuente_activacion.set("escalonada")

#Tipo de operación binaria
op_binaria_label=tk.LabelFrame(sec1,text="Operación binaria")
op_binaria_label.grid(row=0,column=2)
fuente_op = tk.StringVar()
op_and=tk.Radiobutton(op_binaria_label,text="AND",variable=fuente_op,value="and",command=cambiador)
op_or=tk.Radiobutton(op_binaria_label,text="OR",variable=fuente_op,value="or",command=cambiador)
op_and.grid(row=0,column=0)
op_or.grid(row=1,column=0)
fuente_op.set("and")

#Imagen de la tabla de operaciones binarias
imagen_tabla = Image.open("tabla_binaria.png")
imagen_tabla = imagen_tabla.resize((300, 120)) 
imagen_tabla = ImageTk.PhotoImage(imagen_tabla)
imagen_tabla_label = tk.Label(sec1,image=imagen_tabla)
imagen_tabla_label.grid(row=0,column=3)

#Sección 2 que contiene el frame principal
sec2 = tk.Label(frame)
sec2.grid(row=1,column=0)

#Label Frame de pesos originales
peso_antes_label = tk.LabelFrame(sec2,text="Pesos originales", labelanchor="n")
peso_antes_label.grid(row=1,column=0)

#w0 original
valor_w0_viejo=tk.StringVar()
w0_viejo=tk.Label(peso_antes_label,text="w₀")
w0_viejo.grid(row=0,column=0)
w0_viejo_entry=tk.Entry(peso_antes_label,textvariable=valor_w0_viejo, state="readonly",justify="center",width=15)
w0_viejo_entry.grid(row=1,column=0)
valor_w0_viejo.set("")

#w1 original
valor_w1_viejo = tk.StringVar()
w1_viejo = tk.Label(peso_antes_label, text="w₁")
w1_viejo.grid(row=0, column=1)
w1_viejo_entry = tk.Entry(peso_antes_label, textvariable=valor_w1_viejo, state="readonly",justify="center",width=15)
w1_viejo_entry.grid(row=1, column=1)
valor_w1_viejo.set("")

#w2 original
valor_w2_viejo = tk.StringVar()
w2_viejo = tk.Label(peso_antes_label, text="w₂")
w2_viejo.grid(row=0, column=2)
w2_viejo_entry = tk.Entry(peso_antes_label, textvariable=valor_w2_viejo, state="readonly",justify="center",width=15)
w2_viejo_entry.grid(row=1, column=2)
valor_w2_viejo.set("")

#Label Frame de pesos originales
peso_nuevo_label = tk.LabelFrame(sec2,text="Pesos después del aprendizaje", labelanchor="n")
peso_nuevo_label.grid(row=1,column=1)

#w0 con aprendizaje
valor_w0_nuevo = tk.StringVar()
w0_nuevo = tk.Label(peso_nuevo_label, text="w₀")
w0_nuevo.grid(row=0, column=0)
w0_nuevo_entry = tk.Entry(peso_nuevo_label, textvariable=valor_w0_nuevo, state="readonly", justify="center",width=15 )
w0_nuevo_entry.grid(row=1, column=0)
valor_w0_nuevo.set("")

#w1 con aprendizaje
valor_w1_nuevo = tk.StringVar()
w1_nuevo = tk.Label(peso_nuevo_label, text="w₁")
w1_nuevo.grid(row=0, column=1)
w1_nuevo_entry = tk.Entry(peso_nuevo_label, textvariable=valor_w1_nuevo, state="readonly", justify="center",width=15)
w1_nuevo_entry.grid(row=1, column=1)
valor_w1_nuevo.set("")

#w2 con aprendizaje
valor_w2_nuevo = tk.StringVar()
w2_nuevo = tk.Label(peso_nuevo_label, text="w₂")
w2_nuevo.grid(row=0, column=2)
w2_nuevo_entry = tk.Entry(peso_nuevo_label, textvariable=valor_w2_nuevo, state="readonly", justify="center",width=15)
w2_nuevo_entry.grid(row=1, column=2)
valor_w2_nuevo.set("")

#Sección 3 que contiene el frame principal
sec3 = tk.Label(frame)
sec3.grid_columnconfigure(0, weight=3)
sec3.grid_columnconfigure(1, weight=1)
sec3.grid(row=2, column=0, sticky="w")  

#Sub-sección que contiene la sección 3
minisec1 = tk.Label(sec3)
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

#Sección 4 que contiene el frame principal
sec4 = tk.Label(frame)
sec4.grid(row=4, column=0, sticky="n")  

#Botón de agregar vector
agregar_vector_btn = tk.Button(sec4, text="Agregar Vector", bg="white", width="60", command=agregar_vector)
agregar_vector_btn.grid(row=0, column=0, sticky="n")

#Botón de calcular salidas
calcular = tk.Button(sec4,text="Calcular Salidas",bg="white",width="30",command=calculo_vectores)
calcular.grid(row=0,column=1,sticky="n")

#Padding de los widgets
for widget in peso_antes_label.winfo_children():
    widget.grid_configure(padx=10,pady=5)

for widget in peso_nuevo_label.winfo_children():
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

for widget in sec4.winfo_children():
    widget.grid_configure(padx=10, pady=5)

#Scrollbar vertical para permitir múltiples vectores 
canvas = tk.Canvas(sec3)
scrollbar = tk.Scrollbar(sec3, orient="vertical", command=canvas.yview)
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


#Label vector
vector = tk.Label(minisec1, text="Vectores",font=("Arial", 13,"bold","underline"), pady=10)
vector.grid(row=0, column=0, sticky="n", columnspan=2)

#Label salidas
resultados = tk.Label(minisec1, text="Salidas",font=("Arial", 13,"bold","underline"), pady=10)
resultados.grid(row=0, column=2, sticky="n")

#Adicón del vector incial
agregar_vector()

#Lectura y asignación de pesos iniciales
sesgoretornado, pesosretornado = readConfig()
valor_w0_viejo.set(sesgoretornado)
valor_w1_viejo.set(pesosretornado[0])
valor_w2_viejo.set(pesosretornado[1])

#Loop de la ventana creada
window.mainloop()
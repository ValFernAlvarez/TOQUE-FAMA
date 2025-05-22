#------------IMPORT PARA GUI---------------------------
from tkinter import *
import random as rdm
import pygame

#------------CONFIG. DE VENTANA---------------------------
ventana=Tk() #Variable para ventana
ventana.title("TOQUE-FAMA") #Título de ventana
ventana.geometry("1300x650")  #Dimensión de ventana
ventana.resizable(False, False) #Evita redimensionar
ventana.config(bg='black') #Color de fondo para ventana
icon=PhotoImage(file='diseno/icono.png') #Variable de ícono
ventana.iconphoto(True,icon) #Implementación de ícono


#------------VARIABLES GLOBALES---------------------------
nivel=StringVar() #Habilite cualquier nivel
lst_sec=[]  #Lista secreta
cnt_intento_mx=0  #Contador de cantidad de intentos máximos según nivel
cnt_intento_actl=0  #Contador de intentos actualmente usados

#---CREAR DE NÚMERO 4 DÍGITOS (lista con 4 componentes) SECRETO---
def crear_lst_sec(): #Función para crear lista secreta
    global lst_sec #Globalizar lista secreta
    lst_sec=[] #Lista secreta
    for element in range (8): #Ciclo para agregar dígitos a la lista secreta
        dig=rdm.randint(0,9) #Variable para un dígito aleatorio
        if dig not in lst_sec: #Condicional para evitar repeticiones y agregar dígitos
            lst_sec.append(dig) #Agrega a la lista
        if len(lst_sec)==4: #Condicional para asegurar 4 dígitos
            break #Cierra función al completar la lista secreta


#------------MECANISMO DEL JUEGO---------------------------
#---ELEGIR NIVEL---
def elegir_niv(niv): #Función para elegir nivel
    global cnt_intento_mx, cnt_intento_actl #Globalizar intentos máximos e intentos actuales
    cnt_intento_actl=0 #Contador de intentos actualmente usados
    if niv=="experto": #Condicionales para elegir nivel
        cnt_intento_mx=5  #Experto: 5 intentos
    elif niv=="intermedio":
        cnt_intento_mx=7  #Intermedio: 7 intentos
    elif niv=="principiante":
        cnt_intento_mx=10  #Principiante: 10 intentos
    crear_lst_sec()  #Se llama la función crear_lst_sec
    entrada.delete(0, END) #Reanudar entrada
    resultado.config(text="") #Para mensajes de toques, famas, errores, pérdida o triunfos.
    pantalla_inicio.pack_forget() #Cambiarse a la pantalla_juego
    pantalla_juego.pack(fill="both", expand=True) #Llama pantalla_juego

#---VERIFICAR INTENTO---
def verificar_intento(): #Función para verificar intento de usuario
    global cnt_intento_actl #Globalizar cnt_intento_actl
    cnt_intento_actl+=1 #Agregar intento
    dig_usr=entrada.get().split() #Se obtiene la respuesta del usuario del widget 'entrada'
    lst_usr=[] #Crear lista de usuario
    try:
        for element_usr in dig_usr: #Ciclo para agregar dígitos del usuario
            if int(element_usr)>=0 and int(element_usr)<=9: #Verifica si son dígitos de 0 a 9
                lst_usr.append(int(element_usr))
    except: #Verificar dígito de la lista
        resultado.config(text="Todos los valores deben ser números.") #Retornar frase en 'resultado' si no cumple las reglas
        return
    if len(lst_usr)!=4:  #Verificar longitud de lista
        resultado.config(text="La lista debe tener exactamente 4 dígitos positivos.") #Retornar frase en 'resultado' si no cumple las reglas
        return
    if len(set(lst_usr))!=4:  # Verificar no repetidos
        resultado.config(text="Los dígitos no deben repetirse.") #Retornar frase en 'resultado' si no cumple las reglas
        return
    
    #---CONTEO DE FAMA Y TOQUE---
    #--CONTADORES--
    cnt_fama=0  # Contador de fama
    cnt_toque=0  # Contador de toque
    #--CICLO DE COMPARACIÓN--
    for dig_pos in range (4): #Ciclo de posiciones para los dígitos en la lista de usuario
        for busqueda in range (4): #Ciclo para la busqueda de posiciones en la lista secreta
            if lst_usr[dig_pos]==lst_sec[busqueda] and lst_usr.index(lst_usr[dig_pos])==lst_sec.index(lst_sec[busqueda]): #Condicional para la suma de fama
                cnt_fama+=1 #Suma de fama
            if lst_usr[dig_pos]==lst_sec[busqueda] and lst_usr.index(lst_usr[dig_pos])!=lst_sec.index(lst_sec[busqueda]): #Condicional para la suma de toque
                cnt_toque+=1 #Suma de toque
    resultado.config(text=f"Toque: {cnt_toque}  Fama: {cnt_fama}  Intento {cnt_intento_actl} de {cnt_intento_mx}") #Retornar en 'resultado' los contadores, intentos actuales y máximos

    #--FINAL DEL JUEGO--
    if cnt_fama==4: #Condicional para ganar el juego
        resultado.config(text="Felicidades! Ganaste el juego.") #Retornar en 'resultado' mensaje de victoria
        boton_verificar_intento.config(state=DISABLED) #Desactivar boton_verificar_intento

    #---CONDICIONAL PARA PERDER---
    elif cnt_intento_actl>=cnt_intento_mx: #Condicional para perder el juego
        resultado.config(text=f"Perdiste! El número era: {' '.join(map(str, lst_sec))}") #Retornar en 'resultado' mensaje de pérdida
        boton_verificar_intento.config(state=DISABLED) #Desactivar boton_verificar_intento

#------------REINICIAR JUEGO---------------------------  
def reiniciar_juego(): #Función para reiniciar el juego, devolver a la pantalla_inicio
    pantalla_juego.pack_forget() #Cambiarse a pantalla_inicio
    boton_verificar_intento.config(state=NORMAL) #Devolver el estado del botón de verificación para el nuevo juego
    pantalla_inicio.pack(fill="both", expand=True) #Llama pantalla_inicio


#------------PANTALLA INICIO--------------------------
#---CONFIG. DE FONDO---
fondo=PhotoImage(file='diseno/fondo.png') #Variable de imagen de fondo
pantalla_inicio = Frame(ventana) #Creación de pantalla de inicio
canvas=Canvas(pantalla_inicio,width=450,height=650) #Canvas para imagen como fondo de pantalla
canvas.pack(fill="both", expand=True) #Agrega Canvas al frane
canvas.create_image(0, 0, image=fondo, anchor="nw") #Agrega imagen al Canvas

pantalla_inicio.pack(fill="both", expand=True) #Agrega frame pantalla_inicio

#---MUSICA---
play_img=PhotoImage(file='diseno/play.png') #Variable para imagen de boton_play
stop_img=PhotoImage(file='diseno/stop.png') #Variable para imagen de boton_stop
pygame.mixer.init() #Inicializa pygame
def play (): #Función para correr música
    pygame.mixer.music.load("diseno/musica.mp3") #Carga archivo de música (.mp3)
    pygame.mixer.music.play(-1) #Cantidad de repetición
def stop (): #Función para parar música
    pygame.mixer.music.stop() #Para música
boton_play=Button(pantalla_inicio,command=play,image=play_img, bg="#09092a", fg="#09092a",bd=0) #Botón para empezar música
canvas.create_window(1150, 80, window=boton_play) #Agrega botón_play a canvas
boton_stop=Button(pantalla_inicio,command=stop,image=stop_img, bg="#09092a", fg="#09092a",bd=0) #Botón para parar música
canvas.create_window(1230, 80, window=boton_stop) #Agrega botón_stop a canvas
    
#---Widget:Titulo---
frames=[PhotoImage(file='diseno/titulo.gif', format=f'gif -index {i}') for i in range(2)]  #2-frames para el GIF
titulo=Label(pantalla_inicio, image=frames[0], bd=0)  #Para no tener borde
canvas.create_window(650, 125, window=titulo)
def animar_1(i=0): #Función de animación para el gif de título
    titulo.config(image=frames[i])
    ventana.after(500, animar_1, (i+1)%len(frames))  #Cambiar cada 300ms
animar_1()

#---Widget: Otros elementos---
reglas=Label(pantalla_inicio, text="REGLAS:\n- Adivina un número secreto de 4 dígitos distintos.\n- FAMA=Dígito y posición correcta.\n- TOQUE=Dígito correcto, posición incorrecta.", fg="white", bg="#09092a", font=("Helvetica",15,"bold")) #Texto de inicio con las reglas del juego
canvas.create_window(650, 270, window=reglas) #Agrega a canvas
selec_niv=Label(pantalla_inicio, text="NIVELES:", fg="white", bg="#11093f", font=("Helvetica",25,"bold")) #Texto de selección de nivel
canvas.create_window(650, 400, window=selec_niv) #Agrega a canvas
boton_principiante=Button(pantalla_inicio, text="Principiante (10 intentos)", command=lambda: elegir_niv("principiante"), activebackground="#0cc0df", activeforeground="white",font=("Helvetica",15,"bold"),bg="#8288ef",fg="white") #Botón de nivel principiante
canvas.create_window(375, 490, window=boton_principiante) #Agrega a canvas
boton_intermedio=Button(pantalla_inicio, text="Intermedio (7 intentos)", command=lambda: elegir_niv("intermedio"), activebackground="#0cc0df", activeforeground="white",font=("Helvetica",15,"bold"),bg="#8288ef",fg="white") #Botón de nivel intermedio
canvas.create_window(650, 490, window=boton_intermedio) #Agrega a canvas
boton_experto=Button(pantalla_inicio, text="Experto (5 intentos)", command=lambda: elegir_niv("experto"), activebackground="#0cc0df", activeforeground="white",font=("Helvetica",15,"bold"),bg="#8288ef",fg="white") #Botón de nivel experto
canvas.create_window(900, 490, window=boton_experto) #Agrega a canvas

#------------PANTALLA JUEGO---------------------------
pantalla_juego=Frame(ventana) #Creación de pantalla de juego
pantalla_juego.pack(fill="both", expand=True) #Agrega frame pantalla_juego
canvas_2=Canvas(pantalla_juego,width=450, height=400) #canvas_2 para imagen como fondo de pantalla
canvas_2.pack(fill="both", expand=True) #Agrega canvas_2 al frame
bg_2=canvas_2.create_image(0, 0, image=fondo, anchor="nw") #Agrega imagen al canvas_2
#---MÚSICA---
boton_play=Button(pantalla_juego,command=play,image=play_img, bg="#09092a", fg="#09092a",bd=0) #Botón para empezar música
canvas_2.create_window(1150, 80, window=boton_play) #Agrega botón_play a canvas_2
boton_stop=Button(pantalla_juego,command=stop,image=stop_img, bg="#09092a", fg="#09092a",bd=0) #Botón para parar música
canvas_2.create_window(1230, 80, window=boton_stop) #Agrega botón_stop a canvas_2

#---Widget:Titulo---
frames_2=[PhotoImage(file='diseno/titulo2.gif', format=f'gif -index {i}') for i in range(2)]  #2-frames para el GIF
titulo_2=Label(pantalla_juego, image=frames_2[0], bd=0)  #Para no tener borde
canvas_2.create_window(650, 125, window=titulo_2)
def animar_2(i=0): #Función de animación para el gif de título
    titulo_2.config(image=frames_2[i])
    ventana.after(500, animar_2, (i+1)%len(frames_2))  #Cambiar cada 300ms
animar_2()
    
#---Widget: Otros elementos---
indicaciones=Label(pantalla_juego, text="Ingresa 4 números entre 0 y 9, separados por espacio:",  fg="white", bg="#09092a", font=("Helvetica",15,"bold")) #Texto de indicaciones
canvas_2.create_window(650, 270, window=indicaciones) #Agrega a canvas_2
entrada=Entry(pantalla_juego, justify=CENTER,bg="#46205d",fg="white",font=("Helvetica",25,"bold")) #Entrada para el intento del usuario
canvas_2.create_window(650, 350, window=entrada) #Agrega a canvas_2
boton_verificar_intento=Button(pantalla_juego, text="VERIFICAR", command=verificar_intento, activebackground="#0cc0df", activeforeground="white",font=("Helvetica",15,"bold"),bg="#8288ef",fg="white") #Botón de verificación de intento
canvas_2.create_window(650, 428, window=boton_verificar_intento) #Agrega a canvas_2
resultado=Label(pantalla_juego, text="",  fg="white", bg="#180c4c", font=("Helvetica",15,"bold"))  #Texto variable para indicar verificación positiva o negativa del intento y triunfo o pérdida del juego
canvas_2.create_window(650, 520, window=resultado) #Agrega a canvas_2
boton_reiniciar=Button(pantalla_juego, text="REINICIAR JUEGO", command=reiniciar_juego, activebackground="#0cc0df", activeforeground="white",font=("Helvetica",15,"bold"),bg="#8288ef",fg="white") #Botón para reiniciar el juego
canvas_2.create_window(650, 588, window=boton_reiniciar) #Agrega a canvas_2

#------------EJECUTAR INTERFAZ---------------------------
ventana.mainloop() #Bucle para mantener abierta la ventana
import tkinter
from tkinter import Scale, Label, PhotoImage
import random
import pygame
import os

# Inicializar pygame para el manejo de sonido
pygame.mixer.init()

FILAS = 25
COLUMNAS = 25
TAMAÑO_CELDA = 25

ANCHO_VENTANA = TAMAÑO_CELDA * COLUMNAS  # 25*25 = 625
ALTO_VENTANA = TAMAÑO_CELDA * FILAS  # 25*25 = 625

class Celda:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Cargar sonido de comer
archivo_sonido_comer = "./Music/comer.mp3"
if os.path.exists(archivo_sonido_comer):
    sonido_comer = pygame.mixer.Sound(archivo_sonido_comer)
    sonido_comer.set_volume(1.0)  # Volumen
else:
    print(f"Error: no se encontró el archivo de sonido '{archivo_sonido_comer}'")

# Cargar sonido de cambio de color
archivo_sonido_cambio_color = "./Music/cambio_color.mp3"
if os.path.exists(archivo_sonido_cambio_color):
    sonido_cambio_color = pygame.mixer.Sound(archivo_sonido_cambio_color)
    sonido_cambio_color.set_volume(1.0)  # Volumen
else:
    print(f"Error: no se encontró el archivo de sonido '{archivo_sonido_cambio_color}'")

# Lista colores serpiente
colores_personalizados = ["yellow", "hotpink", "darkblue", "darkorange", "white", "indigo", "olivedrab", "maroon", "gray", "tan"]

# Variable global para el color de la serpiente
color_serpiente = "lime green"

def cambiar_color_serpiente():
    global color_serpiente, puntaje
    secuencia_colores = ["lime green"] + colores_personalizados
    indice_color = (puntaje // 10) % len(secuencia_colores)
    color_serpiente = secuencia_colores[indice_color]
    if puntaje % 10 == 0 and puntaje != 0:  # Reproduce el sonido solo en múltiplos de 10
        if os.path.exists(archivo_sonido_cambio_color):
            sonido_cambio_color.play()

# Ventana del juego
ventana = tkinter.Tk()
ventana.title("Serpiente comelona | Creado por Mauricio")
ventana.resizable(False, False)

# Cargar el icono PNG
ruta_icono = "./assets/icon.png"  
if os.path.exists(ruta_icono):
    icono = PhotoImage(file=ruta_icono)
    ventana.iconphoto(False, icono)
else:
    print(f"Error: no se encontró el archivo de icono '{ruta_icono}'")

canvas = tkinter.Canvas(ventana, bg="black", width=ANCHO_VENTANA, height=ALTO_VENTANA, borderwidth=0, highlightthickness=0)
canvas.pack()
ventana.update()

# centrar la ventana
ancho_ventana = ventana.winfo_width()
alto_ventana = ventana.winfo_height()
ancho_pantalla = ventana.winfo_screenwidth()
alto_pantalla = ventana.winfo_screenheight()

ventana_x = int((ancho_pantalla / 2) - (ancho_ventana / 2))
ventana_y = int((alto_pantalla / 2) - (alto_ventana / 2))

# formato "(w)x(h)+(x)+(y)"
ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{ventana_x}+{ventana_y}")

# inicializar variables del juego
serpiente = Celda(TAMAÑO_CELDA * 5, TAMAÑO_CELDA * 5)  # ojos de serpiente
comida = Celda(TAMAÑO_CELDA * 10, TAMAÑO_CELDA * 10)
velocidadX = 0
velocidadY = 0
cuerpo_serpiente = []  
juego_terminado = False
puntaje = 0
puntaje_maximo = 0  # Reinicia a 0 el puntaje maximo cuando se cierra el juego

boton_reintentar = None

def reiniciar_juego():
    global serpiente, comida, velocidadX, velocidadY, cuerpo_serpiente, juego_terminado, puntaje, boton_reintentar, color_serpiente
    serpiente = Celda(TAMAÑO_CELDA * 5, TAMAÑO_CELDA * 5)
    comida = Celda(TAMAÑO_CELDA * 10, TAMAÑO_CELDA * 10)
    velocidadX = 0
    velocidadY = 0
    cuerpo_serpiente = []
    juego_terminado = False
    puntaje = 0
    color_serpiente = "lime green"  # Restablecer el color de la serpiente
    if boton_reintentar:
        boton_reintentar.destroy()  # Elimina boton de reintentar al apretar
        boton_reintentar = None
    canvas.delete("all")  # Limpiar el juego
    dibujar()  # redibuja el juego inmediatamente

def cambiar_direccion(e):  # e = event
    global velocidadX, velocidadY, juego_terminado
    if juego_terminado:
        return  

    if e.keysym == "Up" and velocidadY != 1:
        velocidadX = 0
        velocidadY = -1
    elif e.keysym == "Down" and velocidadY != -1:
        velocidadX = 0
        velocidadY = 1
    elif e.keysym == "Left" and velocidadX != 1:
        velocidadX = -1
        velocidadY = 0
    elif e.keysym == "Right" and velocidadX != -1:
        velocidadX = 1
        velocidadY = 0

def mover():
    global serpiente, comida, cuerpo_serpiente, juego_terminado, puntaje
    
    if juego_terminado:
        return

    # Verificar el cruce fronterizo y rodear
    if serpiente.x < 0:
        serpiente.x = ANCHO_VENTANA - TAMAÑO_CELDA
    elif serpiente.x >= ANCHO_VENTANA:
        serpiente.x = 0
    if serpiente.y < 0:
        serpiente.y = ALTO_VENTANA - TAMAÑO_CELDA
    elif serpiente.y >= ALTO_VENTANA:
        serpiente.y = 0

    for celda in cuerpo_serpiente:
        if serpiente.x == celda.x and serpiente.y == celda.y:
            juego_terminado = True
            return

    # colisión
    if serpiente.x == comida.x and serpiente.y == comida.y:
        cuerpo_serpiente.append(Celda(comida.x, comida.y))
        comida.x = random.randint(0, COLUMNAS - 1) * TAMAÑO_CELDA
        comida.y = random.randint(0, FILAS - 1) * TAMAÑO_CELDA
        puntaje += 1
        if os.path.exists(archivo_sonido_comer):
            sonido_comer.play()  
        cambiar_color_serpiente()

    # actualizar el cuerpo de la serpiente
    for i in range(len(cuerpo_serpiente) - 1, -1, -1):
        celda = cuerpo_serpiente[i]
        if i == 0:
            celda.x = serpiente.x
            celda.y = serpiente.y
        else:
            celda_previa = cuerpo_serpiente[i - 1]
            celda.x = celda_previa.x
            celda.y = celda_previa.y

    serpiente.x += velocidadX * TAMAÑO_CELDA
    serpiente.y += velocidadY * TAMAÑO_CELDA

def dibujar():
    global serpiente, comida, cuerpo_serpiente, juego_terminado, puntaje, boton_reintentar, puntaje_maximo
    mover()

    canvas.delete("all")

    # Comida
    canvas.create_rectangle(comida.x, comida.y, comida.x + TAMAÑO_CELDA, comida.y + TAMAÑO_CELDA, fill='red')

    # Cabeza de serpiente
    canvas.create_rectangle(serpiente.x, serpiente.y, serpiente.x + TAMAÑO_CELDA, serpiente.y + TAMAÑO_CELDA, fill=color_serpiente)

    # Ojos
    radio_ojo = TAMAÑO_CELDA // 8
    desplazamiento_ojo_x = TAMAÑO_CELDA // 6
    desplazamiento_ojo_y = TAMAÑO_CELDA // 4
    # Ojo izquierdo
    canvas.create_oval(serpiente.x + desplazamiento_ojo_x, serpiente.y + desplazamiento_ojo_y,
                       serpiente.x + desplazamiento_ojo_x + radio_ojo * 2, serpiente.y + desplazamiento_ojo_y + radio_ojo * 2,
                       fill='black')
    # Ojo derecho
    canvas.create_oval(serpiente.x + TAMAÑO_CELDA - desplazamiento_ojo_x - radio_ojo * 2, serpiente.y + desplazamiento_ojo_y,
                       serpiente.x + TAMAÑO_CELDA - desplazamiento_ojo_x, serpiente.y + desplazamiento_ojo_y + radio_ojo * 2,
                       fill='black')

    # Cuerpo de la serpiente
    for celda in cuerpo_serpiente:
        canvas.create_rectangle(celda.x, celda.y, celda.x + TAMAÑO_CELDA, celda.y + TAMAÑO_CELDA, fill=color_serpiente)

    # Puntaje
    canvas.create_text(10, 10, anchor='nw', fill='white', font=('TkDefaultFont', 14), text=f"Puntaje: {puntaje}")

    if puntaje > puntaje_maximo:
        puntaje_maximo = puntaje
    canvas.create_text(ANCHO_VENTANA - 10, 10, anchor='ne', fill='white', font=('TkDefaultFont', 14), text=f"Puntaje Máximo: {puntaje_maximo}")

    # Si el juego termina, muestra el mensaje y un botón de reintentar
    if juego_terminado:
        canvas.create_text(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 - 20, fill='white', font=('TkDefaultFont', 24), text="Juego Terminado")
        boton_reintentar = tkinter.Button(ventana, text="Reintentar", command=reiniciar_juego)
        boton_reintentar.pack()
        boton_reintentar.place(x=ANCHO_VENTANA // 2 - 50, y=ALTO_VENTANA // 2 + 20)

    # Redibuja el juego después de un pequeño retraso
    canvas.after(100, dibujar)

# Configurar los controles
ventana.bind("<KeyPress>", cambiar_direccion)

# Iniciar el bucle del juego
dibujar()

ventana.mainloop()

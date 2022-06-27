
import pygame
from pygame.locals import *
import random

pygame.init()

# Definimos las constantes que vamos a ir usando durante nuestro programa.
W, H = 612, 408             # Ancho y alto de la pantalla, respectivamente
width,height = 120,120      # Tamaño del rectangulo del personaje (walking)
w_,h_ =200,200              # Tamaño de la imagen central
vel = 5                     # Velocidad para el personaje
x_pos = 50                  # Posicion del personaje con respecto al eje X  | Hablamos realmente de la posicion del vértice superior izquierdo del rectangulo 
y_pos = H - height          # Posicion del personaje con respecto al eje Y  | "imaginario" que contiene a nuestro personaje. 
NEGRO = [0, 0, 0]           # Definimos el color negro
BLANCO = [255, 255, 255]    # y el blanco


win = pygame.display.set_mode((W,H))               # Asignamos a la variable win el encuadre de nuestra ventana
pygame.display.set_caption("FELIZ NAVIDAD. CICE")  # e indicamos el mensaje que queremos que aparezca en la barra superior


#?...···...···...···...···...···...···...···...···FUNCIONES...···...···...···...···...···...···...···...···...···*#

def configura_imagenes():
    cont = 0                           # Recorremos la lista de imagenes para irlas escalando y guardando en su lista correspondiente
    for img in imagenes_walk:          # según la dirrección en la que esté caminando el muñequito
        if cont in (0,1,2):
            img_convert = img.convert()
            img_convert.set_colorkey(NEGRO)
            walkRight.append(pygame.transform.scale(img_convert, (width,height)))
        if cont in (3,4,5):
            img_convert = img.convert()
            img_convert.set_colorkey(NEGRO)
            walkLeft.append(pygame.transform.scale(img_convert, (width,height)))
        if cont in (6,7,8):
            img_convert = img.convert()
            img_convert.set_colorkey(NEGRO)
            walkUp.append(pygame.transform.scale(img_convert, (width,height)))
        if cont in (9,10,11):
            img_convert = img.convert()
            img_convert.set_colorkey(NEGRO)
            walkDown.append(pygame.transform.scale(img_convert, (width,height)))
        if cont in (12,13,14):                                                     # Las 3 ultimas corresponden al muñeco hablando
            daliTalking.append(pygame.transform.scale(img, (w_+60,h_+60)))
        cont += 1

def redrawGameWindow1():

    global dali_rect, buttom_rect

    win.blit(bg, (0,0))                    # Redibujamos background  |
    win.blit(scaled_cice,(204,50))         # La imagen de cice       |  Imagenes que completan nuestro escenario (fijas)
    win.blit(scaled_play_buttom,(420,170)) # Start_buttom            | (es una manera de limpiar la pantalla de todo lo demas antes de imprimir el muñeco en la nueva posicion)
    buttom_rect = scaled_play_buttom.get_rect().move(420,170)
    if muestra_mensaje:
        myfont = pygame.font.SysFont('Comic Sans MS', 18)
        textsurface = myfont.render('Pulsa la barra espaciadora para escuchar el mensaje.', False, BLANCO)
        win.blit(textsurface,(0,0))


    global walkCount            # De esta manera podemos usar y modificar la variable walkCount declarada fuera de la funcion

    if walkCount + 1 >= 9 :   #? 9 Es el numero de imagenes que existen para cada direccion al cubo 3^3 para que solo cambie de imagen cada 3 ciclos
        walkCount = 0         #? es complicado de explicar pero basicamente hace que los movimientos del muñeco sean mas lentos aunque tambien puedes modificar
                              #? la velocidad del clock para ver el efecto en la velocidad del movimiento del caracter.
    if left:                                                 #|
        win.blit(walkLeft[walkCount//3], (x_pos,y_pos))      #|

        walkCount += 1                                       #|
    elif right:                                              #| En este if, simplemente, imprimimos la imagen del muñeco que corresponda a la direccion
        win.blit(walkRight[walkCount//3], (x_pos,y_pos))     #| detectada por teclado y que nos viene reflejada en las variables de la funcion principal: left right up down
        walkCount += 1                                       #| con valor True o False. Accedemos a la lista de imagenes que corresponda a dicha direccion, a la posicion 
    elif up:                                                 #| walkCount//3 que siempre será (0,1 u 2) puesto que dijimos arriba que walkCount < 9. También le pasamos
        win.blit(walkUp[walkCount//3], (x_pos,y_pos))        #| la posicion en la que situaremos el vertice superior izquierdo de la imagen, modificados en la 
        walkCount += 1                                       #| función principal, tras haber aplicado la velocidad (vel).
    elif down:                                               #|
        win.blit(walkDown[walkCount//3], (x_pos,y_pos))      #|
        walkCount += 1                                       #|
    else:                                   #| Si todas las variables estan en False, el muñeco está parado así que imprimimos la imagen que guardamos al principio en char
        win.blit(char, (x_pos, y_pos))      #|
        walkCount = 0                       #| Reiniciamos walkCount a 0 puesto que ha dejado de moverse
   
    dali_rect = char.get_rect().move(x_pos, y_pos)
         
def redrawGameWindow2():

    win.blit(bg, (0,0))                         # Redibujamos background  |
    win.blit(daliTalking[gestos[contador]],(180,50))    # La cara de Dalí         |  Imagenes que completan nuestro escenario (fijas)
   
def makeMusic(filename):
    pygame.mixer.music.load(filename)

def playMusic(loops=0):
    pygame.mixer.music.play(loops)

def stopMusic():
    pygame.mixer.music.stop()

def control_quit():
    global run
    for event in pygame.event.get():     #|
        if event.type == pygame.QUIT:    #|  Controla el evento QUIT para parar el bucle al cerrar
            run = False                  #|

def control_movimientos(keys):
    global left,right,up,down,x_pos,y_pos,run,dali_rect,buttom_rect,muestra_mensaje

    if keys[pygame.K_LEFT] and x_pos > vel:  #| Si la posicion del evento que controla la tecla left es igual a 1 Y la posicion del muñeco con respecto al eje x
        x_pos -= vel                         #| es mayor que la velocidad : a la posicion x le restamos la velocidad que viene a ser la cantidad de pixeles
        left = True                          #| que desea desplazar en cada ejecucion del bucle. Marcamos como True la direccion a la que va y el resto se resetean 
        right = False                        #| todas a False.
        up = False                           #| Pasa exactamente lo mismo con las demás teclas de dirección solo que con diferentes condiciones 
        down = False                         #| y operaciones con la velocidad. Veamos:

    elif keys[pygame.K_RIGHT] and x_pos < W - width:  #| Con esta segunda condición controlamos que la posicion del muñeco (recordemos que es la posicion de su vértice superior izquierdo)
        x_pos += vel                                  #| quede dentro de la pantalla.                              |
        left = False                                  #| x_pos                                                     |  <-- Aqui termina la pantalla de juego
        right = True                                  #|  º__________widht____________                    x_pos    |      siendo esta la posicion W (ancho de la pantalla)
        up = False                                    #|  |                           |                    ª_______|__widht__________    
        down = False                                  #|  |     IMAGEN PERSONAJE      |                    |       | IMAGEN FUERA    |
                                                      #|  |                           |                    |       | DE PANTALLA     |

    elif keys[pygame.K_UP] and y_pos > H - height*1.8:  #| Aqúi simplemente he usado la medida de la altura del rectangulo del personaje para limitar el movimiento
        y_pos -= vel                                    #| del muñeco por la pantalla ya que solo quiero que se mueva por el suelo. Pensé que mas o menos era dos veces 
        left = False                                    #| esa medida. Probé 1.8 y corta el paso justo por donde yo quería. A sido un poco a ojo. Y la operación 
        right = False                                   #| H - (1.8*height) sigue exactamente la lógica de la explicación anterior pero con respecto al eje y 
        up = True
        down = False

    elif keys[pygame.K_DOWN] and y_pos < H - height :   #| Igualmente este sigue exactamente la misma lógica. Son condiciones todas para limitar la imagen dentro de la pantalla.
        y_pos += vel
        left = False
        right = False
        up = False
        down = True
        
    else:                  # Si ninguna de las teclas anteriores ha sido pulsada, reiniciamos a 0 la variable walkCount
        left = False       # y a False todas las variables de direccion.
        right = False
        up = False
        down = False
        walkCount = 0

    if dali_rect.colliderect(buttom_rect):
        muestra_mensaje = True
        if keys[pygame.K_SPACE]:
            mensaje = makeSound("./data/sounds/boom.mp3")
            playSound(mensaje,0)
            run = False

def nevar():
    global lista_nieve

    for i in range(len(lista_nieve)):                             # Procesamos cada copo de la lista.
        pygame.draw.circle(win, BLANCO, lista_nieve[i], 2)        # Dibujamos el copo de nieve
        lista_nieve[i][1] += 1                                    # Desplazamos un píxel hacia abajo el copo de nieve.
         
        if lista_nieve[i][1] > H:               # Si el copo se escapa del fondo de la pantalla.
            y = random.randrange(-50, -10)      # Lo movemos justo encima del todo
            lista_nieve[i][1] = y
            x = random.randrange(0, W)          # Le damos una nueva ubicación x
            lista_nieve[i][0] = x

def makeSound(filename):
    pygame.mixer.init()
    thissound = pygame.mixer.Sound(filename)

    return thissound

def playSound(sound, loops=0):
    sound.play(loops)

def stopSound(sound):
    sound.stop()

#?...···...···...···...···...···...···...···...·FIN FUNCIONES...···...···...···...···...···...···...···...···...···*#


#?.........................................CONFIGURACION IMAGENES.....................................................*#

# Importamos todas las imagenes en una misma lista. En este caso tenemos 3 por cada direccion: right, left, down y up
imagenes_walk = [pygame.image.load('./data/images/dali_right1.png'), pygame.image.load('./data/images/dali_right2.png'), pygame.image.load('./data/images/dali_right3.png'), pygame.image.load('./data/images/dali_left1.png'), pygame.image.load('./data/images/dali_left2.png'), pygame.image.load('./data/images/dali_left3.png'), pygame.image.load('./data/images/dali_up1.png'), pygame.image.load('./data/images/dali_up2.png'), pygame.image.load('./data/images/dali_up3.png'),pygame.image.load('./data/images/dali_down1.png'),pygame.image.load('./data/images/dali_down2.png'), pygame.image.load('./data/images/dali_down3.png'),pygame.image.load("./data/images/dali.png"), pygame.image.load("./data/images/dali2.png"), pygame.image.load("./data/images/dali3.png")]

walkRight,walkLeft,walkUp,walkDown,daliTalking = [],[],[],[],[]

configura_imagenes()

char = walkDown[1] # Vamos a asignarle la posicion en la que el character está de frente para cuando éste esté en pausa. (Cuando no esté recibiendo orden de moverse.)

bg = pygame.image.load('./data/images/dancefloor.jpg') # Cargamos en la variable bg la imagen para el background
cice = pygame.image.load('./data/images/cice_christmas.png') # Cargamos el logo de cice navideño, y en la siguiente linea lo escalamos para que tenga el tamaño que queremos.
scaled_cice = pygame.transform.scale(cice, (w_,h_))
play_buttom = pygame.image.load('./data/images/play_buttom.png') # Cargamos el botón de PLAY, y en la siguiente linea lo escalamos también.
scaled_play_buttom = pygame.transform.scale(play_buttom, (100,80))
buttom_rect= pygame.__rect_constructor(100,80,420,170)
dali_rect= pygame.__rect_constructor(x_pos,y_pos,width,height)
last_bg = pygame.image.load('./data/images/dancefloor.jpg')
scaled_last_bg = pygame.transform.scale(last_bg, (200,400))

lista_nieve = []        # Creamos un array vacío para llenarlo de "copos de nieve"
 
for i in range(50):                 # Iteramos 50 veces y añadimos un copo de nieve en una ubicación (x,y) aleatoria.
    x = random.randrange(0, W)
    y = random.randrange(0, H)
    lista_nieve.append([x, y])

#?...........................................FIN CONFIGURACION IMAGENES...............................................*#

makeMusic("./data/sounds/beepbeep.mp3")   # Cargamos el sonido base
playMusic(-1)   # Reproducimos la cancion con loop = -1 para que se reproduzca en bucle

clock = pygame.time.Clock() # Asignamos un reloj de pygame a la variable clock

left = False  # Inicializamos las variables que vamos a necesitar 
right = False
up = False
down = False
walkCount = 0
muestra_mensaje = False
contador = 0
contador2 = 0
contador3 = 0  

run = True  # Condicion del bucle, iniciada como True para que pueda acceder al bucle la primera vez.

while run:

    clock.tick(20) # Asignamos un límite de 20fps

    control_quit()

    keys = pygame.key.get_pressed()   # Almacenamos en keys la lista de 0s y 1s que controla los eventos de teclado, donde todos son 0 hasta que 
                                      # se pulsa una tecla, que entonces su posicion correspondiente en la lista se convertirá en 1
    control_movimientos(keys)

    redrawGameWindow1()     

    nevar()
    
    pygame.display.update()   # Actualiza pantalla

stopMusic()
makeMusic("./data/sounds/mensaje_dali.mp3")
playMusic()

run = True
gestos = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,1,0,2,0,1,0,2,0,1,1,2,1,0,2,0,1,0,2,0,0,0,0,0,0,0,0,0,0,1,1,2,1,0,2,0,1,0,2,0] # Secuencia de gestos de la cara de Dali cuando esta dando el mensaje.

while run:

    clock.tick(13) # Asignamos un límite de 13fps

    control_quit()

    redrawGameWindow2()     

    nevar()

    if contador==len(gestos)-1: 
        contador=0
        contador2 += 1
    else: 
        contador += 1
        contador3 += 1
        if contador3 == 28:
            bg_sound = makeSound("./data/sounds/bellaciao.wav")
            playSound(bg_sound,0)
        if contador2 == 7 and contador >= 10:
            contador = 0
            
    pygame.display.update()   # Actualiza pantalla

pygame.quit()
    

import pygame
import random

# Dimensiones de la ventana
ANCHO_VENTANA = 640
ALTO_VENTANA = 640

# Tamaño de cada casilla del tablero
TAMANO_CASILLA = ANCHO_VENTANA // 8

# Colores
COLOR_FONDO = (255, 255, 255)
COLOR_CASILLA_BLANCA = (255, 255, 255)
COLOR_CASILLA_NEGRA = (120, 120, 120)
COLOR_CABALLO_1 = (255, 0, 0)
COLOR_CABALLO_2 = (0, 0, 255)
COLOR_PUNTOS = (0, 0, 0)
COLOR_TEXTO = (0, 0, 0)

# Dificultades del juego
DIFICULTAD_PRINCIPIANTE = 2
DIFICULTAD_AMATEUR = 4
DIFICULTAD_EXPERTO = 6


# Función heurística para el nivel principiante
def funcion_heuristica_principiante(tablero, puntaje_jugador_1, puntaje_jugador_2):
    return puntaje_jugador_1 - puntaje_jugador_2

# Función heurística para el nivel amateur
def funcion_heuristica_amateur(tablero, puntaje_jugador_1, puntaje_jugador_2):
    return puntaje_jugador_1 - puntaje_jugador_2**2

# Función heurística para el nivel experto
def funcion_heuristica_experto(tablero, puntaje_jugador_1, puntaje_jugador_2):
    return puntaje_jugador_1 - puntaje_jugador_2**2

# Inicializar Pygame
pygame.init()

# Crear la ventana
ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Smart Horses")

# Fuentes de texto
fuente_puntaje = pygame.font.SysFont("Arial", 24)
fuente_turno = pygame.font.SysFont("Arial", 32, True)

imagen_caballo_1 = pygame.image.load("horse1.png")
imagen_caballo_1 = pygame.transform.scale(imagen_caballo_1, (TAMANO_CASILLA, TAMANO_CASILLA))

imagen_caballo_2 = pygame.image.load("horse0.png")
imagen_caballo_2 = pygame.transform.scale(imagen_caballo_2, (TAMANO_CASILLA, TAMANO_CASILLA))

def generar_tablero_inicial():
    tablero = [[0] * 8 for _ in range(8)]
    
    # Generar posiciones aleatorias de los caballos
    caballo_1 = (random.randint(0, 7), random.randint(0, 7))
    caballo_2 = (random.randint(0, 7), random.randint(0, 7))
    
    # Generar casillas con puntos
    valor =  1
    for _ in range(7):
        fila = random.randint(0, 7)
        columna = random.randint(0, 7)
        tablero[fila][columna] = valor
        valor = valor +1

    return tablero, caballo_1, caballo_2

def dibujar_tablero(tablero, caballo_1, caballo_2, puntaje_jugador_1, puntaje_jugador_2, turno_jugador_1):
    # Limpiar la ventana
    ventana.fill(COLOR_FONDO)
    
    # Dibujar las casillas
    for fila in range(8):
        for columna in range(8):
            color_casilla = COLOR_CASILLA_BLANCA if (fila + columna) % 2 == 0 else COLOR_CASILLA_NEGRA
            pygame.draw.rect(ventana, color_casilla, (columna * TAMANO_CASILLA, fila * TAMANO_CASILLA, TAMANO_CASILLA, TAMANO_CASILLA))
    
    # Dibujar los puntos
    for fila in range(8):
        for columna in range(8):
            if tablero[fila][columna] > 0:
                texto_puntos = fuente_puntaje.render(str(tablero[fila][columna]), True, COLOR_PUNTOS)
                ventana.blit(texto_puntos, (columna * TAMANO_CASILLA + TAMANO_CASILLA // 2 - texto_puntos.get_width() // 2, fila * TAMANO_CASILLA + TAMANO_CASILLA // 2 - texto_puntos.get_height() // 2))
            
    # Dibujar los caballos
    ventana.blit(imagen_caballo_1, (caballo_1[1] * TAMANO_CASILLA, caballo_1[0] * TAMANO_CASILLA))
    ventana.blit(imagen_caballo_2, (caballo_2[1] * TAMANO_CASILLA, caballo_2[0] * TAMANO_CASILLA))

    # Mostrar el puntaje de cada jugador
    texto_puntaje_jugador_1 = fuente_puntaje.render(f"Puntaje Jugador 1: {puntaje_jugador_1}", True, COLOR_TEXTO)
    texto_puntaje_jugador_2 = fuente_puntaje.render(f"Puntaje Jugador 2: {puntaje_jugador_2}", True, COLOR_TEXTO)
    ventana.blit(texto_puntaje_jugador_1, (10, 10))
    ventana.blit(texto_puntaje_jugador_2, (10, 40))
    
    # Mostrar el turno del jugador
    texto_turno = fuente_turno.render("Turno Jugador 1" if turno_jugador_1 else "Turno Jugador 2", True, COLOR_TEXTO)
    ventana.blit(texto_turno, (ANCHO_VENTANA // 2 - texto_turno.get_width() // 2, 10))
    
    # Actualizar la ventana
    pygame.display.update()

def obtener_input():
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif evento.type == pygame.MOUSEBUTTONUP:
                pos_mouse = pygame.mouse.get_pos()
                fila = pos_mouse[1] // TAMANO_CASILLA
                columna = pos_mouse[0] // TAMANO_CASILLA
                return fila, columna

def mover_caballo(tablero, origen, destino):
    fila_origen, columna_origen = origen
    fila_destino, columna_destino = destino
    
    valor_casilla = tablero[fila_destino][columna_destino]
    
    tablero[fila_destino][columna_destino] = tablero[fila_origen][columna_origen]
    tablero[fila_origen][columna_origen] = 0
    
    return (fila_destino, columna_destino), valor_casilla

def hay_casillas_con_puntos(tablero):
    for fila in tablero:
        if any(casilla > 0 for casilla in fila):
            return True
    return False

def es_movimiento_valido(tablero, origen, destino):
    if origen == destino:
        return False
    
    fila_origen, columna_origen = origen
    fila_destino, columna_destino = destino
    
    if fila_destino < 0 or fila_destino >= 8 or columna_destino < 0 or columna_destino >= 8:
        return False
    
    diferencia_fila = abs(fila_destino - fila_origen)
    diferencia_columna = abs(columna_destino - columna_origen)
    
    if diferencia_fila == 2 and diferencia_columna == 1:
        return True
    elif diferencia_fila == 1 and diferencia_columna == 2:
        return True
    
    return False

def generar_movimientos_posibles(tablero, caballo, nivel_dificultad):
    fila, columna = caballo
    
    if nivel_dificultad == DIFICULTAD_PRINCIPIANTE:
        movimientos = [
            (fila + 2, columna + 1), (fila + 2, columna - 1),
            (fila - 2, columna + 1), (fila - 2, columna - 1),
            (fila + 1, columna + 2), (fila + 1, columna - 2),
            (fila - 1, columna + 2), (fila - 1, columna - 2)
        ]
    elif nivel_dificultad == DIFICULTAD_AMATEUR:
        movimientos = [
            (fila + 2, columna + 1), (fila + 2, columna - 1),
            (fila - 2, columna + 1), (fila - 2, columna - 1),
            (fila + 1, columna + 2), (fila + 1, columna - 2),
            (fila - 1, columna + 2), (fila - 1, columna - 2),
            (fila + 1, columna), (fila - 1, columna),
            (fila, columna + 1), (fila, columna - 1)
        ]
    elif nivel_dificultad == DIFICULTAD_EXPERTO:
        movimientos = [
            (fila + 2, columna + 1), (fila + 2, columna - 1),
            (fila - 2, columna + 1), (fila - 2, columna - 1),
            (fila + 1, columna + 2), (fila + 1, columna - 2),
            (fila - 1, columna + 2), (fila - 1, columna - 2),
            (fila + 1, columna), (fila - 1, columna),
            (fila, columna + 1), (fila, columna - 1),
            (fila + 2, columna), (fila - 2, columna),
            (fila, columna + 2), (fila, columna - 2)
        ]
    else:
        movimientos = []
    
    movimientos_validos = []
    for movimiento in movimientos:
        if es_movimiento_valido(tablero, caballo, movimiento):
            movimientos_validos.append(movimiento)
    
    return movimientos_validos

def minimax(tablero, caballo_1, caballo_2, puntaje_jugador_1, puntaje_jugador_2, nivel_dificultad, maximo_nivel, turno_jugador_1):
    if maximo_nivel == 0 or not hay_casillas_con_puntos(tablero):
        return puntaje_jugador_1 - puntaje_jugador_2
    
    if turno_jugador_1:
        puntaje_maximo = float('-inf')
        caballo = caballo_1
        jugador_actual = 1
    else:
        puntaje_maximo = float('inf')
        caballo = caballo_2
        jugador_actual = 2
    
    movimientos_posibles = generar_movimientos_posibles(tablero, caballo, nivel_dificultad)
    
    for movimiento in movimientos_posibles:
        fila_origen, columna_origen = caballo
        fila_destino, columna_destino = movimiento
        
        valor_casilla = tablero[fila_destino][columna_destino]
        
        tablero[fila_destino][columna_destino] = 0
        tablero[fila_origen][columna_origen] = valor_casilla

        if turno_jugador_1:
            nuevo_puntaje_jugador_1 = puntaje_jugador_1 + valor_casilla
            nuevo_puntaje_jugador_2 = puntaje_jugador_2
        else:
            nuevo_puntaje_jugador_1 = puntaje_jugador_1
            nuevo_puntaje_jugador_2 = puntaje_jugador_2 + valor_casilla
        
        puntaje = minimax(tablero, caballo_1, caballo_2, nuevo_puntaje_jugador_1, nuevo_puntaje_jugador_2, nivel_dificultad, maximo_nivel - 1, not turno_jugador_1)
        
        if (turno_jugador_1 and puntaje > puntaje_maximo) or (not turno_jugador_1 and puntaje < puntaje_maximo):
            puntaje_maximo = puntaje
        
        tablero[fila_destino][columna_destino] = valor_casilla
        tablero[fila_origen][columna_origen] = 0
    
    return puntaje_maximo

def jugar_partida(nivel_dificultad):
    tablero, caballo_1, caballo_2 = generar_tablero_inicial()
    puntaje_jugador_1 = 0
    puntaje_jugador_2 = 0
    turno_jugador_1 = True

    

    while hay_casillas_con_puntos(tablero):
        dibujar_tablero(tablero, caballo_1, caballo_2, puntaje_jugador_1, puntaje_jugador_2, turno_jugador_1)
        
        if turno_jugador_1:
            print("Turno del Jugador 1:")
            origen = caballo_1
        else:
            print("Turno del Jugador 2:")
            origen = caballo_2
        
        movimiento_valido = False
        while not movimiento_valido:
            if turno_jugador_1:
                print("Movimiento Automático del Jugador 1...")
                movimientos_posibles = generar_movimientos_posibles(tablero, origen, nivel_dificultad)
                movimiento = movimientos_posibles[random.randint(0, len(movimientos_posibles) - 1)]
            else:
                #print("Ingrese las coordenadas de destino (fila y columna):")
                movimiento = obtener_input()
            
            movimiento_valido = es_movimiento_valido(tablero, origen, movimiento)
        
        if turno_jugador_1:
            caballo_1, valor_casilla = mover_caballo(tablero, caballo_1, movimiento)
            puntaje_jugador_1 += valor_casilla
        else:
            caballo_2, valor_casilla = mover_caballo(tablero, caballo_2, movimiento)
            puntaje_jugador_2 += valor_casilla
        
        turno_jugador_1 = not turno_jugador_1
    
    dibujar_tablero(tablero, caballo_1, caballo_2, puntaje_jugador_1, puntaje_jugador_2, turno_jugador_1)
    
    puntaje_final_jugador_1 = puntaje_jugador_1
    puntaje_final_jugador_2 = puntaje_jugador_2

    if nivel_dificultad == DIFICULTAD_PRINCIPIANTE:
        funcion_heuristica = funcion_heuristica_principiante
    elif nivel_dificultad == DIFICULTAD_AMATEUR:
        funcion_heuristica = funcion_heuristica_amateur
    elif nivel_dificultad == DIFICULTAD_EXPERTO:
        funcion_heuristica = funcion_heuristica_experto
    if nivel_dificultad != 0:
        funcion_heuristica = minimax(tablero, caballo_1, caballo_2, puntaje_jugador_1, puntaje_jugador_2, nivel_dificultad, nivel_dificultad, True)
        
        if funcion_heuristica > 0:
            puntaje_final_jugador_1 += funcion_heuristica
        elif funcion_heuristica < 0:
            puntaje_final_jugador_2 -= funcion_heuristica
    
    if puntaje_final_jugador_1 > puntaje_final_jugador_2:
        print("¡Jugador 1 ha ganado!")
    elif puntaje_final_jugador_1 < puntaje_final_jugador_2:
        print("¡Jugador 2 ha ganado!")
    else:
        print("¡Empate!")
    
    pygame.quit()

jugar_partida(DIFICULTAD_EXPERTO)
# Variable para rastrear el estado anterior de los dedos
estado_anterior = None  # Inicialmente no hay estado previo

def dedos_levantados(hand_landmarks):
    """
    Determina qué dedos están levantados en base a las posiciones de los puntos de referencia de la mano.
    """
    dedos = []
    
    # Determinar si el pulgar está levantado:
    # Se considera levantado si el punto 4 (punta del pulgar) está a la izquierda (x <) del punto 3.
    if hand_landmarks[4].x < hand_landmarks[3].x:
        dedos.append(1)  # Pulgar levantado
    else:
        dedos.append(0)  # Pulgar abajo

    # Determinar si los otros dedos están levantados:
    # Se compara la posición y (altura) de la punta del dedo (punto i) con su base (punto i-2).
    for i in [8, 12, 16, 20]:  # Índice, medio, anular, meñique
        if hand_landmarks[i].y < hand_landmarks[i - 2].y:
            dedos.append(1)  # Dedo levantado
        else:
            dedos.append(0)  # Dedo abajo

    return dedos


def detectar_numero(dedos, hand_landmarks):
    """
    Detecta números del 0 al 10 basados en los dedos levantados.
    Los gestos se determinan de la siguiente manera:
    """
    global estado_anterior  # Para rastrear transiciones

    # Número 0: Todos los dedos están abajo
    if dedos == [0, 0, 0, 0, 0]:
        estado_anterior = "cerrada"  # Actualizamos el estado a "mano cerrada"
        return "0"

    # Número 1: Solo el índice está levantado
    elif dedos == [0, 1, 0, 0, 0]:
        return "1"

    # Número 2: El índice y el medio están levantados
    elif dedos == [0, 1, 1, 0, 0]:
        return "2"

    # Número 3: El índice, el medio y el anular están levantados
    elif dedos == [0, 1, 1, 1, 0]:
        return "3"

    # Número 4: Todos los dedos, excepto el pulgar, están levantados
    elif dedos == [0, 1, 1, 1, 1]:
        return "4"

    # Número 5: Todos los dedos están levantados
    elif dedos == [1, 1, 1, 1, 1]:
        if estado_anterior == "cerrada":  # Si el estado anterior era "mano cerrada"
            estado_anterior = "abierta"  # Actualizamos el estado a "mano abierta"
            return "10"  # Transición completa: 10
        estado_anterior = "abierta"  # Seguimos en "mano abierta"
        return "5"

    # Número 6: Solo el pulgar está levantado
    elif dedos == [1, 0, 0, 0, 0]:
        return "6"

    # Número 7: El pulgar y el índice están levantados
    elif dedos == [1, 1, 0, 0, 0]:
        return "7"

    # Número 8: El pulgar, el índice y el medio están levantados
    elif dedos == [1, 1, 1, 0, 0]:
        return "8"

    # Número 9: Todos los dedos, excepto el meñique, están levantados
    elif dedos == [1, 1, 1, 1, 0]:
        return "9"

    # Si no coincide con ningún patrón conocido
    return "Número desconocido"

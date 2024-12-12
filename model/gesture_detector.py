import math

def dedos_levantados(hand_landmarks):
    dedos = []
    if hand_landmarks[4].x < hand_landmarks[3].x:
        dedos.append(1)
    else:
        dedos.append(0)

    for i in [8, 12, 16, 20]:
        if hand_landmarks[i].y < hand_landmarks[i - 2].y:
            dedos.append(1)
        else:
            dedos.append(0)

    return dedos

def detectar_numero(dedos, hand_landmarks):
    if dedos == [1, 1, 1, 1, 1]:
        return "5"
    elif dedos == [0, 1, 0, 0, 0]:
        return "1"
    elif dedos == [0, 1, 1, 0, 0]:
        return "2"
    elif dedos == [1, 1, 1, 0, 0]:
        return "3"
    elif dedos == [0, 1, 1, 1, 1]:
        return "4"
    return "Número desconocido"

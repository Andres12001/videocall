def detectar_accion(dedos, hand_landmarks):
    """
    Detecta acciones específicas basadas en posiciones de los dedos y gestos asociados.
    """

    # "Yo": Índice apuntando hacia el pecho, otros dedos cerrados
    if dedos == [0, 1, 0, 0, 0]:  # Solo el índice levantado
        # Verificar que el índice apunta hacia el pecho (por ejemplo, landmark[8] cerca del cuerpo)
        return "Yo"

    # "Tú": Índice apuntando hacia adelante, otros dedos cerrados
    if dedos == [0, 1, 0, 0, 0]:  # Solo el índice levantado
        # Verificar que el índice apunta hacia adelante
        # Puedes añadir lógica adicional de orientación aquí si es necesario
        return "Tú"

    # "Usted": Mano extendida hacia adelante (como un saludo formal)
    if dedos == [1, 1, 1, 1, 1]:  # Mano abierta (todos los dedos levantados)
        # Verificar que la mano está orientada hacia adelante
        return "Usted"

    # Si no se detecta ninguna acción conocida
    return "Acción desconocida"

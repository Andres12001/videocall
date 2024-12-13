def detectar_palabra(dedos, hand_landmarks, mano_izquierda=None, mano_derecha=None):
    """
    Detecta palabras en Lengua de Señas Chilena (LSCh) basadas en posiciones de los dedos,
    relaciones espaciales entre manos y ubicación en el espacio.
    """

    # "Hola": Mano abierta, todos los dedos levantados
    if dedos == [1, 1, 1, 1, 1]:  # Mano abierta (todos los dedos levantados)
        return "Hola"

    # "Cómo estás": Ambas manos extendidas, una sobre otra
    if mano_izquierda and mano_derecha:
        palma_superior = mano_izquierda.landmark[9].y < mano_derecha.landmark[9].y
        palma_inferior = mano_izquierda.landmark[9].y > mano_derecha.landmark[9].y
        if palma_superior or palma_inferior:
            return "Cómo estás"

    # "Bien": Pulgar hacia arriba, otros dedos cerrados
    if dedos == [1, 0, 0, 0, 0]:  # Solo el pulgar levantado
        pulgar_hacia_arriba = hand_landmarks[4].y < hand_landmarks[3].y  # Y del pulgar menor que la base
        if pulgar_hacia_arriba:
            return "Bien"

    # "Mal": Ambas manos con los pulgares hacia abajo
    if mano_izquierda and mano_derecha:
        # Verificar que ambas manos tienen el pulgar hacia abajo
        pulgar_izq_hacia_abajo = (
            mano_izquierda.landmark[4].y > mano_izquierda.landmark[3].y  # Pulgar izquierdo hacia abajo
        )
        pulgar_der_hacia_abajo = (
            mano_derecha.landmark[4].y > mano_derecha.landmark[3].y  # Pulgar derecho hacia abajo
        )

        if pulgar_izq_hacia_abajo and pulgar_der_hacia_abajo:
            return "Mal"

    # "Más o Menos": Mano extendida hacia adelante, en la esquina inferior derecha
    if dedos == [1, 1, 1, 1, 1]:  # Mano abierta
        # Verificar orientación hacia adelante
        palma_hacia_adelante = (
            hand_landmarks[0].z > -0.2  # Profundidad de la muñeca indica que la mano está frente a la cámara
        )

        # Verificar que la mano esté en la esquina inferior derecha
        posicion_inferior_derecha = (
            hand_landmarks[0].x > 0.7 and  # Coordenada X está en la derecha (70% de la anchura)
            hand_landmarks[0].y > 0.7      # Coordenada Y está en la parte inferior (70% de la altura)
        )

        if palma_hacia_adelante and posicion_inferior_derecha:
            return "Más o Menos"

    # Si el gesto no coincide con ningún patrón conocido
    return "Palabra desconocida"

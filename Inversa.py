def ingresar_matriz():
    # Esta función permite al usuario ingresar una matriz cuadrada.
    filas = int(input("Ingrese el número de filas y columnas (la matriz debe ser cuadrada): "))
    matriz = []
    # Se solicitan los elementos de la matriz fila por fila
    print("Ingrese los elementos de la matriz fila por fila, separados por espacios:")
    for i in range(filas):
        # Cada fila se convierte en una lista de números flotantes
        fila = list(map(float, input(f"Fila {i + 1}: ").split()))
        matriz.append(fila)
    return matriz

def mostrar_matriz_con_linea(matriz_extendida, n):
    # Esta función imprime la matriz aumentada con una línea de separación.
    for fila in matriz_extendida:
        # Parte izquierda de la matriz (original)
        original = " ".join(f"{x:.1f}" for x in fila[:n])
        # Parte derecha de la matriz (identidad)
        identidad = " ".join(f"{x:.1f}" for x in fila[n:])
        # Se imprime la matriz con una barra vertical separando ambas partes
        print(f"[ {original} | {identidad} ]")

def matriz_identidad(tamano):
    # Crea una matriz identidad del tamaño especificado.
    identidad = [[1 if i == j else 0 for j in range(tamano)] for i in range(tamano)]
    return identidad

def inversa_gauss_jordan(matriz):
    # Función principal para calcular la inversa usando el método de Gauss-Jordan.
    
    n = len(matriz)  # Número de filas y columnas de la matriz.
    identidad = matriz_identidad(n)  # Creamos la matriz identidad del mismo tamaño.
    
    # Combinamos la matriz original con la identidad para formar la matriz aumentada.
    matriz_extendida = [fila + identidad[i] for i, fila in enumerate(matriz)]
    
    print("\nMatriz aumentada inicial:")
    mostrar_matriz_con_linea(matriz_extendida, n)  # Mostramos la matriz aumentada.

    # Aplicamos el método Gauss-Jordan para convertir la parte izquierda en la matriz identidad.
    for i in range(n):
        # Si el pivote es 0, se intercambian filas para evitar problemas en los cálculos.
        if matriz_extendida[i][i] == 0:
            for j in range(i+1, n):
                if matriz_extendida[j][i] != 0:
                    # Intercambio de filas
                    matriz_extendida[i], matriz_extendida[j] = matriz_extendida[j], matriz_extendida[i]
                    print(f"\nIntercambio de filas {i+1} y {j+1}:")
                    mostrar_matriz_con_linea(matriz_extendida, n)
                    break
            else:
                # Si no se puede intercambiar, la matriz es singular y no tiene inversa.
                print("\nLa matriz es singular y no tiene inversa.")
                return None

        # Normalizamos la fila dividiendo cada elemento de la fila por el pivote
        pivote = matriz_extendida[i][i]
        print(f"\nDividiendo la fila {i+1} por el pivote {pivote:.1f}:")
        for j in range(2 * n):
            matriz_extendida[i][j] /= pivote
        mostrar_matriz_con_linea(matriz_extendida, n)

        # Hacemos ceros en las demás posiciones de la columna actual
        for j in range(n):
            if i != j:
                factor = matriz_extendida[j][i]
                # Restamos un múltiplo de la fila actual para hacer ceros en la columna.
                print(f"\nRestando {factor:.1f} veces la fila {i+1} de la fila {j+1}:")
                for k in range(2 * n):
                    matriz_extendida[j][k] -= factor * matriz_extendida[i][k]
                mostrar_matriz_con_linea(matriz_extendida, n)
    
    # Extraemos la parte derecha de la matriz aumentada (que ahora es la inversa)
    inversa = [fila[n:] for fila in matriz_extendida]
    return inversa

def main():
    # Función principal que controla el flujo del programa.
    print("Bienvenido al programa para calcular la inversa de una matriz usando el método de Gauss-Jordan")
    matriz = ingresar_matriz()  # El usuario ingresa la matriz.

    print("\nMatriz ingresada:")
    # Mostramos la matriz original con la identidad pegada a la derecha.
    mostrar_matriz_con_linea([fila + matriz_identidad(len(matriz))[i] for i, fila in enumerate(matriz)], len(matriz))

    # Calculamos la inversa usando el método de Gauss-Jordan.
    inversa = inversa_gauss_jordan(matriz)

    # Si la inversa existe, la mostramos.
    if inversa:
        print("\nLa inversa de la matriz es:")
        mostrar_matriz_con_linea(inversa, len(inversa))

if __name__ == "__main__":
    main()

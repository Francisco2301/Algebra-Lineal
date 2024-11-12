import math
import sympy as sp

# Definimos el símbolo 'x' para uso en SymPy
x = sp.symbols('x')

# Solicitamos al usuario la función y la convertimos en una expresión simbólica
funcion_input = input("Ingrese la función f(x): ")

# Reemplazamos '^' por '**' para manejar potencias
funcion_input = funcion_input.replace('^', '**')

# Intentamos convertir la función ingresada a una expresión simbólica
try:
    funcion_expr = sp.sympify(funcion_input)
except Exception as e:
    print(f"Error al interpretar la función: {e}")
    exit()

# Preguntamos al usuario si desea ingresar la derivada o calcularla automáticamente
opcion = input("¿Desea ingresar la derivada manualmente? (s/n): ").lower()

if opcion == 's':
    derivada_input = input("Ingrese la derivada f'(x): ")
    # Reemplazamos '^' por '**' en la derivada ingresada
    derivada_input = derivada_input.replace('^', '**')
    # Intentamos convertir la derivada ingresada a una expresión simbólica
    try:
        derivada_expr = sp.sympify(derivada_input)
    except Exception as e:
        print(f"Error al interpretar la derivada: {e}")
        exit()
else:
    # Calculamos la derivada utilizando SymPy
    derivada_expr = sp.diff(funcion_expr, x)
    print(f"La derivada calculada es: f'(x) = {derivada_expr}")

# Solicitamos al usuario el valor inicial, tolerancia y número máximo de iteraciones
try:
    x0 = float(input("Ingrese el valor inicial x0: "))
    tolerancia = float(input("Ingrese la tolerancia (ejemplo: 0.0001): "))
    iter_max = int(input("Ingrese el número máximo de iteraciones: "))
except ValueError:
    print("Error: Por favor, ingrese valores numéricos válidos.")
    exit()

# Creamos funciones numéricas evaluables a partir de las expresiones simbólicas
funcion_num = sp.lambdify(x, funcion_expr, modules=['math'])
derivada_num = sp.lambdify(x, derivada_expr, modules=['math'])

# Implementamos el método de Newton-Raphson
print("\nIteración\t x_n\t\t f(x_n)\t\t f'(x_n)\t Error")

for iteracion in range(1, iter_max + 1):
    # Evaluamos la función y su derivada en el valor actual de x
    try:
        fx = funcion_num(x0)
        fpx = derivada_num(x0)
    except Exception as e:
        print(f"Error al evaluar las funciones en x = {x0}: {e}")
        exit()

    # Verificamos que la derivada no sea cero
    if fpx == 0:
        print(f"La derivada es cero en x = {x0}. El método no puede continuar.")
        break

    # Calculamos el nuevo valor de x usando la fórmula de Newton-Raphson
    x1 = x0 - fx / fpx

    # Calculamos el error absoluto
    error = abs(x1 - x0)

    # Mostramos los resultados de la iteración actual
    print(f"{iteracion}\t\t {x1:.6f}\t {fx:.6f}\t {fpx:.6f}\t {error:.6f}")

    # Verificamos si el error es menor que la tolerancia
    if error < tolerancia:
        print(f"\nLa raíz aproximada es: {x1:.6f}")
        break

    # Actualizamos x0 para la siguiente iteración
    x0 = x1
else:
    print("\nEl método no convergió en las iteraciones dadas.")

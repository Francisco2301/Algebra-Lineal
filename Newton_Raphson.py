import math
import sympy as sp
import matplotlib.pyplot as plt

# Definimos el símbolo 'x' para uso en SymPy
x = sp.symbols('x')

# Función para corregir la función ingresada por el usuario
def corregir_funcion(funcion):
    # Reemplazamos 'sen' por 'sin' en caso de que el usuario lo escriba en español
    funcion = funcion.replace('sen', 'sin')
    # Reemplazamos '^' por '**' para manejar potencias
    funcion = funcion.replace('^', '**')
    return funcion

# Solicitamos al usuario la función y la corregimos
funcion_input = input("Ingrese la función f(x): ")
funcion_input = corregir_funcion(funcion_input)

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
    derivada_input = corregir_funcion(derivada_input)
    try:
        derivada_expr = sp.sympify(derivada_input)
    except Exception as e:
        print(f"Error al interpretar la derivada: {e}")
        exit()
else:
    # Calculamos la derivada utilizando SymPy
    derivada_expr = sp.diff(funcion_expr, x)
    print(f"La derivada calculada es: f'(x) = {derivada_expr}")

# Solicitamos al usuario el número de raíces que desea encontrar
try:
    num_raices = int(input("¿Cuántas raíces desea encontrar?: "))
    if num_raices <= 0:
        print("El número de raíces debe ser mayor que cero.")
        exit()
except ValueError:
    print("Error: Por favor, ingrese un número entero válido.")
    exit()

# Solicitamos los valores iniciales para cada raíz
valores_iniciales = []
for i in range(num_raices):
    try:
        x0 = float(input(f"Ingrese el valor inicial x0 para la raíz {i+1}: "))
        valores_iniciales.append(x0)
    except ValueError:
        print("Error: Por favor, ingrese un valor numérico válido.")
        exit()

# Solicitamos la tolerancia y el número máximo de iteraciones
try:
    tolerancia = float(input("Ingrese la tolerancia (ejemplo: 0.0001): "))
    iter_max = int(input("Ingrese el número máximo de iteraciones: "))
except ValueError:
    print("Error: Por favor, ingrese valores numéricos válidos.")
    exit()

# Creamos funciones numéricas evaluables a partir de las expresiones simbólicas
funcion_num = sp.lambdify(x, funcion_expr, modules=['math'])
derivada_num = sp.lambdify(x, derivada_expr, modules=['math'])

# Lista para almacenar las raíces encontradas
raices_encontradas = []

# Implementamos el método de Newton-Raphson para cada valor inicial
for idx, x0 in enumerate(valores_iniciales):
    print(f"\n*** Buscando la raíz {idx+1} a partir de x0 = {x0} ***")
    print("Iteración\t x_n\t\t f(x_n)\t\t f'(x_n)\t Error")
    for iteracion in range(1, iter_max + 1):
        # Evaluamos la función y su derivada en el valor actual de x
        try:
            fx = funcion_num(x0)
            fpx = derivada_num(x0)
        except Exception as e:
            print(f"Error al evaluar las funciones en x = {x0}: {e}")
            break  # Salimos del bucle si hay un error en la evaluación

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
            # Evaluamos la función en la raíz encontrada para verificar qué tan cerca está de cero
            f_raiz = funcion_num(x1)
            print(f"\nLa raíz aproximada es: {x1:.6f}")
            print(f"f(raíz) = {f_raiz:.6e}")
            raices_encontradas.append(x1)
            break

        # Actualizamos x0 para la siguiente iteración
        x0 = x1
    else:
        print("\nEl método no convergió en las iteraciones dadas.")

# Rutina de graficación
# Definimos el rango de x para la gráfica
print("\n--- Graficando la función ---")
try:
    x_min = float(input("Ingrese el valor mínimo de x para la gráfica: "))
    x_max = float(input("Ingrese el valor máximo de x para la gráfica: "))
    if x_min >= x_max:
        print("Error: x_min debe ser menor que x_max.")
        exit()
except ValueError:
    print("Error: Por favor, ingrese valores numéricos válidos.")
    exit()

# Generamos valores de x para la gráfica
paso = (x_max - x_min) / 1000  # Definimos un número de puntos para una buena resolución
x_vals = [x_min + i * paso for i in range(1001)]
y_vals = []

# Calculamos los valores de y correspondientes
for xi in x_vals:
    try:
        yi = funcion_num(xi)
        y_vals.append(yi)
    except Exception:
        # En caso de error (por ejemplo, división por cero), asignamos None
        y_vals.append(None)

# Graficamos la función
plt.figure(figsize=(10, 6))
plt.plot(x_vals, y_vals, label='f(x)')
plt.axhline(0, color='black', linewidth=0.5)

# Marcamos las raíces encontradas en la gráfica
for raiz in raices_encontradas:
    plt.plot(raiz, 0, 'ro', label=f'Raíz {raiz:.6f}')

plt.title('Gráfica de la función y raíces encontradas')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.legend()
plt.grid(True)
plt.show()

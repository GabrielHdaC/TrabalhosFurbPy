import math
import matplotlib.pyplot as plt
import numpy as np
import sys

# Entrada de dados
a = float(input("Digite o coeficiente a: "))
b = float(input("Digite o coeficiente b: "))
c = float(input("Digite o coeficiente c: "))

print(f"\nFunção: f(x) = {a}x² + {b}x + {c}")

# Caso especial: todos zero
if a == 0 and b == 0 and c == 0:
    print("\nFunção indefinida: f(x) = 0")
    print("→ Toda reta é o eixo x, logo existem infinitas raízes.")
    sys.exit()

# Caso de função linear (a == 0, mas b ≠ 0)
if a == 0 and b != 0:
    print("\nEssa não é uma função quadrática, é linear: f(x) = bx + c")
    # Raiz: -c/b
    raiz = -c / b
    print(f"Raiz única: x = {raiz}")
    print(f"Interseção com eixo y: f(0) = {c}")

    # Gráfico da reta
    x = np.linspace(-10, 10, 400)
    y = b*x + c
    plt.axhline(0, color="black", linewidth=1)
    plt.axvline(0, color="black", linewidth=1)
    plt.plot(x, y, label="f(x) = bx + c")
    plt.scatter(raiz, 0, color="green", label="Raiz")
    plt.title("Função Linear")
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.legend()
    plt.grid()
    plt.show()
    sys.exit()

# Caso de função constante (a == 0, b == 0, c ≠ 0)
if a == 0 and b == 0 and c != 0:
    print(f"\nEssa é uma função constante: f(x) = {c}")
    print("→ Não possui raízes reais (linha paralela ao eixo x).")

    # Gráfico da constante
    x = np.linspace(-10, 10, 400)
    y = np.full_like(x, c)
    plt.axhline(0, color="black", linewidth=1)
    plt.axvline(0, color="black", linewidth=1)
    plt.plot(x, y, label="f(x) = c")
    plt.title("Função Constante")
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.legend()
    plt.grid()
    plt.show()
    sys.exit()

# Caso normal: função quadrática
print("\nFunção quadrática válida!")

# Discriminante
delta = b**2 - 4*a*c
print(f"Discriminante (Δ): {delta}")

# Raízes
raizes = []
if delta < 0:
    print("Não existem raízes reais.")
elif delta == 0:
    x = -b / (2*a)
    print(f"Raiz única: x = {x}")
    raizes = [x]
else:
    x1 = (-b + math.sqrt(delta)) / (2*a)
    x2 = (-b - math.sqrt(delta)) / (2*a)
    print(f"Duas raízes reais: x1 = {x1}, x2 = {x2}")
    raizes = [x1, x2]

# Vértice
xv = -b / (2*a)
yv = a*xv**2 + b*xv + c
tipo = "mínimo" if a > 0 else "máximo"
print(f"Vértice: ({xv}, {yv}) → ponto de {tipo}")

# Interseção com eixo y
print(f"Interseção com eixo y: f(0) = {c}")

# Gráfico da parábola
x = np.linspace(xv-10, xv+10, 400)
y = a*x**2 + b*x + c

plt.axhline(0, color="black", linewidth=1)
plt.axvline(0, color="black", linewidth=1)

plt.plot(x, y, label="f(x)")
plt.scatter(xv, yv, color="red", label="Vértice")
for r in raizes:
    plt.scatter(r, 0, color="green", label=f"Raiz {r:.2f}")

plt.title("Função Quadrática")
plt.xlabel("x")
plt.ylabel("f(x)")
plt.legend()
plt.grid()
plt.show()

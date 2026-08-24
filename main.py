import inventory

pistol = inventory.Pistol()
pistol.print()

nombre = input("Ingresa el nombre de tu personaje: ")

print()
print("Escoge tu estilo:")
print("1. Valiente")
print("2. Sigiloso")
print("3. Inteligente")
print("4. Agresivo")

opcion_juego = input("Elige uno: ")

if opcion_juego == "1":
    juego = "Valiente"
    habilidad_juego = "Hace 10 puntos más de daño."

elif opcion_juego == "2":
    juego = "Sigiloso"
    habilidad_juego = "Los zombis tardan más en detectarte."

elif opcion_juego == "3":
    juego = "Inteligente"
    habilidad_juego = "Encuentra más recursos."

elif opcion_juego == "4":
    juego = "Agresivo"
    habilidad_juego = "Hace más daño, pero gasta más munición."

else:
    juego = "Desconocido"
    habilidad_juego = "Sin habilidad."


print()
print("Escoge tu rol:")
print("1. Médico")
print("2. Militar")
print("3. Bombero")
print("4. Mecánico")

print()
print("Beneficios:")
print("Médico: Las medicinas curan un 50% más.")
print("Militar: Hace un 20% más de daño con armas de fuego.")
print("Bombero: Tiene más vida inicial y resiste mejor.")
print("Mecánico: Repara armas y consigue más munición.")

opcion_rol = input("Elige uno: ")

if opcion_rol == "1":
    rol = "Médico"
    habilidad_rol = "Las medicinas curan un 50% más."

elif opcion_rol == "2":
    rol = "Militar"
    habilidad_rol = "Hace un 20% más de daño con armas de fuego."

elif opcion_rol == "3":
    rol = "Bombero"
    habilidad_rol = "Tiene más vida inicial y resiste mejor."

elif opcion_rol == "4":
    rol = "Mecánico"
    habilidad_rol = "Repara armas y consigue más munición."

else:
    rol = "Desconocido"
    habilidad_rol = "Sin habilidad."


print()
print("Escoge tu origen:")
print("1. México")
print("2. Canadá")
print("3. España")
print("4. Rusia")

opcion_origen = input("Opción tu origen: ")

if opcion_origen == "1":
    origen = "México"

elif opcion_origen == "2":
    origen = "Canadá"

elif opcion_origen == "3":
    origen = "España"

elif opcion_origen == "4":
    origen = "Rusia"

else:
    origen = "Desconocido"


print()
print("Escoge tu inventario:")

inventario = [
    {"name": "Pistola", "bullets": 20, "damage": 15, "price": 100, "sale": 40},
    {"name": "Botiquín", "hp_recovery": 10, "price": 50, "sale": 20},
    {"name": "Munición para armas pequeñas", "amount": 30, "price": 30, "sale": 15},
    {"name": "Vendas", "amount": 5, "price": 20, "sale": 10},
    {"name": "Rifle", "bullets": 10, "damage": 25, "price": 200, "sale": 80},
    {"name": "Cuchillo cuerpo a cuerpo", "damage": 10, "price": 50, "sale": 20},
    {"name": "Pala", "damage": 8, "price": 30, "sale": 10},
    {"name": "Escopeta", "bullets": 5, "damage": 35, "price": 300, "sale": 120},
    {"name": "Munición para armas pesadas", "amount": 15, "price": 50, "sale": 25},
]


coins = 100

print()
print("Monedas:", coins)


print()
print("Escoge 3 elementos para tu inventario:")
print()

inventario_seleccionado = []


for i, objeto in enumerate(inventario):
    print(f"{i + 1}. {objeto['name']}")


while len(inventario_seleccionado) < 3:
    opcion_inventario = input("Elige un objeto (1-9): ")

    if opcion_inventario.isdigit() and 1 <= int(opcion_inventario) <= len(inventario):
        objeto_seleccionado = inventario[int(opcion_inventario) - 1]

        if objeto_seleccionado not in inventario_seleccionado:
            inventario_seleccionado.append(objeto_seleccionado)

            print(f"{objeto_seleccionado['name']} agregado a tu inventario.")

        else:
            print("Ya has seleccionado este objeto. Elige otro.")

    else:
        print("Opción inválida. Por favor, elige un número del 1 al 9.")


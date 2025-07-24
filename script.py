import requests
from datetime import datetime

API_MESAS = "http://127.0.0.1:5000/mesas"
API_RESERVAS = "http://127.0.0.1:5000/reservas"
RESTAURANTE_ID = 5
FECHA_RESERVA = datetime.now().strftime('%Y-%m-%d')

try:
    res = requests.get(API_MESAS)
    res.raise_for_status()
    mesas_data = res.json()

    mesas_restaurante = [
        m['id'] for m in mesas_data
        if m['restaurante_id'] == RESTAURANTE_ID
    ]

    if not mesas_restaurante:
        print(f"❌ No se encontraron mesas para el restaurante ID {RESTAURANTE_ID}")
        exit()

except Exception as e:
    print(f"❌ Error al obtener mesas: {e}")
    exit()

clientes = list(range(1, 17))

for i, cliente_id in enumerate(clientes):
    mesa_id = mesas_restaurante[i % len(mesas_restaurante)]

    reserva = {
        "cliente_id": cliente_id,
        "restaurante_id": RESTAURANTE_ID,
        "mesa_id": mesa_id,
        "fecha": FECHA_RESERVA,
        "comentarios": f"Reserva generada para cliente {cliente_id}",
        "estado": "confirmada"
    }

    try:
        res = requests.post(API_RESERVAS, json=reserva)
        data = res.json()

        if res.status_code == 201:
            print(f"{i+1}. Cliente {cliente_id} - Mesa {mesa_id} -> Reserva creada")
        else:
            print(f"{i+1}. Cliente {cliente_id} - Mesa {mesa_id} -> Error {res.status_code}: {data.get('error', 'Error desconocido')}")

    except Exception as e:
        print(f"{i+1}. Cliente {cliente_id} - Mesa {mesa_id} -> Excepción: {e}")

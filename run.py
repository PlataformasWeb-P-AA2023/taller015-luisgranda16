import pandas as pd
import requests

propietarios = pd.read_csv('data/propietarios.csv', delimiter='|')
print(propietarios)

for index, row in propietarios.iterrows():
    cedula = row['cedula']
    nombre = row['nombre']
    apellido = row['apellido']
    
    data = {
        'cedula': cedula,
        'nombre': nombre,
        'apellido': apellido
    }
    
    r = requests.post('http://127.0.0.1:8000/propietarios/', data=data, auth=('lucho', '1234'))
    
    if r.status_code == 201:
        print(f"Propietario '{nombre} {apellido}' creado exitosamente.")
    else:
        print(f"Error al crear el propietario '{nombre} {apellido}'. Error {r.status_code}: {r.text}")


edificios = pd.read_csv('data/edificios.csv', delimiter='|')
print(edificios)

for index, row in edificios.iterrows():
    nombre = row['nombre']
    direccion = row['dirección']
    ciudad = row['ciudad']
    tipo = row['tipo']

    data = {
        'nombre': nombre,
        'direccion': direccion,
        'ciudad': ciudad,
        'tipo': tipo
    }
    
    r = requests.post('http://127.0.0.1:8000/edificios/', data=data, auth=('lucho', '1234'))
    
    if r.status_code == 201:
        print(f"Edificio '{nombre}' creado exitosamente.")
    else:
        print(f"Error al crear el propietario '{nombre} {apellido}'. Error {r.status_code}: {r.text}")


departamentos = pd.read_csv('data/departamentos.csv', delimiter='|')
print(departamentos)

def obtener_id_propietario(cedula_propietario):
    url = f'http://127.0.0.1:8000/propietarios/?cedula={cedula_propietario}'
    r = requests.get(url, auth=('lucho', '1234'))
    print(r)
    if r.status_code == 200:
        propietarios = r.json()
        print(propietarios)
        for p in propietarios:
            if p['cedula'] == cedula_propietario:
                return p['id']
    return None

def obtener_id_edificio(nombre_edificio):
    url = f'http://127.0.0.1:8000/edificios/?nombre={nombre_edificio}'
    r = requests.get(url, auth=('lucho', '1234'))
    if r.status_code == 200:
        edificios = r.json()
        for e in edificios:
            if e['nombre'] == nombre_edificio:
                return e['id']
    return None

for index, row in departamentos.iterrows():
    cedula_propietario = row['Propietario']
    costo = row['Costo']
    num_cuartos = row['Cuartos']
    nombre_edificio = row['Edificio']

    propietario_id = obtener_id_propietario(cedula_propietario)
    print(propietario_id)
    edificio_id = obtener_id_edificio(nombre_edificio)
    print(edificio_id)

    if propietario_id is None:
        print(f"El propietario con cédula '{cedula_propietario}' no existe.")
        continue

    if edificio_id is None:
        print(f"El edificio '{nombre_edificio}' no existe.")
        continue

    data = {
        'propietario': propietario_id,
        'costo': costo,
        'num_cuartos': num_cuartos,
        'edificio': edificio_id
    }

    r = requests.post('http://127.0.0.1:8000/departamentos/', data=data, auth=('lucho', '1234'))

    if r.status_code == 201:
        print(f"Departamento del propietario'{cedula_propietario}' creado.")
    else:
        print(f"Error al crear el departamento'{cedula_propietario}'. Error {r.status_code}: {r.text}")
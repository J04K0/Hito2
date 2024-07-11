import requests
from pymongo import MongoClient

# Conexión a MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client.pokedex
collection = db.pokemon

# Crear índices para evitar duplicados y mejorar el rendimiento
collection.create_index("id", unique=True)
collection.create_index("name")

# Diccionario de generaciones y sus respectivos nombres y rangos de IDs
generations = {
    "Generation I": range(1, 152),   
    "Generation II": range(152, 200),  
}

# Función para obtener datos detallados de cada Pokémon
def get_pokemon_data(pokemon_url):
    response = requests.get(pokemon_url)
    if response.status_code == 200:
        data = response.json()
        return {
            "id": data['id'],
            "name": data['name'],
            "generation": "",
            "stats": {stat['stat']['name']: stat['base_stat'] for stat in data['stats']},
            "types": [t['type']['name'] for t in data['types']]
        }
    return None

# Extraer y almacenar datos en MongoDB con generación incluida
def import_all_pokemon(max_pokemon=200):
    count = 0
    for gen_name, ids in generations.items():
        for pokemon_id in ids:
            if count >= max_pokemon:
                break
            url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_id}'
            pokemon_data = get_pokemon_data(url)
            if pokemon_data:
                pokemon_data['generation'] = gen_name
                try:
                    collection.insert_one(pokemon_data)
                    count += 1
                    print(f"Inserted {pokemon_data['name']} from {gen_name}")
                except Exception as e:
                    print(f"Failed to insert {pokemon_data['name']}: {e}")
        if count >= max_pokemon:
            break

# Ejecutar la importación de todos los Pokémon
import_all_pokemon()
print("Datos de los Pokémon almacenados en MongoDB.")

import requests
from pymongo import MongoClient

# Conexión a MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client.pokedex
collection = db.pokemon

# Función para obtener la lista de tipos de Pokémon desde la API de PokeAPI
def get_type_effectiveness():
    url = "https://pokeapi.co/api/v2/type/"
    response = requests.get(url)
    if response.status_code == 200:
        types_data = response.json()
        return types_data['results']
    return []

# Función para obtener la efectividad de un tipo atacante contra un tipo defensor
def get_effectiveness(attacking_type, defending_type):
    url = f"https://pokeapi.co/api/v2/type/{attacking_type}/"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        effectiveness = {
            "super_effective": [t['name'] for t in data['damage_relations']['double_damage_to']],
            "not_very_effective": [t['name'] for t in data['damage_relations']['half_damage_to']],
            "ineffective": [t['name'] for t in data['damage_relations']['no_damage_to']]
        }
        if defending_type in effectiveness['super_effective']:
            return f"{attacking_type.capitalize()} es muy efectivo contra {defending_type.capitalize()}."
        elif defending_type in effectiveness['not_very_effective']:
            return f"{attacking_type.capitalize()} no es muy efectivo contra {defending_type.capitalize()}."
        elif defending_type in effectiveness['ineffective']:
            return f"{attacking_type.capitalize()} no tiene efecto contra {defending_type.capitalize()}."
        else:
            return f"{attacking_type.capitalize()} tiene efectividad normal contra {defending_type.capitalize()}."
    return "Error al obtener la efectividad del tipo."

# Función para comparar la efectividad de todos los tipos de Pokémon
def compare_types():
    attacking_types = collection.distinct("types")
    defending_types = collection.distinct("types")
    
    effectiveness_results = []
    
    for attacking_type in attacking_types:
        for defending_type in defending_types:
            if attacking_type != defending_type:
                effectiveness = get_effectiveness(attacking_type, defending_type)
                effectiveness_results.append((attacking_type, defending_type, effectiveness))
    
    return effectiveness_results

if __name__ == "__main__":
    # Solicitar al usuario los tipos de Pokémon para la consulta de efectividad
    attacking_type = input("Ingrese el tipo de Pokémon atacante: ").strip().lower()
    defending_type = input("Ingrese el tipo de Pokémon defensor: ").strip().lower()
    effectiveness = get_effectiveness(attacking_type, defending_type)
    print(f"\nEficacia de {attacking_type.capitalize()} contra {defending_type.capitalize()}:")
    print(effectiveness)
    
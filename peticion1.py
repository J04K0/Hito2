from pymongo import MongoClient

# Conexión a MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client.pokedex
collection = db.pokemon

def get_pokemon_by_generation(generation_name):
    # Realizar la consulta a la base de datos
    pokemons = collection.find({"generation": generation_name}, {"_id": 0, "name": 1, "generation": 1})
    
    # Convertir el resultado a una lista y retornar
    return list(pokemons)

if __name__ == "__main__":
    # Ejemplo de uso
    generation = "Generation II"
    pokemons = get_pokemon_by_generation(generation)
    for pokemon in pokemons:
        print(pokemon)

from pymongo import MongoClient

# Conexión a MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client.pokedex
collection = db.pokemon

def get_average_stats_by_type(pokemon_type):
    # Realizar la consulta a la base de datos para obtener Pokémon de un tipo específico
    pokemons = collection.find({"types": pokemon_type}, {"_id": 0, "stats": 1})
    
    # Inicializar acumuladores para las estadísticas
    total_stats = {}
    count = 0
    
    # Sumar las estadísticas de cada Pokémon
    for pokemon in pokemons:
        count += 1
        for stat_name, stat_value in pokemon['stats'].items():
            if stat_name not in total_stats:
                total_stats[stat_name] = 0
            total_stats[stat_name] += stat_value
    
    # Calcular los promedios
    if count > 0:
        average_stats = {stat_name: total / count for stat_name, total in total_stats.items()}
    else:
        average_stats = {}
    
    return average_stats

if __name__ == "__main__":    
    # Solicitar al usuario el tipo de Pokémon para la consulta de estadísticas promedio
    pokemon_type = input("\nIngrese el tipo de Pokémon para calcular las estadísticas promedio: ").strip().lower()
    average_stats = get_average_stats_by_type(pokemon_type)
    print(f"\nEstadísticas promedio para el tipo {pokemon_type}:")
    for stat_name, avg_value in average_stats.items():
        print(f"{stat_name}: {avg_value}")

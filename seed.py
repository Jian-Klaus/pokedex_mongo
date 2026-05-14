import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def seed_db():
    uri = "mongodb://127.0.0.1:27017"
    client = AsyncIOMotorClient(uri)
    db = client.pokedex_db
    collection = db.pokemons
    
    pokemons_data = [
        {
            "pokedex_id": 1,
            "name": "Bulbasaur",
            "region": "Kanto",
            "evolution_info": {
                "stage": "1º Estágio",
                "has_mega": False,
                "pre_evolution": None,
                "next_evolution": {"name": "Ivysaur", "pokedex_id": 2, "method": "Level 16"}
            },
            "types": ["Grass", "Poison"],
            "measurements": {"height": 0.7, "weight": 6.9},
            "base_stats": {"hp": 45, "attack": 49, "defense": 49, "special_attack": 65, "special_defense": 65, "speed": 45},
            "abilities": [{"name": "Overgrow", "is_hidden": False}, {"name": "Chlorophyll", "is_hidden": True}],
            "assets": {
                "sprites": {
                    "male": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/1.png",
                    "female": None,
                    "mega": None
                },
                "cry_url": "https://raw.githubusercontent.com/PokeAPI/cries/main/cries/pokemon/latest/1.ogg",
                "footprint_url": None
            },
            "moves_summary": [{"name": "Tackle", "level": 1, "move_id": "m_normal_01"}, {"name": "Vine Whip", "level": 9, "move_id": "m_grass_01"}]
        },
        {
            # Adicionado Charizard para testar a mecânica de Mega Evolução
            "pokedex_id": 6,
            "name": "Charizard",
            "region": "Kanto",
            "evolution_info": {
                "stage": "3º Estágio",
                "has_mega": True, # A flag que ativa o botão MEGA no React
                "pre_evolution": {"name": "Charmeleon", "pokedex_id": 5, "method": "Level 36"},
                "next_evolution": None
            },
            "types": ["Fire", "Flying"],
            "measurements": {"height": 1.7, "weight": 90.5},
            "base_stats": {"hp": 78, "attack": 84, "defense": 78, "special_attack": 109, "special_defense": 85, "speed": 100},
            "abilities": [{"name": "Blaze", "is_hidden": False}, {"name": "Solar Power", "is_hidden": True}],
            "assets": {
                "sprites": {
                    "male": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/6.png",
                    "female": None,
                    # URL oficial do Mega Charizard X
                    "mega": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/10034.png"
                },
                "cry_url": "https://raw.githubusercontent.com/PokeAPI/cries/main/cries/pokemon/latest/6.ogg",
                "footprint_url": None
            },
            "moves_summary": [{"name": "Flamethrower", "level": 30, "move_id": "m_fire_03"}, {"name": "Dragon Claw", "level": 36, "move_id": "m_dragon_01"}]
        },
        {
            "pokedex_id": 7,
            "name": "Squirtle",
            "region": "Kanto",
            "evolution_info": {
                "stage": "1º Estágio",
                "has_mega": False,
                "pre_evolution": None,
                "next_evolution": {"name": "Wartortle", "pokedex_id": 8, "method": "Level 16"}
            },
            "types": ["Water"],
            "measurements": {"height": 0.5, "weight": 9.0},
            "base_stats": {"hp": 44, "attack": 48, "defense": 65, "special_attack": 50, "special_defense": 64, "speed": 43},
            "abilities": [{"name": "Torrent", "is_hidden": False}, {"name": "Rain Dish", "is_hidden": True}],
            "assets": {
                "sprites": {
                    "male": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/7.png",
                    "female": None,
                    "mega": None
                },
                "cry_url": "https://raw.githubusercontent.com/PokeAPI/cries/main/cries/pokemon/latest/7.ogg",
                "footprint_url": None
            },
            "moves_summary": [{"name": "Tackle", "level": 1, "move_id": "m_normal_01"}, {"name": "Water Gun", "level": 3, "move_id": "m_water_01"}]
        },
        {
            "pokedex_id": 25,
            "name": "Pikachu",
            "region": "Kanto",
            "evolution_info": {
                "stage": "2º Estágio",
                "has_mega": False,
                "pre_evolution": {"name": "Pichu", "pokedex_id": 172, "method": "Felicidade Alta"},
                "next_evolution": {"name": "Raichu", "pokedex_id": 26, "method": "Thunder Stone"}
            },
            "types": ["Electric"],
            "measurements": {"height": 0.4, "weight": 6.0},
            "base_stats": {"hp": 35, "attack": 55, "defense": 40, "special_attack": 50, "special_defense": 50, "speed": 90},
            "abilities": [{"name": "Static", "is_hidden": False}, {"name": "Lightning Rod", "is_hidden": True}],
            "assets": {
                "sprites": {
                    # Utilizando os modelos 3D do Pokémon HOME que possuem diferença de gênero
                    "male": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/home/25.png",
                    "female": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/home/female/25.png",
                    "mega": None
                },
                "cry_url": "https://raw.githubusercontent.com/PokeAPI/cries/main/cries/pokemon/latest/25.ogg",
                "footprint_url": None
            },
            "moves_summary": [{"name": "Thunder Shock", "level": 1, "move_id": "m_electric_01"}, {"name": "Quick Attack", "level": 10, "move_id": "m_normal_05"}]
        }
    ]

    try:
        await collection.delete_many({})
        await collection.create_index("pokedex_id", unique=True)
        result = await collection.insert_many(pokemons_data)
        print(f"Sucesso! {len(result.inserted_ids)} Pokémons inseridos no banco.")
    except Exception as e:
        print(f"Erro ao popular o banco: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(seed_db())
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient

app = FastAPI()

# Configuração de CORS para o Vite (React) não ser bloqueado
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Conexão com o MongoDB usando a rede host validada
uri = "mongodb+srv://klaus:11bx1371@pokedex.s1okeyp.mongodb.net/?appName=Pokedex"
client = AsyncIOMotorClient(uri)
db = client.pokedex_db
collection = db.pokemons

@app.get("/pokemons")
async def get_all_pokemons():
    pokemons = []
    # Busca e ordena pelo Pokedex ID
    cursor = collection.find({}).sort("pokedex_id", 1)
    async for doc in cursor:
        doc["_id"] = str(doc["_id"]) # Converte o ObjectId do Mongo para String
        pokemons.append(doc)
    return pokemons

@app.get("/pokemons/{pokedex_id}")
async def get_pokemon_by_id(pokedex_id: int):
    pokemon = await collection.find_one({"pokedex_id": pokedex_id})
    if pokemon:
        pokemon["_id"] = str(pokemon["_id"])
        return pokemon
    raise HTTPException(status_code=404, detail="Pokémon não encontrado")
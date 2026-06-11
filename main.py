from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

class Trainer(BaseModel):
    name: str
    birth_date: str
    favorite_type: str
    favorite_pokemon: str  # Vamos guardar o nome do Pokémon aqui
    favorite_region: str
    profile_picture: Optional[str] = ""  # Base64 da imagem. Opcional para não quebrar se não tiver foto.

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

# 1. CREATE (Criar Treinador)
@app.post("/trainer")
async def create_trainer(trainer: Trainer):
    # Por ser um app pessoal, deletamos qualquer treinador antigo para manter apenas 1
    await db.trainers.delete_many({})
    
    # Inserimos o novo treinador na nova collection 'trainers'
    new_trainer = await db.trainers.insert_one(trainer.dict())
    return {"message": "Treinador criado com sucesso!", "id": str(new_trainer.inserted_id)}

# 2. READ (Buscar Treinador)
@app.get("/trainer")
async def get_trainer():
    # Busca o único treinador que existe no banco
    trainer = await db.trainers.find_one({})
    if trainer:
        trainer["_id"] = str(trainer["_id"]) # Converte o ObjectId do Mongo para texto
        return trainer
    
    # Se não achar ninguém, retorna um aviso (o Frontend vai usar isso para mostrar o botão "Novo Treinador")
    return {"message": "Nenhum treinador encontrado"}

# 3. UPDATE (Atualizar Treinador)
@app.put("/trainer")
async def update_trainer(trainer: Trainer):
    # Substitui os dados do treinador existente pelos dados novos
    result = await db.trainers.update_one({}, {"$set": trainer.dict()})
    if result.modified_count == 1:
        return {"message": "Cartão de Treinador atualizado com sucesso!"}
    return {"message": "Nenhuma alteração foi feita."}

# 4. DELETE (Deletar Treinador)
@app.delete("/trainer")
async def delete_trainer():
    # Limpa a collection
    await db.trainers.delete_many({})
    return {"message": "Registro de Treinador apagado! Aventura resetada."}
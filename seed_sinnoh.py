import asyncio
import httpx
from motor.motor_asyncio import AsyncIOMotorClient

sem = asyncio.Semaphore(15)

# 1. Regras de Evolução
EVO_OVERRIDES = {
    "Vileplume": "Leaf Stone", "Bellossom": "Sun Stone", "Poliwrath": "Water Stone", "Politoed": "Troca c/ King's Rock",
    "Slowbro": "Level 37", "Slowking": "Troca c/ King's Rock", "Magnezone": "Thunder Stone", "Steelix": "Troca c/ Metal Coat",
    "Lickilicky": "Aprender Rollout", "Rhyperior": "Troca c/ Protector", "Chansey": "Oval Stone", "Tangrowth": "Aprender AncientPower",
    "Kingdra": "Troca c/ Dragon Scale", "Electivire": "Troca c/ Electirizer", "Magmortar": "Troca c/ Magmarizer",
    "Vaporeon": "Water Stone", "Jolteon": "Thunder Stone", "Flareon": "Fire Stone", "Espeon": "Felicidade (Dia)",
    "Umbreon": "Felicidade (Noite)", "Leafeon": "Leaf Stone", "Glaceon": "Ice Stone", "Sylveon": "Felicidade + Fairy Move",
    "Sudowoodo": "Aprender Mimic", "Ambipom": "Aprender Double Hit", "Yanmega": "Aprender AncientPower", "Farigiraf": "Aprender Twin Beam",
    "Dudunsparce": "Aprender Hyper Drill", "Gliscor": "Razor Fang (Noite)", "Weavile": "Razor Claw (Noite)", "Sneasler": "Razor Claw (Dia)",
    "Mamoswine": "Aprender AncientPower", "Mantine": "Upar c/ Remoraid", "Porygon2": "Troca c/ Upgrade", "Porygon-z": "Troca c/ Dubious Disc",
    "Hitmonlee": "Ataque > Defesa", "Hitmonchan": "Defesa > Ataque", "Hitmontop": "Ataque = Defesa", "Gallade": "Dawn Stone (Macho)",
    "Ninjask": "Level 20", "Shedinja": "Espaço Vago na Party", "Probopass": "Thunder Stone", "Roselia": "Felicidade (Dia)",
    "Milotic": "Troca c/ Prism Scale", "Dusknoir": "Troca c/ Reaper Cloth", "Chimecho": "Felicidade (Noite)", 
    "Huntail": "Troca c/ Deep Sea Tooth", "Gorebyss": "Troca c/ Deep Sea Scale", "Vespiquen": "Level 21 (Fêmea)", 
    "Froslass": "Dawn Stone (Fêmea)", "Mothim": "Level 20 (Macho)", "Wormadam": "Level 20 (Fêmea)",
    "Kleavor": "Black Augurite"
}

# Bloqueios
BLOCKED_EVOS = ["Clodsire", "Overqwil", "Cursola", "Wyrdeer", "Manaphy", "Phione"]

# 2. DICIONÁRIO DE FORMAS EXATAS 
FORMS_DICT = {
    # Megas Kanto
    3: [{"name": "Mega", "query": "venusaur-mega"}],
    6: [{"name": "Mega X", "query": "charizard-mega-x"}, {"name": "Mega Y", "query": "charizard-mega-y"}],
    9: [{"name": "Mega", "query": "blastoise-mega"}],
    15: [{"name": "Mega", "query": "beedrill-mega"}],
    18: [{"name": "Mega", "query": "pidgeot-mega"}],
    65: [{"name": "Mega", "query": "alakazam-mega"}],
    80: [{"name": "Mega", "query": "slowbro-mega"}],
    94: [{"name": "Mega", "query": "gengar-mega"}],
    115: [{"name": "Mega", "query": "kangaskhan-mega"}],
    127: [{"name": "Mega", "query": "pinsir-mega"}],
    130: [{"name": "Mega", "query": "gyarados-mega"}],
    142: [{"name": "Mega", "query": "aerodactyl-mega"}],
    150: [{"name": "Mega X", "query": "mewtwo-mega-x"}, {"name": "Mega Y", "query": "mewtwo-mega-y"}],
    
    # Megas Johto
    181: [{"name": "Mega", "query": "ampharos-mega"}],
    208: [{"name": "Mega", "query": "steelix-mega"}],
    212: [{"name": "Mega", "query": "scizor-mega"}],
    214: [{"name": "Mega", "query": "heracross-mega"}],
    229: [{"name": "Mega", "query": "houndoom-mega"}],
    248: [{"name": "Mega", "query": "tyranitar-mega"}],

    # Megas Hoenn & Primais
    254: [{"name": "Mega", "query": "sceptile-mega"}],
    257: [{"name": "Mega", "query": "blaziken-mega"}],
    260: [{"name": "Mega", "query": "swampert-mega"}],
    282: [{"name": "Mega", "query": "gardevoir-mega"}],
    302: [{"name": "Mega", "query": "sableye-mega"}],
    303: [{"name": "Mega", "query": "mawile-mega"}],
    306: [{"name": "Mega", "query": "aggron-mega"}],
    308: [{"name": "Mega", "query": "medicham-mega"}],
    310: [{"name": "Mega", "query": "manectric-mega"}],
    319: [{"name": "Mega", "query": "sharpedo-mega"}],
    323: [{"name": "Mega", "query": "camerupt-mega"}],
    334: [{"name": "Mega", "query": "altaria-mega"}],
    354: [{"name": "Mega", "query": "banette-mega"}],
    359: [{"name": "Mega", "query": "absol-mega"}],
    362: [{"name": "Mega", "query": "glalie-mega"}],
    373: [{"name": "Mega", "query": "salamence-mega"}],
    376: [{"name": "Mega", "query": "metagross-mega"}],
    380: [{"name": "Mega", "query": "latias-mega"}],
    381: [{"name": "Mega", "query": "latios-mega"}],
    382: [{"name": "Primal", "query": "kyogre-primal"}],
    383: [{"name": "Primal", "query": "groudon-primal"}],
    384: [{"name": "Mega", "query": "rayquaza-mega"}],
    386: [{"name": "Attack", "query": "deoxys-attack"}, {"name": "Defense", "query": "deoxys-defense"}, {"name": "Speed", "query": "deoxys-speed"}],

    # Sinnoh Megas & Formas Variadas (Wormadam, Rotom, etc)
    413: [{"name": "Sandy Cloak", "query": "wormadam-sandy"}, {"name": "Trash Cloak", "query": "wormadam-trash"}],
    421: [{"name": "Sunshine", "query": "cherrim-sunshine"}],
    422: [{"name": "East Sea", "query": "shellos-east"}],
    423: [{"name": "East Sea", "query": "gastrodon-east"}],
    428: [{"name": "Mega", "query": "lopunny-mega"}],
    445: [{"name": "Mega", "query": "garchomp-mega"}],
    448: [{"name": "Mega", "query": "lucario-mega"}],
    460: [{"name": "Mega", "query": "abomasnow-mega"}],
    475: [{"name": "Mega", "query": "gallade-mega"}],
    479: [{"name": "Heat", "query": "rotom-heat"}, {"name": "Wash", "query": "rotom-wash"}, {"name": "Frost", "query": "rotom-frost"}, {"name": "Fan", "query": "rotom-fan"}, {"name": "Mow", "query": "rotom-mow"}],
    483: [{"name": "Origin", "query": "dialga-origin"}],
    484: [{"name": "Origin", "query": "palkia-origin"}],
    487: [{"name": "Origin", "query": "giratina-origin"}],
    492: [{"name": "Sky", "query": "shaymin-sky"}],
    
    # Adicionando o Galarian Mr. Mime como forma para aparecer no modal
    122: [{"name": "Galarian", "query": "mr-mime-galar"}]
}

def get_evo_method(next_name, details):
    if next_name in EVO_OVERRIDES: return EVO_OVERRIDES[next_name]
    if not details: return "Básico"
    d = details[0]
    trigger = d.get("trigger", {}).get("name", "")
    if trigger == "level-up":
        lvl = d.get("min_level")
        return f"Level {lvl}" if lvl else "Felicidade"
    elif trigger == "use-item":
        return d.get("item", {}).get("name", "").replace("-", " ").title()
    elif trigger == "trade": return "Troca"
    return "Evolução"

def parse_chain(chain, target_name, pre_name=None, pre_method=None):
    current_name = chain['species']['name'].capitalize()
    
    if current_name.lower() == target_name.lower():
        next_evos = []
        for next_node in chain.get('evolves_to', []):
            next_name = next_node['species']['name'].capitalize()
            if next_name in BLOCKED_EVOS or (current_name == "Phione" and next_name == "Manaphy"): 
                continue
            next_method = get_evo_method(next_name, next_node.get('evolution_details', []))
            next_evos.append({"name": next_name, "method": next_method})
        
        pre_evo = {"name": pre_name, "method": pre_method} if pre_name else None
        return pre_evo, next_evos

    for next_chain in chain.get('evolves_to', []):
        next_name = next_chain['species']['name'].capitalize()
        method_to_next = get_evo_method(next_name, next_chain.get('evolution_details', []))
        res_pre, res_next = parse_chain(next_chain, target_name, current_name, method_to_next)
        if res_pre is not None or res_next: return res_pre, res_next
            
    return None, []

async def get_pokemon_data(client, pokedex_id):
    async with sem:
        try:
            resp = await client.get(f"https://pokeapi.co/api/v2/pokemon/{pokedex_id}")
            data = resp.json()
            
            species_resp = await client.get(f"https://pokeapi.co/api/v2/pokemon-species/{pokedex_id}")
            species_data = species_resp.json()
            
            chain_resp = await client.get(species_data["evolution_chain"]["url"])
            chain_data = chain_resp.json()

            # REGRA MESTRA: Interceptação do Mime Jr. e Mr. Mime
            if data["name"] == "farfetchd" or data["name"] == "phione" or data["name"] == "manaphy": 
                pre_evo, next_evos = None, []
            elif data["name"] == "mime-jr":
                pre_evo = None
                next_evos = [
                    {"name": "Mr. Mime", "method": "Aprender Mimic"},
                    {"name": "Galarian Mr. Mime", "method": "Aprender Mimic (Galar)"}
                ]
            elif data["name"] == "mr-mime":
                pre_evo = {"name": "Mime Jr.", "method": "Aprender Mimic"}
                next_evos = []
            else: 
                pre_evo, next_evos = parse_chain(chain_data["chain"], data["name"])

            # BUSCA DINÂMICA DE FORMAS E TIPOS BASEADO NA 'QUERY'
            alternate_forms = []
            if pokedex_id in FORMS_DICT:
                for form in FORMS_DICT[pokedex_id]:
                    try:
                        f_resp = await client.get(f"https://pokeapi.co/api/v2/pokemon/{form['query']}")
                        if f_resp.status_code == 200:
                            f_data = f_resp.json()
                            sprite_url = f_data['sprites']['other']['official-artwork']['front_default'] or f_data['sprites']['front_default']
                            types = [t["type"]["name"].capitalize() for t in f_data["types"]]
                            alternate_forms.append({"name": form['name'], "sprite": sprite_url, "types": types})
                    except Exception as e:
                        pass # Falha silenciosa para não travar o banco

            raw_name = data["name"].title()
            # Limpeza de sufixos de banco de dados
            clean_name = raw_name.replace("-Normal", "").replace("-Altered", "").replace("-Plant", "").replace("-Land", "")
            # Ajustes manuais para manter a hifenização oficial
            if clean_name == "Mr-Mime": clean_name = "Mr. Mime"
            elif clean_name == "Mime-Jr": clean_name = "Mime Jr."
            elif clean_name == "Ho-Oh": clean_name = "Ho-Oh"
            elif clean_name == "Porygon-Z": clean_name = "Porygon-Z"

            pokemon = {
                "pokedex_id": data["id"],
                "name": clean_name, # Usando o nome limpo!
                "region": "Sinnoh" if pokedex_id > 386 else "Hoenn" if pokedex_id > 251 else "Johto" if pokedex_id > 151 else "Kanto",
                "region": "Sinnoh" if pokedex_id > 386 else "Hoenn" if pokedex_id > 251 else "Johto" if pokedex_id > 151 else "Kanto",
                "types": [t["type"]["name"].capitalize() for t in data["types"]],
                "measurements": {"height": data["height"] / 10, "weight": data["weight"] / 10},
                "base_stats": {s["stat"]["name"].replace("-", "_"): s["base_stat"] for s in data["stats"]},
                "abilities": [{"name": a["ability"]["name"].capitalize(), "is_hidden": a["is_hidden"]} for a in data["abilities"]],
                "evolution_info": {"stage": "Evoluído" if pre_evo else "Básico", "has_mega": pokedex_id in FORMS_DICT, "pre_evolution": pre_evo, "next_evolutions": next_evos},
                "assets": {
                    "sprites": {"male": data["sprites"]["other"]["official-artwork"]["front_default"], "female": data["sprites"]["other"]["home"]["front_female"]},
                    "cry_url": f"https://raw.githubusercontent.com/PokeAPI/cries/main/cries/pokemon/latest/{data['id']}.ogg"
                },
                "moves_summary": [{"name": m["move"]["name"].capitalize(), "level": 1} for m in data["moves"][:6]],
                "alternate_forms": alternate_forms
            }
            print(f"[{pokedex_id}/493] {pokemon['name']} perfeitamente mapeado.")
            return pokemon

        except Exception as e:
            print(f"Erro no Pokemon {pokedex_id}: {e}")
            return None

async def main():
    uri = "mongodb+srv://klaus:11bx1371@pokedex.s1okeyp.mongodb.net/?appName=Pokedex"
    mongo_client = AsyncIOMotorClient(uri)
    db = mongo_client.pokedex_db
    collection = db.pokemons
    
    await collection.delete_many({})
    async with httpx.AsyncClient(timeout=60.0) as http_client:
        tasks = [get_pokemon_data(http_client, i) for i in range(1, 494)]
        all_pokemons = await asyncio.gather(*tasks)
        valid_pokemons = [p for p in all_pokemons if p is not None]
        await collection.insert_many(valid_pokemons)
        print(f"BINGO! {len(valid_pokemons)} Pokémons salvos com suas formas exatas e lore purista.")

if __name__ == "__main__":
    asyncio.run(main())
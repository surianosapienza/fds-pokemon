pokemon_types = {
    "bulbasaur": ["GRASS", "POISON"],
    "ivysaur": ["GRASS", "POISON"],
    "venusaur": ["GRASS", "POISON"],
    "charmander": ["FIRE"],
    "charmeleon": ["FIRE"],
    "charizard": ["FIRE", "FLYING"],
    "squirtle": ["WATER"],
    "wartortle": ["WATER"],
    "blastoise": ["WATER"],
    "caterpie": ["BUG"],
    "metapod": ["BUG"],
    "butterfree": ["BUG", "FLYING"],
    "weedle": ["BUG", "POISON"],
    "kakuna": ["BUG", "POISON"],
    "beedrill": ["BUG", "POISON"],
    "pidgey": ["NORMAL", "FLYING"],
    "pidgeotto": ["NORMAL", "FLYING"],
    "pidgeot": ["NORMAL", "FLYING"],
    "rattata": ["NORMAL"],
    "raticate": ["NORMAL"],
    "spearow": ["NORMAL", "FLYING"],
    "fearow": ["NORMAL", "FLYING"],
    "ekans": ["POISON"],
    "arbok": ["POISON"],
    "pikachu": ["ELECTRIC"],
    "raichu": ["ELECTRIC"],
    "sandshrew": ["GROUND"],
    "sandslash": ["GROUND"],
    "nidoran♀": ["POISON"],
    "nidorina": ["POISON"],
    "nidoqueen": ["POISON", "GROUND"],
    "nidoran♂": ["POISON"],
    "nidorino": ["POISON"],
    "nidoking": ["POISON", "GROUND"],
    "clefairy": ["NORMAL"],   # in Gen 1 Fairy non esisteva
    "clefable": ["NORMAL"],
    "vulpix": ["FIRE"],
    "ninetales": ["FIRE"],
    "jigglypuff": ["NORMAL"],
    "wigglytuff": ["NORMAL"],
    "zubat": ["POISON", "FLYING"],
    "golbat": ["POISON", "FLYING"],
    "oddish": ["GRASS", "POISON"],
    "gloom": ["GRASS", "POISON"],
    "vileplume": ["GRASS", "POISON"],
    "paras": ["BUG", "GRASS"],
    "parasect": ["BUG", "GRASS"],
    "venonat": ["BUG", "POISON"],
    "venomoth": ["BUG", "POISON"],
    "diglett": ["GROUND"],
    "dugtrio": ["GROUND"],
    "meowth": ["NORMAL"],
    "persian": ["NORMAL"],
    "psyduck": ["WATER"],
    "golduck": ["WATER"],
    "mankey": ["FIGHTING"],
    "primeape": ["FIGHTING"],
    "growlithe": ["FIRE"],
    "arcanine": ["FIRE"],
    "poliwag": ["WATER"],
    "poliwhirl": ["WATER"],
    "poliwrath": ["WATER", "FIGHTING"],
    "abra": ["PSYCHIC"],
    "kadabra": ["PSYCHIC"],
    "alakazam": ["PSYCHIC"],
    "machop": ["FIGHTING"],
    "machoke": ["FIGHTING"],
    "machamp": ["FIGHTING"],
    "bellsprout": ["GRASS", "POISON"],
    "weepinbell": ["GRASS", "POISON"],
    "victreebel": ["GRASS", "POISON"],
    "tentacool": ["WATER", "POISON"],
    "tentacruel": ["WATER", "POISON"],
    "geodude": ["ROCK", "GROUND"],
    "graveler": ["ROCK", "GROUND"],
    "golem": ["ROCK", "GROUND"],
    "ponyta": ["FIRE"],
    "rapidash": ["FIRE"],
    "slowpoke": ["WATER", "PSYCHIC"],
    "slowbro": ["WATER", "PSYCHIC"],
    "magnemite": ["ELECTRIC"],
    "magneton": ["ELECTRIC"],
    "farfetchd": ["NORMAL", "FLYING"],
    "doduo": ["NORMAL", "FLYING"],
    "dodrio": ["NORMAL", "FLYING"],
    "seel": ["WATER"],
    "dewgong": ["WATER", "ICE"],
    "grimer": ["POISON"],
    "muk": ["POISON"],
    "shellder": ["WATER"],
    "cloyster": ["WATER", "ICE"],
    "gastly": ["GHOST", "POISON"],
    "haunter": ["GHOST", "POISON"],
    "gengar": ["GHOST", "POISON"],
    "onix": ["ROCK", "GROUND"],
    "drowzee": ["PSYCHIC"],
    "hypno": ["PSYCHIC"],
    "krabby": ["WATER"],
    "kingler": ["WATER"],
    "voltorb": ["ELECTRIC"],
    "electrode": ["ELECTRIC"],
    "exeggcute": ["GRASS", "PSYCHIC"],
    "exeggutor": ["GRASS", "PSYCHIC"],
    "cubone": ["GROUND"],
    "marowak": ["GROUND"],
    "hitmonlee": ["FIGHTING"],
    "hitmonchan": ["FIGHTING"],
    "lickitung": ["NORMAL"],
    "koffing": ["POISON"],
    "weezing": ["POISON"],
    "rhyhorn": ["GROUND", "ROCK"],
    "rhydon": ["GROUND", "ROCK"],
    "chansey": ["NORMAL"],
    "tangela": ["GRASS"],
    "kangaskhan": ["NORMAL"],
    "horsea": ["WATER"],
    "seadra": ["WATER"],
    "goldeen": ["WATER"],
    "seaking": ["WATER"],
    "staryu": ["WATER"],
    "starmie": ["WATER", "PSYCHIC"],
    "mr.mime": ["PSYCHIC"],
    "scyther": ["BUG", "FLYING"],
    "jynx": ["ICE", "PSYCHIC"],
    "electabuzz": ["ELECTRIC"],
    "magmar": ["FIRE"],
    "pinsir": ["BUG"],
    "tauros": ["NORMAL"],
    "magikarp": ["WATER"],
    "gyarados": ["WATER", "FLYING"],
    "lapras": ["WATER", "ICE"],
    "ditto": ["NORMAL"],
    "eevee": ["NORMAL"],
    "vaporeon": ["WATER"],
    "jolteon": ["ELECTRIC"],
    "flareon": ["FIRE"],
    "porygon": ["NORMAL"],
    "omanyte": ["ROCK", "WATER"],
    "omastar": ["ROCK", "WATER"],
    "kabuto": ["ROCK", "WATER"],
    "kabutops": ["ROCK", "WATER"],
    "aerodactyl": ["ROCK", "FLYING"],
    "snorlax": ["NORMAL"],
    "articuno": ["ICE", "FLYING"],
    "zapdos": ["ELECTRIC", "FLYING"],
    "moltres": ["FIRE", "FLYING"],
    "dratini": ["DRAGON"],
    "dragonair": ["DRAGON"],
    "dragonite": ["DRAGON", "FLYING"],
    "mewtwo": ["PSYCHIC"],
    "mew": ["PSYCHIC"]
    }

supereffective_type = {
    "NORMAL": [],
    "FIRE": ["GRASS", "ICE", "BUG"],
    "WATER": ["FIRE", "GROUND", "ROCK"],
    "ELECTRIC": ["WATER", "FLYING"],
    "GRASS": ["WATER", "GROUND", "ROCK"],
    "ICE": ["GRASS", "GROUND", "FLYING", "DRAGON"],
    "FIGHTING": ["NORMAL", "ICE", "ROCK"],
    "POISON": ["GRASS"],
    "GROUND": ["FIRE", "ELECTRIC", "POISON", "ROCK"],
    "FLYING": ["GRASS", "FIGHTING", "BUG"],
    "PSYCHIC": ["FIGHTING", "POISON"],
    "BUG": ["GRASS", "PSYCHIC"],
    "ROCK": ["FIRE", "ICE", "FLYING", "BUG"],
    "GHOST": ["PSYCHIC", "GHOST"],
    "DRAGON": ["DRAGON"]
    }

notreallyeffective_type = {
    "NORMAL": ["ROCK"],
    "FIRE": ["FIRE", "WATER", "ROCK", "DRAGON"],
    "WATER": ["WATER", "GRASS", "DRAGON"],
    "ELECTRIC": ["ELECTRIC", "GRASS", "DRAGON"],
    "GRASS": ["FIRE", "GRASS", "POISON", "FLYING", "BUG", "DRAGON"],
    "ICE": ["FIRE", "WATER", "ICE"],
    "FIGHTING": ["POISON", "FLYING", "PSYCHIC", "BUG"],
    "POISON": ["POISON", "GROUND", "ROCK", "GHOST"],
    "GROUND": ["GRASS", "BUG"],
    "FLYING": ["ELECTRIC", "ROCK"],
    "PSYCHIC": ["PSYCHIC"],
    "BUG": ["FIRE", "FIGHTING", "POISON", "FLYING", "GHOST"],
    "ROCK": ["FIGHTING", "GROUND"],
    "GHOST": [],
    "DRAGON": []
}

noteffective_type = {
    "NORMAL": ["GHOST"],
    "FIRE": [],
    "WATER": [],
    "ELECTRIC": ["GROUND"],
    "GRASS": [],
    "ICE": [],
    "FIGHTING": ["GHOST"],
    "POISON": [],
    "GROUND": ["FLYING"],
    "FLYING": [],
    "PSYCHIC": [],
    "BUG": [],
    "ROCK": [],
    "GHOST": ["NORMAL"],
    "DRAGON": []
}

def pokemon_type(poke):
    # I associate at every pokemon its types   
    types=pokemon_types.get(poke.lower(),["UNKNOWN"])
    return types

def move_effectiveness(move_type, poke_types):
    """
    here we return the multiplier of effectivness (0; 0.5; 1; 2) of the move made on the pokemon
    """

    multiplier = 1
    for type in poke_types:
        if type in supereffective_type[move_type]:
            multiplier*=2
        elif type in notreallyeffective_type[move_type]:
            multiplier*=0.5
        elif type in noteffective_type[move_type]:
            multiplier*=0
    return int(round(multiplier))

def pkmn_effectiveness(pkmn1_type, pkmn2_type):
    multiplier = 1
    for type1 in pkmn1_type:
        for type2 in pkmn2_type:
            if type1 in supereffective_type[type2]:
                multiplier*=2
            elif type1 in notreallyeffective_type[type2]:
                multiplier*=0.5
    return True if multiplier >= 2 else False

def is_supereffective(move_type, poke_types):
    for type in poke_types:
        if type in supereffective_type[move_type]:
            return True
    return False
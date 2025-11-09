import numpy as np
import pandas as pd
import src.data_management as my_dm

all_types = ['dragon', 'electric', 'fire', 'flying', 'ghost', 'grass', 'ground', 'ice', 'normal', 'notype', 'poison', 'psychic', 'rock', 'water']


def p1_features(p1_team: list[dict]):
    features = {}
    #"""
    stats = ['base_hp', 'base_atk', 'base_def', 'base_spa', 'base_spd', 'base_spe']
    for stat in stats:               ### This helps the model to have a better idea abt the time instead of having only mean
        values = [p.get(stat, 0) for p in p1_team]
        features[f'p1_min_{stat}'] = np.min(values)
        features[f'p1_max_{stat}'] = np.max(values)
        features[f'p1_std_{stat}'] = np.std(values)
    p1_mean_atk = np.mean([np.max([p['base_atk'], p['base_spa']]) for p in p1_team])
    p1_mean_hp = np.mean([p.get('base_hp', 0) for p in p1_team])
    p1_mean_spe = np.mean([p.get('base_spe', 0) for p in p1_team])
    p1_mean_def = np.mean([np.mean([p['base_def'], p['base_spd']]) for p in p1_team])
    p1_mean_stats = np.mean([p1_mean_hp, p1_mean_spe, p1_mean_atk, p1_mean_def])
    features['p1_mean_atk'] = p1_mean_atk
    features['p1_mean_spe'] = p1_mean_spe
    features['p1_mean_def'] = p1_mean_def
    features['p1_mean_hp'] = p1_mean_hp
    features['p1_mean_stats'] = p1_mean_stats
    ### We can also build derivated feature like how much is off/def our team
    # team stats
    base_atk = np.mean([p.get('base_atk', 0) for p in p1_team])
    base_spa = np.mean([p.get('base_spa', 0) for p in p1_team])
    base_def = np.mean([p.get('base_def', 0) for p in p1_team])
    base_spd = np.mean([p.get('base_spd', 0) for p in p1_team])
    base_spe = np.mean([p.get('base_spe', 0) for p in p1_team])
    base_hp  = np.mean([p.get('base_hp', 0) for p in p1_team])
    ## constructing new features
    offense = base_atk + base_spa
    defense = base_def + base_spd
    features['p1_offense_mean']    = offense
    features['p1_defense_mean']    = defense
    features['p1_atk_def_ratio']   = p1_mean_atk / (p1_mean_def + 1e-6)
    # average per-Pokémon total base stats
    p1_totals = [sum(p.get(s, 0) for s in stats) for p in p1_team]
    features['p1_total_base_power'] = float(np.mean(p1_totals))
    features['p1_stat_variety']     = float(np.std(p1_totals))
    features['p1_style_index']      = offense / (offense + defense + 1e-6)
    features['p1_hp_ratio']         = base_hp / (offense + defense + base_spe + 1e-6)
    
    # fastest member speed 
    features['p1_max_speed'] = float(np.max([p.get('base_spe', 0) for p in p1_team]))

    """
    """
    type_counts = {t: 0 for t in all_types}
    for p in p1_team:
        for t in p.get('types', []):
            type_counts[t] += 1
    team_size = len(p1_team)
    for t in all_types:
        features[f'p1_type_{t}'] = type_counts[t] / team_size if team_size > 0 else 0
    return features

def p2_lead_features(p2_lead):
    features = {}
    # Player 2's lead Pokémon's stats
    features['p2_lead_hp'] = p2_lead.get('base_hp', 0)
    features['p2_lead_spe'] = p2_lead.get('base_spe', 0)
    features['p2_lead_atk'] = p2_lead.get('base_atk', 0)
    features['p2_lead_def'] = p2_lead.get('base_def', 0)
    features['p2_lead_spd'] = p2_lead.get('base_spd', 0)
    features['p2_lead_spa'] = p2_lead.get('base_spa', 0)
    ## types of p2 lead
    
    for t in all_types:
        features[f'p2_lead_type_{t}'] = 0.0
    for t in p2_lead.get('types', []):
        if t in all_types:
            features[f'p2_lead_type_{t}'] = 1.0
    return features

def status_features(timeline):
    features = {}
    total_statuses = ['slp', 'fnt', 'tox', 'psn', 'brn', 'frz', 'par', 'nostatus']
    dict_status_p1 = {status : 0 for status in total_statuses}
    dict_status_p2 = {status : 0 for status in total_statuses}
    for turn in timeline:
        if turn["p1_pokemon_state"].get("status"):
            turn_status = turn["p1_pokemon_state"].get("status")
            dict_status_p1[turn_status] += 1
        if turn["p2_pokemon_state"].get("status"):
            turn_status = turn["p2_pokemon_state"].get("status")
            dict_status_p2[turn_status] += 1
    
    for status in total_statuses:
        if status == 'nostatus':
            continue
        #features[f"p1_{status}_count"] = dict_status_p1.get(status, 0)
        #features[f"p2_{status}_count"] = dict_status_p2.get(status, 0)
        features[f"p1-p2_{status}_count"] = dict_status_p1.get(status, 0) - dict_status_p2.get(status, 0)
    # Single sum of all the status with their respect weight
    
    dict_status_p1["slp"] *= 0
    dict_status_p1["fnt"] *= 100
    dict_status_p1["tox"] *= 60
    dict_status_p1["psn"] *= 35
    dict_status_p1["brn"] *= 45
    dict_status_p1["frz"] *= 95
    dict_status_p1["par"] *= 40
    dict_status_p1["nostatus"] *= 0
    dict_status_p2["slp"] *= 0
    dict_status_p2["fnt"] *= 100
    dict_status_p2["tox"] *= 60
    dict_status_p2["psn"] *= 35
    dict_status_p2["brn"] *= 45
    dict_status_p2["frz"] *= 95
    dict_status_p2["par"] *= 40
    dict_status_p2["nostatus"] *= 0

    #features["p1_status_weighted_sum"] = sum([val for val in dict_status_p1.values()])
    #features["p2_status_weighted_sum"] = sum([val for val in dict_status_p2.values()])
    #features["p2-p1_status_difference"] = features["p2_status_weighted_sum"] - features["p1_status_weighted_sum"]
    p1_status_weighted_sum = sum([val for val in dict_status_p1.values()])
    p2_status_weighted_sum = sum([val for val in dict_status_p2.values()])
    features["p2-p1_status_difference"] = p2_status_weighted_sum - p1_status_weighted_sum
    
    ## fnt  features
    
    # Difference in fnt pkm
    #features["p1-p2_fnt_pokemon_number"] = dict_status_p1.get('fnt', 0) - dict_status_p2.get('fnt', 0)
    # fnt pkmn over total pokemon
    #features["p1_fnt_over_total_pkmn"] = features["p1_fnt_count"]/6
    #features["p2_fnt_over_total_pkmn"] = features["p2_fnt_count"]/6

    return features

def effect_features(timeline):
    features = {}
    total_effects = ['disable', 'firespin', 'confusion', 'substitute', 'wrap', 'clamp', 'typechange', 'reflect', 'noeffect']
    dict_effects_p1 = {effect : 0 for effect in total_effects}
    dict_effects_p2 = {effect : 0 for effect in total_effects}
    for turn in timeline:
        if turn["p1_pokemon_state"].get("effects"):
            turn_effects_p1 = turn["p1_pokemon_state"].get("effects")
            for effect in turn_effects_p1:
                dict_effects_p1[effect] += 1
        if turn["p2_pokemon_state"].get("effects"):
            turn_effects_p2 = turn["p2_pokemon_state"].get("effects")
            for effect in turn_effects_p2:
                dict_effects_p2[effect] += 1            
    for effect in total_effects:
        #features[f"p1_{effect}_count"] = dict_effects_p1.get(effect, 0)
        #features[f"p2_{effect}_count"] = dict_effects_p2.get(effect, 0)
        features[f"p1-p2_{effect}_count"] = dict_effects_p1.get(effect, 0) - dict_effects_p2.get(effect, 0) 
    
    return features


def battle_features(timeline):
    features = {}
    # Average HP percentage for both players
    p1_hp = [turn["p1_pokemon_state"].get("hp_pct", np.nan) for turn in timeline]
    p2_hp = [turn["p2_pokemon_state"].get("hp_pct", np.nan) for turn in timeline]
    #features["p1_mean_hp_pct"] = np.nanmean(p1_hp)
    #features["p2_mean_hp_pct"] = np.nanmean(p2_hp)
    features["p1-p2_mean_hp_pct"] = np.nanmean(p1_hp) - np.nanmean(p2_hp)
    #features["p1_final_hp"] = p1_hp[-1]
    #features["p2_final_hp"] = p2_hp[-1]
    #features["p1_total_damage"] = max(p1_hp) - min(p1_hp)
    #features["p2_total_damage"] = max(p2_hp) - min(p2_hp
    # Count probably critical moves
    
    p1_moves_used = [turn["p1_move_details"]["name"] for turn in timeline if turn.get("p1_move_details")]
    p2_moves_used = [turn["p2_move_details"]["name"] for turn in timeline if turn.get("p2_move_details")]
    high_crit = {"Crabhammer", "Karate Chop", "Razor Leaf", "Slash", "crabhammer", "karate chop", "razor leaf", "slash"}
    #features["p1_highcrit_moves_used"] = sum(m in high_crit for m in p1_moves_used)
    #features["p2_highcrit_moves_used"] = sum(m in high_crit for m in p2_moves_used)
    features["p1-p2_highcrit_moves_used"] = sum(m in high_crit for m in p1_moves_used) - sum(m in high_crit for m in p2_moves_used)
    # Count total moves used
    p1_moves = [turn.get("p1_move_details", {}).get("name") for turn in timeline if turn.get("p1_move_details")]
    p2_moves = [turn.get("p2_move_details", {}).get("name") for turn in timeline if turn.get("p2_move_details")]
    #features["p1_total_moves"] = len(p1_moves)
    #features["p2_total_moves"] = len(p2_moves)
    features["p1-p2_total_moves"] = len(p1_moves) - len(p2_moves)
    # Count unique move types used
    p1_move_types = [turn["p1_move_details"].get("type") for turn in timeline if turn.get("p1_move_details")]
    p2_move_types = [turn["p2_move_details"].get("type") for turn in timeline if turn.get("p2_move_details")]
    #features["p1_unique_move_types"] = len(set(p1_move_types))
    #features["p2_unique_move_types"] = len(set(p2_move_types))
    features["p1-p2_unique_move_types"] = len(set(p1_move_types)) - len(set(p2_move_types))
    #""
    p1_pkmns = set([turn["p1_pokemon_state"]["name"] for turn in timeline])
    p2_pkmns = set([turn["p2_pokemon_state"]["name"] for turn in timeline])
    ### status and effects features
    ## general status feature
    features.update(status_features(timeline))
    ## effects feature
    features.update(effect_features(timeline))
    ## Boosts (attack, defense, etc.)
    boost_keys = ["atk", "def", "spa", "spd", "spe"]
    for key in boost_keys:
        p1_boosts = [turn["p1_pokemon_state"]["boosts"].get(key, 0) for turn in timeline]
        p2_boosts = [turn["p2_pokemon_state"]["boosts"].get(key, 0) for turn in timeline]
        features[f"p1_mean_boost_{key}"] = np.mean(p1_boosts)
        features[f"p2_mean_boost_{key}"] = np.mean(p2_boosts)
    # Number of time the player switched pokemon
    features["p1_switch_number"] = sum([1 for turn in timeline if not turn.get("p1_move_details")])
    features["p2_switch_number"] = sum([1 for turn in timeline if not turn.get("p2_move_details")])
    # Number of SPECIAL or PHYSICAL moves and Number of STATUS moves of p1 and p2
    #features["p1_attack_moves"] = sum([1 for turn in timeline if turn.get("p1_move_details") and turn["p1_move_details"]["category"] in ["SPECIAL", "PHYSICAL"]])
    #features["p2_attack_moves"] = sum([1 for turn in timeline if turn.get("p2_move_details") and turn["p2_move_details"]["category"] in ["SPECIAL", "PHYSICAL"]])
    features["p1-p2_attack_moves"] = sum([1 for turn in timeline if turn.get("p1_move_details") and turn["p1_move_details"]["category"] in ["SPECIAL", "PHYSICAL"]]) - sum([1 for turn in timeline if turn.get("p2_move_details") and turn["p2_move_details"]["category"] in ["SPECIAL", "PHYSICAL"]])
    #features["p1_status_moves"] = sum([1 for turn in timeline if turn.get("p1_move_details") and turn["p1_move_details"]["category"] not in ["SPECIAL", "PHYSICAL"]])
    #features["p2_status_moves"] = sum([1 for turn in timeline if turn.get("p2_move_details") and turn["p2_move_details"]["category"] not in ["SPECIAL", "PHYSICAL"]])
    features["p1-p2_status_moves"] = sum([1 for turn in timeline if turn.get("p1_move_details") and turn["p1_move_details"]["category"] not in ["SPECIAL", "PHYSICAL"]]) - sum([1 for turn in timeline if turn.get("p2_move_details") and turn["p2_move_details"]["category"] not in ["SPECIAL", "PHYSICAL"]])
    # Average of base power value for SPECIAL or PHYSICAL moves of p1 and p2
    #features["p1_mean_base_power"] = np.nanmean([turn['p1_move_details']['base_power'] for turn in timeline if turn.get("p1_move_details") and turn["p1_move_details"]["category"] in ["SPECIAL", "PHYSICAL"]])
    #features["p2_mean_base_power"] = np.nanmean([turn['p2_move_details']['base_power'] for turn in timeline if turn.get("p2_move_details") and turn["p2_move_details"]["category"] in ["SPECIAL", "PHYSICAL"]])
    features["p1-p2_mean_base_power"] = np.nanmean([turn['p1_move_details']['base_power'] for turn in timeline if turn.get("p1_move_details") and turn["p1_move_details"]["category"] in ["SPECIAL", "PHYSICAL"]]) - np.nanmean([turn['p2_move_details']['base_power'] for turn in timeline if turn.get("p2_move_details") and turn["p2_move_details"]["category"] in ["SPECIAL", "PHYSICAL"]])
    
    # number of missed moves
    #features['p1_missed_moves_count'], features['p2_missed_moves_count'] = my_dm.missed_count_moves(timeline)
    p1_missed_moves_count, p2_missed_moves_count = my_dm.missed_count_moves(timeline)
    features['p1-p2_missed_moves_count'] = p1_missed_moves_count - p2_missed_moves_count
    
    # Number of same pokemon type moves (stab)
    #features["p1_same_type_moves_number"] = sum([1 for turn in timeline if turn.get("p1_move_details") and turn["p1_move_details"]["type"] in my_dm.pokemon_type(turn["p1_pokemon_state"]["name"]) and turn["p1_move_details"]["category"] in ["SPECIAL", "PHYSICAL"]])
    #features["p2_same_type_moves_number"] = sum([1 for turn in timeline if turn.get("p2_move_details") and turn["p2_move_details"]["type"] in my_dm.pokemon_type(turn["p2_pokemon_state"]["name"]) and turn["p2_move_details"]["category"] in ["SPECIAL", "PHYSICAL"]])
    features["p1-p2_same_type_moves_number"] = sum([1 for turn in timeline if turn.get("p1_move_details") and turn["p1_move_details"]["type"] in my_dm.pokemon_type(turn["p1_pokemon_state"]["name"]) and turn["p1_move_details"]["category"] in ["SPECIAL", "PHYSICAL"]]) - sum([1 for turn in timeline if turn.get("p2_move_details") and turn["p2_move_details"]["type"] in my_dm.pokemon_type(turn["p2_pokemon_state"]["name"]) and turn["p2_move_details"]["category"] in ["SPECIAL", "PHYSICAL"]])
    # Average of multiplier effectivness (stab included)
    #value = np.nanmean([my_dm.move_effectiveness(turn["p1_move_details"]["type"], turn["p2_pokemon_state"]["name"], turn["p1_move_details"]["type"] in my_dm.pokemon_type(turn["p1_pokemon_state"]["name"])) for turn in timeline if turn.get("p1_move_details") and turn["p1_move_details"]["category"] in ["SPECIAL", "PHYSICAL"]])
    #features["p1_effectivness_avg"] = 0 if np.isnan(value) else value
    #value = np.nanmean([my_dm.move_effectiveness(turn["p2_move_details"]["type"], turn["p1_pokemon_state"]["name"], turn["p2_move_details"]["type"] in my_dm.pokemon_type(turn["p2_pokemon_state"]["name"])) for turn in timeline if turn.get("p2_move_details") and turn["p2_move_details"]["category"] in ["SPECIAL", "PHYSICAL"]])
    #features["p2_effectivness_avg"] = 0 if np.isnan(value) else value
    value = np.nanmean([my_dm.move_effectiveness(turn["p1_move_details"]["type"], turn["p2_pokemon_state"]["name"], turn["p1_move_details"]["type"] in my_dm.pokemon_type(turn["p1_pokemon_state"]["name"])) for turn in timeline if turn.get("p1_move_details") and turn["p1_move_details"]["category"] in ["SPECIAL", "PHYSICAL"]])
    p1_effectivness_avg = 0 if np.isnan(value) else value
    value = np.nanmean([my_dm.move_effectiveness(turn["p2_move_details"]["type"], turn["p1_pokemon_state"]["name"], turn["p2_move_details"]["type"] in my_dm.pokemon_type(turn["p2_pokemon_state"]["name"])) for turn in timeline if turn.get("p2_move_details") and turn["p2_move_details"]["category"] in ["SPECIAL", "PHYSICAL"]])
    p2_effectivness_avg = 0 if np.isnan(value) else value
    features["p1-p2_effectivness_avg"] = p1_effectivness_avg - p2_effectivness_avg 
    # Number of supereffective moves
    #features["p1_supereffective_moves_count"] = sum([my_dm.is_supereffective(my_dm.move_effectiveness(turn["p1_move_details"]["type"], turn["p2_pokemon_state"]["name"])) for turn in timeline if turn.get("p1_move_details") and turn["p1_move_details"]["category"] in ["SPECIAL", "PHYSICAL"]])
    #features["p2_supereffective_moves_count"] = sum([my_dm.is_supereffective(my_dm.move_effectiveness(turn["p2_move_details"]["type"], turn["p1_pokemon_state"]["name"])) for turn in timeline if turn.get("p2_move_details") and turn["p2_move_details"]["category"] in ["SPECIAL", "PHYSICAL"]])
    features["p1-p2_supereffective_moves_count"] = sum([my_dm.is_supereffective(my_dm.move_effectiveness(turn["p1_move_details"]["type"], turn["p2_pokemon_state"]["name"])) for turn in timeline if turn.get("p1_move_details") and turn["p1_move_details"]["category"] in ["SPECIAL", "PHYSICAL"]]) - sum([my_dm.is_supereffective(my_dm.move_effectiveness(turn["p2_move_details"]["type"], turn["p1_pokemon_state"]["name"])) for turn in timeline if turn.get("p2_move_details") and turn["p2_move_details"]["category"] in ["SPECIAL", "PHYSICAL"]])

    # Sum of priority moves LOGICA SBAGLIATA
    #features["p1_priority_moves"] = sum([1 for turn in timeline if turn.get("p1_move_details") and turn["p1_move_details"].get("priority")])
    #features["p2_priority_moves"] = sum([1 for turn in timeline if turn.get("p2_move_details") and turn["p2_move_details"].get("priority")]
    # Number of supereffective pokemon of p1 in respect to p2
    #features["p1_supereffective_density"] = sum(1 for pkmn1 in p1_pkmns for pkmn2 in p2_pkmns if my_dm.is_supereffective(my_dm.pkmn_effectiveness(pkmn1, pkmn2)))/(len(p1_pkmns)*len(p2_pkmns))
    #features["p2_supereffective_density"] = sum(1 for pkmn1 in p1_pkmns for pkmn2 in p2_pkmns if my_dm.is_supereffective(my_dm.pkmn_effectiveness(pkmn2, pkmn1)))/(len(p1_pkmns)*len(p2_pkmns))
    #features["p1-p2_se_densities"] = features["p2_supereffective_density"] - features["p1_supereffective_density"]
    features["p1-p2_se_densities"] = sum(1 for pkmn1 in p1_pkmns for pkmn2 in p2_pkmns if my_dm.is_supereffective(my_dm.pkmn_effectiveness(pkmn1, pkmn2)))/(len(p1_pkmns)*len(p2_pkmns)) - sum(1 for pkmn1 in p1_pkmns for pkmn2 in p2_pkmns if my_dm.is_supereffective(my_dm.pkmn_effectiveness(pkmn2, pkmn1)))/(len(p1_pkmns)*len(p2_pkmns))
    # P1 pkmn having at least a supereffective target in p2 team
    features["p1_attackers_share"] = sum(any(my_dm.is_supereffective(my_dm.pkmn_effectiveness(pkmn1, pkmn2)) for pkmn2 in p2_pkmns) for pkmn1 in p1_pkmns) / 6
    # P1 pkmn that are target of at least one pkmn in team 2
    features["p1_defensive_share"] = sum(any(my_dm.is_supereffective(my_dm.pkmn_effectiveness(pkmn2, pkmn1)) for pkmn2 in p2_pkmns) for pkmn1 in p1_pkmns) / 6
    # mean of hp percentage for p1 team and p2 team on last informations
    p1_hp_pctg = {p1_pkmn : None for p1_pkmn in p1_pkmns}
    p2_hp_pctg = {p2_pkmn : None for p2_pkmn in p2_pkmns}
    for turn in timeline:
        p1_hp_pctg.update({turn["p1_pokemon_state"]["name"] : turn["p1_pokemon_state"]["hp_pct"]})
        p2_hp_pctg.update({turn["p2_pokemon_state"]["name"] : turn["p2_pokemon_state"]["hp_pct"]})
    
    #features["p1_remain_health_avg"] = (sum(p1_hp_pctg.values()) + 1*(6-len(p1_hp_pctg)))/6
    #features["p2_remain_health_avg"] = (sum(p2_hp_pctg.values()) + 1*(6-len(p2_hp_pctg)))/6
    #features["health_difference"] = features["p2_remain_health_avg"] - features["p1_remain_health_avg"]
    features["health_difference"] = (sum(p1_hp_pctg.values()) + 1*(6-len(p1_hp_pctg)))/6 - (sum(p2_hp_pctg.values()) + 1*(6-len(p2_hp_pctg)))/6
    return features

def create_features(data: list[dict]) -> pd.DataFrame:
    """
    Feature extraction function.
    """
    feature_list = []
    for battle in data:
        features = {}
        features["battle_id"] = battle.get("battle_id", -1)
        if battle.get('player_won') is not None:
            features['player_won'] = int(battle['player_won'])
        # --- Player 1 Team Features ---
        p1_team = battle.get('p1_team_details', [])
        if p1_team:
            features.update(p1_features(p1_team))
        # --- Player 2 Lead Features ---
        p2_lead = battle.get('p2_lead_details')
        if p2_lead:
            features.update(p2_lead_features(p2_lead))
        ## Extracting battle features
        timeline = battle.get("battle_timeline", [])
        if len(timeline) > 0:
            #"""
            features.update(battle_features(timeline))

        feature_list.append(features)
        
    return pd.DataFrame(feature_list).fillna(0)

def create_essentials_features(data):
    feature_list = []
    for battle in data:
        features = {}
        features["battle_id"] = battle.get("battle_id", -1)
        if battle.get('player_won') is not None:
            features['player_won'] = int(battle['player_won'])
        # --- Player 1 Team Features ---
        p1_team = battle.get('p1_team_details', [])
        if p1_team:
            stats = ['base_hp', 'base_atk', 'base_def', 'base_spa', 'base_spd', 'base_spe']
            for stat in stats:               ### This helps the model to have a better idea abt the time instead of having only mean
                values = [p.get(stat, 0) for p in p1_team]
            p1_mean_atk = np.mean([np.max([p['base_atk'], p['base_spa']]) for p in p1_team])
            p1_mean_hp = np.mean([p.get('base_hp', 0) for p in p1_team])
            p1_mean_spe = np.mean([p.get('base_spe', 0) for p in p1_team])
            p1_mean_def = np.mean([np.mean([p['base_def'], p['base_spd']]) for p in p1_team])
            p1_mean_stats = np.mean([p1_mean_hp, p1_mean_spe, p1_mean_atk, p1_mean_def])
            features['p1_mean_spe'] = p1_mean_spe
            features['p1_mean_stats'] = p1_mean_stats
            ### We can also build derivated feature like how much is off/def our team
            # team stats
            base_atk = np.mean([p.get('base_atk', 0) for p in p1_team])
            base_spa = np.mean([p.get('base_spa', 0) for p in p1_team])
            base_def = np.mean([p.get('base_def', 0) for p in p1_team])
            base_spd = np.mean([p.get('base_spd', 0) for p in p1_team])
            base_spe = np.mean([p.get('base_spe', 0) for p in p1_team])
            base_hp  = np.mean([p.get('base_hp', 0) for p in p1_team])
            ## constructing new features
            offense = base_atk + base_spa
            defense = base_def + base_spd
            features['p1_offense_mean']    = offense
            features['p1_defense_mean']    = defense
            features['p1_atk_def_ratio']   = p1_mean_atk / (p1_mean_def + 1e-6)
            # average per-Pokémon total base stats
            p1_totals = [sum(p.get(s, 0) for s in stats) for p in p1_team]
            features['p1_total_base_power'] = float(np.mean(p1_totals))

            # fastest member speed 
            features['p1_max_speed'] = float(np.max([p.get('base_spe', 0) for p in p1_team]))
        p2_lead = battle.get('p2_lead_details')
        if p2_lead:
            p2_lead_hp = p2_lead.get('base_hp', 0)
            p2_lead_spe = p2_lead.get('base_spe', 0)
            p2_lead_atk = p2_lead.get('base_atk', 0)
            p2_lead_def = p2_lead.get('base_def', 0)
            p2_lead_spd = p2_lead.get('base_spd', 0)
            p2_lead_spa = p2_lead.get('base_spa', 0)
            features['p2_lead_spe'] = p2_lead_spe
            features['p2_lead_mean_stats'] = np.mean([p2_lead_hp, p2_lead_spe, p2_lead_atk, p2_lead_def, p2_lead_spd, p2_lead_spa])

        timeline = battle.get("battle_timeline", [])
        if len(timeline) > 0:
            features.update(status_features(timeline))
            features["p1-p2_mean_base_power"] = np.nanmean([turn['p1_move_details']['base_power'] for turn in timeline if turn.get("p1_move_details") and turn["p1_move_details"]["category"] in ["SPECIAL", "PHYSICAL"]]) - np.nanmean([turn['p2_move_details']['base_power'] for turn in timeline if turn.get("p2_move_details") and turn["p2_move_details"]["category"] in ["SPECIAL", "PHYSICAL"]])
            p1_missed_moves_count, p2_missed_moves_count = my_dm.missed_count_moves(timeline)
            features['p1-p2_missed_moves_count'] = p1_missed_moves_count - p2_missed_moves_count
            p1_pkmns = set([turn["p1_pokemon_state"]["name"] for turn in timeline])
            p2_pkmns = set([turn["p2_pokemon_state"]["name"] for turn in timeline])
            p1_hp_pctg = {p1_pkmn : None for p1_pkmn in p1_pkmns}
            p2_hp_pctg = {p2_pkmn : None for p2_pkmn in p2_pkmns}
            for turn in timeline:
                p1_hp_pctg.update({turn["p1_pokemon_state"]["name"] : turn["p1_pokemon_state"]["hp_pct"]})
                p2_hp_pctg.update({turn["p2_pokemon_state"]["name"] : turn["p2_pokemon_state"]["hp_pct"]})

            #features["p1_remain_health_avg"] = (sum(p1_hp_pctg.values()) + 1*(6-len(p1_hp_pctg)))/6
            #features["p2_remain_health_avg"] = (sum(p2_hp_pctg.values()) + 1*(6-len(p2_hp_pctg)))/6
            #features["health_difference"] = features["p2_remain_health_avg"] - features["p1_remain_health_avg"]
            features["health_difference"] = (sum(p1_hp_pctg.values()) + 1*(6-len(p1_hp_pctg)))/6 - (sum(p2_hp_pctg.values()) + 1*(6-len(p2_hp_pctg)))/6
        feature_list.append(features)
    
    return pd.DataFrame(feature_list).fillna(0)
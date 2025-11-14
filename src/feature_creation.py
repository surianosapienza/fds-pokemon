import numpy as np
import pandas as pd
import src.data_management as my_dm

all_types = ['dragon', 'electric', 'fire', 'flying', 'ghost', 'grass', 'ground', 'ice', 'normal', 'notype', 'poison', 'psychic', 'rock', 'water']


def p1_features(p1_team: list[dict]):
    features = {}
    
    # Stats count
    stats = ['base_hp', 'base_atk', 'base_def', 'base_spa', 'base_spd', 'base_spe']
    for stat in stats: 
        values = [p.get(stat, 0) for p in p1_team]
        features[f'p1_min_{stat}'] = np.min(values)
        features[f'p1_max_{stat}'] = np.max(values)
        features[f'p1_std_{stat}'] = np.std(values)

    # Mean count of single stats
    p1_mean_hp = np.mean([p.get('base_hp', 0) for p in p1_team])
    p1_mean_spe = np.mean([p.get('base_spe', 0) for p in p1_team])
    p1_mean_base_atk = np.mean([p.get('base_atk', 0) for p in p1_team])
    p1_mean_base_spa = np.mean([p.get('base_spa', 0) for p in p1_team])
    p1_mean_base_def = np.mean([p.get('base_def', 0) for p in p1_team])
    p1_mean_base_spd = np.mean([p.get('base_spd', 0) for p in p1_team])

    p1_mean_best_atk = np.mean([np.max([p['base_atk'], p['base_spa']]) for p in p1_team])
    p1_mean_avg_def = np.mean([np.mean([p['base_def'], p['base_spd']]) for p in p1_team])
    

    features['p1_mean_hp'] = p1_mean_hp
    features['p1_mean_spe'] = p1_mean_spe
    features['p1_mean_atk'] = p1_mean_base_atk
    features['p1_mean_def'] = p1_mean_base_def 

    # Feature Derivate
    offense = p1_mean_base_atk + p1_mean_base_spa
    defense = p1_mean_base_def + p1_mean_base_spd
    
    features['p1_offense_mean'] = offense
    features['p1_defense_mean'] = defense
    features['p1_atk_def_ratio'] = p1_mean_best_atk / (p1_mean_avg_def + 1e-6) # Uso le tue specializzate

    p1_totals = [sum(p.get(s, 0) for s in stats) for p in p1_team]
    features['p1_total_base_power'] = float(np.mean(p1_totals))
    features['p1_stat_variety'] = float(np.std(p1_totals))
    features['p1_style_index'] = offense / (offense + defense + 1e-6)
    features['p1_hp_ratio'] = p1_mean_hp / (offense + defense + p1_mean_spe + 1e-6)
    
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
    
    return features

def p1_vs_p2_features(features: dict):
    new_features = {}
    new_features['p1_max_speed_vs_p2_lead_spe'] = features.get('p1_max_speed', 0) - features.get('p2_lead_spe', 0)
    new_features['p1_mean_spe_vs_p2_lead_spe'] = features.get('p1_mean_spe', 0) - features.get('p2_lead_spe', 0)

    return new_features

def status_features(timeline, team1, team2):
    features = {}
    total_statuses = ['slp', 'fnt', 'tox', 'psn', 'brn', 'frz', 'par', 'nostatus']
    dict_status_p1 = {status : 0 for status in total_statuses}
    dict_status_p2 = {status : 0 for status in total_statuses}
    dict_t1_status = {p1 : "nostatus" for p1 in team1}
    dict_t2_status = {p2 : "nostatus" for p2 in team2}

    for turn in timeline:
        p1_name = turn["p1_pokemon_state"]['name']
        turn_status = turn["p1_pokemon_state"].get("status")

        if turn_status and turn_status != 'nostatus':
            dict_status_p1[turn_status] += 1
            dict_t1_status[p1_name] = turn_status

        p2_name = turn["p2_pokemon_state"]['name']
        turn_status = turn["p2_pokemon_state"].get("status")
        
        if turn_status and turn_status != 'nostatus':
            dict_status_p2[turn_status] += 1
            dict_t2_status[p2_name] = turn_status

    final_statuses_t1 = list(dict_t1_status.values())
    final_statuses_t2 = list(dict_t2_status.values())

    debilitating_statuses = {'slp', 'frz', 'par'}
    dot_statuses = {'psn', 'tox', 'brn'}

    p1_final_debilitating_count = sum(1 for s in final_statuses_t1 if s in debilitating_statuses)
    p2_final_debilitating_count = sum(1 for s in final_statuses_t2 if s in debilitating_statuses)
    
    p1_final_dot_count = sum(1 for s in final_statuses_t1 if s in dot_statuses)
    p2_final_dot_count = sum(1 for s in final_statuses_t2 if s in dot_statuses)
    
    p1_final_non_fnt_status_count = p1_final_debilitating_count + p1_final_dot_count
    p2_final_non_fnt_status_count = p2_final_debilitating_count + p2_final_dot_count
    
    # Diff in debilitating pkmn count
    features['final_debilitating_diff'] = p2_final_debilitating_count - p1_final_debilitating_count
    
    # Diff in debilitating pkmn count
    features['final_dot_diff'] = p2_final_dot_count - p1_final_dot_count
    
    # Diff in total statuses
    features['final_non_fnt_status_diff'] = p2_final_non_fnt_status_count - p1_final_non_fnt_status_count
    
    for status in total_statuses:
        if status == 'nostatus':
            continue
        features[f"p1_{status}_count"] = dict_status_p1.get(status, 0)
        features[f"p2_{status}_count"] = dict_status_p2.get(status, 0)
        features[f"p1-p2_{status}_count"] = dict_status_p1.get(status, 0) - dict_status_p2.get(status, 0)

    

    # Single sum of all the status with their respect weight
    
    status_weights = {
        'nostatus': 0,
        'psn': 10,  
        'brn': 15,  
        'par': 30, 
        'tox': 25,  
        'slp': 80, 
        'frz': 90,  
        'fnt': 100  
    }
    
    p1_status_weighted_sum = sum(count * status_weights.get(status, 0) for status, count in dict_status_p1.items())
    
    p2_status_weighted_sum = sum(count * status_weights.get(status, 0) for status, count in dict_status_p2.items())

    features["p1-p2_status_difference"] = p2_status_weighted_sum - p1_status_weighted_sum


    
    ## fnt  features
    
     # fnt pkmn over total pokemon
    features["p1_fnt_over_total_pkmn"] = dict_status_p1.get('fnt', 0)/6
    features["p2_fnt_over_total_pkmn"] = dict_status_p1.get('fnt', 0)/6

    return features

def effect_features(timeline):
    features = {}
    total_effects = ['disable', 'firespin', 'confusion', 'substitute', 'wrap', 'clamp', 'typechange', 'reflect', 'noeffect']
    
    neg_effects = {'disable', 'firespin', 'confusion', 'wrap', 'clamp'}

    pos_effects = {'substitute', 'reflect'}

    dict_effects_p1 = {effect : 0 for effect in total_effects}
    dict_effects_p2 = {effect : 0 for effect in total_effects}
    for turn in timeline:
        if turn["p1_pokemon_state"].get("effects"):
            turn_effects_p1 = turn["p1_pokemon_state"].get("effects")
            for effect in turn_effects_p1:
                if effect in dict_effects_p1:
                    dict_effects_p1[effect] += 1
                    
        if turn["p2_pokemon_state"].get("effects"):
            turn_effects_p2 = turn["p2_pokemon_state"].get("effects")
            for effect in turn_effects_p2:
                if effect in dict_effects_p2:
                    dict_effects_p2[effect] += 1 \
                               
    p1_positive_turns = sum(dict_effects_p1.get(e, 0) for e in pos_effects)
    p2_positive_turns = sum(dict_effects_p2.get(e, 0) for e in pos_effects)
    
    p1_negative_turns = sum(dict_effects_p1.get(e, 0) for e in neg_effects)
    p2_negative_turns = sum(dict_effects_p2.get(e, 0) for e in neg_effects)

    # We distinguish between two different types of effects
    # Positive advantage
    features["p1-p2_positive_effect_diff"] = p1_positive_turns - p2_positive_turns
    
    # Negative advantage
    features["p1-p2_negative_effect_diff"] = p2_negative_turns - p1_negative_turns

    return features

def potential_threat_features(timeline, p1_team_details, p2_lead_details):
    features = {}
   
    p1_stats_map = {p['name']: p for p in p1_team_details}
    
    # Because we only have the stats of the lead pkmn of p2, we can just assume the avg stats for a competitive pokemon
    AVG_META_STATS = {'base_spe': 80, 'base_atk': 80, 'base_spa': 80}

    # Weights of statuses
    # SLP/FRZ almost always a death sentence
    STATUS_MULTIPLIERS = {
        'nostatus': 1.0,
        'psn': 0.9,   
        'tox': 0.8,   
        'brn': 0.6,  
        'par': 0.4,  
        'slp': 0.1,  
        'frz': 0.0, 
        'fnt': 0.0,
        None: 1.0
    }

    p1_state_tracker = {} 
    p2_state_tracker = {}
    
    for p in p1_team_details:
        p1_state_tracker[p['name']] = {'hp_pct': 1.0, 'status': 'nostatus'}
        
    if p2_lead_details:
        p2_state_tracker[p2_lead_details['name']] = {'hp_pct': 1.0, 'status': 'nostatus'}

    # We scan through the timeline to get the final hp_pct and final status of all pokemon
    for turn in timeline:
        p1_name = turn["p1_pokemon_state"]["name"]
        p1_state_tracker[p1_name] = {
            'hp_pct': turn["p1_pokemon_state"]["hp_pct"],
            'status': turn["p1_pokemon_state"].get("status", "nostatus")
        }
        
        p2_name = turn["p2_pokemon_state"]["name"]
        p2_state_tracker[p2_name] = {
            'hp_pct': turn["p2_pokemon_state"]["hp_pct"],
            'status': turn["p2_pokemon_state"].get("status", "nostatus")
        }

    # We compute the potential threat of the pokemon
    
    def calculate_pt(tracker, stats_map, is_p2=False):
        total_pt = 0
        
        for name, state in tracker.items():
            hp = state['hp_pct']
            status = state['status']
            
            if hp <= 0 or status == 'fnt':
                continue
                
            # Here we get back the base stats
            if not is_p2 and name in stats_map:
                base_spe = stats_map[name].get('base_spe', 80)
                base_off = max(stats_map[name].get('base_atk', 80), stats_map[name].get('base_spa', 80))
            elif is_p2 and p2_lead_details and name == p2_lead_details['name']:
                base_spe = p2_lead_details.get('base_spe', 80)
                base_off = max(p2_lead_details.get('base_atk', 80), p2_lead_details.get('base_spa', 80))
            else:
                # If p2 is not the lead pkmn than we just assume his avg stats
                base_spe = AVG_META_STATS['base_spe']
                base_off = AVG_META_STATS['base_atk']

            
            status_mult = STATUS_MULTIPLIERS.get(status, 1.0)
            # We elevate to the 1.3 the base speed because in gen 1 it is an important factor to crit moves
            threat_score = hp * base_off * (base_spe ** 1.3) * status_mult
            total_pt += threat_score
            
        return total_pt

    p1_pt = calculate_pt(p1_state_tracker, p1_stats_map, is_p2=False)
    p2_pt = calculate_pt(p2_state_tracker, {}, is_p2=True)
    
    features["p1-p2_potential_threat_diff"] = p1_pt - p2_pt
    return features

def battle_features(timeline):
    features = {}
    
    features['p1_switched_on_turn1'] = 0 if timeline[0].get("p1_move_details") else 1
    features['p2_switched_on_turn1'] = 0 if timeline[0].get("p2_move_details") else 1
    # Average HP percentage for both players
    p1_hp = [turn["p1_pokemon_state"].get("hp_pct", np.nan) for turn in timeline]
    p2_hp = [turn["p2_pokemon_state"].get("hp_pct", np.nan) for turn in timeline]

    p1_hp_changes = np.diff(p1_hp)
    p2_hp_changes = np.diff(p2_hp)

    p1_total_healing = np.nansum(np.maximum(0, p1_hp_changes))
    p2_total_healing = np.nansum(np.maximum(0, p2_hp_changes))

    p1_total_damage_taken = np.nansum(np.minimum(0, p1_hp_changes)) * -1
    p2_total_damage_taken = np.nansum(np.minimum(0, p2_hp_changes)) * -1

    features["p1_total_healing"] = p1_total_healing
    features["p2_total_healing"] = p2_total_healing
    features["p1_total_damage_taken"] = p1_total_damage_taken
    features["p2_total_damage_taken"] = p2_total_damage_taken
    
    features["p1-p2_total_healing"] = p1_total_healing - p2_total_healing
    features["p1-p2_total_damage_taken"] = p1_total_damage_taken - p2_total_damage_taken
    features["p1-p2_mean_hp_pct"] = np.nanmean(p1_hp) - np.nanmean(p2_hp)
    
    # Slope of hp percentage
    hp_diffs = [turn["p1_pokemon_state"]["hp_pct"] - turn["p2_pokemon_state"]["hp_pct"] for turn in timeline]
    turns = np.arange(len(hp_diffs)) 
    slope, _ = np.polyfit(turns, hp_diffs, 1)
    features['hp_advantage_slope'] = slope

    # Momentum of the last 5 turns 
    last_5_diffs = hp_diffs[-5:]
    features['hp_adv_last_5_turns'] = np.nanmean(last_5_diffs)

    # Crit features using a bug that was present in gen 1 competitive pokemon
    p1_moves_used = [turn["p1_move_details"]["name"] for turn in timeline if turn.get("p1_move_details")]
    p2_moves_used = [turn["p2_move_details"]["name"] for turn in timeline if turn.get("p2_move_details")]
    high_crit = {"Crabhammer", "Karate Chop", "Razor Leaf", "Slash", "crabhammer", "karate chop", "razor leaf", "slash"}
    p1_highcrit_moves_used = sum(m in high_crit for m in p1_moves_used)
    p2_highcrit_moves_used = sum(m in high_crit for m in p2_moves_used)
    features["p1-p2_highcrit_moves_used"] = p1_highcrit_moves_used - p2_highcrit_moves_used

    # Count total moves used
    p1_moves = [turn.get("p1_move_details", {}).get("name") for turn in timeline if turn.get("p1_move_details")]
    p2_moves = [turn.get("p2_move_details", {}).get("name") for turn in timeline if turn.get("p2_move_details")]
    features["p1-p2_total_moves"] = len(p1_moves) - len(p2_moves)

    # Count unique move types used
    p1_move_types = [turn["p1_move_details"].get("type") for turn in timeline if turn.get("p1_move_details")]
    p2_move_types = [turn["p2_move_details"].get("type") for turn in timeline if turn.get("p2_move_details")]
    features["p1-p2_unique_move_types"] = len(set(p1_move_types)) - len(set(p2_move_types))
    
    p1_pkmns = sorted(list(set([turn["p1_pokemon_state"]["name"] for turn in timeline])))
    p2_pkmns = sorted(list(set([turn["p2_pokemon_state"]["name"] for turn in timeline])))
    
    # Meta count featrue based on competitive pkmn info
    META_POKEMON = {'Tauros', 'Snorlax', 'Chansey', 'Exeggutor', 'Alakazam', 'Starmie', 'Zapdos', 'Lapras', 'Jolteon'}
    p1_meta_count = sum(1 for p in p1_pkmns if p in META_POKEMON)
    p2_meta_count = sum(1 for p in p2_pkmns if p in META_POKEMON)
    features['p1-p2_meta_count'] = p1_meta_count - p2_meta_count
    
    ### status and effects features
    
    ## general status feature
    features.update(status_features(timeline, p1_pkmns, p2_pkmns))
    
    ## effects feature
    features.update(effect_features(timeline))
    
    ## Boosts (attack, defense, etc.) features
    
    boost_keys = ["atk", "def", "spa", "spd", "spe"]
    for key in boost_keys:
        p1_boosts = [turn["p1_pokemon_state"]["boosts"].get(key, 0) for turn in timeline]
        p2_boosts = [turn["p2_pokemon_state"]["boosts"].get(key, 0) for turn in timeline]
        p1_mean_boost = np.mean(p1_boosts)
        p2_mean_boost = np.mean(p2_boosts)
        features[f"p1-p2_mean_boost_{key}"] = p1_mean_boost - p2_mean_boost
    
    # Number of time the player switched pokemon
    p1_switch_number = sum([1 for turn in timeline if not turn.get("p1_move_details")])
    p2_switch_number = sum([1 for turn in timeline if not turn.get("p2_move_details")])
    features["p1-p2_switch_number"] = p1_switch_number - p2_switch_number
    # Number of SPECIAL or PHYSICAL moves and Number of STATUS moves of p1 and p2
    p1_attack_moves = sum([1 for turn in timeline if turn.get("p1_move_details") and turn["p1_move_details"]["category"] in ["SPECIAL", "PHYSICAL"]])
    p2_attack_moves = sum([1 for turn in timeline if turn.get("p2_move_details") and turn["p2_move_details"]["category"] in ["SPECIAL", "PHYSICAL"]])
    features["p1-p2_attack_moves"] = p1_attack_moves - p2_attack_moves
    
    p1_status_moves = sum([1 for turn in timeline if turn.get("p1_move_details") and turn["p1_move_details"]["category"] not in ["SPECIAL", "PHYSICAL"]])
    p2_status_moves = sum([1 for turn in timeline if turn.get("p2_move_details") and turn["p2_move_details"]["category"] not in ["SPECIAL", "PHYSICAL"]])
    features["p1-p2_status_moves"] = p1_status_moves - p2_status_moves

    # Count recovery moves used
    RECOVERY_MOVES = {'recover', 'softboiled', 'rest'}
    p1_recovery_moves_used = sum([1 for turn in timeline if turn.get("p1_move_details") and turn["p1_move_details"]["category"] not in ["SPECIAL", "PHYSICAL"] and turn["p1_move_details"]['name'] in RECOVERY_MOVES])
    p2_recovery_moves_used = sum([1 for turn in timeline if turn.get("p2_move_details") and turn["p2_move_details"]["category"] not in ["SPECIAL", "PHYSICAL"] and turn["p2_move_details"]['name'] in RECOVERY_MOVES])
    features['p1-p2_recovery_moves_used'] = p1_recovery_moves_used - p2_recovery_moves_used

    # Average of base power value for SPECIAL or PHYSICAL moves of p1 and p2
    def safe_nanmean(lst):
        return 0 if len(lst) == 0 else np.nanmean(lst)     
    p1_mean_base_power = safe_nanmean([turn['p1_move_details']['base_power'] for turn in timeline if turn.get("p1_move_details") and turn["p1_move_details"]["category"] in ["SPECIAL", "PHYSICAL"]])
    p2_mean_base_power = safe_nanmean([turn['p2_move_details']['base_power'] for turn in timeline if turn.get("p2_move_details") and turn["p2_move_details"]["category"] in ["SPECIAL", "PHYSICAL"]])
    features["p1-p2_mean_base_power"] = p1_mean_base_power - p2_mean_base_power
    
    # number of missed moves
    p1_missed_moves_count, p2_missed_moves_count = my_dm.missed_count_moves(timeline)
    features['p1-p2_missed_moves_count'] = p1_missed_moves_count - p2_missed_moves_count
    
    # Number of same pokemon type moves (stab)
    p1_same_type_moves_number = sum([1 for turn in timeline if turn.get("p1_move_details") and turn["p1_move_details"]["type"] in my_dm.pokemon_type(turn["p1_pokemon_state"]["name"]) and turn["p1_move_details"]["category"] in ["SPECIAL", "PHYSICAL"]])
    p2_same_type_moves_number = sum([1 for turn in timeline if turn.get("p2_move_details") and turn["p2_move_details"]["type"] in my_dm.pokemon_type(turn["p2_pokemon_state"]["name"]) and turn["p2_move_details"]["category"] in ["SPECIAL", "PHYSICAL"]])
    features["p1-p2_same_type_moves_number"] = p1_same_type_moves_number - p2_same_type_moves_number
    
    # Average of multiplier effectivness (stab included)   
    p1_effectivness_avg = safe_nanmean([my_dm.move_effectiveness(turn["p1_move_details"]["type"], turn["p2_pokemon_state"]["name"], turn["p1_move_details"]["type"] in my_dm.pokemon_type(turn["p1_pokemon_state"]["name"])) for turn in timeline if turn.get("p1_move_details") and turn["p1_move_details"]["category"] in ["SPECIAL", "PHYSICAL"]])
    p2_effectivness_avg = safe_nanmean([my_dm.move_effectiveness(turn["p2_move_details"]["type"], turn["p1_pokemon_state"]["name"], turn["p2_move_details"]["type"] in my_dm.pokemon_type(turn["p2_pokemon_state"]["name"])) for turn in timeline if turn.get("p2_move_details") and turn["p2_move_details"]["category"] in ["SPECIAL", "PHYSICAL"]])
    features["p1-p2_effectivness_avg"] = p1_effectivness_avg - p2_effectivness_avg 
    # Number of supereffective moves
    p1_supereffective_moves_count = sum([my_dm.is_supereffective(my_dm.move_effectiveness(turn["p1_move_details"]["type"], turn["p2_pokemon_state"]["name"])) for turn in timeline if turn.get("p1_move_details") and turn["p1_move_details"]["category"] in ["SPECIAL", "PHYSICAL"]])
    p2_supereffective_moves_count = sum([my_dm.is_supereffective(my_dm.move_effectiveness(turn["p2_move_details"]["type"], turn["p1_pokemon_state"]["name"])) for turn in timeline if turn.get("p2_move_details") and turn["p2_move_details"]["category"] in ["SPECIAL", "PHYSICAL"]])
    features["p1-p2_supereffective_moves_count"] = p1_supereffective_moves_count - p2_supereffective_moves_count

    # Number of supereffective pokemon of p1 in respect to p2
    p1_supereffective_density = sum(1 for pkmn1 in p1_pkmns for pkmn2 in p2_pkmns if my_dm.is_supereffective(my_dm.pkmn_effectiveness(pkmn1, pkmn2)))/(len(p1_pkmns)*len(p2_pkmns))
    p2_supereffective_density = sum(1 for pkmn1 in p1_pkmns for pkmn2 in p2_pkmns if my_dm.is_supereffective(my_dm.pkmn_effectiveness(pkmn2, pkmn1)))/(len(p1_pkmns)*len(p2_pkmns))
    features["p1-p2_se_densities"] = p1_supereffective_density - p2_supereffective_density

    # P1 pkmn having at least a supereffective target in p2 team
    p1_atk_share = sum(any(my_dm.is_supereffective(my_dm.pkmn_effectiveness(pkmn1, pkmn2)) for pkmn2 in p2_pkmns) for pkmn1 in p1_pkmns) / 6.0
    p1_def_share = sum(any(my_dm.is_supereffective(my_dm.pkmn_effectiveness(pkmn2, pkmn1)) for pkmn2 in p2_pkmns) for pkmn1 in p1_pkmns) / 6.0
    
    p2_atk_share = sum(any(my_dm.is_supereffective(my_dm.pkmn_effectiveness(pkmn2, pkmn1)) for pkmn1 in p1_pkmns) for pkmn2 in p2_pkmns) / 6.0
    p2_def_share = sum(any(my_dm.is_supereffective(my_dm.pkmn_effectiveness(pkmn1, pkmn2)) for pkmn1 in p1_pkmns) for pkmn2 in p2_pkmns) / 6.0

    features["p1-p2_attackers_share_diff"] = p1_atk_share - p2_atk_share
    features["p1-p2_defensive_share_diff"] = p1_def_share - p2_def_share
    
    # mean of hp percentage for p1 team and p2 team on last informations
    p1_hp_pctg = {p1_pkmn : None for p1_pkmn in p1_pkmns}
    p2_hp_pctg = {p2_pkmn : None for p2_pkmn in p2_pkmns}
    counter1 = 0
    counter2 = 0
    for turn in timeline:
        p1_hp_pctg.update({turn["p1_pokemon_state"]["name"] : turn["p1_pokemon_state"]["hp_pct"]})
        p2_hp_pctg.update({turn["p2_pokemon_state"]["name"] : turn["p2_pokemon_state"]["hp_pct"]})

        counter1 += turn["p1_pokemon_state"]["hp_pct"] > turn["p2_pokemon_state"]["hp_pct"]
        counter2 += turn["p1_pokemon_state"]["hp_pct"] < turn["p2_pokemon_state"]["hp_pct"]
    
    p1_remain_health_avg = (sum(p1_hp_pctg.values()) + 1*(6-len(p1_hp_pctg)))/6
    p2_remain_health_avg = (sum(p2_hp_pctg.values()) + 1*(6-len(p2_hp_pctg)))/6
    features["health_difference"] = p1_remain_health_avg - p2_remain_health_avg
    features["health_advantage_difference"]= counter1 - counter2
    hp_advantage_streak = sum(p1 > p2 for p1, p2 in zip(p1_hp_pctg, p2_hp_pctg))
    features["p1_hp_advantage_final_ratio"] = hp_advantage_streak 
    features["remaining_advantage"] = (p1_remain_health_avg * (1-features["p1_fnt_count"]) - p2_remain_health_avg * (1-features["p2_fnt_count"]))
    return features

def combined_features(features, timeline):
    new_features = {}
    new_features['pt_times_status_advantage'] = features['p1-p2_potential_threat_diff'] * features['p1-p2_status_difference']

    hp_diffs = [t["p1_pokemon_state"].get("hp_pct", np.nan) - t["p2_pokemon_state"].get("hp_pct", np.nan) for t in timeline]
    hp_volatility = np.std(hp_diffs) + 1e-6 
    
    new_features['stable_momentum_slope'] = (features.get('hp_advantage_slope') / hp_volatility)
    p1_dmg_taken = features.get('p1_total_damage_taken', 0)
    p2_dmg_taken = features.get('p2_total_damage_taken', 0)
    
    p1_effective_pressure = p2_dmg_taken / (features.get('p2_total_healing', 0) + 1e-6)
    p2_effective_pressure = p1_dmg_taken / (features.get('p1_total_healing', 0) + 1e-6)
    
    new_features['p1-p2_effective_pressure_diff'] = p1_effective_pressure - p2_effective_pressure
    return new_features

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
        
        features.update(p1_vs_p2_features(features))
        ## Extracting battle features
        timeline = battle.get("battle_timeline", [])
        if len(timeline) > 0:
            #"""
            features.update(battle_features(timeline))
            features.update(potential_threat_features(timeline, p1_team, p2_lead))
            features.update(combined_features(features, timeline))

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

            features["health_difference"] = (sum(p1_hp_pctg.values()) + 1*(6-len(p1_hp_pctg)))/6 - (sum(p2_hp_pctg.values()) + 1*(6-len(p2_hp_pctg)))/6

            hp_advantage_streak = sum(p1 > p2 for p1, p2 in zip(p1_hp_pctg, p2_hp_pctg))
            features["p1_hp_advantage_ratio"] = hp_advantage_streak / len(timeline)
        feature_list.append(features)
    
    return pd.DataFrame(feature_list).fillna(0)

def low_variance_features(df, threshold=0.999):
    to_drop = []
    for col in df.columns:
        top_freq = df[col].value_counts(normalize=True, dropna=False).iloc[0]
        if top_freq >= threshold:
            to_drop.append(col)
    return to_drop
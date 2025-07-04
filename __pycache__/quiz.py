# The "Brain" of our application. All type matchup data is stored here.
TYPE_COLORS = {
    "Normal": "#A8A77A", "Fire": "#EE8130", "Water": "#6390F0",
    "Electric": "#F7D02C", "Grass": "#7AC74C", "Ice": "#96D9D6",
    "Fighting": "#C22E28", "Poison": "#A33EA1", "Ground": "#E2BF65",
    "Flying": "#A98FF3", "Psychic": "#F95587", "Bug": "#A6B91A",
    "Rock": "#B6A136", "Ghost": "#735797", "Dragon": "#6F35FC",
    "Dark": "#705746", "Steel": "#B7B7CE", "Fairy": "#D685AD"
}

TYPE_CHART = {
    "Normal": {"weak_to": ["Fighting"], "resists": [], "immune_to": ["Ghost"]},
    "Fire": {"weak_to": ["Water", "Ground", "Rock"], "resists": ["Fire", "Grass", "Ice", "Bug", "Steel", "Fairy"], "immune_to": []},
    "Water": {"weak_to": ["Grass", "Electric"], "resists": ["Fire", "Water", "Ice", "Steel"], "immune_to": []},
    "Grass": {"weak_to": ["Fire", "Ice", "Poison", "Flying", "Bug"], "resists": ["Water", "Grass", "Electric", "Ground"], "immune_to": []},
    "Electric": {"weak_to": ["Ground"], "resists": ["Electric", "Flying", "Steel"], "immune_to": []},
    # ADDED ICE TYPE DATA
    "Ice": {"weak_to": ["Fire", "Fighting", "Rock", "Steel"], "resists": ["Ice"], "immune_to": []},
    "Fighting": {"weak_to": ["Flying", "Psychic", "Fairy"], "resists": ["Rock", "Bug", "Dark"], "immune_to": []},
    "Poison": {"weak_to": ["Ground", "Psychic"], "resists": ["Grass", "Fighting", "Poison", "Bug", "Fairy"], "immune_to": []},
    "Ground": {"weak_to": ["Water", "Grass", "Ice"], "resists": ["Poison", "Rock"], "immune_to": ["Electric"]},
    "Flying": {"weak_to": ["Electric", "Ice", "Rock"], "resists": ["Grass", "Fighting", "Bug"], "immune_to": ["Ground"]},
    "Psychic": {"weak_to": ["Bug", "Ghost", "Dark"], "resists": ["Fighting", "Psychic"], "immune_to": []},
    "Bug": {"weak_to": ["Fire", "Flying", "Rock"], "resists": ["Grass", "Fighting", "Ground"], "immune_to": []},
    "Rock": {"weak_to": ["Water", "Grass", "Fighting", "Ground", "Steel"], "resists": ["Normal", "Fire", "Poison", "Flying"], "immune_to": []},
    "Ghost": {"weak_to": ["Ghost", "Dark"], "resists": ["Poison", "Bug"], "immune_to": ["Normal", "Fighting"]},
    "Dragon": {"weak_to": ["Ice", "Dragon", "Fairy"], "resists": ["Fire", "Water", "Grass", "Electric"], "immune_to": []},
    "Dark": {"weak_to": ["Fighting", "Bug", "Fairy"], "resists": ["Ghost", "Dark"], "immune_to": ["Psychic"]},
    "Steel": {"weak_to": ["Fire", "Fighting", "Ground"], "resists": ["Normal", "Grass", "Ice", "Flying", "Psychic", "Bug", "Rock", "Dragon", "Steel", "Fairy"], "immune_to": ["Poison"]},
    "Fairy": {"weak_to": ["Poison", "Steel"], "resists": ["Fighting", "Bug", "Dark"], "immune_to": ["Dragon"]}
}

def calculate_multiplier(attack_type, defense_type1, defense_type2=None):
    multiplier = 1.0
    
    matchup1 = TYPE_CHART[defense_type1]
    if attack_type in matchup1["immune_to"]: return 0
    if attack_type in matchup1["weak_to"]: multiplier *= 2
    if attack_type in matchup1["resists"]: multiplier *= 0.5

    if defense_type2:
        matchup2 = TYPE_CHART[defense_type2]
        if attack_type in matchup2["immune_to"]: return 0
        if attack_type in matchup2["weak_to"]: multiplier *= 2
        if attack_type in matchup2["resists"]: multiplier *= 0.5
        
    return multiplier
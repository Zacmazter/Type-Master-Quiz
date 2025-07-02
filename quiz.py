# quiz.py

# --- Data for Modern (Gen 6+) Type Chart ---
TYPE_COLORS_MODERN = {
    "Normal": "#A8A77A", "Fire": "#EE8130", "Water": "#6390F0",
    "Electric": "#F7D02C", "Grass": "#7AC74C", "Ice": "#96D9D6",
    "Fighting": "#C22E28", "Poison": "#A33EA1", "Ground": "#E2BF65",
    "Flying": "#A98FF3", "Psychic": "#F95587", "Bug": "#A6B91A",
    "Rock": "#B6A136", "Ghost": "#735797", "Dragon": "#6F35FC",
    "Dark": "#705746", "Steel": "#B7B7CE", "Fairy": "#D685AD"
}

TYPE_CHART_MODERN = {
    "Normal": {"weak_to": ["Fighting"], "resists": [], "immune_to": ["Ghost"]},
    "Fire": {"weak_to": ["Water", "Ground", "Rock"], "resists": ["Fire", "Grass", "Ice", "Bug", "Steel", "Fairy"], "immune_to": []},
    "Water": {"weak_to": ["Grass", "Electric"], "resists": ["Fire", "Water", "Ice", "Steel"], "immune_to": []},
    "Grass": {"weak_to": ["Fire", "Ice", "Poison", "Flying", "Bug"], "resists": ["Water", "Grass", "Electric", "Ground"], "immune_to": []},
    "Electric": {"weak_to": ["Ground"], "resists": ["Electric", "Flying", "Steel"], "immune_to": []},
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

ALL_TYPES_MODERN = list(TYPE_CHART_MODERN.keys())


# --- Data for Classic (Gen 3) Type Chart ---
# Key differences: No Fairy type, Steel resists Ghost and Dark.
TYPE_COLORS_GEN3 = {k: v for k, v in TYPE_COLORS_MODERN.items() if k != "Fairy"}

TYPE_CHART_GEN3 = {
    "Normal": {"weak_to": ["Fighting"], "resists": [], "immune_to": ["Ghost"]},
    "Fire": {"weak_to": ["Water", "Ground", "Rock"], "resists": ["Fire", "Grass", "Ice", "Bug", "Steel"], "immune_to": []},
    "Water": {"weak_to": ["Grass", "Electric"], "resists": ["Fire", "Water", "Ice", "Steel"], "immune_to": []},
    "Grass": {"weak_to": ["Fire", "Ice", "Poison", "Flying", "Bug"], "resists": ["Water", "Grass", "Electric", "Ground"], "immune_to": []},
    "Electric": {"weak_to": ["Ground"], "resists": ["Electric", "Flying", "Steel"], "immune_to": []},
    "Ice": {"weak_to": ["Fire", "Fighting", "Rock", "Steel"], "resists": ["Ice"], "immune_to": []},
    "Fighting": {"weak_to": ["Flying", "Psychic"], "resists": ["Rock", "Bug", "Dark"], "immune_to": []},
    "Poison": {"weak_to": ["Ground", "Psychic"], "resists": ["Grass", "Fighting", "Poison", "Bug"], "immune_to": []},
    "Ground": {"weak_to": ["Water", "Grass", "Ice"], "resists": ["Poison", "Rock"], "immune_to": ["Electric"]},
    "Flying": {"weak_to": ["Electric", "Ice", "Rock"], "resists": ["Grass", "Fighting", "Bug"], "immune_to": ["Ground"]},
    "Psychic": {"weak_to": ["Bug", "Ghost", "Dark"], "resists": ["Fighting", "Psychic"], "immune_to": []},
    "Bug": {"weak_to": ["Fire", "Flying", "Rock"], "resists": ["Grass", "Fighting", "Ground"], "immune_to": []},
    "Rock": {"weak_to": ["Water", "Grass", "Fighting", "Ground", "Steel"], "resists": ["Normal", "Fire", "Poison", "Flying"], "immune_to": []},
    "Ghost": {"weak_to": ["Ghost", "Dark"], "resists": ["Poison", "Bug"], "immune_to": ["Normal", "Fighting"]},
    "Dragon": {"weak_to": ["Ice", "Dragon"], "resists": ["Fire", "Water", "Grass", "Electric"], "immune_to": []},
    "Dark": {"weak_to": ["Fighting", "Bug"], "resists": ["Ghost", "Dark"], "immune_to": ["Psychic"]},
    "Steel": {"weak_to": ["Fire", "Fighting", "Ground"], "resists": ["Normal", "Grass", "Ice", "Flying", "Psychic", "Bug", "Rock", "Dragon", "Steel", "Ghost", "Dark"], "immune_to": ["Poison"]}
}

ALL_TYPES_GEN3 = list(TYPE_CHART_GEN3.keys())


# --- Global State Manager ---
# This dictionary will hold the currently active game data.
ActiveGameData = {}

def set_active_generation(gen_name):
    """Sets the active type chart and colors for the application."""
    if gen_name == "Gen3":
        ActiveGameData['chart'] = TYPE_CHART_GEN3
        ActiveGameData['colors'] = TYPE_COLORS_GEN3
        ActiveGameData['types_list'] = ALL_TYPES_GEN3
        ActiveGameData['name'] = "Gen3"
    else: # Default to Modern
        ActiveGameData['chart'] = TYPE_CHART_MODERN
        ActiveGameData['colors'] = TYPE_COLORS_MODERN
        ActiveGameData['types_list'] = ALL_TYPES_MODERN
        ActiveGameData['name'] = "Modern"

# --- Core Calculation Logic ---
def calculate_multiplier(attack_type, defense_type1, defense_type2=None):
    """Calculates the multiplier using the currently active type chart."""
    multiplier = 1.0
    current_chart = ActiveGameData['chart']
    
    # Can't have an attack type that doesn't exist in the selected generation
    if attack_type not in current_chart:
        return 1.0

    matchup1 = current_chart[defense_type1]
    if attack_type in matchup1["immune_to"]: return 0
    if attack_type in matchup1["weak_to"]: multiplier *= 2
    if attack_type in matchup1["resists"]: multiplier *= 0.5

    if defense_type2:
        matchup2 = current_chart[defense_type2]
        if attack_type in matchup2["immune_to"]: return 0
        if attack_type in matchup2["weak_to"]: multiplier *= 2
        if attack_type in matchup2["resists"]: multiplier *= 0.5
        
    return multiplier

# Initialize the game with the Modern chart by default.
set_active_generation("Modern")
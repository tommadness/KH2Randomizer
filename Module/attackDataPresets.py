WEAK = "WEAK"
MILD = "MILD"
MEDIUM = "MEDIUM"
STRONG = "STRONG"
HEAVY = "HEAVY"
OVERPOWERED = "OVERPOWERED"
CHAOS = "CHAOS"
DISABLED = "DISABLED"

class AttackDataPresets:

    def __init__(self, attack_data_preset_choice: str):
        super().__init__()
        self.attack_data_preset_choice = attack_data_preset_choice

    @staticmethod
    def attack_data_preset_options() -> dict[str, str]:
        return {
            WEAK: "WEAK",
            MILD: "MILD",
            MEDIUM: "MEDIUM",
            STRONG: "STRONG",
            HEAVY: "HEAVY",
            OVERPOWERED: "OVERPOWERED",
            CHAOS: "CHAOS",
            DISABLED: "DISABLED",
        }

    @staticmethod
    def attack_data_preset_tooltip() -> str:
        return """
        Influences the strength of which these values are randomized.
        PRESET      MIN    MAX  (multiplier)
        Weak =      1.0x - 1.3x difference
        Mild =      1.0x - 1.5x
        Medium =    1.2x - 1.8x
        Strong =    1.5x - 2.2x
        Heavy =     1.8x - 3.0x
        Overpowered = 2.2x - 4.0x
        Chaos =     1.0x - 7.0x

        Remember that the difference can be either positive or negative.
        Some attack data parameters can only be between certain values,
        therefore they do not have such a preset. Revenge Value is handled
        differently to avoid awful gameplay.
        """
    
    @staticmethod
    def multi_hit_preset_tooltip() -> str:
        return """
        Potentially changes moves to do multiple hits and how
        frequently they hit

        The presets influence 2 things: how likely a move becomes a multi hit 
        and the rate of its hits. Generally speaking, can make the game very 
        dangerous if set to Strong or higher.
        """
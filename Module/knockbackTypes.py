JUST_DAMAGE = "Just Damage"
DAMAGE_STUN = "Damage + Stun"
DAMAGE_STUN_KNOCKBACK = "Damage + Stun + Knockback"


class KnockbackTypes:

    def __init__(self, knockback_choice: str):
        super().__init__()
        self.knockback_choice = knockback_choice

    @staticmethod
    def knockback_options() -> dict[str, str]:
        return {
            JUST_DAMAGE: "Just Damage",
            DAMAGE_STUN: "Damage + Stun",
            DAMAGE_STUN_KNOCKBACK: "Damage + Stun + Knockback",
        }

    @staticmethod
    def get_knockback_value(knockback) -> int:
        if knockback == DAMAGE_STUN:
            return 8
        elif knockback == DAMAGE_STUN_KNOCKBACK:
            return 11
        else:
            return 12

    @staticmethod
    def damage_type_tooltip() -> str:
        return """
        Defines the type of knockback the attack/ability will have.
        Keep in mind, changes will also affect enemies that Companions could already affect normally.
        
        Just Damage: Enemies won't be phased (except for certain things like Goofy Tornado which have
        a second attack effect for pulling enemies in).
        
        Damage + Stun: Enemies will be stunned, but won't move very much or at all from their position.
        
        Damage + Stun + Knockback: Like above, but will also be moved.
        """

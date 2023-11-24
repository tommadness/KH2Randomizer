JUST_DAMAGE = "Just Damage"
DAMAGE_STUN = "Damage + Stun"
DAMAGE_STUN_KNOCKBACK = "Damage + Stun + Knockback"
class KnockbackTypes:
    @staticmethod
    def knockback_options() -> dict[str, str]:
        return {
            JUST_DAMAGE: "Just Damage",
            DAMAGE_STUN: "Damage + Stun",
            DAMAGE_STUN_KNOCKBACK: "Damage + Stun + Knockback",
        }
    
    @staticmethod
    def get_knockback_value(knockback):
        if(knockback == DAMAGE_STUN): return 8
        elif(knockback == DAMAGE_STUN_KNOCKBACK): return 11
        else: return 12
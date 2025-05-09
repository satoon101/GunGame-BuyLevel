# ../gungame/plugins/custom/gg_buy_level/rules.py

"""Creates the gg_buy_level rules."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# GunGame
from gungame.core.rules.instance import GunGameRules

# Plugin
from .info import info

# =============================================================================
# >> RULES
# =============================================================================
buy_level_rules = GunGameRules(info.name)
buy_level_rules.register_all_rules()

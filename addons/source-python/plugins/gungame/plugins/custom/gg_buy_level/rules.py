# ../gungame/plugins/custom/gg_buy_level/rules.py

"""Creates the gg_buy_level rules."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# GunGame
from gungame.core.rules.instance import GunGameRules
from gungame.core.rules.strings import rules_translations

# Plugin
from .info import info


# =============================================================================
# >> RULES
# =============================================================================
buy_level_rules = GunGameRules(info.name)

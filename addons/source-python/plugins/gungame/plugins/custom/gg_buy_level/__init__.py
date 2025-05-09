# ../gungame/plugins/custom/gg_buy_level/__init__.py

"""Players can purchase levels with cash they earn."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from collections import defaultdict

# Source.Python
from listeners import OnLevelInit

# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
player_cash = defaultdict(int)


# =============================================================================
# >> LISTENERS
# =============================================================================
@OnLevelInit
def _level_init(map_name):
    """Reset the cash dictionary."""
    player_cash.clear()

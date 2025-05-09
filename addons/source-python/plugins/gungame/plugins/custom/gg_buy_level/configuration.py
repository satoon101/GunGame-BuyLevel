# ../gungame/plugins/custom/gg_buy_level/configuration.py

"""Creates the gg_buy_level configuration."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# GunGame
from gungame.core.config.manager import GunGameConfigManager

# Plugin
from .info import info

# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    "allow_win",
    "kill_reward",
    "level_increase",
    "level_reward",
    "skip_knife",
    "skip_nade",
    "start_amount",
)


# =============================================================================
# >> CONFIGURATION
# =============================================================================
with (
    GunGameConfigManager(info.name) as _config,
    _config.cvar("start_amount", 2000) as start_amount,
    _config.cvar("level_increase", 200) as level_increase,
    _config.cvar("kill_reward", 800) as kill_reward,
    _config.cvar("level_reward", 800) as level_reward,
    _config.cvar("skip_nade") as skip_nade,
    _config.cvar("skip_knife") as skip_knife,
    _config.cvar("allow_win") as allow_win,
):
    start_amount.add_text()
    level_increase.add_text()
    kill_reward.add_text()
    level_reward.add_text()
    skip_nade.add_text()
    skip_knife.add_text()
    allow_win.add_text()

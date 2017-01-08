# ../gungame/plugins/custom/gg_buy_level/commands.py

"""Command registration for gg_buy_level."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# GunGame
from gungame.core.commands.registration import register_command_callback
from gungame.core.players.dictionary import player_dictionary
from gungame.core.weapons.groups import melee_weapons, all_grenade_weapons
from gungame.core.weapons.manager import weapon_order_manager


# =============================================================================
# >> FUNCTIONS
# =============================================================================
@register_command_callback('buy_level', 'BuyLevel:Command')
def _buy_level_callback(command, index, team_only=False):
    from .configuration import (
        allow_win, level_increase, start_amount, skip_knife, skip_nade,
    )

    player = player_dictionary.from_index(index)
    if player.level_weapon in all_grenade_weapons and not skip_nade.get_bool():
        # TODO: send message
        return

    if player.level_weapon in melee_weapons and not skip_knife.get_bool():
        # TODO: send message
        return

    if (
        player.level == weapon_order_manager.max_levels
        and not allow_win.get_bool()
    ):
        # TODO: send message
        return

    amount = start_amount.get_int()
    amount += player.level * level_increase.get_int()

    if amount > player.cash:
        # TODO: send message
        return

    current = player.level
    player.increase_level(1, 'buy')
    if player.level <= current:
        # TODO: send message
        return

    player.cash -= amount

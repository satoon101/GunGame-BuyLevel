# ../gungame/plugins/custom/gg_buy_level/commands.py

"""Command registration for gg_buy_level."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# GunGame
from gungame.core.commands.registration import register_command_callback
from gungame.core.players.dictionary import player_dictionary
from gungame.core.status import GunGameMatchStatus, GunGameStatus
from gungame.core.weapons.groups import all_grenade_weapons, melee_weapons
from gungame.core.weapons.manager import weapon_order_manager

# Plugin
from . import player_cash


# =============================================================================
# >> FUNCTIONS
# =============================================================================
@register_command_callback("buy_level", "BuyLevel:Command")
def _buy_level_callback(index):
    from .configuration import (
        allow_win,
        level_increase,
        skip_knife,
        skip_nade,
        start_amount,
    )
    if GunGameStatus.MATCH is not GunGameMatchStatus.ACTIVE:
        return

    player = player_dictionary.from_index(index)
    if player.level_weapon in all_grenade_weapons and not skip_nade.get_bool():
        player.chat_message(
            message="BuyLevel:Denied:Level",
            index=player.index,
            weapon=player.level_weapon,
        )
        return

    if player.level_weapon in melee_weapons and not skip_knife.get_bool():
        player.chat_message(
            message="BuyLevel:Denied:Level",
            index=player.index,
            weapon=player.level_weapon,
        )
        return

    if (
        player.level == weapon_order_manager.max_levels
        and not allow_win.get_bool()
    ):
        player.chat_message(
            message="BuyLevel:Denied:Win",
            index=player.index,
        )
        return

    amount = start_amount.get_int()
    amount += (player.level - 1) * level_increase.get_int()

    if amount > player.cash:
        player.chat_message(
            message="BuyLevel:Denied:Cash",
            index=player.index,
            current=player.cash,
            required=amount,
        )
        return

    current = player.level
    player.increase_level(1, "buy")
    if player.level <= current:
        player.chat_message(
            message="BuyLevel:Failed",
            index=player.index,
        )
        return

    player.chat_message(
        message="BuyLevel:Purchased",
        index=player.index,
        amount=amount,
    )
    player_cash[player.userid] -= amount
    player.cash = player_cash[player.userid]

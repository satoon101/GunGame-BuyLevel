# ../gungame/plugins/custom/gg_buy_level/gg_buy_level.py

"""Plugin allows layers to purchase levels with cash they earn."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from contextlib import suppress

# Source.Python
from entities.hooks import EntityCondition, EntityPostHook
from events import Event
from memory import make_object
from players.entity import Player

# GunGame
from gungame.core.players.dictionary import player_dictionary
from gungame.core.status import GunGameMatchStatus, GunGameStatus

# Plugin
from . import player_cash
from .configuration import (
    kill_reward,
    level_increase,
    level_reward,
    start_amount,
)


# =============================================================================
# >> GAME EVENTS
# =============================================================================
@Event("player_death")
def _give_kill_reward(game_event):
    """Give cash for the kill."""
    if GunGameStatus.MATCH is not GunGameMatchStatus.ACTIVE:
        return

    userid = game_event["userid"]
    attacker = game_event["attacker"]
    if attacker in (userid, 0):
        return

    victim = player_dictionary[userid]
    killer = player_dictionary[attacker]
    if victim.team_index == killer.team_index:
        return

    _give_cash(attacker, int(kill_reward))


# =============================================================================
# >> GUNGAME EVENTS
# =============================================================================
@Event("gg_level_up")
def _give_level_reward(game_event):
    """Give cash for leveling up."""
    if game_event["reason"] != "buy":
        _give_cash(game_event["leveler"], int(level_reward))


# =============================================================================
# >> ENTITY HOOKS
# =============================================================================
@EntityPostHook(EntityCondition.is_player, "add_account")
def _set_cash(stack_data, return_value):
    """Hooks AddAccount to make sure to only set to the buy_level value."""
    if GunGameStatus.MATCH is not GunGameMatchStatus.ACTIVE:
        return

    with suppress(ValueError):
        player = make_object(Player, stack_data[0])
        player.cash = player_cash[player.userid]


# =============================================================================
# >> HELPER FUNCTIONS
# =============================================================================
def _give_cash(userid, value):
    """Give the player the cash."""
    player_cash[userid] += value

    player = player_dictionary[userid]
    player.cash = player_cash[userid]
    amount = int(start_amount)
    amount += player.level * int(level_increase)

    if amount <= player_cash[userid]:
        player.chat_message(
            message="BuyLevel:Earned",
            index=player.index,
        )

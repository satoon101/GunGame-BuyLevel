# ../gungame/plugins/custom/gg_buy_level/gg_buy_level.py

"""."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from collections import defaultdict
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
from .configuration import (
    level_increase, level_reward, kill_reward, start_amount,
)


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
player_cash = defaultdict(int)


# =============================================================================
# >> GAME EVENTS
# =============================================================================
@Event('player_death')
def _give_kill_reward(game_event):
    if GunGameStatus.MATCH is not GunGameMatchStatus.ACTIVE:
        return

    userid = game_event['userid']
    attacker = game_event['attacker']
    if attacker in (userid, 0):
        return

    victim = player_dictionary[userid]
    killer = player_dictionary[attacker]
    if victim.team == killer.team:
        return

    _give_cash(attacker, kill_reward.get_int())


# =============================================================================
# >> GUNGAME EVENTS
# =============================================================================
@Event('gg_level_up')
def _give_level_reward(game_event):
    if game_event['reason'] != 'buy':
        _give_cash(game_event['leveler'], level_reward.get_int())


# =============================================================================
# >> ENTITY HOOKS
# =============================================================================
@EntityPostHook(EntityCondition.is_player, 'add_account')
def _set_cash(args, return_value):
    if GunGameStatus.MATCH is not GunGameMatchStatus.ACTIVE:
        return

    with suppress(ValueError):
        player = make_object(Player, args[0])
        player.cash = player_cash[player.userid]


# =============================================================================
# >> HELPER FUNCTIONS
# =============================================================================
def _give_cash(userid, value):
    previously_earned = bool(player_cash[userid])
    player_cash[userid] += value

    player = player_dictionary[userid]
    player.cash = player_cash[userid]
    amount = start_amount.get_int()
    amount += player.level * level_increase.get_int()

    if not previously_earned and player_cash[userid] >= amount:
        player.chat_message(
            message='BuyLevel:Earned',
            index=player.index,
        )

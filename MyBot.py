#!/usr/bin/env python3

# Import the Halite SDK, which will let you interact with the game.
import hlt
from hlt import constants

import random
import logging


# This game object contains the initial game state.
game = hlt.Game()
# Respond with your name.
game.ready("Dustician V4")

returnHome = False

while True:
    # Get the latest game state.
    game.update_frame()
    # You extract player metadata and the updated map metadata here for convenience.
    me = game.me
    game_map = game.game_map

    # A command queue holds all the commands you will run this turn.
    command_queue = []

    for ship in me.get_ships():
        if ship.is_full:
            returnHome = True
        if ship.position == me.shipyard.position:
            returnHome = False

        if returnHome:
            command_queue.append(
                ship.move(game_map.naive_navigate(ship, me.shipyard.position)))
            continue
        if game_map[ship.position].halite_amount < constants.MAX_HALITE / 10:
            command_queue.append(
                ship.move(random.choice(["n", "s", "e", "w"])))
        else:
            command_queue.append(ship.stay_still())

    # If you're on the first turn and have enough halite, spawn a ship.
    # Don't spawn a ship if you currently have a ship at port, though.
    if len(me.get_ships()) == 0 and (me.halite_amount >= constants.SHIP_COST and not game_map[me.shipyard].is_occupied):
        command_queue.append(game.me.shipyard.spawn())

    # Send your moves back to the game environment, ending this turn.
    game.end_turn(command_queue)
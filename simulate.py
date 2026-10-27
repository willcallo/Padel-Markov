"""Monte Carlo simulator for padel matches."""

import random


def sim_game_golden(p):
    """Play one game, golden point at 40-40. True if the server holds."""
    a, b = 0, 0
    while True:
        if a == 3 and b == 3:
            return random.random() < p
        if random.random() < p:
            a += 1
        else:
            b += 1
        if a == 4:
            return True
        if b == 4:
            return False


def sim_game_deuce(p):
    """Play one game, advantage at 40-40. True if the server holds."""
    a, b = 0, 0
    while True:
        if random.random() < p:
            a += 1
        else:
            b += 1
        if a >= 4 and a - b >= 2:
            return True
        if b >= 4 and b - a >= 2:
            return False


def sim_game_star(p):
    """Play one game, star point at 40-40. True if the server holds."""
    a, b = 0, 0
    deuces = 0
    while True:
        if random.random() < p:
            a += 1
        else:
            b += 1
        if a == b and a >= 3:
            deuces += 1
        if a >= 4 and a - b >= 2:
            return True
        if b >= 4 and b - a >= 2:
            return False
        if deuces == 3:
            return random.random() < p


def sim_tiebreak(p_a, p_b, first="A"):
    """Play one tiebreak. True if team A wins."""
    a, b = 0, 0
    while True:
        n = a + b
        if ((n + 1) // 2) % 2 == 0:
            server = first
        else:
            server = "B" if first == "A" else "A"

        x = p_a if server == "A" else 1 - p_b

        if random.random() < x:
            a += 1
        else:
            b += 1

        if a >= 7 and a - b >= 2:
            return True
        if b >= 7 and b - a >= 2:
            return False


def sim_set(p_a, p_b, game=sim_game_star, server="A"):
    """Play one set. Returns True if A wins and also returns next server."""
    ga, gb = 0, 0
    while True:
        if server == "A":
            a_won_game = game(p_a)
        else:
            a_won_game = not game(p_b)

        if a_won_game:
            ga += 1
        else:
            gb += 1

        server = "B" if server == "A" else "A"

        if (ga >= 6 and ga - gb >= 2) or ga == 7:
            return True, server
        if (gb >= 6 and gb - ga >= 2) or gb == 7:
            return False, server

        if ga == 6 and gb == 6:
            a_won = sim_tiebreak(p_a, p_b, first=server)
            next_server = "B" if server == "A" else "A"
            return a_won, next_server


def sim_match(p_a, p_b, game=sim_game_star, server="A"):
    """Play one best of 3 match. True if team A wins."""
    sa, sb = 0, 0
    while sa < 2 and sb < 2:
        a_won, server = sim_set(p_a, p_b, game, server)
        if a_won:
            sa += 1
        else:
            sb += 1
    return sa == 2

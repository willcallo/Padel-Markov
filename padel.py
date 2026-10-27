"""Full Markov chain model for padel scoring"""

from functools import cache

@cache
def hold_golden(p, a=0, b=0):
    """Chance the server wins the game, golden point at 40-40."""
    q = 1 - p
    if a == 3 and b == 3:  # 40-40
        return p
    if a == 4:  # server won
        return 1
    if b == 4:  # receiver won
        return 0
    return p * hold_golden(p, a + 1, b) + q * hold_golden(p, a, b + 1)

@cache
def hold_deuce(p, a=0, b=0):
    """Chance the server wins the game, advantage at 40-40."""
    q = 1 - p
    if a == 3 and b == 3:
        return p**2 / (p**2 + q**2)  # win from deuce
    if a == 4:  # server won
        return 1
    if b == 4:  # receiver won
        return 0
    return p * hold_deuce(p, a + 1, b) + q * hold_deuce(p, a, b + 1)

@cache
def hold_star(p, a=0, b=0):
    """Chance the server wins the game, Star Point at 40-40."""
    q = 1 - p
    if a == 3 and b == 3:  # win from first deuce
        d3 = p
        d2 = p**2 + 2 * p * q * d3
        d1 = p**2 + 2 * p * q * d2
        return d1
    if a == 4:  # server won
        return 1
    if b == 4:  # receiver won
        return 0
    return p * hold_star(p, a + 1, b) + q * hold_star(p, a, b + 1)

@cache
def tiebreak_prob(p_a, p_b, a=0, b=0, first="A"):
    """Chance team A wins the tiebreak."""
    if a >= 7 and a - b >= 2:
        return 1
    if b >= 7 and b - a >= 2:
        return 0
    if a == b and a >= 6:
        w = p_a * (1 - p_b)
        l = (1 - p_a) * p_b
        return w / (w + l)

    n = a + b
    if ((n + 1) // 2) % 2 == 0:
        server = first
    else:
        server = "B" if first == "A" else "A"

    if server == "A":
        x = p_a
    else:
        x = 1 - p_b
    return x * tiebreak_prob(p_a, p_b, a + 1, b, first) + (1 - x) * tiebreak_prob(
        p_a, p_b, a, b + 1, first
    )

@cache
def set_prob(
    p_a, p_b, hold=hold_star, ga=0, gb=0, server="A"
):  # where ga and gb are games won by a and b respectively
    """Chance team A wins the set."""
    h_a = hold(p_a)
    h_b = hold(p_b)

    if (ga >= 6 and ga - gb >= 2) or ga == 7:  # A wins the set
        return 1
    if (gb >= 6 and gb - ga >= 2) or gb == 7:  # B wins the set
        return 0
    if ga == 6 and gb == 6:
        return tiebreak_prob(p_a, p_b, first=server)

    if server == "A":
        x = h_a
        next_server = "B"
    else:
        x = 1 - h_b
        next_server = "A"
    return x * set_prob(p_a, p_b, hold, ga + 1, gb, next_server) + (1 - x) * set_prob(
        p_a, p_b, hold, ga, gb + 1, next_server
    )


def match_prob(p_a, p_b, hold=hold_star):
    """Chance team A wins the match (best of 3 sets)."""
    s = set_prob(p_a, p_b, hold)
    return s**2 + 2 * s * (1 - s) * s

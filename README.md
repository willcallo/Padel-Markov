# Padel Markov Model

A Markov chain model for padel scoring that calculates the exact probability of a team winning a game, set, or match from each team's chance of winning a point on their serve. This is then checked using a Monte Carlo simulator.

## Key findings

- **Small edges become big ones across a match.** A team that wins just 52% of all points wins about 69% of their matches. This is because more points being played reduces the effects of luck.
- **The deuce rule barely changes who wins.** Switching the deuce rule from advantage to golden point changes the stronger team's chance of winning by only 1.7 percentage points, because only around 28% of games ever reach 40-40.
- **Star Point is almost identical to advantage.** The new 2026 FIP Star Point rule gives match-win probabilities within 0.3 percentage points of advantage. This means the new rule is likely just to shorten matches, with very little effect on match outcomes.

## How it works

The model assumes every point is independent and that each team wins a point on their own serve with a fixed probability. The score is treated as the state of a Markov chain, and the probability of a team winning the game from any score is determined by conditioning on who wins the next point and working backwards from the end of the game.

My probabilities build up to entire matches. Points win games, games win sets (including tiebreaks), and sets win the match. Under advantage rules, deuce can loop back on itself forever, so simple recursion would never finish. I solved this with an equation instead.

To check my maths, I created a separate Monte Carlo simulator that plays matches point by point. Across all three deuce rules and a range of win probabilities, the simulated and exact win probabilities agree within sampling error.

## Repository structure

| File | Contents |
|---|---|
| `padel.py` | Exact Markov chain model for games, tiebreaks, sets and matches |
| `simulate.py` | Monte Carlo simulator for the same scoring rules |
| `03_results.ipynb` | Model checks and main results |
| `01_exact_model_workings.ipynb` | Working notes from building the exact model |
| `02_simulator_workings.ipynb` | Working notes from building the simulator |


## Running it

```
git clone https://github.com/willcallo/Padel-Markov.git
cd Padel-Markov
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Mac/Linux
pip install -r requirements.txt
```

Then open `03_results.ipynb` and run all cells.

## Next steps

The model assumes points are independent with fixed probabilities. I'm currently collecting point-by-point data from University of Bath NUPL matches and internal recreational tournaments to estimate real serve probabilities at university level and test whether points really are independent. An example of this is whether players perform differently on break points or if they perform better when they build up momentum.

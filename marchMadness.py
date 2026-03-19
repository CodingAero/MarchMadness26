import random
from mensBracket import east, west, south, midwest
# from womensBracket import east, west, south, midwest

temperature = 0.15

def get_weight(t):
    win_pct = t['wins'] / (t['wins'] + t['losses'])
    # rank_factor: lower rank (1) gives higher weight
    return ((win_pct * 20) / (1 + t['rank']/50)) * random.uniform(1.0-temperature, 1.0+temperature)

def balance_weights(w1, w2):
    weight1 = w1 / (w1 + w2)
    weight2 = w2 / (w1 + w2)
    return [weight1, weight2]

def play_game(team1, team2):
    """
    Simulates a game using a composite of win percentage and rank.
    """
    w1, w2 = get_weight(team1), get_weight(team2)
    w_list = balance_weights(w1, w2)
    winner = random.choices([team1, team2], weights=w_list, k=1)[0]
    # print(f'''
    # {team1['name']}
    #         |________ {winner['name']}
    #         |
    # {team2['name']}
    # ''')
    return winner

def run_region(region_teams):
    """
    Simulates a region bracket using standard NCAA seeding matchups.

    Expects `region_teams` to be a list of 16 teams ordered by seed (1 through 16).
    """
    region_winners = []

    # Round of 64: seed-based pairings (indices are 0-based)
    first_round_pairings = [
        (0, 15),  # 1 vs 16
        (7, 8),   # 8 vs 9
        (4, 11),  # 5 vs 12
        (3, 12),  # 4 vs 13
        (5, 10),  # 6 vs 11
        (2, 13),  # 3 vs 14
        (6, 9),   # 7 vs 10
        (1, 14),  # 2 vs 15
    ]

    round_winners = []
    for a, b in first_round_pairings:
        round_winners.append(play_game(region_teams[a], region_teams[b]))
    
    region_winners.append(round_winners)

    # Advance through remaining rounds using standard bracket pairing order
    while len(round_winners) > 1:
        next_round = []
        for i in range(0, len(round_winners), 2):
            next_round.append(play_game(round_winners[i], round_winners[i + 1]))
        round_winners = next_round
        region_winners.append(round_winners)

    for i in range(len(region_winners[0])):
        print(region_winners[0][i]['name'])
    return round_winners[0]

# Final Four Simulation
final_four = [run_region(east), run_region(west), run_region(south), run_region(midwest)]
champ_game = [play_game(final_four[0], final_four[1]), play_game(final_four[2], final_four[3])]
winner = play_game(champ_game[0], champ_game[1])

print(f"The 2026 National Champion is: {winner['name']}")
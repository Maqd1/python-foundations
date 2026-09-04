'''
Core 3

✊ HARD ROCK PAPER SCISSORS

The Tournament Edition with AI Learning 🤖

Create an advanced Rock-Paper-Scissors game with tournament mode and AI that learns!

Game Mechanics:

1. Modes:
   · Quick Match (Best of 3)
   · Tournament (Best of 5 against 5 different AI opponents)
   · Endless Mode (Play until someone wins by 5 points)
2. Weapons System (HARD):
   · Classic: Rock ✊, Paper ✋, Scissors ✌️
   · Advanced: Add Lizard 🦎 and Spock 🖖
   · Rules:
     · Rock crushes Scissors, crushes Lizard
     · Paper covers Rock, disproves Spock
     · Scissors cuts Paper, decapitates Lizard
     · Lizard poisons Spock, eats Paper
     · Spock smashes Scissors, vaporizes Rock
3. AI Opponents with Personalities:
   ```python
   opponents = {
       "Beginner Bob": {
           "strategy": "random",
           "pattern": None,
           "win_rate": 0.3
       },
       "Pattern Paula": {
           "strategy": "pattern_match",
           "pattern": ["rock", "paper", "scissors"],
           "win_rate": 0.6
       },
       "Mind Reader Mike": {
           "strategy": "predictive",
           "player_history": [],
           "win_rate": 0.8
       }
   }
   ```
4. AI Strategies (HARDEST PART):
   · Random: Picks randomly (easy)
   · Pattern Match: Detects if player is following a pattern
   · Predictive: Analyzes player's previous moves and picks counter
   · Adaptive: Learns from mistakes and adjusts
5. Statistics Tracking:
   · Win/loss/draw counts
   · Favorite weapons (most used)
   · Win rate per weapon
   · Longest winning streak

Sample Output:

```
👊 ROCK PAPER SCISSORS TOURNAMENT 👊

Select Mode:
1. Quick Match (Best of 3)
2. Tournament (5 opponents)
3. Endless Mode

Choice: 2

🏆 TOURNAMENT MODE 🏆
Your opponents:
1. Beginner Bob (Easy)
2. Pattern Paula (Medium)
3. Mind Reader Mike (Hard)
4. Adaptive Alice (Expert)
5. Random Rex (Random)

🎯 Match 1/5: vs Beginner Bob
Best of 3

Round 1: Enter (r/p/s/l/sp): r
You: ✊ | Bob: ✌️
You win! 🎉
Score: You 1-0 Bob

Round 2: Enter (r/p/s/l/sp): p
You: ✋ | Bob: ✊
You win! 🎉
Score: You 2-0 Bob

🏆 You defeated Beginner Bob! (2-0)

🎯 Match 2/5: vs Pattern Paula
Best of 3

Round 1: Enter (r/p/s/l/sp): r
You: ✊ | Paula: 🖖
You lose! 😢
Score: You 0-1 Paula

Round 2: Enter (r/p/s/l/sp): r
You: ✊ | Paula: 🖖
You lose again! 🤔
Score: You 0-2 Paula

💀 You lost to Pattern Paula! (0-2)

📊 TOURNAMENT RESULTS:
Wins: 1/5
Overall Score: 1-4

Would you like to see detailed stats? (y/n): y

📈 STATISTICS:
Total games: 5
Wins: 1 (20%)
Losses: 4 (80%)
Draws: 0

Weapon usage:
- Rock: 3 (60%)
- Paper: 1 (20%)
- Scissors: 0 (0%)
- Lizard: 0 (0%)
- Spock: 1 (20%)

Win rate by weapon:
- Rock: 33%
- Paper: 0%
- Spock: 0%

Longest streak: 2 wins
Current streak: 0 wins
```

Concepts Tested: Dictionaries, nested data structures, functions with complex logic, while loops, for loops, break, continue, pass, list operations (appending, counting), conditional logic, scope, random module, pattern detection

---
'''



import random

WEAPONS = ["rock", "paper", "scissors", "lizard", "spock"]

SHORTCUTS = {
    "r": "rock", "rock": "rock",
    "p": "paper", "paper": "paper",
    "s": "scissors", "scissors": "scissors",
    "l": "lizard", "lizard": "lizard",
    "sp": "spock", "spock": "spock",
}

EMOJI = {
    "rock": "\u270a",
    "paper": "\u270b",
    "scissors": "\u270c\ufe0f",
    "lizard": "\U0001f98e",
    "spock": "\U0001f596",
}

# weapon -> list of weapons it beats
BEATS = {
    "rock": ["scissors", "lizard"],
    "paper": ["rock", "spock"],
    "scissors": ["paper", "lizard"],
    "lizard": ["spock", "paper"],
    "spock": ["scissors", "rock"],
}


def make_opponents():
    """Fresh opponent dicts each session, so histories don't leak between games."""
    return {
        "Beginner Bob": {
            "strategy": "random", "difficulty": "Easy", "win_rate": 0.3,
            "pattern": None, "player_history": [], "ai_history": [], "results_history": [],
        },
        "Pattern Paula": {
            "strategy": "pattern_match", "difficulty": "Medium", "win_rate": 0.6,
            "pattern": ["rock", "paper", "scissors"], "player_history": [], "ai_history": [], "results_history": [],
        },
        "Mind Reader Mike": {
            "strategy": "predictive", "difficulty": "Hard", "win_rate": 0.8,
            "pattern": None, "player_history": [], "ai_history": [], "results_history": [],
        },
        "Adaptive Alice": {
            "strategy": "adaptive", "difficulty": "Expert", "win_rate": 0.85,
            "pattern": None, "player_history": [], "ai_history": [], "results_history": [],
        },
        "Random Rex": {
            "strategy": "random", "difficulty": "Random", "win_rate": 0.5,
            "pattern": None, "player_history": [], "ai_history": [], "results_history": [],
        },
    }


stats = {
    "wins": 0,
    "losses": 0,
    "draws": 0,
    "weapon_usage": {w: 0 for w in WEAPONS},
    "weapon_wins": {w: 0 for w in WEAPONS},
    "current_streak": 0,
    "longest_streak": 0,
}


def reset_opponent_history(opponent):
    opponent["player_history"] = []
    opponent["ai_history"] = []
    opponent["results_history"] = []


def counter_move(move):
    """Returns a random weapon that beats the given move."""
    counters = [w for w in WEAPONS if move in BEATS[w]]
    return random.choice(counters)


def detect_player_pattern(history):
    """Looks for a simple repeating cycle (period 2 or 3) in recent player moves."""
    if len(history) >= 2 and history[-1] == history[-2]:
        return history[-1]
    for period in (2, 3):
        if len(history) >= period * 2:
            recent = history[-period * 2:]
            if recent[:period] == recent[period:]:
                return recent[0]
    return None


def ai_random_move(opponent):
    return random.choice(WEAPONS)


def ai_pattern_match_move(opponent):
    detected = detect_player_pattern(opponent["player_history"])
    if detected:
        return counter_move(detected)
    idx = len(opponent["player_history"]) % len(opponent["pattern"])
    return opponent["pattern"][idx]


def ai_predictive_move(opponent):
    history = opponent["player_history"]
    if not history:
        return random.choice(WEAPONS)
    most_common = max(set(history), key=history.count)
    return counter_move(most_common)


def ai_adaptive_move(opponent):
    """Learns from her own losses: counters whatever move just beat her."""
    results = opponent["results_history"]
    history = opponent["player_history"]

    if results and results[-1] == "player_win" and history:
        return counter_move(history[-1])
    elif results and results[-1] == "ai_win":
        pass  # working strategy is winning — stick with the frequency-based approach below

    if history:
        most_common = max(set(history), key=history.count)
        return counter_move(most_common)
    return random.choice(WEAPONS)


def get_ai_move(opponent):
    strategy = opponent["strategy"]
    if strategy == "random":
        return ai_random_move(opponent)
    elif strategy == "pattern_match":
        return ai_pattern_match_move(opponent)
    elif strategy == "predictive":
        return ai_predictive_move(opponent)
    elif strategy == "adaptive":
        return ai_adaptive_move(opponent)
    return random.choice(WEAPONS)


def determine_round_winner(player_move, ai_move):
    if player_move == ai_move:
        return "draw"
    if ai_move in BEATS[player_move]:
        return "player"
    return "ai"


def get_valid_player_move():
    while True:
        raw = input("Enter (r/p/s/l/sp) or 'quit': ").strip().lower()
        if raw == "quit":
            return "quit"
        if raw in SHORTCUTS:
            return SHORTCUTS[raw]
        print("Invalid input. Use r, p, s, l, or sp.")


def update_stats(player_move, result):
    stats["weapon_usage"][player_move] += 1
    if result == "player":
        stats["wins"] += 1
        stats["weapon_wins"][player_move] += 1
        stats["current_streak"] += 1
        stats["longest_streak"] = max(stats["longest_streak"], stats["current_streak"])
    elif result == "ai":
        stats["losses"] += 1
        stats["current_streak"] = 0
    else:
        stats["draws"] += 1
        stats["current_streak"] = 0


def play_round(opponent, opponent_name):
    player_move = get_valid_player_move()
    if player_move == "quit":
        return "quit"

    ai_move = get_ai_move(opponent)

    result = determine_round_winner(player_move, ai_move)

    opponent["player_history"].append(player_move)
    opponent["ai_history"].append(ai_move)
    opponent["results_history"].append(
        "player_win" if result == "player" else "ai_win" if result == "ai" else "draw"
    )

    print(f"You: {EMOJI[player_move]} | {opponent_name}: {EMOJI[ai_move]}")
    if result == "player":
        print("You win! \U0001f389")
    elif result == "ai":
        print("You lose! \U0001f622")
    else:
        print("It's a draw! \U0001f91d")

    update_stats(player_move, result)
    return result


def play_match(opponent, opponent_name, wins_needed):
    """Plays rounds until one side reaches wins_needed. Returns (player_won, p_score, a_score)."""
    reset_opponent_history(opponent)
    p_score = 0
    a_score = 0
    round_num = 1

    while p_score < wins_needed and a_score < wins_needed:
        print(f"\nRound {round_num}:", end=" ")
        result = play_round(opponent, opponent_name)
        if result == "quit":
            print(f"\nYou conceded the match against {opponent_name}.")
            return False, p_score, a_score

        if result == "player":
            p_score += 1
        elif result == "ai":
            a_score += 1

        print(f"Score: You {p_score}-{a_score} {opponent_name}")
        round_num += 1

    player_won = p_score > a_score
    if player_won:
        print(f"\n\U0001f3c6 You defeated {opponent_name}! ({p_score}-{a_score})")
    else:
        print(f"\n\U0001f480 You lost to {opponent_name}! ({p_score}-{a_score})")

    return player_won, p_score, a_score


def choose_opponent(opponents):
    names = list(opponents.keys())
    print("\nChoose your opponent:")
    for i, name in enumerate(names, start=1):
        print(f"{i}. {name} ({opponents[name]['difficulty']})")

    while True:
        raw = input("Choice: ").strip()
        if raw.isdigit() and 1 <= int(raw) <= len(names):
            chosen_name = names[int(raw) - 1]
            return opponents[chosen_name], chosen_name
        print("Invalid choice.")


def quick_match(opponents):
    opponent, name = choose_opponent(opponents)
    print(f"\n\U0001f3af Quick Match: vs {name}\nBest of 3")
    play_match(opponent, name, wins_needed=2)


def tournament_mode(opponents):
    print("\n\U0001f3c6 TOURNAMENT MODE \U0001f3c6")
    print("Your opponents:")
    for i, (name, data) in enumerate(opponents.items(), start=1):
        print(f"{i}. {name} ({data['difficulty']})")

    total_match_wins = 0
    total_p_score = 0
    total_a_score = 0
    match_count = len(opponents)

    for i, (name, opponent) in enumerate(opponents.items(), start=1):
        print(f"\n\U0001f3af Match {i}/{match_count}: vs {name}\nBest of 3")
        won, p_score, a_score = play_match(opponent, name, wins_needed=2)
        total_p_score += p_score
        total_a_score += a_score
        if won:
            total_match_wins += 1

    print("\n\U0001f4ca TOURNAMENT RESULTS:")
    print(f"Wins: {total_match_wins}/{match_count}")
    print(f"Overall Score: {total_p_score}-{total_a_score}")

    see_stats = input("\nWould you like to see detailed stats? (y/n): ").strip().lower()
    if see_stats == "y":
        show_stats()


def endless_mode(opponents):
    opponent, name = choose_opponent(opponents)
    reset_opponent_history(opponent)
    print(f"\n\u267e\ufe0f ENDLESS MODE: vs {name}\nFirst to 5 points wins!")

    p_score = 0
    a_score = 0
    round_num = 1
    while p_score < 5 and a_score < 5:
        print(f"\nRound {round_num}:", end=" ")
        result = play_round(opponent, name)
        if result == "quit":
            print(f"\nYou conceded against {name}.")
            return
        if result == "player":
            p_score += 1
        elif result == "ai":
            a_score += 1
        print(f"Score: You {p_score}-{a_score} {name}")
        round_num += 1

    if p_score > a_score:
        print(f"\n\U0001f3c6 You won Endless Mode against {name}! ({p_score}-{a_score})")
    else:
        print(f"\n\U0001f480 {name} won Endless Mode! ({p_score}-{a_score})")


def show_stats():
    total = stats["wins"] + stats["losses"] + stats["draws"]
    print("\n\U0001f4c8 STATISTICS:")
    print(f"Total games: {total}")
    if total == 0:
        print("No games played yet.")
        return

    print(f"Wins: {stats['wins']} ({stats['wins'] / total:.0%})")
    print(f"Losses: {stats['losses']} ({stats['losses'] / total:.0%})")
    print(f"Draws: {stats['draws']} ({stats['draws'] / total:.0%})")

    print("\nWeapon usage:")
    for w in WEAPONS:
        used = stats["weapon_usage"][w]
        pct = used / total if total else 0
        print(f"- {w.title()}: {used} ({pct:.0%})")

    print("\nWin rate by weapon:")
    for w in WEAPONS:
        used = stats["weapon_usage"][w]
        if used == 0:
            continue
        win_rate = stats["weapon_wins"][w] / used
        print(f"- {w.title()}: {win_rate:.0%}")

    print(f"\nLongest streak: {stats['longest_streak']} wins")
    print(f"Current streak: {stats['current_streak']} wins")


def main():
    opponents = make_opponents()
    print("\U0001f44a ROCK PAPER SCISSORS TOURNAMENT \U0001f44a")

    while True:
        print("\nSelect Mode:")
        print("1. Quick Match (Best of 3)")
        print("2. Tournament (5 opponents)")
        print("3. Endless Mode")
        print("4. View Stats")
        print("5. Exit")
        choice = input("Choice: ").strip()

        if choice == "1":
            quick_match(opponents)
        elif choice == "2":
            tournament_mode(opponents)
        elif choice == "3":
            endless_mode(opponents)
        elif choice == "4":
            show_stats()
        elif choice == "5":
            print("Thanks for playing! \U0001f44b")
            break
        else:
            print("Invalid choice.")
            continue


if __name__ == "__main__":
    main()
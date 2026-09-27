# ✊ Hard Rock Paper Scissors

## Tournament Edition with AI Learning 🤖

Create an advanced Rock-Paper-Scissors game with multiple game modes, an expanded weapon system, AI opponents, and statistics tracking.

## Game Modes

### 1. Quick Match

* Best of 3 rounds.

### 2. Tournament

* Play against **5 different AI opponents**.
* Each opponent has a different personality and strategy.
* Track tournament results.

### 3. Endless Mode

* Continue playing until either the player or AI wins by **5 points**.

## Weapons System

### Classic Weapons

* Rock ✊
* Paper ✋
* Scissors ✌️

### Advanced Weapons

Add:

* Lizard 🦎
* Spock 🖖

### Rules

* Rock crushes Scissors.
* Rock crushes Lizard.
* Paper covers Rock.
* Paper disproves Spock.
* Scissors cuts Paper.
* Scissors decapitates Lizard.
* Lizard poisons Spock.
* Lizard eats Paper.
* Spock smashes Scissors.
* Spock vaporizes Rock.

## AI Opponents

Create AI opponents with different personalities and strategies.

Example:

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

## AI Strategies — Hardest Part

Implement different AI strategies.

### Random

The AI chooses a weapon randomly.

### Pattern Match

The AI detects whether the player is following a pattern and attempts to exploit it.

### Predictive

The AI analyzes the player's previous moves and chooses a counter.

### Adaptive

The AI learns from mistakes and adjusts its strategy during the game.

## Statistics Tracking

Track:

* Win count
* Loss count
* Draw count
* Favorite weapons
* Weapon usage
* Win rate for each weapon
* Longest winning streak
* Current winning streak

## Sample Output

```text
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

## Concepts Tested

* Dictionaries
* Nested data structures
* Functions with complex logic
* `while` loops
* `for` loops
* `break`
* `continue`
* `pass`
* List operations
* `append()`
* `count()`
* Conditional logic
* Variable scope
* `random` module
* Pattern detection
* Statistics tracking

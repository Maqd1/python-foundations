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
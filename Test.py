import Agent 
import Game
#note: it takes > 5 hours to finish running on my computer
count0 = {}# results of random agent
count1 = {}# results of mcts agent with random simulation
count2 = {}# results of mcts agent with heuristic based simulation
count3 = {}# results of simple reflex heuristic agent
for i in range(10000):
    r = Agent.RandomAgent()
    game = Game.BlackJackGame()
    result = game.playGame(r)
    if result == 1:
        if "win" not in count0.keys():
            count0["win"] = 0
        count0["win"] += 1
    if result == 0:
        if "draw" not in count0.keys():
            count0["draw"] = 0
        count0["draw"] += 1
    if result == -1:
        if "lose" not in count0.keys():
            count0["lose"] = 0
        count0["lose"] += 1

for i in range(10000):
    mctsr = Agent.MCTSAgent('r')
    game = Game.BlackJackGame()
    result = game.playGame(mctsr)
    if result == 1:
        if "win" not in count1.keys():
            count1["win"] = 0
        count1["win"] += 1
    if result == 0:
        if "draw" not in count1.keys():
            count1["draw"] = 0
        count1["draw"] += 1
    if result == -1:
        if "lose" not in count1.keys():
            count1["lose"] = 0
        count1["lose"] += 1

for i in range(10000):
    mctsh = Agent.MCTSAgent('h')
    game = Game.BlackJackGame()
    result = game.playGame(mctsh)
    if result == 1:
        if "win" not in count2.keys():
            count2["win"] = 0
        count2["win"] += 1
    if result == 0:
        if "draw" not in count2.keys():
            count2["draw"] = 0
        count2["draw"] += 1
    if result == -1:
        if "lose" not in count2.keys():
            count2["lose"] = 0
        count2["lose"] += 1
        
for i in range(10000):
    h = Agent.HeuristicBasedAgent()
    game = Game.BlackJackGame()
    result = game.playGame(h)
    if result == 1:
        if "win" not in count3.keys():
            count3["win"] = 0
        count3["win"] += 1
    if result == 0:
        if "draw" not in count3.keys():
            count3["draw"] = 0
        count3["draw"] += 1
    if result == -1:
        if "lose" not in count3.keys():
            count3["lose"] = 0
        count3["lose"] += 1
print("The result of the random agent is: ", count0)
print("The result of the mcts agent with random simulation is: ", count1)
print("The results of mcts agent with heuristic based simulation is: ", count2)
print("The result of the simple reflex heuristic agent is: ", count3)

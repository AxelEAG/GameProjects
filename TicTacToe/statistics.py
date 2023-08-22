import pandas as pd
from TicTacToe import tictactoeAI as ttt

data = pd.DataFrame(columns=["Draws", "X Wins", "O Wins"])
amount_bots = 4
repetitions = 1000

bots = {2: "Random", 3: "ChooseWin", 4: "ChooseWinAvoidLose", 5: "MiniMax"}
bots_names = {2: "RD", 3: "CW", 4: "CWAL", 5: "MM"}

for i in range(2, 2 + amount_bots):
    for j in range(2, 2 + amount_bots):
        tally = ttt.repeated_battles(i, j, repetitions, True)
        data.loc[f"{bots_names[i]} vs {bots_names[j]}"] = ([int(tally[None]), int(tally["X"]), int(tally["O"])])

print(data)
data.to_csv("statistics.csv")

# data.DataFrame.to_csv




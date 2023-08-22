import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("statistics.csv") #, index_col=[0])
data.index.name = "Duel X vs O"
print(data)
figure, axis = plt.subplots(4, 4, figsize=(7, 7))

for n in range(data.index.size):
    x = []
    for cols in range(1, 4):
        x.append(data.iloc[n][cols])
    ax = axis[int(n/4), n % 4]
    ax.bar(["Draw", "Win", "Lose"], x)
    ax.grid(which="major", axis="y", linewidth=1)
    ax.grid(which="minor", axis="y", linewidth=0.5)
    ax.minorticks_on()
    ax.set_ylim([0, 1000])
    ax.set_title(data.iloc[n][0]) #, fontsize=8)

figure.tight_layout(pad=2.0)
plt.show()

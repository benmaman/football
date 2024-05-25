import pandas as pd
import numpy as np
import operator
from flask import Flask, request, render_template, redirect, url_for
app = Flask(__name__)


class Team():
    def __init__(self,num_players):
        self.num_players=num_players
        self.players=[]
        self.scores=[]
        return
    
    def add_player(self,player,score):
        self.players.append(player)
        self.scores.append(score)
        self.num_players+=1
    
    def add_goalkeeper(self,player):
        self.players.append(player)
        self.num_players+=1

#user params
total_players=18
num_teams=2

#script
players_per_team = total_players // num_teams
teams = []

#assign teams
for i in range(num_teams):
    teams.append(Team(num_players=0))





df=pd.read_csv(r'player_stats.csv')
goal_keeper=list(df[df['goalkeeper'] ==1].sample(num_teams)['player'])
df = df[df['goalkeeper'] != 1]
df=df.sample(total_players-num_teams)
df=df.sort_values(by='score',ascending=False)
team_index = 0

for score  in range(4, 0, -1):
    same_score_players=df[df['score']==score ]["player"].values
    np.random.shuffle(same_score_players)
    teams.sort(key=operator.attrgetter('num_players'))

    for player in same_score_players:
        teams.sort(key=lambda x: x.num_players, reverse=False)  # Sort descending
        teams[team_index].add_player(player, score)


#add goalkeepers
for i in range(num_teams):
    teams[i].add_goalkeeper(goal_keeper[i])
# Output the teams' composition
for index, team in enumerate(teams):
    print(f"Team {index + 1}: Number of Players = {team.num_players}")
    print(f"Players: {team.players}")
    print(f"Scores: {np.mean(team.scores)}")


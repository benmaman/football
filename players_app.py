from flask import Flask, request, render_template, redirect, url_for
import pandas as pd
import numpy as np
import operator

players_app = Flask(__name__)

class Team():
    def __init__(self, num_players=0):
        self.num_players = num_players
        self.players = []
        self.scores = []

    def add_player(self, player, score):
        self.players.append(player)
        self.scores.append(score)
        self.num_players += 1
    
    def add_goalkeeper(self, player):
        self.players.append(player)
        self.num_players += 1

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file:
            df = pd.read_csv(file)
            process_data(df)
            return redirect(url_for('results'))
    return render_template('upload.html')

def process_data(df):
    num_teams = 2  # This could be made dynamic by user input
    total_players = 18  # As above, could be user input

    teams = [Team(num_players=0) for _ in range(num_teams)]
    goal_keeper = list(df[df['goalkeeper'] == 1].sample(num_teams)['player'])
    df = df[df['goalkeeper'] != 1]
    df = df.sample(total_players - num_teams)
    df = df.sort_values(by='score', ascending=False)
    
    team_index = 0
    for score in range(4, 0, -1):
        same_score_players = df[df['score'] == score]["player"].values
        np.random.shuffle(same_score_players)
        for player in same_score_players:
            teams.sort(key=operator.attrgetter('num_players'))
            teams[0].add_player(player, score)

    for i in range(num_teams):
        teams[i].add_goalkeeper(goal_keeper[i])
    
    # Store results globally or use database/session
    global results
    results = [(team.num_players, team.players, np.mean(team.scores)) for team in teams]

@app.route('/results')
def results():
    global results
    return render_template('results.html', results=results)

if __name__ == '__main__':
    players_app.run(debug=True)

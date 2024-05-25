from flask import Flask, request, render_template, redirect, url_for, flash
import pandas as pd
import numpy as np
import operator

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Needed for session management and flash messages

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
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        num_teams = int(request.form['num_teams'])
        total_players = int(request.form['total_players'])
        if file:
            df = pd.read_csv(file)
            if not process_data(df, num_teams, total_players):
                flash('Error processing data. Please check your CSV and numbers of teams/players.')
                return redirect(request.url)
            return redirect(url_for('results'))
    return render_template('upload.html')

def process_data(df, num_teams, total_players):
    if len(df) < total_players:
        return False  # Not enough players in the CSV to form teams
    teams = [Team(num_players=0) for _ in range(num_teams)]
    goal_keeper = list(df[df['goalkeeper'] == 1].sample(n=num_teams, replace=False)['player'])
    df = df[df['goalkeeper'] != 1]
    df = df.sample(n=total_players - num_teams, replace=False)
    df = df.sort_values(by='score', ascending=False)
    
    for score in range(4, 0, -1):
        same_score_players = df[df['score'] == score]["player"].values
        np.random.shuffle(same_score_players)
        for player in same_score_players:
            teams.sort(key=operator.attrgetter('num_players'))
            teams[0].add_player(player, score)

    for i in range(num_teams):
        teams[i].add_goalkeeper(goal_keeper[i])
    
    global results
    results = [(team.num_players, team.players, np.mean(team.scores)) for team in teams]
    return True

@app.route('/results')
def results():
    global results
    return render_template('results.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)

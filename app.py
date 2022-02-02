import os
import json
import subprocess

from scores import Score, Scores
from flask import Flask, request, render_template, send_from_directory, redirect
import config
app = Flask(__name__)

groups_file = os.path.expanduser(config.groups_file)
submissions_path = os.path.expanduser(config.submissions_path)
scores_path = os.path.expanduser(config.scores_file)
groups = json.loads(open(groups_file, 'r').read())
# print(groups)
scores = Scores(scores_path)


@app.route("/submissions/<group_id>/files", defaults={"u_path": ""})
@app.route("/submissions/<group_id>/files/<path:u_path>")
def serve_html(group_id, u_path):
    s_path = ''

    if '/' in u_path:
        s_path = '/' + u_path.rsplit('/', 1)[0]
        u_path = u_path.rsplit('/', 1)[1]
    return send_from_directory(f'{submissions_path}/{group_id}{s_path}', u_path)


@app.route('/')
def view_list():
    # projects = os.listdir(os.path.expanduser(config.submissions_path))
    return render_template('list.html', groups=groups, scores=scores)


@app.route('/submissions/<group_id>/score', methods=['POST'])
def score_submission(group_id):
    scores.save_score(group_id, json.loads(request.data))
    return 'ok'


@app.route('/submissions/<group_id>/open')
def open_folder(group_id):
    subprocess.Popen(["open", submissions_path + '/' + group_id])


@app.route('/submissions/<group_id>/next')
def next_submission(group_id):
    index = next(i for i,v in enumerate(groups) if v["id"] == group_id)
    next_group = groups[(index + 1 )% len(groups)]
    return redirect('/submissions/' + next_group["id"])


@app.route('/submissions/<group_id>/prev')
def prev_submission(group_id):
    index = next(i for i, v in enumerate(groups) if v["id"] == group_id)
    next_group = groups[(index - 1) % len(groups)]
    return redirect('/submissions/' + next_group["id"])


@app.route('/submissions/<group_id>')
def view_submission(group_id):
    g = scores.get(group_id)
    return render_template('submission.html', group=g, score=g)


@app.route('/submissions', methods=['POST'])
def grade_submission(group_id):
    return request.json

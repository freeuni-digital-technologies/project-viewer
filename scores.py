import json
from json import JSONEncoder


class Score:
    def __init__(self, dct_or_team_id):
        if isinstance(dct_or_team_id, str):
            self.id = dct_or_team_id
            self.design = 0
            self.functionality = 0
            self.report = 0
            self.concept = 0
            self.comment = ''
        else:
            self.id = dct_or_team_id["id"]
            self.design = dct_or_team_id["design"]
            self.functionality = dct_or_team_id["functionality"]
            self.report = dct_or_team_id["report"]
            self.concept = dct_or_team_id["concept"]
            self.comment = dct_or_team_id["comment"]


class ScoreEncoder(JSONEncoder):
    def default(self, score: Score):
        return score.__dict__


class Scores:
    def __init__(self, filename):
        self.filename = filename
        try:
            self.scores: [Score] = list(map(Score, json.loads(open(filename, 'r').read())))
        except FileNotFoundError:
            self.scores = []
        except json.decoder.JSONDecodeError:
            self.scores = []

    def get(self, team_id):
        try:
            n = next(s for s in self.scores if s.id == team_id)
        except StopIteration:
            n = Score(team_id)
            self.scores.append(n)
            self.save_file()
        return n

    def save_score(self, group_id, score_dict):
        try:
            index = self.get_index(group_id)
        except StopIteration:
            self.scores.append(Score(group_id))
            index = self.get_index(group_id)
        for k in score_dict.keys():
            if k == 'comment':
                value = score_dict[k]
            else:
                value = int(score_dict[k])
            setattr(self.scores[index], k, value)
        self.save_file()

    def get_total(self, team_id):
        n = self.get(team_id)
        return str(n.functionality + n.report + n.design + n.concept)

    def get_index(self, team_id):
        return next(i for (i, s) in enumerate(self.scores) if s.id == team_id)

    def save(self, team_id, score: Score):
        index = self.get_index(team_id)
        self.scores[index] = score
        self.save_file()

    def save_file(self):
        open(self.filename, 'w').write(json.dumps(self.scores, cls=ScoreEncoder))
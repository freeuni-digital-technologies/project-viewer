from dataclasses import dataclass
import os
import logging


@dataclass
class ProjectPaths:
    scores_file: str = ''
    submissions_path: str = ''
    groups_file: str = ''


def project_paths(data_path: str = '~/dev/dt/data') -> ProjectPaths:
    paths = ProjectPaths()
    data_path = os.path.expanduser(data_path)
    paths.scores_file = data_path + "/manualResults/project_scores.json"
    paths.submissions_path = data_path + "/files"
    paths.groups_file = data_path + "/projects.json"
    return paths


def check_paths(paths: ProjectPaths):
    verify_path_exists(paths.submissions_path)
    verify_path_exists(paths.groups_file)
    verify_path_exists(paths.scores_file)


def verify_path_exists(path: str):
    if not os.path.exists(path):
        logging.error('could not find file ' + path)
        exit(1)

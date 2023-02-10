# Project viewer

## Setup and run
```shell
# installing dependencies
pipenv install 
# or if not using pipenv
python3 -m pip install Flask

# run
pipenv run app
# or
python3 -m flask run
```

## Configuration
App needs these 3 files/directories, specified in `paths.py`
- submissions_path - directory with all the submissions
- scores_file - where to save scores
- groups_file - json file for reading names and ids of groups 


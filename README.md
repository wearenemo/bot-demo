# Getting started

 1. Make sure to have [pipenv](https://pypi.org/project/pipenv/) installed
 1. clone this repo
 1. `cd` into this repo 
 1. `pipenv install`
 1. ask Andy for the token
    1. set as env var with: `export CRAPS_TOKEN="<TOKEN>"`
    1. or edit .env and add `CRAPS_TOKEN="<TOKEN>"`
 1. from project root directory do: `pipenv run python main.py` 

## Contributing
To keep things easy and avoid lots of merge conflicts, let's try to stick to "one person works in `./bot` and one works in `./game` at a time"

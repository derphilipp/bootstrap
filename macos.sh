#!/bin/bash

command -v brew   2>/dev/null >/dev/null || (/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)" && brew tap "caskroom/cask")
command -v pipenv 2>/dev/null >/dev/null || brew install pipenv
pipenv install --three
pipenv run ansible-galaxy install -r requirements.yml  --roles-path=./roles
pipenv run ansible-playbook playbook.yml -i inventory.yml --extra-vars="ansible_python_interpreter=$(pipenv run which python)"
echo "Done"


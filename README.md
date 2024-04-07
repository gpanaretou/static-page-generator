# static-page-generator
Using Python to build a static page generator

## Setup instructions
### For Linux/wsl

Install these dependencies for `pyenv`

`
sudo apt update
sudo apt install -y build-essential zlib1g-dev libssl-dev
sudo apt install -y libreadline-dev libbz2-dev libsqlite3-dev libffi-dev
`

### Install PYENV with WEBI

Run this command to install `pyenv` with webi.

`
curl -sS https://webi.sh/pyenv | sh
`

1. Open your `~/.bashrc` or `~/.zshrc`, or whatever shell you are using 

`nano ~/.bashrc`

2. Add these lines to the bottom of the file in this order (some might already be there):

`
export PYENV_ROOT="$HOME/.pyenv"
command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
`

### Install Python 3
Run this command to install python 3.12.2 with `pyenv`:

`
pyenv install -v 3.12.2
`

Set that version as default:

`
pyenv gloabal -v 3.12.2
`

Lastly, to make sure everything works out:
`
python --version
`
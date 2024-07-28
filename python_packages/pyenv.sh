# https://realpython.com/intro-to-pyenv/

brew install openssl readline sqlite3 xz zlib
brew install pyenv pyenv-virtualenv

pyenv update

pyenv install --list
pyenv install --list | grep " 3\.[678]"
pyenv install -v 3.7.2

pyenv versions
ls ~/.pyenv/versions/

pyenv uninstall 2.7.15
rm -rf ~/.pyenv/versions/2.7.15

pyenv global 3.10.14
pyenv global system
pyenv version
python -V
pyenv which pip

pyenv commands

# Search order:
pyenv shell 3.8-dev   # sets the PYENV_VERSION env
pyenv local 2.7.15    # creates a .python-version file in your current directory
pyenv global 3.10.14  # pyenv global
system python

pyenv virtualenv 3.10.14 exp
pyenv local exp
pyenv activate exp
pyenv deactivate
python -V

# ipykernel
python -m pip install ipykernel
python -m ipykernel install --user

https://docs.anaconda.com/anaconda/

```
# Install Anaconda (macOS, Linux, Windows)
# Download from: https://www.anaconda.com/products/distribution
bash ~/Downloads/Anaconda3-*-MacOSX-x86_64.sh

# Update conda
conda update conda
conda update anaconda

# List available Python versions (conda-forge channel recommended)
conda search "^python$"
conda search "^python$" --channel conda-forge

# Create a new environment with a specific Python version and package
conda create -n myenv python=3.10 ipython

# List environments
conda env list
conda info --envs

# Remove an environment
conda remove --name myenv --all

# Set the default environment to activate automatically on shell startup
echo "conda activate myenv" >> ~/.bashrc
# or for zsh:
echo "conda activate myenv" >> ~/.zshrc

# Activate/deactivate environments
conda activate myenv
conda deactivate

# Check Python version in environment
python -V

# Find path to pip in active environment
which pip

# List available conda commands
conda --help

# Environment search order:
# 1. conda activate <env_name>   # activate specific environment
# 2. conda deactivate           # back to base or system Python

# Create a virtual environment (alternative to conda envs, using venv)
python -m venv myvenv
source myvenv/bin/activate
deactivate

# Install ipykernel in the environment (conda version)
conda install ipykernel
python -m ipykernel install --user --name myenv --display-name "Python (myenv)"
```

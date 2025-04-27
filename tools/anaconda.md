# Anaconda Quick Reference

[Official Anaconda Documentation](https://docs.anaconda.com/anaconda/)

## Installation

- Download the installer from the [Anaconda Distribution page](https://www.anaconda.com/products/distribution)
- Example installation command for macOS:
  ```bash
  bash ~/Downloads/Anaconda3-*-MacOSX-x86_64.sh
  ```

## Update Conda and Anaconda

```bash
conda update conda
conda update anaconda
```

## Python Versions

- List available Python versions (conda-forge channel recommended):

  ```bash
  conda search "^python$"
  conda search "^python$" --channel conda-forge
  ```

## Create a New Environment

- With a specific Python version and package:

  ```bash
  conda create -n myenv python=3.10 ipython
  ```

## Manage Environments

- List environments:

  ```bash
  conda env list
  conda info --envs
  ```

- Remove an environment:

  ```bash
  conda remove --name myenv --all
  ```

- Set the default environment to activate automatically on shell startup:

  ```bash
  echo "conda activate myenv" >> ~/.bashrc
  # or for zsh:
  echo "conda activate myenv" >> ~/.zshrc
  ```

- Activate/deactivate environments:

  ```bash
  conda activate myenv
  conda deactivate
  ```

## Package Management

- Install packages in the current environment:

  ```bash
  conda install numpy pandas matplotlib
  ```

- To install from the conda-forge channel:

  ```bash
  conda install -c conda-forge scikit-learn
  ```

- List installed packages:

  ```bash
  conda list
  ```

- Remove a package:

  ```bash
  conda remove package_name
  ```

## Miscellaneous

- Check Python version in environment:

  ```bash
  python -V
  ```

- Find path to pip in active environment:

  ```bash
  which pip
  ```

- List available conda commands:

  ```bash
  conda --help
  ```

- Install ipykernel in the environment (conda version):

  ```bash
  conda install ipykernel
  python -m ipykernel install --user
  ```

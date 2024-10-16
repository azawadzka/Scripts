"""https://click.palletsprojects.com/en/8.1.x/#documentation"""

import click


@click.group(chain=True)
def cli():
    pass

def validate_version(ctx, param, value):
    """Validate and clean (too many responsibilities but that's just for an example)"""
    VERSIONS = ['gpt-4', 'gpt-4o', 'gpt-o1']
    value = value.lower()
    if value not in VERSIONS:
        raise click.BadParameter(f"Model must be oe of: {VERSIONS}")
    return value

@cli.command()
@click.option('--model', prompt='Which model should be used?', help='The model to use.', envvar='MODEL', callback=validate_version)
def ask_chatgpt(model):
    """Dummy method that should send a request do ChatGPT."""
    click.echo(f"Hello from {model}.")

@cli.command()
def ask_claude():
    """Dummy method that should send a request do Claude."""
    click.secho(f"Hello from Claude.", fg='magenta', blink=True, bold=True)


if __name__ == '__main__':
    """
    python click_.py ask-chatgpt  # functions as arguments; will prompt for model; will use callback
    python click_.py ask-chatgpt --model GPT-o1  # 
    python click_.py ask-chatgpt ask-claude  # chaining
    export MODEL=gpt-4; python click_.py ask-chatgpt  # will use env
    python click_.py ask-claude  # is pink but doesn't blink :(
    """
    cli()



"""Can integrate with setuptools entry_points

from setuptools import setup

setup(
    name='yourscript',
    version='0.1.0',
    py_modules=['yourscript'],
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'yourscript = yourscript:cli',
        ],
    },
)
"""

"""Arguments vs. options

Arguments can do less than options. The following features are only available for options:
- automatic prompting for missing input
- act as flags (boolean or otherwise)
- option values can be pulled from environment variables, arguments can not
- options are fully documented in the help page, arguments are not (this is intentional as arguments might be too specific to be automatically documented)
"""

"""Can gather use multiple clis together
cli = click.CommandCollection(sources=[cli1, cli2])
"""

"""Envs with registered prefixes are recognized automatically if they match option name

@cli.command()
@click.option('--username')
def greet(username):
    click.echo(f"Hello {username}!")

cli(auto_envvar_prefix='GREETER')

export GREETER_USERNAME=John
"""

"""Arguments support object handling

@click.argument('input', type=click.File('rb'))
@click.argument('filename', type=click.Path(exists=True))
"""

"""Testing

from click.testing import CliRunner
from sync import cli

def test_sync():
  runner = CliRunner()
  result = runner.invoke(cli, ['--debug', 'sync'])
  assert result.exit_code == 0
  assert 'Debug mode is on' in result.output
  assert 'Syncing' in result.output
"""

"""Has progressbar, can open apps
"""

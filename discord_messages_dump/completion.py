"""Command completion for discord-dump CLI."""

import os
import click

from discord_messages_dump.cli import cli


def install_completion():
    """Install command completion for bash/zsh."""
    shell = os.environ.get('SHELL', '').split('/')[-1]
    
    if shell not in ('bash', 'zsh'):
        click.echo(f"Unsupported shell: {shell}. Only bash and zsh are supported.")
        return
    
    # Generate completion script
    completion_script = f"""
# discord-dump completion for {shell}
_{shell}_discord_dump_completion() {{
    local IFS=$'\\n'
    local response

    response=$(env COMP_WORDS="${{COMP_WORDS[*]}}" COMP_CWORD=$COMP_CWORD _DISCORD_DUMP_COMPLETE={shell}_complete $1)

    for completion in $response; do
        IFS=',' read type value <<< "$completion"
        if [[ $type == 'dir' ]]; then
            COMPREPLY=( $(compgen -d -- "$value") )
        elif [[ $type == 'file' ]]; then
            COMPREPLY=( $(compgen -f -- "$value") )
        elif [[ $type == 'plain' ]]; then
            COMPREPLY+=($value)
        fi
    done
    return 0
}}

complete -F _{shell}_discord_dump_completion -o nospace discord-dump
"""
    
    # Determine completion file path
    if shell == 'bash':
        completion_file = os.path.expanduser('~/.bash_completion')
    else:  # zsh
        completion_file = os.path.expanduser('~/.zshrc')
    
    # Check if completion already installed
    try:
        with open(completion_file, 'r') as f:
            content = f.read()
            if 'discord-dump completion' in content:
                click.echo(f"Completion for discord-dump already installed in {completion_file}")
                return
    except FileNotFoundError:
        pass
    
    # Append completion script to file
    try:
        with open(completion_file, 'a') as f:
            f.write(completion_script)
        click.echo(f"Completion for discord-dump installed in {completion_file}")
        click.echo(f"Please restart your shell or run 'source {completion_file}' to enable completion")
    except Exception as e:
        click.echo(f"Error installing completion: {str(e)}")


if __name__ == '__main__':
    install_completion()

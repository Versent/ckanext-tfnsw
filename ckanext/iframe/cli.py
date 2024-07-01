import click


@click.group(short_help="iframe CLI.")
def iframe():
    """iframe CLI.
    """
    pass


@iframe.command()
@click.argument("name", default="iframe")
def command(name):
    """Docs.
    """
    click.echo("Hello, {name}!".format(name=name))


def get_commands():
    return [iframe]

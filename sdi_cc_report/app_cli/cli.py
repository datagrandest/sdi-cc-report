import click
from prompt_toolkit.key_binding import KeyBindings

from sdi_cc_report.app_cli import commands


bindings = KeyBindings()

@bindings.add('c-q')
@click.pass_obj
def _(app, event):
    """Exit"""
    commands.on_exit(app)


@click.group(invoke_without_command=True)
@click.pass_obj
@click.pass_context
def cli(ctx, app):
    """Pleasantries CLI"""
    app.bindings = bindings
    app.cli(ctx)


@cli.command()
@click.pass_obj
def repl(app):
    """Start an interactive session"""
    app.cli_repl(app)
    

@cli.command(name='clear')
def on_clear():
    """Clear screen"""
    commands.on_clear()


@cli.command(name='exit')
@click.pass_obj
def on_exit(app):
    """Exit"""
    commands.on_exit(app)


@cli.command(name='test')
@click.pass_obj
def on_test(app):
    """
    > report text
    """
    commands.on_test(app)


@cli.command(name='reports')
@click.argument('files', nargs=-1, default=None)
@click.option('--csv', '-c', default='', multiple=False, type=str, help='Filename to save data to CSV')
@click.option('--export', '-e', default=None, type=str, help='Filename to export result')
@click.pass_obj
def on_reports(app, files, csv, export):
    """
    > reports [FILES] [--csv CVS] [--export EXPORT]

    Affiche la liste des fichiers disponibles ou les informations du ou des fichiers indiqués par FILES
    """
    commands.on_reports(app, files, csv, export)


@cli.command(name='errors')
@click.argument('file', nargs=-1)
@click.option('--csv', '-c', default='', multiple=False, type=str, help='Filename to save data to CSV')
@click.option('--search', '-s', default='', multiple=False, type=str, help='Search query to filter layers list')
@click.option('--workspace', '-ws', default='', multiple=False, type=str, help='Filter layers list according workspace name (if report type is WMS or WFS)')
@click.option('--name', '-n', default='', multiple=False, type=str, help='Filter layers list according name layer')
@click.option('--id', '-i', default=None, multiple=False, help='Id of layers to display')
@click.option('--limit', '-l', default='10', type=str, help='Number of layers to return')
@click.option('--export', '-e', default=None, type=str, help='Filename to export result')
@click.pass_obj
def on_errors(app, file, csv, search, workspace, name, id, limit, export):
    """
    > errors [FILE] [--csv CSV] [--search SEARCH] [--workspace WS] [--id ID] [--limit LIMIT] [--export EXPORT]
    Affiche la liste des erreurs du rapport [FILE]
    """
    commands.on_errors(app, file, csv, search, workspace, name, id, limit, export)


@cli.command(name='layers')
@click.argument('file', nargs=-1)
@click.option('--csv', '-c', default='', multiple=False, type=str, help='Filename to save data to CSV')
@click.option('--search', '-s', default='', multiple=False, type=str, help='Search query to filter layers list')
@click.option('--workspace', '-ws', default='', multiple=False, type=str, help='Filter layers list according workspace name (if report type is WMS or WFS)')
@click.option('--name', '-n', default='', multiple=False, type=str, help='Filter layers list according name layer')
@click.option('--id', '-i', default=None, multiple=False, help='Id of layers to display')
@click.option('--limit', '-l', default='10', type=str, help='Number of layers to return')
@click.option('--export', '-e', default=None, type=str, help='Filename to export result')
@click.pass_obj
def on_layers(app, file, csv, search, workspace, name, id, limit, export):
    """
    > layers [FILE] [--csv CSV] [--search SEARCH] [--workspace WS] [--id ID] [--limit LIMIT] [--export EXPORT]
    Affiche la liste des layers du rapport [FILE]
    """
    commands.on_layers(app, file, csv, search, workspace, name, id, limit, export)


@cli.command(name='ws')
@click.argument('file', nargs=-1)
@click.option('--csv', '-c', default='', multiple=False, type=str, help='Filename to save data to CSV')
@click.option('--search', '-s', default='', multiple=False, type=str, help='Search query to filter workspaces list')
@click.option('--limit', '-l', default='10', type=str, help='Number of workspaces to return')
@click.option('--export', '-e', default=None, type=str, help='Filename to export result')
@click.pass_obj
def on_workspaces(app, file, csv, search, limit, export):
    """
    > ws [FILE] [--csv CSV] [--search SEARCH] [--limit LIMIT] [--export EXPORT]
    Affiche la liste des workspaces du rapport [FILE]
    """
    commands.on_workspaces(app, file, csv, search, limit, export)





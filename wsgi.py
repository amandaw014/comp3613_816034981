import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import User, Competition, Result  # Import the models
from App.main import create_app
from App.controllers import (
    create_user, get_all_users_json, get_all_users, initialize,  # User-related controllers
    create_competition, get_all_competitions, get_competition_results, import_competition_results
)  # Competition-related controllers

# This commands file allows you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database initialized')


'''
User Commands
'''

# Create a user CLI group
user_cli = AppGroup('user', help='User object commands') 

@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli)  # Add the group to the CLI


'''
Competition Commands
'''

# Create a competition CLI group
competition_cli = AppGroup('competition', help='Competition object commands')

@competition_cli.command("create", help="Creates a competition")
@click.argument("name")
@click.argument("date")
@click.argument("description")
def create_competition_command(name, date, description):
    create_competition(name, date, description)
    print(f'Competition "{name}" created!')

@competition_cli.command("list", help="Lists competitions in the database")
@click.argument("format", default="string")
def list_competitions_command(format):
    competitions = get_all_competitions()
    if format == 'string':
        for comp in competitions:
            print(f'{comp}')
    else:
        print([comp.to_json() for comp in competitions])

app.cli.add_command(competition_cli)


'''
Competition Results Commands
'''

# Create a results CLI group
results_cli = AppGroup('result', help='Competition result commands')

@results_cli.command("import", help="Imports competition results from a CSV file")
@click.argument("file_path")
def import_results_command(file_path):
    import_competition_results(file_path)
    print(f'Results imported from {file_path}!')

@results_cli.command("list", help="Lists results for all competitions")
@click.argument("format", default="string")
def list_results_command(format):
    results = get_competition_results()
    if format == 'string':
        for res in results:
            print(res)
    else:
        print([res.to_json() for res in results])

app.cli.add_command(results_cli)


'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))

app.cli.add_command(test)

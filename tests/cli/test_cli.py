import pytest
from typer.testing import CliRunner
from cli.main import app

runner = CliRunner()

def test_list_people_help():
    result = runner.invoke(app, ['list-people', '--help'])
    assert result.exit_code == 0
    assert "Usage" in result.output

def test_list_planets_help():
    result = runner.invoke(app, ['list-planets', '--help'])
    assert result.exit_code == 0
    assert "Usage" in result.output

def test_invalid_command():
    result = runner.invoke(app, ['invalid'])
    assert result.exit_code != 0
    assert "Usage" in result.output or "No such command" in result.output

def test_list_people_parsing(monkeypatch):
    called = {}
    def fake_get_resource(resource, page=1, sort_by=None, search=None):
        called.update(dict(resource=resource, page=page, sort_by=sort_by, search=search))
        return {'results': [], 'count': 0}
    monkeypatch.setattr('cli.main.api_client.get_resource', fake_get_resource)
    result = runner.invoke(app, ['list-people', '--page', '2', '--sort-by', 'name', '--search', 'luke'])
    assert result.exit_code == 0
    assert called['resource'] == 'people'
    assert called['page'] == 2
    assert called['sort_by'] == 'name'
    assert called['search'] == 'luke'

def test_list_planets_parsing(monkeypatch):
    called = {}
    def fake_get_resource(resource, page=1, sort_by=None, search=None):
        called.update(dict(resource=resource, page=page, sort_by=sort_by, search=search))
        return {'results': [], 'count': 0}
    monkeypatch.setattr('cli.main.api_client.get_resource', fake_get_resource)
    result = runner.invoke(app, ['list-planets', '--page', '3', '--sort-by', 'climate', '--search', 'tatooine'])
    assert result.exit_code == 0
    assert called['resource'] == 'planets'
    assert called['page'] == 3
    assert called['sort_by'] == 'climate'
    assert called['search'] == 'tatooine' 
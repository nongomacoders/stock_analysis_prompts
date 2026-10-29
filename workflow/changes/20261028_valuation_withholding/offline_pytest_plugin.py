"""Run local regression checks without any Python network connections."""
import json
import sys
from pathlib import Path

def pytest_sessionstart(session):
    def deny_network(event, args):
        if event in {'socket.connect', 'socket.connect_ex', 'socket.getaddrinfo', 'socket.sendto'}:
            raise PermissionError('Network disabled for local valuation regression tests')
    sys.addaudithook(deny_network)

def pytest_sessionfinish(session, exitstatus):
    reporter=session.config.pluginmanager.getplugin('terminalreporter')
    counts={key:len(items) for key,items in reporter.stats.items()} if reporter else {}
    output=Path(session.config.getoption('basetemp')).parent / (Path(session.config.getoption('basetemp')).name + '-result.json')
    output.write_text(json.dumps({'exit_code':int(exitstatus),'counts':counts,'network':'All Python DNS/connect/sendto denied for the test session'},indent=2),encoding='utf-8')

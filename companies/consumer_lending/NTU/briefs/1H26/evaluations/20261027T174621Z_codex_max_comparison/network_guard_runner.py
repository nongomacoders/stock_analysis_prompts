"""Run approved comparison while prohibiting connections outside OpenRouter.
No changes to the application client, prompts, or model options.
"""
import ipaddress
from pathlib import Path
import runpy
import shutil
import socket
import sys
from urllib.parse import urlsplit

sys.stdout.reconfigure(encoding='utf-8')
resolved = socket.getaddrinfo('openrouter.ai', 443, type=socket.SOCK_STREAM)
allowed_ips = {str(ipaddress.ip_address(item[4][0])) for item in resolved}

def restrict_network(event, args):
    if event == 'urllib.Request':
        url = urlsplit(args[0])
        if url.scheme != 'https' or url.hostname != 'openrouter.ai' or url.port not in (None, 443):
            raise PermissionError('Blocked destination outside explicitly approved OpenRouter HTTPS')
    elif event == 'socket.getaddrinfo':
        host = str(args[0]).lower()
        if host != 'openrouter.ai':
            raise PermissionError('Blocked DNS resolution outside explicitly approved OpenRouter')
    elif event == 'socket.connect':
        address = args[1]
        if not isinstance(address, tuple) or len(address) < 2 or str(address[0]) not in allowed_ips or address[1] != 443:
            raise PermissionError('Blocked socket connection outside resolved OpenRouter HTTPS endpoints')

sys.addaudithook(restrict_network)
print('Network guard: OpenRouter HTTPS only; all other urllib/DNS/socket destinations denied.', flush=True)
try:
    runpy.run_path('scratch/run_ntu_max_comparison.py', run_name='__main__')
finally:
    latest=Path('scratch/ntu_comparison_latest.txt')
    if latest.exists():
        run=Path(latest.read_text(encoding='utf-8').strip())
        shutil.copy2('scratch/run_ntu_openrouter_only.py', run/'network_guard_runner.py')

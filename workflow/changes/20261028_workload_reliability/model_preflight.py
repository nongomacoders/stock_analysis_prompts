"""Read public OpenRouter model metadata; no credentials or company data."""
import json
import urllib.request
from pathlib import Path

url = 'https://openrouter.ai/api/v1/models'
with urllib.request.urlopen(url, timeout=30) as response:
    items = json.load(response)['data']
selected = [m for m in items if m['id'].startswith('google/gemini') or 'deepseek-v4.1-flash' in m['id']]
Path(__file__).with_name('available_models.json').write_text(json.dumps(selected, indent=2), encoding='utf-8')
for item in selected:
    print(json.dumps({key: item.get(key) for key in ('id', 'name', 'context_length', 'pricing', 'supported_parameters')}))

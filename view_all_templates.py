import os
import re

seed_files = [f for f in os.listdir('.') if f.startswith('seed_') and f.endswith('.py')]

print('='*70)
print('ALL TEMPLATES WITH THEIR CURRENT NAMES')
print('='*70)
print()

for seed_file in sorted(seed_files):
    try:
        with open(seed_file, 'r') as f:
            content = f.read()
            title_match = re.search(r'[\'"]title[\'"]\s*:\s*[\'"]([^\'"]+)[\'"]', content)
            if title_match:
                print(f'{seed_file:45} → {title_match.group(1)}')
    except Exception as e:
        pass
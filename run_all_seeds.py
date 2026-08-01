import os
import importlib

print("="*60)
print("RUNNING ALL SEED FILES")
print("="*60)

seed_files = [f.replace('.py', '') for f in os.listdir('.') if f.startswith('seed_') and f.endswith('.py')]
count = 0
failed = []

for seed_name in seed_files:
    try:
        mod = importlib.import_module(seed_name)
        for attr in dir(mod):
            if attr.startswith('seed_') and callable(getattr(mod, attr)):
                getattr(mod, attr)()
                count += 1
                print(f'✅ {seed_name}')
                break
    except Exception as e:
        failed.append(f'{seed_name}: {str(e)[:50]}')
        print(f'❌ {seed_name}: {str(e)[:50]}')

print()
print("="*60)
print(f"✅ {count} seed files executed successfully!")
if failed:
    print(f"❌ {len(failed)} files failed:")
    for f in failed:
        print(f"  - {f}")
print("="*60)
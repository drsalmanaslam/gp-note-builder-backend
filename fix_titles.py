import os
import re

print("="*70)
print("REMOVING 'Assessment' FROM TEMPLATE TITLES")
print("="*70)
print()

# Files to skip
skip_files = ['seed_all_templates.py', 'seed_categories.py', 'seed_db.py', 
              'seed_question_types.py', 'seed_templates.py', 'seed_toggle_templates.py',
              'view_all_templates.py', 'remove_assessment_from_titles.py']

seed_files = [f for f in os.listdir('.') if f.startswith('seed_') and f.endswith('.py')]
seed_files = [f for f in seed_files if f not in skip_files]

count = 0
for seed_file in sorted(seed_files):
    try:
        with open(seed_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find the title
        match = re.search(r'"title": "([^"]+)"', content)
        if not match:
            match = re.search(r"'title': '([^']+)'", content)
        if not match:
            continue
            
        old_title = match.group(1)
        new_title = re.sub(r'\s*Assessment\s*$', '', old_title)
        new_title = re.sub(r'\s*Assessment\s*-\s*', ' - ', new_title)
        new_title = re.sub(r'\s*Assessment\s*', ' ', new_title).strip()
        
        if old_title != new_title:
            # Replace both quote styles
            content = content.replace(f'"{old_title}"', f'"{new_title}"')
            content = content.replace(f"'{old_title}'", f"'{new_title}'")
            
            with open(seed_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ {seed_file:45} → {new_title}")
            count += 1
    except Exception as e:
        print(f"❌ Error with {seed_file}: {e}")

print()
print("="*70)
print(f"Updated {count} files")
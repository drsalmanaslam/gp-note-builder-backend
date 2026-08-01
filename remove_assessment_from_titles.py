import os
import re

# Files to exclude from renaming (keep these as-is)
EXCLUDE_FILES = [
    'seed_all_templates.py',
    'seed_categories.py',
    'seed_db.py',
    'seed_question_types.py',
    'seed_templates.py',
    'seed_toggle_templates.py',
    'seed_toggle_template.py'
]

def remove_assessment_from_title(title):
    """Remove ' Assessment' from the end of a title"""
    # Remove " Assessment" from the end (with space)
    if title.endswith(' Assessment'):
        return title[:-11]  # Remove ' Assessment' (11 characters including space)
    return title

def process_seed_file(filepath):
    """Process a single seed file and replace the title"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find the title
        title_match = re.search(r'[\'"]title[\'"]\s*:\s*[\'"]([^\'"]+)[\'"]', content)
        if not title_match:
            return None, None
        
        old_title = title_match.group(1)
        new_title = remove_assessment_from_title(old_title)
        
        if old_title == new_title:
            return old_title, None  # No change needed
        
        # Replace the title in the content
        new_content = content.replace(f'"{old_title}"', f'"{new_title}"')
        new_content = new_content.replace(f"'{old_title}'", f"'{new_title}'")
        
        # Write back the file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return old_title, new_title
        
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return None, None

def main():
    print("="*70)
    print("REMOVING 'Assessment' FROM TEMPLATE TITLES")
    print("="*70)
    print()
    
    seed_files = [f for f in os.listdir('.') if f.startswith('seed_') and f.endswith('.py')]
    
    # Filter out excluded files
    seed_files = [f for f in seed_files if f not in EXCLUDE_FILES]
    
    changes_made = 0
    no_change = 0
    
    for seed_file in sorted(seed_files):
        old_title, new_title = process_seed_file(seed_file)
        
        if old_title and new_title:
            print(f"✅ {seed_file:45}")
            print(f"   '{old_title}'")
            print(f"   → '{new_title}'")
            print()
            changes_made += 1
        elif old_title and not new_title:
            # print(f"⏭️  {seed_file:45} → No change needed (no 'Assessment' found)")
            no_change += 1
    
    print("="*70)
    print(f"SUMMARY: {changes_made} files updated, {no_change} files unchanged")
    print("="*70)

if __name__ == "__main__":
    main()
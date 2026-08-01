import os
import re

def fix_seed_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Pattern: if existing: update else: create
        # We need to change to: if existing: delete then create (always create)
        
        # Look for the pattern where existing is checked
        if 'if existing:' not in content:
            return False, "No existing check found"
        
        # Find the block that handles existing
        # We'll replace the whole if/else block with delete+create
        
        # This pattern matches the update block
        pattern = r'if existing:\s*\n\s*# Update existing template instead of deleting\s*\n\s*existing\.description = .*?\s*\n\s*existing\.content = .*?\s*\n\s*existing\.category = .*?\s*\n\s*existing\.is_public = .*?\s*\n\s*existing\.updated_at = datetime\.now\(timezone\.utc\)\s*\n\s*db\.commit\(\)\s*\n\s*print\(.*?\)\s*\n\s*new_t = Template\(.*?\)\s*\n\s*db\.add\(new_t\)\s*\n\s*db\.commit\(\)\s*\n\s*print\(.*?\)'
        
        replacement = '''if existing:
    # Delete existing template (full replacement)
    db.delete(existing)
    db.commit()
    print(f"🗑️ Removed old: {t['title']}")

# Create fresh template
new_t = Template(title=t["title"], description=t["description"], category=t["category"], content=t["content"], is_public=True, created_by=admin.id, version=1)
db.add(new_t)
db.commit()
print(f"✅ Template '{t['title']}' created with sections!")'''
        
        new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True, "Fixed"
        else:
            return False, "Pattern not found"
            
    except Exception as e:
        return False, f"Error: {str(e)}"

def main():
    print("="*70)
    print("FIXING SEED FILES TO DELETE + CREATE")
    print("="*70)
    print()
    
    seed_files = [f for f in os.listdir('.') if f.startswith('seed_') and f.endswith('.py')]
    seed_files = [f for f in seed_files if f not in ['seed_all_templates.py', 'seed_db.py', 'seed_categories.py', 'fix_seeds_delete_create.py']]
    
    updated = 0
    skipped = 0
    
    for seed_file in sorted(seed_files):
        success, message = fix_seed_file(seed_file)
        if success:
            print(f"✅ {seed_file} - {message}")
            updated += 1
        else:
            print(f"⏭️  {seed_file} - {message}")
            skipped += 1
    
    print()
    print("="*70)
    print(f"SUMMARY: {updated} files updated, {skipped} files skipped")
    print("="*70)

if __name__ == "__main__":
    main()
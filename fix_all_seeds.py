import os
import re

def fix_seed_file(filepath):
    """Fix seed file to use DELETE + CREATE instead of UPDATE + CREATE"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if it already has the delete pattern
        if 'db.delete(existing)' in content:
            return False, "Already fixed"
        
        # Pattern to match: if existing: update block then create new
        # This pattern handles the inconsistent variable names (t vs template_data)
        pattern = r'(existing = db\.query\(Template\)\.filter\(.*?\)\.first\(\)\s*\n\s*)if existing:\s*\n\s*# Update existing template instead of deleting\s*\n\s*existing\.description = .*?\s*\n\s*existing\.content = .*?\s*\n\s*existing\.category = .*?\s*\n\s*existing\.is_public = .*?\s*\n\s*existing\.updated_at = datetime\.now\(timezone\.utc\)\s*\n\s*db\.commit\(\)\s*\n\s*print\(.*?\)\s*\n\s*(new_template|new_t) = Template\(.*?\)\s*\n\s*db\.add\(\1\)\s*\n\s*db\.commit\(\)\s*\n\s*print\(.*?\)'
        
        # Replace with delete + create
        replacement = r'\1if existing:\n    # Delete existing template (full replacement)\n    db.delete(existing)\n    db.commit()\n    print(f"🗑️ Removed old template")\n\n# Create fresh template\n\2 = Template(title=template_data["title"], description=template_data["description"], category=template_data["category"], content=template_data["content"], is_public=True, created_by=admin.id, version=1)\ndb.add(\2)\ndb.commit()\nprint(f"✅ Template created!")'
        
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
    print("FIXING ALL SEED FILES")
    print("="*70)
    print()
    
    seed_files = [f for f in os.listdir('.') if f.startswith('seed_') and f.endswith('.py')]
    seed_files = [f for f in seed_files if f not in ['seed_all_templates.py', 'seed_db.py', 'seed_categories.py', 'fix_all_seeds.py']]
    
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
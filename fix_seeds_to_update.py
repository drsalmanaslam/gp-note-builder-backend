import os
import re

def fix_seed_file(filepath):
    """Convert seed file from delete+create to update+create"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if it already has the update pattern
        if 'if existing:' in content and 'existing.description' in content:
            return False, "Already updated"
        
        # Find the pattern: "if existing: db.delete(existing); db.commit()"
        # Replace with update pattern
        new_content = re.sub(
            r'if existing:\s+db\.delete\(existing\);\s+db\.commit\(\)',
            '''
    if existing:
        # Update existing template instead of deleting
        existing.description = t["description"]
        existing.content = t["content"]
        existing.category = t["category"]
        existing.is_public = t["is_public"]
        existing.updated_at = datetime.now(timezone.utc)
        db.commit()
        print(f"🔄 Updated: {t['title']}")''',
            content
        )
        
        # Also fix the pattern with newline
        if new_content == content:
            new_content = re.sub(
                r'if existing:\s*\n\s+db\.delete\(existing\)\s*\n\s+db\.commit\(\)',
                '''
    if existing:
        # Update existing template instead of deleting
        existing.description = t["description"]
        existing.content = t["content"]
        existing.category = t["category"]
        existing.is_public = t["is_public"]
        existing.updated_at = datetime.now(timezone.utc)
        db.commit()
        print(f"🔄 Updated: {t['title']}")''',
                content
            )
        
        # Need to also add the import for datetime if not present
        if 'from datetime import datetime, timezone' not in new_content:
            # Add import after the existing imports
            new_content = new_content.replace(
                'from app.models import User, Template, Category',
                'from app.models import User, Template, Category\nfrom datetime import datetime, timezone'
            )
        
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True, "Updated"
        else:
            return False, "Pattern not found"
            
    except Exception as e:
        return False, f"Error: {str(e)}"

def main():
    print("="*70)
    print("FIXING SEED FILES TO UPDATE INSTEAD OF DELETE")
    print("="*70)
    print()
    
    seed_files = [f for f in os.listdir('.') if f.startswith('seed_') and f.endswith('.py')]
    seed_files = [f for f in seed_files if f not in ['seed_all_templates.py', 'seed_db.py', 'seed_categories.py', 'fix_seeds_to_update.py']]
    
    updated = 0
    skipped = 0
    errors = 0
    
    for seed_file in sorted(seed_files):
        success, message = fix_seed_file(seed_file)
        if success:
            print(f"✅ {seed_file}")
            updated += 1
        elif "Already updated" in message:
            print(f"⏭️  {seed_file} - Already updated")
            skipped += 1
        else:
            print(f"⚠️  {seed_file} - {message}")
            skipped += 1
    
    print()
    print("="*70)
    print(f"SUMMARY: {updated} files updated, {skipped} files skipped, {errors} errors")
    print("="*70)

if __name__ == "__main__":
    main()
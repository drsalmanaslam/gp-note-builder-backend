import os
import re

# The admin username to use
NEW_ADMIN = "gpclinicaldirector@notebuilder"

# Files to skip (these don't need updating)
SKIP_FILES = [
    'seed_db.py',
    'seed_categories.py',
    'seed_all_templates.py',
    'seed_templates.py',
    'seed_question_types.py',
    'seed_toggle_template.py',
    'seed_toggle_templates.py',
    'update_all_seeds.py'
]

def update_seed_file(filepath):
    """Update a seed file to use the new admin username"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if it already uses the new admin
        if f'username == "{NEW_ADMIN}"' in content:
            return False, "Already using new admin"
        
        # Check if it uses "admin"
        if 'username == "admin"' not in content:
            return False, "No admin reference found"
        
        # Replace all instances of "admin" username check
        new_content = content.replace(
            'username == "admin"',
            f'username == "{NEW_ADMIN}"'
        )
        
        # Also replace "admin" in comments/print statements where it refers to the user
        # Be careful not to replace "admin" as a role
        # We'll only replace the exact pattern
        
        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True, "Updated"
        
    except Exception as e:
        return False, f"Error: {str(e)}"

def main():
    print("="*70)
    print("UPDATING ALL SEED FILES TO USE gpclinicaldirector@notebuilder")
    print("="*70)
    print()
    
    seed_files = [f for f in os.listdir('.') if f.startswith('seed_') and f.endswith('.py')]
    seed_files = [f for f in seed_files if f not in SKIP_FILES]
    
    updated = 0
    skipped = 0
    errors = 0
    
    for seed_file in sorted(seed_files):
        success, message = update_seed_file(seed_file)
        if success:
            print(f"✅ {seed_file:45} → {message}")
            updated += 1
        elif "Already using" in message:
            print(f"⏭️  {seed_file:45} → Already using {NEW_ADMIN}")
            skipped += 1
        else:
            print(f"⏭️  {seed_file:45} → {message}")
            skipped += 1
    
    print()
    print("="*70)
    print(f"SUMMARY: {updated} files updated, {skipped} files skipped, {errors} errors")
    print("="*70)
    
    # Now handle seed_db.py separately
    print("\n📝 Manually update seed_db.py to remove admin creation:")
    print("Open seed_db.py and comment out or remove the admin creation code.")

if __name__ == "__main__":
    main()
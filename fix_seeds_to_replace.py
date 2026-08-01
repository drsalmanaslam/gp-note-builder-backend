import os
import re

def fix_seed_file(filepath):
    """Convert seed file from update+create to delete+create (full replacement)"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if it already has the delete pattern
        if 'db.delete(existing)' in content:
            return False, "Already using delete+create"
        
        # Find the update pattern and replace with delete+create
        # Pattern: if existing: existing.description = ... then else: create new
        new_content = re.sub(
            r'if existing:\s*# Update existing template instead of deleting\s*existing\.description = template_data\["description"\]\s*existing\.content = template_data\["content"\]\s*existing\.category = template_data\["category"\]\s*existing\.is_public = template_data\["is_public"\]\s*existing\.updated_at = datetime\.now\(timezone\.utc\)\s*db\.commit\(\)\s*print\(f"🔄 Updated: \'{template_data\[\'title\'\]}\'"\)\s*else:\s*# Create template with proper structure\s*new_template = Template\(\s*title=template_data\["title"\],\s*description=template_data\["description"\],\s*category=template_data\["category"\],\s*content=template_data\["content"\],\s*is_public=template_data\["is_public"\],\s*created_by=admin\.id,\s*version=1\s*\)\s*db\.add\(new_template\)\s*db\.commit\(\)\s*db\.refresh\(new_template\)\s*print\(f"✅ Template \'{template_data\[\'title\'\]}\' created with questions"\)',
            '''
    if existing:
        # Delete existing template (full replacement)
        db.delete(existing)
        db.commit()
        print(f"🗑️ Removed old '{template_data['title']}' template")
    
    # Create template with proper structure (fresh copy)
    new_template = Template(
        title=template_data["title"],
        description=template_data["description"],
        category=template_data["category"],
        content=template_data["content"],
        is_public=template_data["is_public"],
        created_by=admin.id,
        version=1
    )
    db.add(new_template)
    db.commit()
    db.refresh(new_template)
    print(f"✅ Template '{template_data['title']}' created with questions")
    ''',
            content,
            flags=re.DOTALL
        )
        
        # If the pattern didn't match, try a simpler approach
        if new_content == content:
            # Simple replacement for the update block
            new_content = re.sub(
                r'if existing:\s*\n\s*existing\.description = template_data\["description"\]\s*\n\s*existing\.content = template_data\["content"\]\s*\n\s*existing\.category = template_data\["category"\]\s*\n\s*existing\.is_public = template_data\["is_public"\]\s*\n\s*existing\.updated_at = datetime\.now\(timezone\.utc\)\s*\n\s*db\.commit\(\)\s*\n\s*print\(f"🔄 Updated: \'{template_data\[\'title\'\]}\'"\)\s*\n\s*else:\s*\n\s*# Create template with proper structure\s*\n\s*new_template = Template\(\s*\n\s*title=template_data\["title"\],\s*\n\s*description=template_data\["description"\],\s*\n\s*category=template_data\["category"\],\s*\n\s*content=template_data\["content"\],\s*\n\s*is_public=template_data\["is_public"\],\s*\n\s*created_by=admin\.id,\s*\n\s*version=1\s*\n\s*\)\s*\n\s*db\.add\(new_template\)\s*\n\s*db\.commit\(\)\s*\n\s*db\.refresh\(new_template\)\s*\n\s*print\(f"✅ Template \'{template_data\[\'title\'\]}\' created with questions"\)',
                '''
    if existing:
        # Delete existing template (full replacement)
        db.delete(existing)
        db.commit()
        print(f"🗑️ Removed old '{template_data['title']}' template")
    
    # Create template with proper structure (fresh copy)
    new_template = Template(
        title=template_data["title"],
        description=template_data["description"],
        category=template_data["category"],
        content=template_data["content"],
        is_public=template_data["is_public"],
        created_by=admin.id,
        version=1
    )
    db.add(new_template)
    db.commit()
    db.refresh(new_template)
    print(f"✅ Template '{template_data['title']}' created with questions")
    ''',
                content,
                flags=re.DOTALL
            )
        
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True, "Updated to delete+create"
        else:
            return False, "Pattern not found"
            
    except Exception as e:
        return False, f"Error: {str(e)}"

def main():
    print("="*70)
    print("FIXING SEED FILES TO DELETE + CREATE (FULL REPLACEMENT)")
    print("="*70)
    print()
    
    seed_files = [f for f in os.listdir('.') if f.startswith('seed_') and f.endswith('.py')]
    seed_files = [f for f in seed_files if f not in ['seed_all_templates.py', 'seed_db.py', 'seed_categories.py', 'fix_seeds_to_replace.py']]
    
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
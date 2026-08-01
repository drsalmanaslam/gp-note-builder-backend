import os
import re

def remove_consultation_type_from_file(filepath):
    """Remove Consultation Type from a seed file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if the file has consultation type
        if '_consultation_type' not in content:
            return False, "No consultation type found"
        
        # Find and remove the consultation type question
        # Pattern 1: With label "Consultation Type"
        pattern1 = r'\{\s*"id":\s*"_consultation_type",\s*"type":\s*"select",\s*"label":\s*"Consultation Type",\s*"required":\s*true,\s*"options":\s*\[[^\]]*\]\s*\},?\s*'
        new_content = re.sub(pattern1, '', content, flags=re.DOTALL)
        
        # Pattern 2: With label "Consultation Type *" 
        pattern2 = r'\{\s*"id":\s*"_consultation_type",\s*"type":\s*"select",\s*"label":\s*"Consultation Type \*",\s*"required":\s*true,\s*"options":\s*\[[^\]]*\]\s*\},?\s*'
        new_content = re.sub(pattern2, '', new_content, flags=re.DOTALL)
        
        # Pattern 3: More flexible pattern
        pattern3 = r'\{\s*"id":\s*"_consultation_type",[^}]*"options":\s*\[[^\]]*\]\s*\},?\s*'
        new_content = re.sub(pattern3, '', new_content, flags=re.DOTALL)
        
        if new_content == content:
            return False, "Pattern not found"
        
        # Write back the file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True, "Removed consultation type"
        
    except Exception as e:
        return False, f"Error: {str(e)}"

def main():
    print("="*70)
    print("REMOVING CONSULTATION TYPE FROM ALL SEED FILES")
    print("="*70)
    print()
    
    seed_files = [f for f in os.listdir('.') if f.startswith('seed_') and f.endswith('.py')]
    seed_files = [f for f in seed_files if f not in ['seed_all_templates.py', 'seed_db.py', 'seed_categories.py', 'remove_consultation_type.py']]
    
    updated = 0
    skipped = 0
    
    for seed_file in sorted(seed_files):
        success, message = remove_consultation_type_from_file(seed_file)
        if success:
            print(f"✅ {seed_file} - {message}")
            updated += 1
        else:
            print(f"⏭️  {seed_file} - {message}")
            skipped += 1
    
    print()
    print("="*70)
    print(f"SUMMARY: {updated} files updated, {skipped} files unchanged")
    print("="*70)
    
    print("\n📝 Also note: You may want to remove the Consultation Type from:")
    print("   - The frontend ConsultationBuilder.jsx component")
    print("   - The templateEngine.js rendering logic")

if __name__ == "__main__":
    main()
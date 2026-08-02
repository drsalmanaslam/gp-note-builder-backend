"""
Convert ALL seed files to INSERT-ONLY mode.
If template exists by title -> skip entirely. Never update or delete.
"""
import os
import re

seed_dir = '.'
fixed_count = 0

for filename in sorted(os.listdir(seed_dir)):
    if not filename.startswith('seed_') or not filename.endswith('.py'):
        continue
    
    filepath = os.path.join(seed_dir, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Pattern: Replace the "if existing:" block with SKIP logic
    # This handles both "if existing: db.delete(existing)" and "if existing: existing.description = ..."
    content = re.sub(
        r"if existing:.*?(?=\n\s*# Create fresh template|\n\s*new_t = Template|\n\s*template = Template|\n\s*db\.add\()",
        """if existing:
        print(f"⏭️  SKIPPED: {title} already exists (ID={existing.id})")
        db.close()
        return""",
        content,
        flags=re.DOTALL
    )
    
    # Also handle the case where there's no "# Create fresh template" comment
    if 'if existing:' in content and 'SKIPPED' not in content:
        content = re.sub(
            r"if existing:.*?(?=\n\s*\n\s*#|\n\s*\n\s*template|\n\s*\n\s*new_t|\n\s*\n\s*db\.add)",
            """if existing:
        print(f"⏭️  SKIPPED: {title} already exists (ID={existing.id})")
        db.close()
        return""",
            content,
            flags=re.DOTALL
        )
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        fixed_count += 1
        print(f"✅ Fixed: {filename}")

print(f"\n🎉 Converted {fixed_count} seed files to INSERT-ONLY mode!")
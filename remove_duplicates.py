from app.database import SessionLocal
from app.models import Template
from collections import defaultdict

db = SessionLocal()

# Find all templates
templates = db.query(Template).all()
print(f"Total templates before dedup: {len(templates)}")

# Group by title
title_groups = defaultdict(list)
for t in templates:
    title_groups[t.title].append(t)

duplicates_removed = 0

for title, items in title_groups.items():
    if len(items) > 1:
        # Keep the first one (oldest), delete the rest
        sorted_items = sorted(items, key=lambda x: x.created_at)
        keep = sorted_items[0]
        for dup in sorted_items[1:]:
            db.delete(dup)
            duplicates_removed += 1
            print(f"🗑️ Removed duplicate: '{dup.title}' (ID: {dup.id})")

db.commit()

# Verify
remaining = db.query(Template).count()
print(f"\n✅ Removed {duplicates_removed} duplicates")
print(f"📊 Templates now: {remaining}")

db.close()
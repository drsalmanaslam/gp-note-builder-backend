from app.database import SessionLocal
from app.models import Template, Category

db = SessionLocal()

# Define merges: {old_name: new_name}
merges = {
    "Gastrointestinal": "Gastroenterology",
    "Eye": "Ophthalmology",
    "Elderly Care": "Geriatrics",
}

for old_name, new_name in merges.items():
    old_cat = db.query(Category).filter(Category.name == old_name).first()
    new_cat = db.query(Category).filter(Category.name == new_name).first()
    
    if not old_cat:
        print(f"⏭️  {old_name} not found, skipping")
        continue
    
    if not new_cat:
        # Create the new category if it doesn't exist
        new_cat = Category(name=new_name)
        db.add(new_cat)
        db.commit()
        print(f"✅ Created category: {new_name}")
    
    # Update all templates with old category to new category
    count = db.query(Template).filter(Template.category == old_name).update(
        {Template.category: new_name}
    )
    
    # Delete the old category
    db.delete(old_cat)
    db.commit()
    
    print(f"✅ Merged {count} templates from '{old_name}' → '{new_name}'")

print("\nDone! Run /cleanup-duplicates and /seed-all on Render.")
db.close()
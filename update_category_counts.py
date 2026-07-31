from app.database import SessionLocal
from app.models import Category, Template

db = SessionLocal()

# Correct counts from your database
correct_counts = {
    'Musculoskeletal': 10,
    'General': 2,
    'Dermatology': 10,
    'Respiratory': 19,
    'Chronic Disease Reviews': 11,
    'Cardiovascular': 18,
    'Gastroenterology': 15,
    'Neurology': 3,
    'ENT': 18,
    'Urology': 2,
    'Gynaecology': 1,
    'Paediatrics': 7,
    'Mental Health': 3,
    'Endocrinology': 5,
    'Ophthalmology': 8,
    'Elderly Care': 2,
    "Men's Health": 11,
    "Women's Health": 24,
    'Sexual Health': 1,
    'Abnormal Labs/Investigations': 20,
    'GP-Related Topics': 3
}

categories = db.query(Category).all()
for cat in categories:
    if cat.name in correct_counts:
        cat.template_count = correct_counts[cat.name]
        print(f"✅ Updated {cat.name}: {cat.template_count} templates")
    else:
        # Count from database if not in the list
        count = db.query(Template).filter(Template.category == cat.name).count()
        cat.template_count = count
        print(f"✅ Updated {cat.name}: {count} templates (from database)")

db.commit()
print("\n✅ All category counts updated successfully!")
db.close()
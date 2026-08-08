from app.database import SessionLocal
from app.models import Category

def seed_categories():
    db = SessionLocal()
    
    default_categories = [
        {"name": "Cardiovascular", "color": "#EF4444", "description": "Heart and circulatory system"},
        {"name": "Respiratory", "color": "#3B82F6", "description": "Lungs and breathing"},
        {"name": "Gastroenterology", "color": "#F59E0B", "description": "Digestive system"},
        {"name": "Neurology", "color": "#8B5CF6", "description": "Brain and nervous system"},
        {"name": "ENT", "color": "#EC4899", "description": "Ear, nose, and throat"},
        {"name": "Dermatology", "color": "#F472B6", "description": "Skin and hair"},
        {"name": "Urology", "color": "#06B6D4", "description": "Urinary system"},
        {"name": "Gynaecology", "color": "#EC4899", "description": "Women's reproductive health"},
        {"name": "Paediatrics", "color": "#FCD34D", "description": "Children's health"},
        {"name": "Mental Health", "color": "#A78BFA", "description": "Psychological wellbeing"},
        {"name": "Musculoskeletal", "color": "#F97316", "description": "Bones and muscles"},
        {"name": "Endocrinology", "color": "#14B8A6", "description": "Hormones and glands"},
        {"name": "Ophthalmology", "color": "#60A5FA", "description": "Eye health"},
        {"name": "Geriatrics", "color": "#9CA3AF", "description": "Geriatric medicine and frailty"},
        {"name": "Men's Health", "color": "#3B82F6", "description": "Men's health issues"},
        {"name": "Women's Health", "color": "#EC4899", "description": "Women's health issues"},
        {"name": "Sexual Health", "color": "#F472B6", "description": "Sexual and reproductive health"},
        {"name": "Chronic Disease Reviews", "color": "#6366F1", "description": "Long-term condition management"},
        {"name": "Abnormal Labs/Investigations", "color": "#8B5CF6", "description": "Abnormal blood results and investigations"},
        {"name": "GP-Related Topics", "color": "#6B7280", "description": "Reference guides, forms, and administration"},
        {"name": "Infectious Disease", "color": "#EF4444", "description": "Infections and communicable diseases"},
        {"name": "OOH", "color": "#DC2626", "description": "Out of Hours — urgent and emergency presentations"},
        {"name": "General", "color": "#6B7280", "description": "General practice templates"},
    ]
    
    for cat_data in default_categories:
        existing = db.query(Category).filter(Category.name == cat_data["name"]).first()
        if not existing:
            category = Category(
                name=cat_data["name"],
                color=cat_data["color"],
                description=cat_data["description"],
                is_active=True
            )
            db.add(category)
            print(f"✅ Category '{cat_data['name']}' created")
    
    db.commit()
    db.close()
    print("All categories seeded successfully!")

if __name__ == "__main__":
    seed_categories()
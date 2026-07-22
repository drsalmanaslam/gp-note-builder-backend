from app.database import SessionLocal
from app.models import Category

def seed_categories():
    db = SessionLocal()
    
    default_categories = [
        {"name": "Cardiovascular", "icon": "❤️", "color": "#EF4444", "description": "Heart and circulatory system"},
        {"name": "Respiratory", "icon": "🫁", "color": "#3B82F6", "description": "Lungs and breathing"},
        {"name": "Gastroenterology", "icon": "🫄", "color": "#F59E0B", "description": "Digestive system"},
        {"name": "Neurology", "icon": "🧠", "color": "#8B5CF6", "description": "Brain and nervous system"},
        {"name": "ENT", "icon": "👂", "color": "#EC4899", "description": "Ear, nose, and throat"},
        {"name": "Dermatology", "icon": "🩹", "color": "#F472B6", "description": "Skin and hair"},
        {"name": "Urology", "icon": "🫘", "color": "#06B6D4", "description": "Urinary system"},
        {"name": "Gynaecology", "icon": "👩‍⚕️", "color": "#EC4899", "description": "Women's reproductive health"},
        {"name": "Paediatrics", "icon": "👶", "color": "#FCD34D", "description": "Children's health"},
        {"name": "Mental Health", "icon": "🧘", "color": "#A78BFA", "description": "Psychological wellbeing"},
        {"name": "Musculoskeletal", "icon": "🦴", "color": "#F97316", "description": "Bones and muscles"},
        {"name": "Endocrinology", "icon": "🧬", "color": "#14B8A6", "description": "Hormones and glands"},
        {"name": "Ophthalmology", "icon": "👁️", "color": "#60A5FA", "description": "Eye health"},
        {"name": "Elderly Care", "icon": "👴", "color": "#9CA3AF", "description": "Geriatric medicine"},
        {"name": "Men's Health", "icon": "👨‍⚕️", "color": "#3B82F6", "description": "Men's health issues"},
        {"name": "Women's Health", "icon": "👩‍⚕️", "color": "#EC4899", "description": "Women's health issues"},
        {"name": "Sexual Health", "icon": "💑", "color": "#F472B6", "description": "Sexual and reproductive health"},
        {"name": "Chronic Disease Reviews", "icon": "📋", "color": "#6366F1", "description": "Long-term condition management"},
    ]
    
    for cat_data in default_categories:
        existing = db.query(Category).filter(Category.name == cat_data["name"]).first()
        if not existing:
            category = Category(
                name=cat_data["name"],
                icon=cat_data["icon"],
                color=cat_data["color"],
                description=cat_data["description"],
                is_active=True
            )
            db.add(category)
            print(f"✅ Category '{cat_data['name']}' created")
    
    db.commit()
    db.close()
    print("🎉 All categories seeded successfully!")

if __name__ == "__main__":
    seed_categories()
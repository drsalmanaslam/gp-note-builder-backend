from app.database import SessionLocal
from app.models import Template
from app.auth import get_password_hash

def check_templates():
    db = SessionLocal()
    
    # Get all templates
    templates = db.query(Template).all()
    
    if not templates:
        print("❌ No templates found in database.")
        db.close()
        return
    
    print(f"✅ Found {len(templates)} templates:\n")
    
    for template in templates:
        print(f"Title: {template.title}")
        print(f"Category: {template.category}")
        print(f"Content type: {type(template.content)}")
        
        if template.content:
            content = template.content
            if isinstance(content, dict) and 'sections' in content:
                sections = content['sections']
                print(f"Sections: {len(sections)}")
                for section in sections:
                    title = section.get('title', 'Untitled')
                    questions = section.get('questions', [])
                    print(f"  - {title}: {len(questions)} questions")
            else:
                print("⚠️ Template content structure is not as expected.")
                print(f"  Keys: {list(content.keys()) if isinstance(content, dict) else 'Not a dict'}")
        print("-" * 50)
    
    db.close()

if __name__ == "__main__":
    check_templates()
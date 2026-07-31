from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_lichen_planus_vulval():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Women's Health").first()
    if not category: category = Category(name="Women's Health"); db.add(category); db.commit()

    t = {
        "title": "Lichen Planus - Vulval Region",
        "description": "Focused vulval lichen planus assessment covering itch vs pain differential, examination findings (erosions, Wickham's striae), vulval care advice, and gynaecology/dermatology referral.",
        "category": "Women's Health",
        "content": {"sections": [
            {
                "title": "History",
                "section_type": "history",
                "questions": [
                    {"id": "lpv_duration", "type": "text", "label": "Duration of Symptoms", "required": True, "placeholder": "e.g., 3 months"},
                    {"id": "lpv_primary_symptom", "type": "single_select", "label": "Main Presenting Symptom (Guides Differential)", "required": True, "options": ["Itch Predominant", "Pain Predominant", "Both Itch + Pain"]},
                    {"id": "lpv_itch_causes", "type": "multi_select", "label": "If ITCH Predominant - Consider", "required": False, "options": ["Lichen Sclerosus (Labia Minora)", "Eczema (Labia Majora)", "Psoriasis (Labia Majora)", "Candida Infection"]},
                    {"id": "lpv_pain_causes", "type": "multi_select", "label": "If PAIN Predominant - Consider", "required": False, "options": ["Lichen Planus (Labia Minora)", "Malignancy", "Herpes / GAS Infection", "Aphthous Ulcer"]},
                    {"id": "lpv_pain_triggers", "type": "multi_select", "label": "Pain Triggers", "required": False, "options": ["Tampon Insertion", "Cycling", "Sitting", "Sexual Intercourse", "None"]},
                    {"id": "lpv_discharge", "type": "toggle", "label": "Discharge?", "required": False}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "lpv_vulval_exam", "type": "multi_select", "label": "External Vulval Examination", "required": True, "options": ["Erosion Present", "Scarring Present", "Resorption of Labia Minora", "Normal"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Erosion/scarring/resorption pattern = consistent with lichen planus.", "red_flag_negative": ""},
                    {"id": "lpv_speculum", "type": "single_select", "label": "Speculum Examination", "required": False, "options": ["Performed", "Not Performed - Likely to Cause Significant Pain (Documented)", "Not Indicated"]},
                    {"id": "lpv_extragenital", "type": "multi_select", "label": "Extragenital / Full Body Exam (Including Oral Cavity + Nails)", "required": True, "options": ["Polygonal Papules", "Flat-Topped Firm Plaques", "Shiny Appearance", "Wickham's Striae (Fine White Lines)", "Oral Involvement", "Nail Involvement", "None Found"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Extragenital involvement = systemic disease. Refer dental/ENT/GI/ophthalmology as appropriate.", "red_flag_negative": ""},
                    {"id": "lpv_extragenital_sites", "type": "text", "label": "Extragenital Sites Affected (If Present)", "required": False, "placeholder": "e.g., Oral mucosa, wrists, shins"}
                ]
            },
            {
                "title": "Patient Education & Vulval Care Advice",
                "section_type": "plan",
                "questions": [
                    {"id": "lpv_skincare", "type": "multi_select", "label": "Vulval Care Advice Given", "required": False, "options": ["Avoid Perfumed Soaps, Shower Gels, Wipes, Antiseptics", "Use Bland Emollient to Wash (Avoid Washing Too Frequently)", "Apply Bland Emollient Regularly", "Wear White Cotton Underwear"]},
                    {"id": "lpv_resources", "type": "multi_select", "label": "Patient Resources Given", "required": False, "options": ["BAD Vulval Skincare Leaflet", "BAD Lichen Planus Leaflet"]}
                ]
            },
            {
                "title": "Referral & Plan",
                "section_type": "plan",
                "safety_netting": "Lichen planus (vulval): typically affects labia minora (vs lichen sclerosus/eczema/psoriasis which affect labia majora). Key exam findings: erosion, scarring, resorption of labia minora, extragenital features (Wickham's striae, oral/nail involvement). Refer gynaecology/dermatology - may require systemic treatment: hydroxychloroquine, mycophenolate mofetil, ciclosporin, or methotrexate. If extragenital involvement: additional referrals as indicated (dental, ENT, GI, ophthalmology). Vulval care: avoid irritants, use bland emollients, cotton underwear. Patient resources: BAD Vulval Skincare + Lichen Planus leaflets.",
                "questions": [
                    {"id": "lpv_diagnosis", "type": "single_select", "label": "Impression", "required": True, "options": ["Lichen Planus - Vulval (Consistent Exam Findings)", "Lichen Planus - Vulval + Extragenital", "?Lichen Sclerosus (Labia Minora - Itch)", "?Eczema/Psoriasis (Labia Majora)", "Alternative Diagnosis"]},
                    {"id": "lpv_referral_gynae", "type": "toggle", "label": "Refer Gynaecology / Dermatology? (Systemic Treatment May Be Required)", "required": True},
                    {"id": "lpv_referral_other", "type": "multi_select", "label": "Additional Referrals (If Extragenital Involvement)", "required": False, "options": ["Dental", "ENT", "GI", "Ophthalmology", "None Required"]},
                    {"id": "lpv_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., Await gynaecology/dermatology OPD, return if symptoms worsen"}
                ]
            }
        ]},
        "is_public": True
    }

    existing = db.query(Template).filter(Template.title == t["title"], Template.created_by == admin.id).first()
    
    if existing:
        # Update existing template instead of deleting
        existing.description = t["description"]
        existing.content = t["content"]
        existing.category = t["category"]
        existing.is_public = t["is_public"]
        existing.updated_at = datetime.now(timezone.utc)
        db.commit()
        print(f"🔄 Updated: {t['title']}")
    new_t = Template(title=t["title"], description=t["description"], category=t["category"], content=t["content"], is_public=True, created_by=admin.id, version=1)
    db.add(new_t); db.commit()
    print(f"Template '{t['title']}' created with {len(t['content']['sections'])} sections!"); db.close()

if __name__ == "__main__":
    seed_lichen_planus_vulval()
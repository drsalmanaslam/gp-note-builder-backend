from app.database import SessionLocal
from app.models import User, Template, Category

def seed_implanon():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Women's Health").first()
    if not category: category = Category(name="Women's Health"); db.add(category); db.commit()

    t = {
        "title": "Implanon (Etonogestrel) Insertion",
        "description": "Implanon insertion procedure template covering pre-procedure checks, patient education, LARC efficacy comparison, insertion site details, and follow-up scheduling.",
        "category": "Women's Health",
        "content": {"sections": [
            {
                "title": "Pre-Procedure Checks",
                "section_type": "history",
                "questions": [
                    {"id": "imp_hcg", "type": "single_select", "label": "Pregnancy Test (hCG) - MUST Be Negative Before Insertion", "required": True, "options": ["Negative", "Positive - CANNOT INSERT"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Positive hCG = do NOT insert. Refer antenatal services.", "red_flag_negative": ""},
                    {"id": "imp_documentation_read", "type": "toggle", "label": "Patient Has Read All Provided Documentation + Queries Answered?", "required": True},
                    {"id": "imp_consent", "type": "toggle", "label": "Consent Form Signed? (e.g., ICGP Consent Form)", "required": True}
                ]
            },
            {
                "title": "Patient Education - Before Insertion",
                "section_type": "plan",
                "questions": [
                    {"id": "imp_side_effects", "type": "multi_select", "label": "Side Effects Discussed", "required": True, "options": ["Breast Discomfort", "Fluid Retention", "Increased Acne", "Headaches", "Mood Changes"]},
                    {"id": "imp_bleeding", "type": "multi_select", "label": "Bleeding Pattern Changes Discussed", "required": True, "options": ["Irregular Periods (Common)", "Heavy Periods", "Amenorrhoea (No Periods)", "All Possible Patterns Explained"]},
                    {"id": "imp_infection_risk", "type": "toggle", "label": "Small Risk of Wound Infection Explained?", "required": True},
                    {"id": "imp_scar", "type": "toggle", "label": "Aware Small Scar Will Remain at Insertion Site?", "required": True}
                ]
            },
            {
                "title": "LARC Efficacy Comparison (Reference)",
                "section_type": "plan",
                "questions": [
                    {"id": "imp_efficacy_note", "type": "single_select", "label": "Efficacy Discussed? (Implanon 0.01 > Mirena 0.2 > Depo 0.3 per 100 Women-Years)", "required": False, "options": ["Implanon: 0.01 (Most Effective)", "Mirena IUS: 0.2", "Depo-Provera: 0.3 (Higher Due to Return Visits)", "All Discussed"]}
                ]
            },
            {
                "title": "Procedure",
                "section_type": "examination",
                "questions": [
                    {"id": "imp_arm", "type": "single_select", "label": "Insertion Site", "required": True, "options": ["Left Arm", "Right Arm"]},
                    {"id": "imp_site_detail", "type": "toggle", "label": "Inner Aspect, 10cm Above Medial Epicondyle, Over Triceps?", "required": True},
                    {"id": "imp_antiseptic", "type": "toggle", "label": "Skin Cleansed with Antiseptic?", "required": True},
                    {"id": "imp_la", "type": "toggle", "label": "Local Anaesthetic: 5ml 1% Xylocaine with Adrenaline?", "required": True},
                    {"id": "imp_inserted", "type": "toggle", "label": "New Implanon Inserted + Device Palpable After Insertion?", "required": True},
                    {"id": "imp_steristrips", "type": "toggle", "label": "Steri-Strips Applied?", "required": True},
                    {"id": "imp_bandage", "type": "toggle", "label": "Bandage Applied Over Steri-Strips?", "required": True}
                ]
            },
            {
                "title": "Post-Procedure Plan",
                "section_type": "plan",
                "safety_netting": "Return if: signs of wound infection (redness, swelling, pus, increasing pain), device not palpable, arm pain/swelling, persistent heavy bleeding, or any concerns. Implanon is effective for 3 years from insertion. Keep bandage dry for 24-48 hours. Steri-strips can be removed after 3-5 days. Bruising at insertion site is normal. If device not palpable: use additional contraception + return for assessment. Patient information leaflet given.",
                "questions": [
                    {"id": "imp_diagnosis", "type": "single_select", "label": "Impression", "required": True, "options": ["Implanon Inserted Successfully", "Insertion Attempted - Refer", "Procedure Not Performed"]},
                    {"id": "imp_replacement_date", "type": "text", "label": "Removal/Replacement Due (3 Years from Insertion)", "required": True, "placeholder": "e.g., 29/07/2029"},
                    {"id": "imp_leaflet", "type": "toggle", "label": "Patient Information Leaflet Given?", "required": True},
                    {"id": "imp_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., Removal appointment scheduled for [date], return sooner if concerns"}
                ]
            }
        ]},
        "is_public": True
    }

    existing = db.query(Template).filter(Template.title == t["title"], Template.created_by == admin.id).first()
    if existing: db.delete(existing); db.commit()
    new_t = Template(title=t["title"], description=t["description"], category=t["category"], content=t["content"], is_public=True, created_by=admin.id, version=1)
    db.add(new_t); db.commit()
    print(f"Template '{t['title']}' created with {len(t['content']['sections'])} sections!"); db.close()

if __name__ == "__main__":
    seed_implanon()
from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_gallstones():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Gastroenterology").first()
    if not category: category = Category(name="Gastroenterology"); db.add(category); db.commit()

    t = {
        "title": "Gallstones / Biliary Colic",
        "description": "Focused assessment for gallstone disease covering biliary colic vs cholecystitis vs cholangitis differentiation, Murphy's sign, and surgical referral criteria.",
        "category": "Gastroenterology",
        "content": {"sections": [
            {
                "title": "Pain History",
                "section_type": "history",
                "questions": [
                    {"id": "gs_presenting_complaint", "type": "text", "label": "Presenting Complaint", "required": True, "placeholder": "e.g., Intermittent severe RUQ pain, worse after fatty meals"},
                    {"id": "gs_pain_character", "type": "single_select", "label": "Pain Character", "required": True, "options": ["Colicky, intermittent RUQ pain (Biliary Colic)", "Constant severe RUQ pain (Cholecystitis)", "RUQ pain + jaundice + fever (Cholangitis - RED FLAG)"]},
                    {"id": "gs_radiation", "type": "single_select", "label": "Radiation", "required": False, "options": ["Right shoulder", "Interscapular area", "Neither"]},
                    {"id": "gs_trigger", "type": "toggle", "label": "Worse After Fatty Food?", "required": True},
                    {"id": "gs_obstructive", "type": "multi_select", "label": "Obstructive Jaundice Screen", "required": True, "options": ["Pale stools", "Dark urine", "Neither present"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Pale stools + dark urine = biliary obstruction (choledocholithiasis). Urgent surgical referral.", "red_flag_negative": ""},
                    {"id": "gs_associated", "type": "multi_select", "label": "Associated Symptoms", "required": True, "options": ["Vomiting", "Pyrexia / fever / rigors", "Neither present"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Fever + RUQ pain + jaundice = CHARCOT'S TRIAD (cholangitis). EMERGENCY admission.", "red_flag_negative": ""},
                    {"id": "gs_previous_uss", "type": "toggle", "label": "Previous Ultrasound Abdomen?", "required": False}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "gs_vitals", "type": "text", "label": "Vital Signs", "required": True, "placeholder": "e.g., Temp 37°C, HR 78"},
                    {"id": "gs_abdo", "type": "single_select", "label": "Abdominal Examination", "required": True, "options": ["Mild tenderness RUQ on deep palpation", "Marked tenderness RUQ", "Murphy's sign POSITIVE (arrest on inspiration) - ?Cholecystitis", "Guarding / rigidity present - RED FLAG"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Murphy's sign + fever = acute cholecystitis. Guarding/rigidity = ?perforation. Urgent surgical admission.", "red_flag_negative": ""},
                    {"id": "gs_rif", "type": "toggle", "label": "RIF Tenderness? (?Appendicitis mimicking biliary pain)", "required": False},
                    {"id": "gs_jaundice", "type": "toggle", "label": "Jaundice Visible?", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Jaundice + RUQ pain = choledocholithiasis or pancreatic head mass. Urgent investigation.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "Cholelithiasis / Biliary Colic (intermittent, post-prandial)",
                    "Acute Cholecystitis (constant pain, Murphy's sign, fever)",
                    "Choledocholithiasis (obstructive jaundice, dilated ducts)",
                    "Cholangitis (Charcot's triad: RUQ pain + fever + jaundice - EMERGENCY)",
                    "Pancreatitis (epigastric radiating to back)",
                    "Peptic Ulcer Disease",
                    "Appendicitis (RIF pain)",
                    "Right Lower Lobe Pneumonia (referred pain)"
                ],
                "questions": [
                    {"id": "gs_diagnosis", "type": "single_select", "label": "Clinical Impression", "required": True, "options": ["Cholelithiasis / Biliary Colic", "Acute Cholecystitis Suspected - URGENT", "Obstructive Jaundice / Choledocholithiasis - URGENT", "Cholangitis Suspected - EMERGENCY", "Alternative diagnosis more likely"]}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Return immediately or attend A&E if: high temperature/fever/rigors, worsening pain, jaundice develops, vomiting, or signs of obstruction (pale stools, dark urine). Charcot's triad (RUQ pain + fever + jaundice) = cholangitis EMERGENCY. Biliary colic: Buscopan or Colofac for symptomatic relief. USS abdomen to confirm gallstones + assess bile duct dilatation. If cholecystitis suspected: urgent surgical referral for admission + IV antibiotics. If choledocholithiasis: urgent surgical/GI referral for ERCP. Avoid fatty foods. May need elective cholecystectomy if recurrent biliary colic.",
                "questions": [
                    {"id": "gs_imaging", "type": "single_select", "label": "Imaging", "required": True, "options": ["Ultrasound Abdomen Requested", "Not required at this stage", "Already performed"]},
                    {"id": "gs_symptomatic", "type": "single_select", "label": "Symptomatic Treatment", "required": False, "options": ["Buscopan (Hyoscine) 10mg TDS", "Colofac (Mebeverine) 135mg TDS", "None"]},
                    {"id": "gs_referral", "type": "single_select", "label": "Referral", "required": False, "options": ["None - manage in primary care", "Routine surgical referral (pending USS)", "Urgent surgical referral (cholecystitis/choledocholithiasis)", "Emergency A&E (cholangitis)"]},
                    {"id": "gs_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., Await USS result, surgical referral if confirmed, review if symptoms persist"}
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
    seed_gallstones()
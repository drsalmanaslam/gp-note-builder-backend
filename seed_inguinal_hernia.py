from app.database import SessionLocal
from app.models import User, Template, Category

def seed_inguinal_hernia():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Gastroenterology").first()
    if not category: category = Category(name="Gastroenterology"); db.add(category); db.commit()

    t = {
        "title": "Inguinal Hernia Assessment",
        "description": "Focused assessment for inguinal hernia covering strangulation red flags, deep ring occlusion test, differentiation of direct vs indirect, and surgical referral pathway.",
        "category": "Gastroenterology",
        "content": {"sections": [
            {
                "title": "RED FLAGS - Strangulation / Obstruction (A&E IMMEDIATELY)",
                "section_type": "history",
                "questions": [
                    {"id": "ih_irreducible", "type": "toggle", "label": "Lump Become Irreducible?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Irreducible hernia + pain = STRANGULATION until proven otherwise. A&E IMMEDIATELY.", "red_flag_negative": ""},
                    {"id": "ih_severe_pain", "type": "toggle", "label": "Severe Pain at Hernia Site?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Severe pain + hernia = ?strangulation. SURGICAL EMERGENCY. A&E immediately.", "red_flag_negative": ""},
                    {"id": "ih_vomiting", "type": "toggle", "label": "Vomiting?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Vomiting + hernia = ?obstruction. SURGICAL EMERGENCY. A&E immediately.", "red_flag_negative": ""},
                    {"id": "ih_absolute_constipation", "type": "toggle", "label": "Absolute Constipation? (No Stool or Flatus Passing)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Absolute constipation = OBSTRUCTION. SURGICAL EMERGENCY. A&E immediately.", "red_flag_negative": ""},
                    {"id": "ih_distension", "type": "toggle", "label": "Abdominal Distension?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Distension + hernia = ?obstruction. A&E immediately.", "red_flag_negative": ""},
                    {"id": "ih_redness", "type": "toggle", "label": "Redness / Skin Changes Over Lump?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Skin changes = ?strangulation with ischaemia. A&E immediately.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "History",
                "section_type": "history",
                "questions": [
                    {"id": "ih_presenting_complaint", "type": "text", "label": "Presenting Complaint", "required": True, "placeholder": "e.g., Lump in right groin for 2 months, appears when coughing"},
                    {"id": "ih_duration", "type": "text", "label": "Duration of Swelling", "required": True, "placeholder": "e.g., 2 months"},
                    {"id": "ih_side", "type": "single_select", "label": "Side", "required": True, "options": ["Right", "Left", "Bilateral"]},
                    {"id": "ih_pattern", "type": "single_select", "label": "Pattern", "required": True, "options": ["Intermittent (Comes and Goes)", "Persistent"]},
                    {"id": "ih_reducibility", "type": "single_select", "label": "Reducibility", "required": True, "options": ["Reducible", "Irreducible - RED FLAG"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Irreducible hernia = risk of strangulation. Urgent surgical referral.", "red_flag_negative": ""},
                    {"id": "ih_stool_flatus", "type": "toggle", "label": "Still Passing Stool and Flatus Normally?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Not passing stool/flatus = ?obstruction. A&E immediately.", "red_flag_negative": ""},
                    {"id": "ih_onset_trigger", "type": "single_select", "label": "First Noticed After", "required": False, "options": ["Lifting / Straining", "Coughing / Sneezing", "No Specific Trigger", "Gradual - No Clear Onset"]},
                    {"id": "ih_trajectory", "type": "single_select", "label": "Trajectory", "required": True, "options": ["Static - No Change", "Getting Bigger"]},
                    {"id": "ih_provocative", "type": "multi_select", "label": "Appears / Worsens With", "required": True, "options": ["Coughing", "Bending", "Standing", "Sneezing", "Resolves Lying Down", "None"]}
                ]
            },
            {
                "title": "Risk Factors",
                "section_type": "history",
                "questions": [
                    {"id": "ih_risk_factors", "type": "multi_select", "label": "Risk Factors", "required": True, "options": ["Chronic Cough / COPD", "Heavy Lifting (Occupational / Gym)", "Chronic Constipation / Straining", "Previous Hernia Repair", "Obesity", "Pregnancy", "None"]},
                    {"id": "ih_occupation", "type": "text", "label": "Occupation (Lifting/Straining Risk + Return-to-Work)", "required": False, "placeholder": "e.g., Construction worker / Manual labour"}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "ih_bmi", "type": "number", "label": "BMI (kg/m²)", "required": False, "placeholder": "e.g., 28"},
                    {"id": "ih_location", "type": "single_select", "label": "Lump Location", "required": True, "options": ["Above Inguinal Ligament (Inguinal Hernia)", "Below Inguinal Ligament (Femoral Hernia - RED FLAG)"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Femoral hernia = HIGH risk of strangulation. Urgent surgical referral.", "red_flag_negative": ""},
                    {"id": "ih_size", "type": "text", "label": "Size of Lump", "required": False, "placeholder": "e.g., 3cm"},
                    {"id": "ih_consistency", "type": "single_select", "label": "Consistency", "required": False, "options": ["Soft", "Firm", "Tender - RED FLAG"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Tender hernia = ?strangulation. Urgent surgical assessment.", "red_flag_negative": ""},
                    {"id": "ih_reducibility_exam", "type": "single_select", "label": "Reducibility on Examination", "required": True, "options": ["Fully Reducible", "Partially Reducible", "Not Reducible - RED FLAG"]},
                    {"id": "ih_cough_impulse", "type": "toggle", "label": "Cough Impulse Present?", "required": True},
                    {"id": "ih_deep_ring_test", "type": "single_select", "label": "Deep Ring Occlusion Test (Pressure Over Deep Ring ~1.5cm Above Midpoint of Inguinal Ligament)", "required": False, "options": ["Hernia Controlled = INDIRECT Inguinal Hernia", "Hernia NOT Controlled = DIRECT Inguinal Hernia", "Not Assessed"]},
                    {"id": "ih_genitalia", "type": "single_select", "label": "External Genitalia", "required": False, "options": ["Normal", "Abnormal (Scrotal Extension)"]}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "Indirect Inguinal Hernia (Lateral to Inferior Epigastric Vessels, Through Deep Ring)",
                    "Direct Inguinal Hernia (Medial to Inferior Epigastric Vessels, Through Hesselbach's Triangle)",
                    "Femoral Hernia (Below Inguinal Ligament, HIGH Strangulation Risk)",
                    "Inguinal Lymphadenopathy",
                    "Hydrocele (Transilluminates)",
                    "Varicocele (Bag of Worms)",
                    "Saphena Varix (Disappears on Lying Flat, Cough Impulse)",
                    "Undescended Testis"
                ],
                "questions": [
                    {"id": "ih_diagnosis", "type": "single_select", "label": "Clinical Impression", "required": True, "options": ["Indirect Inguinal Hernia - Reducible", "Direct Inguinal Hernia - Reducible", "Inguinal Hernia - Irreducible (Urgent Surgical)", "Femoral Hernia - URGENT (High Strangulation Risk)", "Suspected Strangulation / Obstruction - A&E IMMEDIATELY"]}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "EMERGENCY - attend A&E immediately if: lump becomes irreducible, severe pain at hernia site, vomiting, abdominal distension, absolute constipation (no stool or flatus), or redness/skin changes over the lump. These are signs of STRANGULATION or OBSTRUCTION - a surgical emergency. Routine management: refer to general surgery for elective repair. Arrange ultrasound scan if diagnostic uncertainty. Lifestyle: avoid heavy lifting/straining until surgical review, manage constipation, treat chronic cough. Occupational advice: may need modified duties until repair.",
                "questions": [
                    {"id": "ih_referral", "type": "single_select", "label": "Referral", "required": True, "options": ["Routine General Surgery (Elective Repair)", "Urgent General Surgery (Irreducible / Tender)", "A&E IMMEDIATELY (Strangulation / Obstruction)", "USS Requested (Diagnostic Uncertainty)"]},
                    {"id": "ih_lifestyle", "type": "multi_select", "label": "Lifestyle Advice", "required": False, "options": ["Avoid Heavy Lifting / Straining Until Review", "Manage Constipation", "Treat Chronic Cough", "Occupational Advice - Modified Duties"]},
                    {"id": "ih_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., Await surgical OPD, A&E if red flags, USS if requested"}
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
    seed_inguinal_hernia()
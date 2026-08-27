from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_hernia():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: 
        print("Admin not found.")
        db.close()
        return

    category = db.query(Category).filter(Category.name == "General Surgery").first()
    if not category: 
        category = Category(name="General Surgery")
        db.add(category)
        db.commit()

    t = {
        "title": "Umbilical / Epigastric Hernia Assessment",
        "description": "Practical GP assessment and management of umbilical and epigastric hernias, including red flag screening for incarceration/strangulation.",
        "category": "General Surgery",
        "content": {"sections": [
            {
                "title": "History",
                "section_type": "history",
                "questions": [
                    {
                        "id": "hernia_presenting_complaint",
                        "type": "text",
                        "label": "Presenting Complaint",
                        "required": True,
                        "placeholder": "e.g., Lump around umbilicus noticed 3 months ago",
                        "output_phrase": "c/o: {value}"
                    },
                    {
                        "id": "hernia_onset_duration",
                        "type": "text",
                        "label": "Onset and Duration",
                        "required": True,
                        "placeholder": "e.g., Noticed 3 months ago, gradually increasing",
                        "output_phrase": "Onset: {value}"
                    },
                    {
                        "id": "hernia_size_change",
                        "type": "single_select",
                        "label": "Change in Size",
                        "required": True,
                        "options": ["Stable", "Increasing", "Intermittent", "Decreasing"],
                        "output_phrase": "Size change: {value}"
                    },
                    {
                        "id": "hernia_pain",
                        "type": "single_select",
                        "label": "Pain",
                        "required": True,
                        "options": ["None", "Mild discomfort", "Painful", "Severe pain - RED FLAG"],
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Severe pain - consider incarceration/strangulation.",
                        "red_flag_negative": "",
                        "output_phrase": "Pain: {value}"
                    },
                    {
                        "id": "hernia_pain_character",
                        "type": "text",
                        "label": "Pain Character and Severity",
                        "required": False,
                        "placeholder": "e.g., Dull ache, sharp with straining, constant",
                        "output_phrase": "Pain character: {value}"
                    },
                    {
                        "id": "hernia_aggravating",
                        "type": "multi_select",
                        "label": "Aggravating Factors",
                        "required": False,
                        "options": ["Coughing", "Lifting", "Straining", "Exercise", "Bending", "None"],
                        "output_phrase": "Aggravated by: {value}"
                    },
                    {
                        "id": "hernia_reducible",
                        "type": "single_select",
                        "label": "Reducible?",
                        "required": True,
                        "options": ["Yes - reducible", "No - not reducible - RED FLAG", "Yes - reduces when lying down", "Variable"],
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Irreducible hernia - consider incarceration.",
                        "red_flag_negative": "",
                        "output_phrase": "Reducible: {value}"
                    },
                    {
                        "id": "hernia_sudden_increase",
                        "type": "toggle",
                        "label": "Any Sudden Increase in Size?",
                        "required": False,
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Sudden increase in size - consider incarceration/strangulation.",
                        "red_flag_negative": "",
                        "output_phrase": "Sudden increase: {value}"
                    },
                    {
                        "id": "hernia_previous_irreducibility",
                        "type": "toggle",
                        "label": "Previous Episodes of Irreducibility?",
                        "required": False,
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Previous irreducibility - discuss surgical repair.",
                        "red_flag_negative": "",
                        "output_phrase": "Previous irreducibility: {value}"
                    },
                    {
                        "id": "hernia_nausea",
                        "type": "toggle",
                        "label": "Nausea / Vomiting?",
                        "required": False,
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Nausea/vomiting - urgent surgical/ED assessment.",
                        "red_flag_negative": "",
                        "output_phrase": "Nausea/vomiting: {value}"
                    },
                    {
                        "id": "hernia_distension",
                        "type": "toggle",
                        "label": "Abdominal Distension?",
                        "required": False,
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Abdominal distension - consider obstruction.",
                        "red_flag_negative": "",
                        "output_phrase": "Distension: {value}"
                    },
                    {
                        "id": "hernia_constipation",
                        "type": "multi_select",
                        "label": "Bowel Symptoms",
                        "required": False,
                        "options": ["Constipation", "Obstipation (no passage of stool/flatus) - RED FLAG", "Change in bowel habit", "Blood in stool", "Normal"],
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Obstipation - urgent surgical assessment for obstruction.",
                        "red_flag_negative": "",
                        "output_phrase": "Bowel symptoms: {value}"
                    },
                    {
                        "id": "hernia_previous_surgery",
                        "type": "textarea",
                        "label": "Previous Hernia / Abdominal Surgery",
                        "required": False,
                        "placeholder": "e.g., Previous hernia repair, laparotomy, C-section",
                        "output_phrase": "Previous surgery: {value}"
                    }
                ]
            },
            {
                "title": "Risk Factors",
                "section_type": "history",
                "questions": [
                    {
                        "id": "hernia_bmi",
                        "type": "number",
                        "label": "BMI",
                        "required": False,
                        "placeholder": "e.g., 32",
                        "output_phrase": "BMI: {value}"
                    },
                    {
                        "id": "hernia_occupation",
                        "type": "text",
                        "label": "Occupation / Heavy Lifting",
                        "required": False,
                        "placeholder": "e.g., Construction worker, heavy lifting daily",
                        "output_phrase": "Occupation: {value}"
                    },
                    {
                        "id": "hernia_chronic_cough",
                        "type": "toggle",
                        "label": "Chronic Cough?",
                        "required": False,
                        "output_phrase": "Chronic cough: {value}"
                    },
                    {
                        "id": "hernia_constipation_risk",
                        "type": "toggle",
                        "label": "Chronic Constipation / Straining?",
                        "required": False,
                        "output_phrase": "Constipation: {value}"
                    },
                    {
                        "id": "hernia_pregnancy",
                        "type": "single_select",
                        "label": "Pregnancy History (if female)",
                        "required": False,
                        "options": ["Not applicable", "Never pregnant", "Previous pregnancy", "Multiparous (≥3 pregnancies)", "Current pregnancy"],
                        "output_phrase": "Pregnancy: {value}"
                    },
                    {
                        "id": "hernia_ascites",
                        "type": "toggle",
                        "label": "Ascites / Liver Disease?",
                        "required": False,
                        "output_phrase": "Ascites: {value}"
                    },
                    {
                        "id": "hernia_smoking",
                        "type": "single_select",
                        "label": "Smoking Status",
                        "required": False,
                        "options": ["Non-smoker", "Ex-smoker", "Current smoker"],
                        "output_phrase": "Smoking: {value}"
                    }
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {
                        "id": "hernia_general",
                        "type": "single_select",
                        "label": "General Appearance",
                        "required": True,
                        "options": ["Well", "Unwell - RED FLAG", "Systemically unwell - RED FLAG"],
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Unwell/systemically unwell - urgent surgical/ED assessment.",
                        "red_flag_negative": "",
                        "output_phrase": "General: {value}"
                    },
                    {
                        "id": "hernia_abdomen_soft",
                        "type": "single_select",
                        "label": "Abdomen",
                        "required": True,
                        "options": ["Soft, non-tender", "Tender - RED FLAG", "Rigid/guarding - RED FLAG", "Distended - RED FLAG"],
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Tender/rigid/distended abdomen - urgent surgical/ED assessment.",
                        "red_flag_negative": "",
                        "output_phrase": "Abdomen: {value}"
                    },
                    {
                        "id": "hernia_location",
                        "type": "single_select",
                        "label": "Hernia Location",
                        "required": True,
                        "options": ["Umbilical", "Paraumbilical", "Epigastric", "Incisional", "Other"],
                        "output_phrase": "Location: {value}"
                    },
                    {
                        "id": "hernia_size",
                        "type": "text",
                        "label": "Size",
                        "required": False,
                        "placeholder": "e.g., 2 cm",
                        "output_phrase": "Size: {value}"
                    },
                    {
                        "id": "hernia_visible",
                        "type": "single_select",
                        "label": "Visible/Palpable Lump",
                        "required": True,
                        "options": ["Visible on standing", "Palpable", "Visible on lying down", "Not visible"],
                        "output_phrase": "Lump: {value}"
                    },
                    {
                        "id": "hernia_tenderness",
                        "type": "single_select",
                        "label": "Tenderness",
                        "required": True,
                        "options": ["Non-tender", "Tender - RED FLAG", "Very tender - RED FLAG"],
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Tender hernia - consider incarceration/strangulation.",
                        "red_flag_negative": "",
                        "output_phrase": "Tenderness: {value}"
                    },
                    {
                        "id": "hernia_skin",
                        "type": "single_select",
                        "label": "Skin Overlying Hernia",
                        "required": True,
                        "options": ["Normal", "Erythematous - RED FLAG", "Discoloured - RED FLAG", "Tense/shiny - RED FLAG"],
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Erythematous/discoloured/shiny skin - consider strangulation.",
                        "red_flag_negative": "",
                        "output_phrase": "Skin: {value}"
                    },
                    {
                        "id": "hernia_cough_impulse",
                        "type": "single_select",
                        "label": "Cough Impulse",
                        "required": True,
                        "options": ["Present", "Absent", "Not assessed"],
                        "output_phrase": "Cough impulse: {value}"
                    },
                    {
                        "id": "hernia_reducible_exam",
                        "type": "single_select",
                        "label": "Reducible on Examination",
                        "required": True,
                        "options": ["Yes", "No - RED FLAG", "Partially"],
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Irreducible hernia - urgent surgical/ED assessment.",
                        "red_flag_negative": "",
                        "output_phrase": "Reducible (exam): {value}"
                    },
                    {
                        "id": "hernia_defect",
                        "type": "single_select",
                        "label": "Defect Palpable",
                        "required": True,
                        "options": ["Yes - palpable", "No", "Uncertain"],
                        "output_phrase": "Defect: {value}"
                    },
                    {
                        "id": "hernia_contents",
                        "type": "single_select",
                        "label": "Contents",
                        "required": True,
                        "options": ["Soft - likely omentum", "Firm - possible bowel - RED FLAG", "Unclear", "Normal"],
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Firm contents - consider bowel involvement/strangulation.",
                        "red_flag_negative": "",
                        "output_phrase": "Contents: {value}"
                    },
                    {
                        "id": "hernia_other_masses",
                        "type": "textarea",
                        "label": "Other Abdominal Masses",
                        "required": False,
                        "placeholder": "e.g., None, other hernias",
                        "output_phrase": "Other masses: {value}"
                    }
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "Uncomplicated umbilical hernia (most common)",
                    "Uncomplicated epigastric hernia",
                    "Paraumbilical hernia",
                    "Incisional hernia",
                    "Incarcerated hernia (irreducible but not strangulated) - RED FLAG",
                    "Strangulated hernia (ischaemic bowel) - RED FLAG",
                    "Umbilical granuloma (infants)",
                    "Lipoma",
                    "Haematoma",
                    "Suture granuloma (post-surgery)",
                    "Metastasis (rare)",
                    "Diastasis recti (not a true hernia)"
                ],
                "questions": [
                    {
                        "id": "hernia_diagnosis",
                        "type": "single_select",
                        "label": "Clinical Diagnosis",
                        "required": True,
                        "options": [
                            "Uncomplicated umbilical hernia",
                            "Uncomplicated epigastric hernia",
                            "Paraumbilical hernia",
                            "Incarcerated hernia - URGENT REFERRAL",
                            "Strangulated hernia - URGENT REFERRAL",
                            "Incisional hernia",
                            "Diastasis recti (no true hernia)",
                            "Uncertain - consider USS/referral"
                        ],
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Incarcerated/strangulated hernia - URGENT same-day ED/surgical assessment.",
                        "red_flag_negative": "",
                        "output_phrase": "Diagnosis: {value}"
                    },
                    {
                        "id": "hernia_complications",
                        "type": "multi_select",
                        "label": "Complications Present",
                        "required": False,
                        "options": [
                            "None",
                            "Incarceration - RED FLAG",
                            "Strangulation - RED FLAG",
                            "Obstruction - RED FLAG",
                            "None"
                        ],
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: {value} - urgent surgical/ED assessment required.",
                        "red_flag_negative": "",
                        "output_phrase": "Complications: {value}"
                    }
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "URGENT ED/SURGICAL ASSESSMENT if: Sudden severe or escalating pain, hernia becomes irreducible, tender/tense/firm lump, overlying erythema/discolouration, nausea/vomiting, abdominal distension, obstruction (failure to pass stool/flatus), systemic illness. If strangulation is suspected - DO NOT attempt repeated forceful reduction.",
                "questions": [
                    {
                        "id": "hernia_management_type",
                        "type": "single_select",
                        "label": "Management Plan",
                        "required": True,
                        "options": [
                            "Reassurance - asymptomatic/minimally symptomatic",
                            "Lifestyle advice (weight, constipation, cough)",
                            "Routine surgical referral - symptomatic/enlarging/recurrent pain",
                            "Same-day ED assessment - URGENT (incarceration/strangulation)",
                            "Surgical referral - as per patient preference"
                        ],
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Same-day ED assessment required - urgent surgical review.",
                        "red_flag_negative": "",
                        "output_phrase": "Management: {value}"
                    },
                    {
                        "id": "hernia_lifestyle_advice",
                        "type": "multi_select",
                        "label": "Lifestyle Advice Given",
                        "required": False,
                        "options": [
                            "Weight management",
                            "Avoid constipation/straining",
                            "Address chronic cough",
                            "Avoid heavy lifting",
                            "Smoking cessation",
                            "None"
                        ],
                        "output_phrase": "Lifestyle advice: {value}"
                    },
                    {
                        "id": "hernia_reassurance",
                        "type": "toggle",
                        "label": "Reassurance Given",
                        "required": False,
                        "output_phrase": "Reassurance: {value}"
                    },
                    {
                        "id": "hernia_surgical_referral",
                        "type": "single_select",
                        "label": "Surgical Referral Plan",
                        "required": True,
                        "options": [
                            "No referral needed",
                            "General Surgery (routine)",
                            "General Surgery (urgent)",
                            "Same-day ED/Surgical assessment",
                            "Already referred"
                        ],
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Same-day/urgent referral required - surgical assessment.",
                        "red_flag_negative": "",
                        "output_phrase": "Surgical referral: {value}"
                    },
                    {
                        "id": "hernia_imaging",
                        "type": "single_select",
                        "label": "Imaging Plan",
                        "required": False,
                        "options": [
                            "No imaging needed",
                            "USS (if diagnosis uncertain)",
                            "CT scan (if clinically indicated)",
                            "Already done"
                        ],
                        "output_phrase": "Imaging: {value}"
                    },
                    {
                        "id": "hernia_red_flag_advice",
                        "type": "toggle",
                        "label": "Red Flag Advice Given to Patient",
                        "required": False,
                        "output_phrase": "Red flag advice: {value}"
                    },
                    {
                        "id": "hernia_followup",
                        "type": "single_select",
                        "label": "Follow-up Plan",
                        "required": True,
                        "options": [
                            "No follow-up needed",
                            "Review in 3 months",
                            "Review in 6 months",
                            "As needed",
                            "Specialist follow-up arranged"
                        ],
                        "output_phrase": "Follow-up: {value}"
                    },
                    {
                        "id": "hernia_notes",
                        "type": "textarea",
                        "label": "Additional Notes",
                        "required": False,
                        "placeholder": "e.g., Patient education, shared decision-making, work/sports advice",
                        "output_phrase": "Notes: {value}"
                    }
                ]
            }
        ]},
        "is_public": True
    }

    existing = db.query(Template).filter(Template.title == t["title"], Template.created_by == admin.id).first()
    
    if existing:
        existing.description = t["description"]
        existing.content = t["content"]
        existing.category = t["category"]
        existing.is_public = t["is_public"]
        existing.updated_at = datetime.now(timezone.utc)
        db.commit()
        print(f"🔄 Updated: {t['title']}")
    else:
        new_t = Template(
            title=t["title"], 
            description=t["description"], 
            category=t["category"], 
            content=t["content"], 
            is_public=True, 
            created_by=admin.id, 
            version=1
        )
        db.add(new_t)
        db.commit()
        print(f"✅ Template '{t['title']}' created with {len(t['content']['sections'])} sections!")
    
    db.close()

if __name__ == "__main__":
    seed_hernia()
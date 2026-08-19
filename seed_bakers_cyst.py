from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_bakers_cyst():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: 
        print("Admin not found.")
        db.close()
        return

    category = db.query(Category).filter(Category.name == "Musculoskeletal").first()
    if not category: 
        category = Category(name="Musculoskeletal")
        db.add(category)
        db.commit()

    t = {
        "title": "Baker's Cyst Assessment",
        "description": "Assessment for patients presenting with posterior knee swelling (Baker's cyst), covering differential diagnosis and management.",
        "category": "Musculoskeletal",
        "content": {"sections": [
            {
                "title": "History",
                "section_type": "history",
                "questions": [
                    {
                        "id": "bakers_presenting_complaint",
                        "type": "text",
                        "label": "Presenting Complaint",
                        "required": True,
                        "placeholder": "e.g., Swelling behind the knee for 2 weeks",
                        "output_phrase": "c/o: {value}"
                    },
                    {
                        "id": "bakers_duration",
                        "type": "text",
                        "label": "Duration of Symptoms",
                        "required": True,
                        "placeholder": "e.g., 2 weeks",
                        "output_phrase": "Duration: {value}"
                    },
                    {
                        "id": "bakers_onset",
                        "type": "single_select",
                        "label": "Onset",
                        "required": True,
                        "options": ["Sudden", "Gradual", "After injury"],
                        "output_phrase": "Onset: {value}"
                    },
                    {
                        "id": "bakers_swelling",
                        "type": "text",
                        "label": "Swelling Description",
                        "required": True,
                        "placeholder": "e.g., Small swelling behind knee, soft",
                        "output_phrase": "Swelling: {value}"
                    },
                    {
                        "id": "bakers_pain",
                        "type": "single_select",
                        "label": "Pain",
                        "required": True,
                        "options": ["No pain", "Mild", "Moderate - limiting activity", "Severe - RED FLAG"],
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Severe pain - consider DVT, rupture, infection.",
                        "red_flag_negative": "",
                        "output_phrase": "Pain: {value}"
                    },
                    {
                        "id": "bakers_range_motion",
                        "type": "single_select",
                        "label": "Range of Motion",
                        "required": True,
                        "options": ["Full ROM", "Slightly limited", "Significantly limited - RED FLAG", "Unable to weight bear - RED FLAG"],
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Significantly limited ROM / unable to weight bear - urgent ortho review.",
                        "red_flag_negative": "",
                        "output_phrase": "ROM: {value}"
                    },
                    {
                        "id": "bakers_dvt_screen",
                        "type": "multi_select",
                        "label": "DVT Red Flag Screen",
                        "required": True,
                        "options": ["Calf swelling (unilateral)", "Calf pain", "Redness/heat", "Warmth", "Wells score high", "None"],
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: DVT symptoms - consider Doppler and anticoagulation.",
                        "red_flag_negative": "",
                        "output_phrase": "DVT screen: {value}"
                    },
                    {
                        "id": "bakers_associated",
                        "type": "multi_select",
                        "label": "Associated Symptoms",
                        "required": False,
                        "options": ["Clicking", "Locking", "Giving way", "Stiffness", "Redness - RED FLAG", "Fever - RED FLAG", "None"],
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Fever/redness - consider septic arthritis.",
                        "red_flag_negative": "",
                        "output_phrase": "Associated: {value}"
                    },
                    {
                        "id": "bakers_knee_history",
                        "type": "textarea",
                        "label": "Previous Knee Problems",
                        "required": False,
                        "placeholder": "e.g., OA, previous meniscal tear, injury",
                        "output_phrase": "Knee history: {value}"
                    },
                    {
                        "id": "bakers_risk_factors",
                        "type": "multi_select",
                        "label": "Risk Factors",
                        "required": False,
                        "options": ["Osteoarthritis", "Rheumatoid arthritis", "Meniscal tear", "Obesity", "Age >40", "None"],
                        "output_phrase": "Risk factors: {value}"
                    }
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {
                        "id": "bakers_inspection",
                        "type": "textarea",
                        "label": "Inspection",
                        "required": True,
                        "placeholder": "e.g., Swelling in popliteal fossa, no redness",
                        "output_phrase": "Inspection: {value}"
                    },
                    {
                        "id": "bakers_palpation",
                        "type": "textarea",
                        "label": "Palpation",
                        "required": True,
                        "placeholder": "e.g., Soft, fluctuant swelling, non-tender",
                        "output_phrase": "Palpation: {value}"
                    },
                    {
                        "id": "bakers_rom",
                        "type": "textarea",
                        "label": "Range of Motion",
                        "required": True,
                        "placeholder": "e.g., Full extension, flexion to 120 degrees",
                        "output_phrase": "ROM: {value}"
                    },
                    {
                        "id": "bakers_special_tests",
                        "type": "textarea",
                        "label": "Special Tests",
                        "required": False,
                        "placeholder": "e.g., McMurray's negative, Lachman's negative",
                        "output_phrase": "Special tests: {value}"
                    },
                    {
                        "id": "bakers_vascular",
                        "type": "single_select",
                        "label": "Vascular Assessment",
                        "required": True,
                        "options": ["Pedal pulses present, normal", "Absent/reduced pulse - RED FLAG", "Calf tenderness - consider DVT", "Normal"],
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Absent/reduced pulse or calf tenderness - urgent DVT scan.",
                        "red_flag_negative": "",
                        "output_phrase": "Vascular: {value}"
                    }
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "Baker's cyst (most common)",
                    "DVT (must exclude)",
                    "Ruptured Baker's cyst (painful, mimic DVT)",
                    "Meniscal cyst",
                    "Popliteal aneurysm (red flag)",
                    "Lipoma",
                    "Ganglion cyst",
                    "Sarcomas (rare but red flag)"
                ],
                "questions": [
                    {
                        "id": "bakers_diagnosis",
                        "type": "single_select",
                        "label": "Clinical Impression",
                        "required": True,
                        "options": ["Baker's cyst", "DVT suspected - refer for USS", "Ruptured Baker's cyst", "Popliteal aneurysm suspected - RED FLAG", "Meniscal cyst", "Other"],
                        "output_phrase": "Diagnosis: {value}"
                    },
                    {
                        "id": "bakers_dvt_risk",
                        "type": "single_select",
                        "label": "DVT Risk Assessment (Wells Score)",
                        "required": False,
                        "options": ["Low risk (<2)", "Moderate risk (2-6)", "High risk (>6) - urgent USS"],
                        "output_phrase": "DVT risk: {value}"
                    }
                ]
            },
            {
                "title": "Plan",
                "section_type": "plan",
                "safety_netting": "Return if: Pain worsens, swelling increases, calf becomes painful/red/hot (DVT), signs of infection (fever, redness), or unable to weight bear. If suspicious of DVT: urgent Doppler USS. If persistent or symptomatic: consider USS to confirm and assess size.",
                "questions": [
                    {
                        "id": "bakers_management",
                        "type": "multi_select",
                        "label": "Management Options",
                        "required": True,
                        "options": ["Reassurance", "Conservative (rest, ice, elevation)", "Analgesia (paracetamol/ibuprofen)", "Compression", "Aspiration (if large/symptomatic)", "Referral to orthopaedics", "USS/DVT scan"],
                        "output_phrase": "Management: {value}"
                    },
                    {
                        "id": "bakers_referral",
                        "type": "single_select",
                        "label": "Referral Plan",
                        "required": True,
                        "options": ["No referral needed", "Orthopaedics (routine)", "Orthopaedics (urgent)", "DVT clinic/Doppler USS", "MSK physiotherapy"],
                        "output_phrase": "Referral: {value}"
                    },
                    {
                        "id": "bakers_followup",
                        "type": "text",
                        "label": "Follow-up Plan",
                        "required": True,
                        "placeholder": "e.g., Review in 4 weeks, or sooner if worsens",
                        "output_phrase": "Follow-up: {value}"
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
    seed_bakers_cyst()
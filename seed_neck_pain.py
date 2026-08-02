from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_neck_pain():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Musculoskeletal").first()
    if not category: category = Category(name="Musculoskeletal"); db.add(category); db.commit()

    t = {
        "title": "Neck Pain / Cervicalgia",
        "description": "Focused neck pain assessment covering mechanical vs radicular causes, red flags for myelopathy/malignancy, and conservative management.",
        "category": "Musculoskeletal",
        "content": {"sections": [
            {
                "title": "History",
                "section_type": "history",
                "questions": [
                    {"id": "neck_presenting_complaint", "type": "text", "label": "Presenting Complaint", "required": True, "placeholder": "e.g., Neck pain and stiffness for 1 week"},
                    {"id": "neck_onset", "type": "single_select", "label": "Onset", "required": True, "options": ["Acute (Wry Neck / Muscle Spasm)", "Gradual", "Post-Trauma / Whiplash"]},
                    {"id": "neck_radiation", "type": "toggle", "label": "Radiating to Arm/Hand? (Radiculopathy)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Arm radiation + neurological symptoms = ?cervical radiculopathy. MRI + orthopaedics.", "red_flag_negative": ""},
                    {"id": "neck_red_flags", "type": "multi_select", "label": "Red Flags", "required": True, "options": ["Bilateral Arm Paraesthesia/Weakness (?Myelopathy)", "Gait Disturbance (?Myelopathy)", "Night Pain (?Malignancy)", "Weight Loss (?Malignancy)", "Fever (?Infection)", "None"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Myelopathy signs = urgent MRI + neurosurgery. Night pain/weight loss = ?malignancy.", "red_flag_negative": ""},
                    {"id": "neck_posture", "type": "multi_select", "label": "Contributing Factors", "required": False, "options": ["Desk Work / Poor Posture", "Sleeping Position", "Stress", "Repetitive Strain"]}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "neck_rom", "type": "single_select", "label": "Range of Movement", "required": True, "options": ["Full", "Restricted - All Directions", "Restricted - Rotation Only", "Restricted - Extension Only"]},
                    {"id": "neck_neuro_upper", "type": "single_select", "label": "Upper Limb Neurological Exam (Power, Sensation, Reflexes)", "required": True, "options": ["Normal", "Abnormal - RED FLAG (?Radiculopathy/Myelopathy)"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Neurological deficit = MRI cervical spine + orthopaedics/neurosurgery.", "red_flag_negative": ""},
                    {"id": "neck_spurling", "type": "toggle", "label": "Spurling's Test Positive? (Radiculopathy)", "required": False}
                ]
            },
            {
                "title": "Assessment & Plan",
                "section_type": "plan",
                "safety_netting": "Return if: bilateral arm symptoms, gait disturbance, night pain, weight loss, fever. Most neck pain is mechanical - resolves within 4-6 weeks. Analgesia: Paracetamol + NSAIDs if no CI. Physiotherapy: posture correction, ergonomic advice, exercises. Avoid prolonged driving/desk work without breaks. Heat/cold therapy. If radiculopathy: consider neuropathic agent (Gabapentin/Amitriptyline) + MRI. If myelopathy signs: urgent MRI + neurosurgery. If red flags for malignancy/infection: urgent investigation.",
                "questions": [
                    {"id": "neck_diagnosis", "type": "single_select", "label": "Impression", "required": True, "options": ["Mechanical Neck Pain / Cervicalgia", "Cervical Radiculopathy", "Whiplash-Associated Disorder", "?Cervical Myelopathy - URGENT MRI", "?Malignancy - Urgent Investigation"]},
                    {"id": "neck_xray", "type": "toggle", "label": "X-Ray Cervical Spine? (Trauma/Red Flags - Not Routine)", "required": False},
                    {"id": "neck_physio", "type": "toggle", "label": "Physiotherapy Referral?", "required": False},
                    {"id": "neck_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., Physio + review in 4-6 weeks, sooner if red flags"}
                ]
            }
        ]},
        "is_public": True
    }

    existing = db.query(Template).filter(Template.title == t["title"], Template.created_by == admin.id).first()
    
    if existing:
        print(f"⏭️  SKIPPED: {title} already exists (ID={existing.id})")
        db.close()
        return
    new_t = Template(title=t["title"], description=t["description"], category=t["category"], content=t["content"], is_public=True, created_by=admin.id, version=1)
    db.add(new_t); db.commit()
    print(f"Template '{t['title']}' created!"); db.close()

if __name__ == "__main__":
    seed_neck_pain()
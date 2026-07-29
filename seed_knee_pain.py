from app.database import SessionLocal
from app.models import User, Template, Category

def seed_knee_pain():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Musculoskeletal").first()
    if not category: category = Category(name="Musculoskeletal"); db.add(category); db.commit()

    t = {
        "title": "Knee Pain",
        "description": "Focused knee pain assessment covering acute injury vs degenerative causes, red flags for septic arthritis, and management.",
        "category": "Musculoskeletal",
        "content": {"sections": [
            {
                "title": "History",
                "section_type": "history",
                "questions": [
                    {"id": "knee_presenting_complaint", "type": "text", "label": "Presenting Complaint", "required": True, "placeholder": "e.g., Right knee pain for 2 weeks"},
                    {"id": "knee_onset", "type": "single_select", "label": "Onset", "required": True, "options": ["Acute Injury / Trauma", "Gradual (Weeks-Months)", "Acute on Chronic"]},
                    {"id": "knee_trauma_mechanism", "type": "single_select", "label": "Mechanism of Injury (If Traumatic)", "required": False, "options": ["Twisting (Meniscal/ACL)", "Direct Blow", "Fall onto Knee", "Hyperextension", "No Trauma"]},
                    {"id": "knee_swelling", "type": "single_select", "label": "Swelling Onset", "required": True, "options": ["Immediate (Within 2h = Haemarthrosis ?ACL/Fracture)", "Delayed (Next Day = Effusion ?Meniscal)", "No Swelling"]},
                    {"id": "knee_locking", "type": "toggle", "label": "Locking / Giving Way?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Locking = ?meniscal tear. Giving way = ?ACL. Refer orthopaedics.", "red_flag_negative": ""},
                    {"id": "knee_red_flags", "type": "multi_select", "label": "Red Flags", "required": True, "options": ["Fever / Systemically Unwell (?Septic Arthritis)", "Inability to Weight Bear", "Gross Deformity", "None"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Septic arthritis = hot, swollen, tender, fever, unable to WB. EMERGENCY - same-day orthopaedics.", "red_flag_negative": ""},
                    {"id": "knee_osteoarthritis", "type": "multi_select", "label": "OA Features", "required": False, "options": ["Age >45", "Morning Stiffness <30 Min", "Crepitus", "Bony Tenderness", "No Warmth", "Pain Worse with Activity"]}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "knee_swelling_exam", "type": "single_select", "label": "Effusion", "required": True, "options": ["Present (Patellar Tap / Bulge Sign)", "Absent"]},
                    {"id": "knee_temp", "type": "toggle", "label": "Hot / Warm? (?Septic/Inflammatory)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Hot + swollen + fever = ?septic arthritis. EMERGENCY.", "red_flag_negative": ""},
                    {"id": "knee_rom", "type": "single_select", "label": "Range of Movement", "required": True, "options": ["Full", "Restricted Flexion", "Restricted Extension", "Fixed Flexion Deformity"]},
                    {"id": "knee_tenderness", "type": "single_select", "label": "Tenderness Location", "required": False, "options": ["Medial Joint Line (?Meniscal/OA)", "Lateral Joint Line (?Meniscal)", "Patellofemoral", "Generalised"]}
                ]
            },
            {
                "title": "Assessment & Plan",
                "section_type": "plan",
                "safety_netting": "Return if: knee becomes hot/swollen/red, inability to weight bear, fever develops (septic arthritis - EMERGENCY). Acute injury with locking/giving way: refer orthopaedics. OA: weight loss, physiotherapy, analgesia (Paracetamol + NSAIDs if no CI), consider intra-articular steroid injection. X-ray if: age >55, bony tenderness, inability to weight bear, deformity. Physiotherapy referral for most knee pain. Knee exercises: quadriceps strengthening, hamstring stretches.",
                "questions": [
                    {"id": "knee_diagnosis", "type": "single_select", "label": "Impression", "required": True, "options": ["?Meniscal Tear", "?ACL Injury", "Osteoarthritis", "Patellofemoral Pain", "?Septic Arthritis - EMERGENCY", "Soft Tissue Injury"]},
                    {"id": "knee_xray", "type": "toggle", "label": "X-Ray Knee? (Ottawa Rules: Age >55, Bony Tenderness, Unable to WB, Deformity)", "required": False},
                    {"id": "knee_physio", "type": "toggle", "label": "Physiotherapy Referral?", "required": False},
                    {"id": "knee_ortho", "type": "toggle", "label": "Orthopaedic Referral? (Locking/Giving Way/Suspected ACL)", "required": False},
                    {"id": "knee_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., Physio + review in 4-6 weeks, sooner if red flags"}
                ]
            }
        ]},
        "is_public": True
    }

    existing = db.query(Template).filter(Template.title == t["title"], Template.created_by == admin.id).first()
    if existing: db.delete(existing); db.commit()
    new_t = Template(title=t["title"], description=t["description"], category=t["category"], content=t["content"], is_public=True, created_by=admin.id, version=1)
    db.add(new_t); db.commit()
    print(f"Template '{t['title']}' created!"); db.close()

if __name__ == "__main__":
    seed_knee_pain()
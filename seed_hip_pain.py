from app.database import SessionLocal
from app.models import User, Template, Category

def seed_hip_pain():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Musculoskeletal").first()
    if not category: category = Category(name="Musculoskeletal"); db.add(category); db.commit()

    t = {
        "title": "Hip Pain",
        "description": "Focused hip pain assessment covering OA, trochanteric bursitis, referred pain, red flags for septic arthritis/fracture, and management.",
        "category": "Musculoskeletal",
        "content": {"sections": [
            {
                "title": "History",
                "section_type": "history",
                "questions": [
                    {"id": "hip_presenting_complaint", "type": "text", "label": "Presenting Complaint", "required": True, "placeholder": "e.g., Left hip pain for 3 months"},
                    {"id": "hip_age", "type": "number", "label": "Age", "required": True, "placeholder": "e.g., 68"},
                    {"id": "hip_onset", "type": "single_select", "label": "Onset", "required": True, "options": ["Acute (Trauma/Fall)", "Gradual (Weeks-Months)"]},
                    {"id": "hip_site", "type": "single_select", "label": "Pain Location", "required": True, "options": ["Groin (Hip Joint)", "Lateral Hip (Trochanteric Bursitis)", "Buttock (Referred from Back/SIJ)", "Thigh"]},
                    {"id": "hip_oa_features", "type": "multi_select", "label": "OA Features", "required": False, "options": ["Age >45", "Morning Stiffness <30 Min", "Pain Worse with Activity", "Relieved by Rest", "Restricted ROM"]},
                    {"id": "hip_red_flags", "type": "multi_select", "label": "Red Flags", "required": True, "options": ["Unable to Weight Bear (?Fracture)", "Fever (?Septic Arthritis)", "Night Pain (?Malignancy)", "Weight Loss (?Malignancy)", "Trauma (?Fracture NOF)", "None"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Unable to WB = ?fracture NOF. Urgent X-ray + orthopaedics. Fever = ?septic. Night pain/weight loss = ?malignancy.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "hip_rom", "type": "single_select", "label": "Range of Movement", "required": True, "options": ["Full", "Restricted - Especially Internal Rotation (OA)", "Restricted - All Directions", "Pain on Resisted Abduction (Bursitis)"]},
                    {"id": "hip_trendelenburg", "type": "toggle", "label": "Trendelenburg Sign Positive?", "required": False},
                    {"id": "hip_trochanteric_tenderness", "type": "toggle", "label": "Tenderness Over Greater Trochanter? (Bursitis)", "required": False},
                    {"id": "hip_back_exam", "type": "toggle", "label": "Back/SIJ Exam Normal? (Exclude Referred Pain)", "required": False}
                ]
            },
            {
                "title": "Assessment & Plan",
                "section_type": "plan",
                "safety_netting": "Return if: unable to weight bear, fever, night pain, weight loss. OA: weight loss, physiotherapy, analgesia (Paracetamol + NSAIDs if no CI). Trochanteric bursitis: NSAIDs + physiotherapy + consider steroid injection. X-ray hip if: OA suspected, trauma, ?fracture. Refer orthopaedics if: severe OA not responding to conservative, ?fracture NOF, septic arthritis. Refer physiotherapy for most hip pain.",
                "questions": [
                    {"id": "hip_diagnosis", "type": "single_select", "label": "Impression", "required": True, "options": ["Osteoarthritis - Hip", "Trochanteric Bursitis", "Referred from Back/SIJ", "?Fracture NOF - Urgent X-Ray", "?Septic Arthritis - EMERGENCY"]},
                    {"id": "hip_xray", "type": "toggle", "label": "X-Ray Hip?", "required": False},
                    {"id": "hip_physio", "type": "toggle", "label": "Physiotherapy Referral?", "required": False},
                    {"id": "hip_ortho", "type": "toggle", "label": "Orthopaedic Referral?", "required": False},
                    {"id": "hip_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., Physio + review in 6 weeks, sooner if red flags"}
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
    seed_hip_pain()
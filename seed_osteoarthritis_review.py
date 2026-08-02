from app.database import SessionLocal
from app.models import User, Template

def seed_osteoarthritis_review():
    db = SessionLocal()
    admin = db.query(User).filter(User.role == "admin").first()
    if not admin: print("❌ No admin!"); db.close(); return

    title = "Osteoarthritis Review"
    existing = db.query(Template).filter(Template.title == title).first()
    if existing: db.delete(existing); db.commit()

    t = Template(title=title, description="Osteoarthritis review covering pain assessment, functional impact, analgesic management per NICE CG177, exercise/physiotherapy, and surgical referral criteria.", category="Musculoskeletal", content={"sections": [
        {"title": "Pain & Function", "section_type": "history", "questions": [
            {"id": "oa_joints", "type": "multi_select", "label": "Affected Joints", "required": True, "options": ["Knee(s)", "Hip(s)", "Hands (DIP/PIP/CMC)", "Spine", "Shoulder", "Ankle/Foot"]},
            {"id": "oa_pain_score", "type": "number", "label": "Pain Score (0-10)", "required": True, "placeholder": "e.g., 6"},
            {"id": "oa_pain_type", "type": "single_select", "label": "Pain Character", "required": True, "options": ["Mechanical (worse with activity, better with rest)", "Inflammatory (morning stiffness >30min)", "Constant (day and night)", "Bone-on-bone"]},
            {"id": "oa_morning_stiffness", "type": "text", "label": "Morning Stiffness Duration (minutes)", "required": True, "placeholder": "e.g., 10 minutes"},
            {"id": "oa_walking_distance", "type": "text", "label": "Walking Distance (before pain stops you)", "required": True, "placeholder": "e.g., 200 metres"},
            {"id": "oa_stairs", "type": "toggle", "label": "Difficulty with Stairs?", "required": True},
            {"id": "oa_sleep", "type": "toggle", "label": "Pain Disturbing Sleep?", "required": True},
            {"id": "oa_work_impact", "type": "single_select", "label": "Impact on Work/Daily Life", "required": True, "options": ["None", "Mild", "Moderate", "Severe - unable to work/function"]}
        ]},
        {"title": "Current Management", "section_type": "history", "questions": [
            {"id": "oa_analgesia", "type": "multi_select", "label": "Current Analgesia", "required": True, "options": ["None", "Paracetamol", "Topical NSAID", "Oral NSAID", "Codeine/Tramadol", "Strong opioids"]},
            {"id": "oa_analgesia_effective", "type": "single_select", "label": "Pain Relief Adequate?", "required": True, "options": ["Yes - well controlled", "Partially - some relief", "No - minimal relief"]},
            {"id": "oa_exercise", "type": "single_select", "label": "Exercise / Physiotherapy", "required": True, "options": ["Regular exercise", "Physiotherapy (current/past)", "None", "Unable due to pain"]},
            {"id": "oa_weight", "type": "number", "label": "Weight (kg)", "required": False, "placeholder": "e.g., 88"},
            {"id": "oa_bmi", "type": "number", "label": "BMI", "required": False, "placeholder": "e.g., 32"},
            {"id": "oa_walking_aid", "type": "toggle", "label": "Uses Walking Aid?", "required": False},
            {"id": "oa_previous_injection", "type": "toggle", "label": "Previous Joint Injection?", "required": False},
            {"id": "oa_previous_surgery", "type": "toggle", "label": "Previous Joint Surgery?", "required": False}
        ]},
        {"title": "Examination", "section_type": "examination", "questions": [
            {"id": "oa_joint_swelling", "type": "toggle", "label": "Joint Swelling/Effusion?", "required": False},
            {"id": "oa_crepitus", "type": "toggle", "label": "Crepitus on Movement?", "required": False},
            {"id": "oa_deformity", "type": "single_select", "label": "Deformity", "required": True, "options": ["None", "Varus (bow-legged)", "Valgus (knock-kneed)", "Fixed flexion", "Heberden's/Bouchard's nodes (hands)"]},
            {"id": "oa_rom", "type": "single_select", "label": "Range of Motion", "required": True, "options": ["Full", "Mild restriction", "Moderate restriction", "Severe restriction / fixed deformity"]},
            {"id": "oa_quadriceps", "type": "toggle", "label": "Quadriceps Wasting? (Knee OA)", "required": False}
        ]},
        {"title": "Red Flags", "section_type": "history", "questions": [
            {"id": "oa_red_hot", "type": "toggle", "label": "Red/Hot/Swollen Joint? (?Septic arthritis/Gout)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Hot swollen joint = ?septic arthritis. Urgent aspiration + orthopaedic referral.", "red_flag_negative": ""},
            {"id": "oa_locking", "type": "toggle", "label": "Joint Locking/Giving Way?", "required": False},
            {"id": "oa_xray", "type": "single_select", "label": "X-ray Findings", "required": False, "options": ["Not done", "Joint space narrowing", "Osteophytes", "Subchondral sclerosis/cysts", "Bone-on-bone (severe)"]}
        ]},
        {"title": "Assessment", "section_type": "assessment", "differentials": ["Primary Osteoarthritis", "Secondary OA (post-trauma, inflammatory)", "Inflammatory Arthritis (RA, PsA, Gout)", "Septic Arthritis (RED FLAG)", "Referred pain (hip OA presenting as knee pain)"]},
        {"title": "Management", "section_type": "plan", "safety_netting": "Return if: joint becomes red/hot/swollen, sudden worsening of pain, joint locking, or analgesia ineffective despite escalation. Core treatments (NICE CG177): education, weight loss (5-10% body weight), exercise (aerobic + strengthening), physiotherapy. Paracetamol + topical NSAID first-line. Oral NSAIDs (with PPI) for short courses. Avoid opioids (limited benefit, significant harm). Consider intra-articular corticosteroid injection for moderate-severe pain. Surgical referral: severe symptoms despite maximal conservative management, significant functional impairment, bone-on-bone on X-ray.", "questions": [
            {"id": "oa_plan", "type": "multi_select", "label": "Management", "required": True, "options": ["Weight loss advice (if overweight)", "Physiotherapy referral", "Exercise programme", "Walking aid", "Paracetamol PRN", "Topical NSAID (gel/cream)", "Oral NSAID + PPI (short course)", "Intra-articular steroid injection", "Orthopaedic referral (surgery)", "Pain clinic referral"]},
            {"id": "oa_injection", "type": "text", "label": "Injection Given", "required": False, "placeholder": "e.g., Depo-Medrone 40mg intra-articular knee"},
            {"id": "oa_xray_request", "type": "toggle", "label": "X-ray Requested?", "required": False},
            {"id": "oa_followup", "type": "text", "label": "Follow-up", "required": True, "placeholder": "e.g., Physio for 6 weeks, return if no improvement, weight review in 3 months"}
        ]}
    ]}, is_public=True, created_by=admin.id)
    db.add(t); db.commit(); print(f"✅ {title}"); db.close()

if __name__ == "__main__": seed_osteoarthritis_review()
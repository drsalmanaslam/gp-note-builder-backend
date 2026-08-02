from app.database import SessionLocal
from app.models import User, Template

def seed_shoulder_pain():
    db = SessionLocal()
    admin = db.query(User).filter(User.role == "admin").first()
    if not admin: print("❌ No admin!"); db.close(); return

    title = "Shoulder Pain"
    existing = db.query(Template).filter(Template.title == title).first()
    if existing: db.delete(existing); db.commit()

    t = Template(title=title, description="Assessment of shoulder pain covering rotator cuff pathology, frozen shoulder, OA, impingement, and red flags. Includes examination tests and management per NICE/BESS guidelines.", category="Musculoskeletal", content={"sections": [
        {"title": "History", "section_type": "history", "questions": [
            {"id": "sh_side", "type": "single_select", "label": "Affected Side", "required": True, "options": ["Right", "Left", "Bilateral"]},
            {"id": "sh_dominant", "type": "toggle", "label": "Dominant Arm Affected?", "required": True},
            {"id": "sh_onset", "type": "single_select", "label": "Onset", "required": True, "options": ["Acute (injury/trauma)", "Gradual (weeks-months)", "Acute-on-chronic"]},
            {"id": "sh_trauma", "type": "single_select", "label": "Trauma/Injury?", "required": True, "options": ["Fall onto shoulder", "Fall onto outstretched hand", "Lifting heavy object", "Repetitive overhead activity", "No trauma"]},
            {"id": "sh_pain_location", "type": "single_select", "label": "Pain Location", "required": True, "options": ["Anterior", "Lateral/over deltoid", "Posterior", "Deep within joint", "Radiating to elbow"]},
            {"id": "sh_pain_type", "type": "single_select", "label": "Pain Character", "required": True, "options": ["Dull ache", "Sharp/stabbing", "Burning", "Constant", "Night pain"]},
            {"id": "sh_night_pain", "type": "toggle", "label": "Pain Worse at Night? (Unable to lie on affected side)", "required": True},
            {"id": "sh_stiffness", "type": "toggle", "label": "Stiffness? (Especially external rotation)", "required": True},
            {"id": "sh_weakness", "type": "toggle", "label": "Weakness? (Overhead activities, lifting)", "required": True},
            {"id": "sh_clicking", "type": "toggle", "label": "Clicking / Catching?", "required": False},
            {"id": "sh_neck_pain", "type": "toggle", "label": "Associated Neck Pain? (Consider cervical spine referral)", "required": True},
            {"id": "sh_occupation", "type": "text", "label": "Occupation / Sport", "required": False, "placeholder": "e.g., Painter, swimmer, weightlifter"}
        ]},
        {"title": "Red Flags", "section_type": "history", "questions": [
            {"id": "sh_red_flag_trauma", "type": "toggle", "label": "Significant Trauma? (?Fracture/Dislocation)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Significant trauma = X-ray. ?Fracture, dislocation, rotator cuff tear.", "red_flag_negative": ""},
            {"id": "sh_deformity", "type": "toggle", "label": "Visible Deformity?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Deformity = ?dislocation, fracture, proximal humerus #. Urgent X-ray.", "red_flag_negative": ""},
            {"id": "sh_redness_swelling", "type": "toggle", "label": "Redness / Hot / Swollen? (?Septic arthritis)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Hot/swollen joint + fever = ?septic arthritis. Urgent aspiration and orthopaedic referral.", "red_flag_negative": ""},
            {"id": "sh_constitutional", "type": "toggle", "label": "Weight Loss / Night Sweats / Fever?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Constitutional symptoms = ?malignancy, infection. Urgent investigation.", "red_flag_negative": ""},
            {"id": "sh_neuro", "type": "toggle", "label": "Neurological Symptoms in Arm?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Neurological deficit = ?cervical radiculopathy, brachial plexus. Urgent assessment.", "red_flag_negative": ""}
        ]},
        {"title": "Examination", "section_type": "examination", "questions": [
            {"id": "sh_inspection", "type": "single_select", "label": "Inspection", "required": True, "options": ["Normal", "Muscle wasting (supraspinatus/infraspinatus)", "Deformity", "Swelling", "Scars"]},
            {"id": "sh_rom_active", "type": "single_select", "label": "Active ROM", "required": True, "options": ["Full range", "Limited abduction", "Limited flexion", "Limited external rotation", "Global limitation"]},
            {"id": "sh_rom_passive", "type": "single_select", "label": "Passive ROM", "required": True, "options": ["Full range", "Limited - capsular pattern (frozen shoulder)", "Limited - non-capsular", "Painful arc (impingement)"]},
            {"id": "sh_painful_arc", "type": "toggle", "label": "Painful Arc (60-120° abduction)?", "required": False},
            {"id": "sh_neer_test", "type": "toggle", "label": "Neer's Impingement Test Positive?", "required": False},
            {"id": "sh_hawkins_test", "type": "toggle", "label": "Hawkins-Kennedy Test Positive?", "required": False},
            {"id": "sh_supraspinatus", "type": "single_select", "label": "Supraspinatus (Empty Can / Jobe's Test)", "required": True, "options": ["Normal", "Weak/painful", "Unable to resist"]},
            {"id": "sh_infraspinatus", "type": "single_select", "label": "Infraspinatus (External Rotation Resistance)", "required": False, "options": ["Normal", "Weak/painful", "Not tested"]},
            {"id": "sh_subscapularis", "type": "single_select", "label": "Subscapularis (Lift-off / Belly Press)", "required": False, "options": ["Normal", "Weak/painful", "Not tested"]}
        ]},
        {"title": "Assessment", "section_type": "assessment", "differentials": ["Subacromial impingement / Bursitis (painful arc, positive impingement tests)", "Rotator cuff tendinopathy / tear (weakness, night pain)", "Frozen shoulder / Adhesive capsulitis (global stiffness, diabetes)", "Glenohumeral OA (crepitus, X-ray changes, older patient)", "Acromioclavicular joint OA (localised tenderness)", "Biceps tendinitis (anterior pain)", "Cervical radiculopathy (neck pain + neurological symptoms)", "Referred pain (cardiac, diaphragmatic)", "Gout / Pseudogout"], "questions": [
            {"id": "sh_diagnosis", "type": "single_select", "label": "Likely Diagnosis", "required": True, "options": ["Subacromial impingement / Bursitis", "Rotator cuff tear / tendinopathy", "Frozen shoulder", "Glenohumeral OA", "AC joint pathology", "Cervical spine referral", "Other"]},
            {"id": "sh_xray", "type": "toggle", "label": "X-ray Requested?", "required": False},
            {"id": "sh_uss", "type": "toggle", "label": "Ultrasound Requested? (Rotator cuff assessment)", "required": False}
        ]},
        {"title": "Management", "section_type": "plan", "safety_netting": "Return if: severe pain not controlled, new weakness, deformity, redness/swelling, or neurological symptoms. Most shoulder pain improves with conservative management. Physiotherapy is key - exercise programmes as effective as surgery for impingement. Corticosteroid injection provides short-term relief (max 3 per year). Frozen shoulder: natural history 1-3 years, physio + consider hydrodilatation or MUA if severe. Rotator cuff tear: physio first-line, surgical repair if traumatic full-thickness tear in younger patients.", "questions": [
            {"id": "sh_plan", "type": "multi_select", "label": "Management", "required": True, "options": ["Analgesia (Paracetamol + NSAID)", "Physiotherapy referral", "Corticosteroid injection", "Subacromial injection", "X-ray shoulder", "USS shoulder", "Orthopaedic referral", "Pain clinic referral", "Sick note"]},
            {"id": "sh_physio_exercises", "type": "toggle", "label": "Exercises / Physio Leaflet Given?", "required": True},
            {"id": "sh_activity_modification", "type": "toggle", "label": "Activity Modification Advised?", "required": True},
            {"id": "sh_injection", "type": "text", "label": "Injection Given", "required": False, "placeholder": "e.g., Depo-Medrone 40mg + Lidocaine subacromial"},
            {"id": "sh_followup", "type": "text", "label": "Follow-up", "required": True, "placeholder": "e.g., Physio for 6 weeks, return if no improvement, orthopaedic referral if persistent"}
        ]}
    ]}, is_public=True, created_by=admin.id)
    db.add(t); db.commit(); print(f"✅ {title}"); db.close()

if __name__ == "__main__": seed_shoulder_pain()
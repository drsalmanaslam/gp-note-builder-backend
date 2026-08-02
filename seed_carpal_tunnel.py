from app.database import SessionLocal
from app.models import User, Template

def seed_carpal_tunnel():
    db = SessionLocal()
    admin = db.query(User).filter(User.role == "admin").first()
    if not admin: print("❌ No admin!"); db.close(); return

    title = "Carpal Tunnel Syndrome"
    existing = db.query(Template).filter(Template.title == title).first()
    if existing: db.delete(existing); db.commit()

    t = Template(title=title, description="Assessment of carpal tunnel syndrome covering Phalen/Tinel tests, nocturnal symptoms, conservative vs surgical management, and NICE guidance.", category="Musculoskeletal", content={"sections": [
        {"title": "History", "section_type": "history", "questions": [
            {"id": "cts_hand", "type": "single_select", "label": "Affected Hand", "required": True, "options": ["Right", "Left", "Bilateral"]},
            {"id": "cts_dominant", "type": "toggle", "label": "Dominant Hand Affected?", "required": True},
            {"id": "cts_numbness", "type": "multi_select", "label": "Numbness/Tingling Distribution", "required": True, "options": ["Thumb", "Index finger", "Middle finger", "Ring finger (radial half)", "Whole hand", "Extending to forearm"]},
            {"id": "cts_nocturnal", "type": "toggle", "label": "Worse at Night? (Wakes from sleep)", "required": True},
            {"id": "cts_shaking", "type": "toggle", "label": "Relieved by Shaking Hand?", "required": True},
            {"id": "cts_weakness", "type": "toggle", "label": "Weakness / Dropping Objects?", "required": True},
            {"id": "cts_duration", "type": "text", "label": "Duration", "required": True, "placeholder": "e.g., 3 months"},
            {"id": "cts_occupation", "type": "text", "label": "Occupation / Repetitive Activities", "required": False, "placeholder": "e.g., Typing, assembly line, hairdresser"},
            {"id": "cts_pregnancy", "type": "toggle", "label": "Pregnant? (Fluid retention)", "required": False},
            {"id": "cts_diabetes", "type": "toggle", "label": "Diabetes?", "required": True},
            {"id": "cts_hypothyroid", "type": "toggle", "label": "Hypothyroidism?", "required": True},
            {"id": "cts_neck_pain", "type": "toggle", "label": "Neck Pain? (?Cervical radiculopathy)", "required": True}
        ]},
        {"title": "Examination", "section_type": "examination", "questions": [
            {"id": "cts_thenar_wasting", "type": "toggle", "label": "Thenar Wasting? (Chronic/severe)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Thenar wasting = severe median nerve compression. Urgent nerve conduction studies + surgical referral.", "red_flag_negative": ""},
            {"id": "cts_phalen", "type": "toggle", "label": "Phalen's Test Positive? (Symptoms reproduced with wrist flexion x60s)", "required": True},
            {"id": "cts_tinel", "type": "toggle", "label": "Tinel's Sign Positive? (Tapping over carpal tunnel)", "required": True},
            {"id": "cts_sensation", "type": "single_select", "label": "Sensation (Median Nerve Distribution)", "required": True, "options": ["Normal", "Reduced", "Absent"]},
            {"id": "cts_power", "type": "single_select", "label": "Thumb Abduction (APB) Power", "required": True, "options": ["Normal (MRC 5/5)", "Mild weakness (4/5)", "Moderate weakness (3/5)", "Severe weakness (≤2/5)"]}
        ]},
        {"title": "Assessment", "section_type": "assessment", "differentials": ["Carpal Tunnel Syndrome (median nerve compression)", "Cervical Radiculopathy (C6/C7 - neck pain + arm symptoms)", "Peripheral Neuropathy (diabetic, B12 deficiency)", "de Quervain's Tenosynovitis (radial wrist pain)", "OA of thumb CMC joint", "Ulnar nerve compression (ring + little finger)"], "questions": [
            {"id": "cts_severity", "type": "single_select", "label": "Severity", "required": True, "options": ["Mild - intermittent symptoms, no neurological deficit", "Moderate - persistent symptoms, mild sensory loss", "Severe - thenar wasting, constant numbness, weakness"]},
            {"id": "cts_nerve_studies", "type": "toggle", "label": "Nerve Conduction Studies Requested?", "required": False}
        ]},
        {"title": "Management", "section_type": "plan", "safety_netting": "Return if: worsening weakness, dropping objects, constant numbness, or thenar wasting develops. Mild-moderate: night splints (wrist in neutral), activity modification, NSAIDs. Consider corticosteroid injection (up to 2 injections, 6 weeks apart). Severe/progressive: refer for nerve conduction studies + surgical decompression. Pregnant women: usually resolves postpartum, conservative management. If suspected cervical radiculopathy: examine neck + upper limb neurology.", "questions": [
            {"id": "cts_plan", "type": "multi_select", "label": "Management", "required": True, "options": ["Night splint (wrist neutral)", "Activity modification", "NSAIDs / Analgesia", "Corticosteroid injection", "Nerve conduction studies", "Orthopaedic / Plastics referral (surgery)", "Physiotherapy"]},
            {"id": "cts_splint", "type": "toggle", "label": "Splint Prescribed/Advised?", "required": False},
            {"id": "cts_injection", "type": "text", "label": "Injection Given", "required": False, "placeholder": "e.g., Depo-Medrone 20mg + Lidocaine"},
            {"id": "cts_followup", "type": "text", "label": "Follow-up", "required": True, "placeholder": "e.g., Review 6 weeks after splint/injection, nerve studies, surgical referral if no improvement"}
        ]}
    ]}, is_public=True, created_by=admin.id)
    db.add(t); db.commit(); print(f"✅ {title}"); db.close()

if __name__ == "__main__": seed_carpal_tunnel()
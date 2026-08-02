from app.database import SessionLocal
from app.models import User, Template

def seed_chronic_pain():
    db = SessionLocal()
    admin = db.query(User).filter(User.role == "admin").first()
    if not admin: print("❌ No admin!"); db.close(); return

    title = "Chronic Pain & Opioid Review"
    existing = db.query(Template).filter(Template.title == title).first()
    if existing: db.delete(existing); db.commit()

    t = Template(title=title, description="Chronic pain assessment and opioid stewardship covering pain characterisation, opioid effectiveness/risks, deprescribing, and non-pharmacological management per NICE NG193 and Faculty of Pain Medicine guidance.", category="General Practice", content={"sections": [
        {"title": "Pain Assessment", "section_type": "history", "questions": [
            {"id": "cp_site", "type": "text", "label": "Primary Pain Site(s)", "required": True, "placeholder": "e.g., Chronic low back pain"},
            {"id": "cp_duration", "type": "text", "label": "Duration", "required": True, "placeholder": "e.g., 5 years"},
            {"id": "cp_diagnosis", "type": "text", "label": "Underlying Diagnosis", "required": True, "placeholder": "e.g., Mechanical LBP, Fibromyalgia, OA"},
            {"id": "cp_pain_score", "type": "number", "label": "Average Pain Score (0-10)", "required": True, "placeholder": "e.g., 7"},
            {"id": "cp_pain_type", "type": "multi_select", "label": "Pain Type", "required": True, "options": ["Nociceptive (mechanical)", "Neuropathic (burning/shooting)", "Nociplastic (central sensitisation)", "Mixed"]},
            {"id": "cp_sleep", "type": "single_select", "label": "Sleep Disturbance", "required": True, "options": ["None", "Mild", "Moderate - wakes frequently", "Severe - cannot sleep"]},
            {"id": "cp_mood", "type": "single_select", "label": "Mood Impact", "required": True, "options": ["None", "Mild low mood", "Moderate depression/anxiety", "Severe - suicidal"]},
            {"id": "cp_function", "type": "single_select", "label": "Functional Impact", "required": True, "options": ["Independent", "Mild limitation", "Moderate - needs help", "Severe - housebound/bedbound"]}
        ]},
        {"title": "Current Analgesia Review", "section_type": "history", "questions": [
            {"id": "cp_opioid", "type": "text", "label": "Current Opioid (Drug + Dose)", "required": True, "placeholder": "e.g., Tramadol 100mg QDS, Morphine MR 20mg BD"},
            {"id": "cp_opioid_duration", "type": "text", "label": "Duration on Opioid", "required": True, "placeholder": "e.g., 2 years"},
            {"id": "cp_opioid_effectiveness", "type": "single_select", "label": "Opioid Effectiveness (Pain Relief %)", "required": True, "options": ["Good (>50% relief)", "Partial (30-50%)", "Minimal (<30%)", "None - taking out of habit"]},
            {"id": "cp_opioid_side_effects", "type": "multi_select", "label": "Opioid Side Effects", "required": True, "options": ["Constipation", "Drowsiness/sedation", "Nausea", "Confusion/cognitive impairment", "Low mood", "Loss of libido", "Hyperalgesia (pain worse)", "None"]},
            {"id": "cp_opioid_risk", "type": "multi_select", "label": "Opioid Risk Factors", "required": True, "options": ["Dose escalation (tolerance)", "Requesting early prescriptions", "Using more than prescribed", "Obtaining from other sources", "Previous substance misuse", "None"]},
            {"id": "cp_other_meds", "type": "text", "label": "Other Analgesics/Adjuvants", "required": False, "placeholder": "e.g., Pregabalin 150mg BD, Paracetamol, Amitriptyline 25mg"},
            {"id": "cp_non_pharm", "type": "multi_select", "label": "Non-Pharmacological Approaches Tried", "required": True, "options": ["Physiotherapy", "Exercise programme", "CBT / Pain management programme", "Acupuncture", "TENS", "Mindfulness/meditation", "Heat/cold therapy", "None"]}
        ]},
        {"title": "Examination", "section_type": "examination", "questions": [
            {"id": "cp_bp", "type": "text", "label": "Blood Pressure", "required": False, "placeholder": "e.g., 135/85"},
            {"id": "cp_weight", "type": "number", "label": "Weight (kg)", "required": False, "placeholder": "e.g., 82"},
            {"id": "cp_gait", "type": "single_select", "label": "Gait / Mobility", "required": True, "options": ["Normal", "Antalgic gait", "Uses walking aid", "Wheelchair/bedbound"]},
            {"id": "cp_site_exam", "type": "text", "label": "Examination Findings (pain site)", "required": False, "placeholder": "e.g., Paraspinal muscle spasm, reduced lumbar flexion"}
        ]},
        {"title": "Assessment", "section_type": "assessment", "differentials": ["Chronic primary pain (no clear underlying cause)", "Chronic secondary pain (OA, neuropathy, post-surgical)", "Opioid-induced hyperalgesia (paradoxical worsening)", "Opioid dependence / misuse", "Co-existing depression/anxiety amplifying pain", "Inadequate non-pharmacological management"], "questions": [
            {"id": "cp_benefit_risk", "type": "single_select", "label": "Opioid Benefit vs Risk", "required": True, "options": ["Clear benefit, manageable risks - continue", "Marginal benefit - consider dose reduction", "No benefit - deprescribe", "Evidence of harm/misuse - MUST deprescribe"]},
            {"id": "cp_deprescribe_readiness", "type": "single_select", "label": "Patient Readiness to Reduce Opioids", "required": True, "options": ["Ready - wants to reduce", "Willing to consider", "Ambivalent/hesitant", "Not willing - resistance"]}
        ]},
        {"title": "Management", "section_type": "plan", "safety_netting": "Opioids have limited evidence for chronic non-cancer pain beyond 3 months. Risks: tolerance, dependence, opioid-induced hyperalgesia, constipation, falls, cognitive impairment, respiratory depression, overdose death. Taper slowly: reduce by 10% of original dose every 1-2 weeks. Never stop abruptly. Refer to pain management programme (multidisciplinary: physio, psychology, OT). Adjuvant medications: consider amitriptyline/gabapentin/pregabalin for neuropathic pain, duloxetine for pain + depression. Return if: severe withdrawal symptoms, suicidal ideation, or pain crisis.", "questions": [
            {"id": "cp_plan", "type": "multi_select", "label": "Management Plan", "required": True, "options": ["Continue current opioids - stable dose", "Opioid dose reduction (taper plan)", "Switch to buprenorphine (safer profile)", "Stop opioids - deprescribe", "Add adjuvant (amitriptyline, pregabalin)", "Refer to pain management programme", "Refer to pain psychology / CBT", "Physiotherapy / exercise referral", "Social prescribing / community support"]},
            {"id": "cp_taper_plan", "type": "text", "label": "Taper Plan", "required": False, "placeholder": "e.g., Reduce morphine by 5mg every 2 weeks, review monthly"},
            {"id": "cp_new_med", "type": "text", "label": "New Medication", "required": False, "placeholder": "e.g., Duloxetine 30mg OD, titrate to 60mg"},
            {"id": "cp_naloxone", "type": "toggle", "label": "Naloxone Kit Discussed? (High-dose opioids >120mg morphine equivalent)", "required": False},
            {"id": "cp_followup", "type": "text", "label": "Follow-up", "required": True, "placeholder": "e.g., Monthly review during taper, pain programme referral, repeat in 4 weeks"}
        ]}
    ]}, is_public=True, created_by=admin.id)
    db.add(t); db.commit(); print(f"✅ {title}"); db.close()

if __name__ == "__main__": seed_chronic_pain()
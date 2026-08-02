from app.database import SessionLocal
from app.models import User, Template

def seed_peripheral_neuropathy():
    db = SessionLocal()
    admin = db.query(User).filter(User.role == "admin").first()
    if not admin: print("❌ No admin!"); db.close(); return

    title = "Peripheral Neuropathy"
    existing = db.query(Template).filter(Template.title == title).first()
    if existing: db.delete(existing); db.commit()

    t = Template(title=title, description="Assessment of peripheral neuropathy covering causes (diabetes, B12, alcohol, chemotherapy), examination, investigations, and neuropathic pain management per NICE CG173.", category="Neurology", content={"sections": [
        {"title": "History", "section_type": "history", "questions": [
            {"id": "pn_symptoms", "type": "multi_select", "label": "Symptoms", "required": True, "options": ["Numbness", "Tingling/Pins and needles", "Burning pain", "Electric shock sensations", "Allodynia (pain from light touch)", "Weakness", "Balance problems", "Restless legs"]},
            {"id": "pn_distribution", "type": "single_select", "label": "Distribution", "required": True, "options": ["Feet only (stocking)", "Hands and feet (glove and stocking)", "Asymmetrical", "Proximal (thighs)", "Single nerve distribution"]},
            {"id": "pn_duration", "type": "text", "label": "Duration", "required": True, "placeholder": "e.g., 6 months"},
            {"id": "pn_progression", "type": "single_select", "label": "Progression", "required": True, "options": ["Stable", "Slowly progressive", "Rapidly progressive - RED FLAG"]},
            {"id": "pn_pain_score", "type": "number", "label": "Pain Score (0-10)", "required": False, "placeholder": "e.g., 7"},
            {"id": "pn_sleep", "type": "toggle", "label": "Disturbing Sleep?", "required": True},
            {"id": "pn_walking", "type": "toggle", "label": "Affecting Walking/Balance?", "required": True}
        ]},
        {"title": "Cause Assessment", "section_type": "history", "questions": [
            {"id": "pn_diabetes", "type": "toggle", "label": "Diabetes? (Most common cause)", "required": True},
            {"id": "pn_dm_duration", "type": "text", "label": "Diabetes Duration & Control (HbA1c)", "required": False, "placeholder": "e.g., T2DM 10 years, HbA1c 78"},
            {"id": "pn_alcohol", "type": "single_select", "label": "Alcohol", "required": True, "options": ["None", "Within limits", "Excess/Chronic"]},
            {"id": "pn_b12", "type": "toggle", "label": "B12 Deficiency?", "required": True},
            {"id": "pn_thyroid", "type": "toggle", "label": "Thyroid Disease?", "required": False},
            {"id": "pn_ckd", "type": "toggle", "label": "CKD?", "required": False},
            {"id": "pn_chemo", "type": "toggle", "label": "Previous Chemotherapy? (Vincristine, cisplatin, taxanes)", "required": True},
            {"id": "pn_medications", "type": "text", "label": "Medications (Amiodarone, Metronidazole, Nitrofurantoin, Phenytoin)", "required": False},
            {"id": "pn_family", "type": "toggle", "label": "Family History of Neuropathy? (Charcot-Marie-Tooth)", "required": False},
            {"id": "pn_autoimmune", "type": "toggle", "label": "Autoimmune Disease? (SLE, RA, Sjogren's)", "required": False}
        ]},
        {"title": "Examination", "section_type": "examination", "questions": [
            {"id": "pn_sensation", "type": "single_select", "label": "Light Touch / Pinprick", "required": True, "options": ["Normal", "Reduced (stocking distribution)", "Reduced (glove and stocking)", "Absent"]},
            {"id": "pn_vibration", "type": "single_select", "label": "Vibration Sense (128Hz Tuning Fork)", "required": True, "options": ["Normal", "Reduced at ankles", "Reduced to knees", "Absent"]},
            {"id": "pn_proprioception", "type": "single_select", "label": "Proprioception (Big Toe)", "required": True, "options": ["Normal", "Impaired", "Absent - Romberg positive"]},
            {"id": "pn_reflexes", "type": "single_select", "label": "Ankle Jerks", "required": True, "options": ["Present", "Reduced", "Absent"]},
            {"id": "pn_power", "type": "single_select", "label": "Motor Power (Ankle/Foot)", "required": True, "options": ["Normal (5/5)", "Mild weakness (4/5)", "Moderate weakness (3/5)", "Foot drop"]},
            {"id": "pn_gait", "type": "single_select", "label": "Gait", "required": True, "options": ["Normal", "High-stepping gait (foot drop)", "Ataxic", "Requires walking aid"]},
            {"id": "pn_feet_inspection", "type": "toggle", "label": "Foot Deformity / Ulcers? (Charcot)", "required": False}
        ]},
        {"title": "Investigations", "section_type": "assessment", "questions": [
            {"id": "pn_bloods", "type": "multi_select", "label": "Blood Tests", "required": False, "options": ["HbA1c / Fasting glucose", "FBC", "B12 / Folate", "TFTs", "U&E (CKD)", "LFTs (alcohol)", "Serum protein electrophoresis (SPEP)", "ANA / ENA (autoimmune)", "None - already investigated"]},
            {"id": "pn_ncs", "type": "toggle", "label": "Nerve Conduction Studies / EMG Required?", "required": False},
            {"id": "pn_neurology_referral", "type": "toggle", "label": "Neurology Referral Required?", "required": False}
        ]},
        {"title": "Assessment", "section_type": "assessment", "differentials": ["Diabetic Peripheral Neuropathy (most common)", "Alcoholic Neuropathy", "B12 Deficiency Neuropathy", "Chemotherapy-Induced Neuropathy", "Idiopathic Peripheral Neuropathy", "Chronic Inflammatory Demyelinating Polyneuropathy (CIDP)", "Charcot-Marie-Tooth (hereditary)", "Mononeuritis Multiplex (vasculitis)", "Paraproteinaemic Neuropathy"], "questions": [
            {"id": "pn_cause", "type": "single_select", "label": "Likely Cause", "required": True, "options": ["Diabetic neuropathy", "Alcoholic neuropathy", "B12 deficiency", "Chemotherapy-induced", "Idiopathic", "Other/Unknown"]},
            {"id": "pn_severity", "type": "single_select", "label": "Severity", "required": True, "options": ["Mild - sensory only, no functional impact", "Moderate - painful, mild functional impact", "Severe - motor involvement, significant disability"]}
        ]},
        {"title": "Management", "section_type": "plan", "safety_netting": "Return if: rapidly worsening weakness, foot drop, falls, or symptoms not responding to treatment. Neuropathic pain treatment (NICE CG173): 1st line - Amitriptyline 10-25mg nocte, Duloxetine 60mg OD, Gabapentin (titrate from 300mg to max 3600mg), or Pregabalin 75-150mg BD. Only ONE drug at a time, trial for 4-8 weeks at adequate dose. Combine if partial response. Topical capsaicin or lidocaine for localised pain. Address underlying cause: diabetes control (HbA1c <58), B12 replacement, alcohol cessation. Foot care: daily inspection, podiatry referral if high risk. Driving: may need to inform DVLA if sensory loss affects driving (check DVLA guidelines).", "questions": [
            {"id": "pn_plan", "type": "multi_select", "label": "Management", "required": True, "options": ["Treat underlying cause", "Start neuropathic pain medication", "Foot care advice + podiatry referral", "Physiotherapy / OT referral", "Nerve conduction studies", "Neurology referral", "DVLA advice if indicated"]},
            {"id": "pn_medication", "type": "text", "label": "Medication Started", "required": False, "placeholder": "e.g., Amitriptyline 10mg nocte, titrate to 25-50mg"},
            {"id": "pn_followup", "type": "text", "label": "Follow-up", "required": True, "placeholder": "e.g., Review in 4 weeks, assess pain response, titrate medication"}
        ]}
    ]}, is_public=True, created_by=admin.id)
    db.add(t); db.commit(); print(f"✅ {title}"); db.close()

if __name__ == "__main__": seed_peripheral_neuropathy()
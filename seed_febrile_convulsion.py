from app.database import SessionLocal
from app.models import User, Template

def seed_febrile_convulsion():
    db = SessionLocal()
    admin = db.query(User).filter(User.role == "admin").first()
    if not admin: print("❌ No admin!"); db.close(); return

    title = "Febrile Convulsion"
    existing = db.query(Template).filter(Template.title == title).first()
    if existing: db.delete(existing); db.commit()

    t = Template(title=title, description="Assessment of febrile convulsions in children covering simple vs complex, red flags for meningitis/encephalitis, safety netting, and parental reassurance per NICE CG160.", category="Paediatrics", content={"sections": [
        {"title": "Seizure Description", "section_type": "history", "questions": [
            {"id": "fc_age", "type": "text", "label": "Age of Child", "required": True, "placeholder": "e.g., 18 months"},
            {"id": "fc_type", "type": "single_select", "label": "Seizure Type", "required": True, "options": ["Simple (<15 minutes, generalised, once in 24h)", "Complex (>15 minutes, focal, or >1 in 24h)", "Febrile status epilepticus (>30 minutes)"]},
            {"id": "fc_duration", "type": "text", "label": "Duration (minutes)", "required": True, "placeholder": "e.g., 3 minutes"},
            {"id": "fc_focal", "type": "toggle", "label": "Focal Features? (One limb, eye deviation)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Focal seizure = complex febrile convulsion. Needs paediatric assessment.", "red_flag_negative": ""},
            {"id": "fc_recurrent_24h", "type": "toggle", "label": "More Than One in 24 Hours?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Recurrent in 24h = complex. Needs paediatric assessment to exclude CNS infection.", "red_flag_negative": ""},
            {"id": "fc_postictal", "type": "single_select", "label": "Post-ictal Recovery", "required": True, "options": ["Full recovery within 1 hour (normal)", "Prolonged drowsiness/confusion - RED FLAG", "Not returned to baseline - RED FLAG"]},
            {"id": "fc_first", "type": "toggle", "label": "First Febrile Convulsion?", "required": True},
            {"id": "fc_previous_afebrile", "type": "toggle", "label": "Previous Afebrile Seizures?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Afebrile seizures + fever = ?epilepsy with intercurrent illness. Paediatric neurology.", "red_flag_negative": ""}
        ]},
        {"title": "Fever Assessment", "section_type": "history", "questions": [
            {"id": "fc_temp", "type": "number", "label": "Temperature (°C)", "required": True, "placeholder": "e.g., 39.2"},
            {"id": "fc_fever_duration", "type": "text", "label": "Duration of Fever Before Seizure", "required": False, "placeholder": "e.g., 12 hours"},
            {"id": "fc_source_fever", "type": "single_select", "label": "Source of Fever", "required": True, "options": ["URTI (runny nose, cough)", "Tonsillitis", "Otitis Media", "Viral illness (non-specific)", "UTI", "Unknown - investigate"]},
            {"id": "fc_rash", "type": "single_select", "label": "Rash?", "required": True, "options": ["None", "Non-blanching petechial/purpuric - RED FLAG", "Non-specific viral rash", "Other"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Non-blanching rash = ?meningococcal sepsis. EMERGENCY. IM Benzylpenicillin + 999.", "red_flag_negative": ""}
        ]},
        {"title": "Red Flags - Exclude Meningitis/Encephalitis", "section_type": "examination", "questions": [
            {"id": "fc_neck_stiffness", "type": "toggle", "label": "Neck Stiffness / Photophobia?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Meningism = ?meningitis/encephalitis. Urgent paediatric assessment + LP.", "red_flag_negative": ""},
            {"id": "fc_bulging_fontanelle", "type": "toggle", "label": "Bulging Fontanelle? (Infants)", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Bulging fontanelle = ?raised ICP, meningitis. Emergency.", "red_flag_negative": ""},
            {"id": "fc_consciousness", "type": "single_select", "label": "Level of Consciousness", "required": True, "options": ["Alert and responsive", "Drowsy but rousable", "Irritable/Inconsolable", "Floppy/unresponsive - RED FLAG"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Altered consciousness = ?CNS infection, post-ictal state. Urgent assessment.", "red_flag_negative": ""},
            {"id": "fc_previous_antibiotics", "type": "toggle", "label": "Recent Antibiotics? (May mask meningitis)", "required": True}
        ]},
        {"title": "Risk Factors", "section_type": "history", "questions": [
            {"id": "fc_family_history", "type": "toggle", "label": "Family History Febrile Convulsions?", "required": True},
            {"id": "fc_development", "type": "single_select", "label": "Developmental Milestones", "required": True, "options": ["Normal for age", "Mild delay", "Significant delay - RED FLAG"]},
            {"id": "fc_vaccinations", "type": "toggle", "label": "Recent Vaccinations? (MMR at 6-11 days post)", "required": False},
            {"id": "fc_immunocompromised", "type": "toggle", "label": "Immunocompromised?", "required": False}
        ]},
        {"title": "Assessment", "section_type": "assessment", "differentials": ["Simple Febrile Convulsion (most common - benign)", "Complex Febrile Convulsion", "Febrile Status Epilepticus (>30 min - emergency)", "CNS Infection (Meningitis/Encephalitis)", "Epilepsy with intercurrent febrile illness", "Rigors / Shivering (not a seizure)", "Breath-holding Attack", "Reflex Anoxic Seizure"], "questions": [
            {"id": "fc_diagnosis", "type": "single_select", "label": "Diagnosis", "required": True, "options": ["Simple Febrile Convulsion - reassure + discharge", "Complex Febrile Convulsion - paediatric assessment", "?CNS Infection - urgent paediatric admission", "Febrile Status Epilepticus - emergency admission"]},
            {"id": "fc_admission", "type": "toggle", "label": "Hospital Admission Required?", "required": True}
        ]},
        {"title": "Management & Parental Reassurance", "section_type": "plan", "safety_netting": "Febrile convulsions are common (3-4% children) and generally benign. They do NOT cause brain damage. Risk of epilepsy after simple febrile convulsion is ~1% (same as general population). Complex febrile convulsions have slightly higher risk (~4-6%). Return immediately or call 999 if: seizure >5 minutes, difficulty breathing, child becomes floppy/unresponsive, non-blanching rash, stiff neck, or photophobia. During seizure: place in recovery position, time it, do NOT put anything in mouth, do NOT restrain. Antipyretics do NOT prevent febrile convulsions but can comfort child. No regular anticonvulsant prophylaxis needed. Buccal midazolam may be prescribed for prolonged seizures (>5 min) in children with history of prolonged/complex febrile convulsions.", "questions": [
            {"id": "fc_plan", "type": "multi_select", "label": "Management", "required": True, "options": ["Reassurance + safety netting", "Fever management advice", "Treat source of fever", "Paediatric referral (complex)", "Admission (CNS infection suspected)", "Buccal Midazolam prescribed (prolonged)", "Parental leaflet provided"]},
            {"id": "fc_safety_net", "type": "toggle", "label": "Red Flags + Seizure First Aid Explained?", "required": True},
            {"id": "fc_leaflet", "type": "toggle", "label": "Febrile Convulsion Leaflet Given?", "required": True},
            {"id": "fc_followup", "type": "text", "label": "Follow-up", "required": True, "placeholder": "e.g., GP review in 1 week if complex, no routine follow-up for simple, return if concerns"}
        ]}
    ]}, is_public=True, created_by=admin.id)
    db.add(t); db.commit(); print(f"✅ {title}"); db.close()

if __name__ == "__main__": seed_febrile_convulsion()
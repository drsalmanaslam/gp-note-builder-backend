from app.database import SessionLocal
from app.models import User, Template

def seed_hayfever():
    db = SessionLocal()
    admin = db.query(User).filter(User.role == "admin").first()
    if not admin: print("❌ No admin!"); db.close(); return

    title = "Hayfever / Allergic Rhinitis"
    existing = db.query(Template).filter(Template.title == title).first()
    if existing: db.delete(existing); db.commit()

    t = Template(title=title, description="Assessment and management of seasonal/perennial allergic rhinitis covering symptom control, antihistamines, nasal steroids, immunotherapy, and differentiating from non-allergic rhinitis per BSACI guidelines.", category="ENT", content={"sections": [
        {"title": "Symptoms", "section_type": "history", "questions": [
            {"id": "hay_type", "type": "single_select", "label": "Pattern", "required": True, "options": ["Seasonal (spring/summer - pollen)", "Perennial (year-round - dust mite, mould, pets)", "Mixed (seasonal + perennial)", "Occupational"]},
            {"id": "hay_sneezing", "type": "toggle", "label": "Sneezing?", "required": True},
            {"id": "hay_rhinorrhoea", "type": "toggle", "label": "Runny Nose (Rhinorrhoea)?", "required": True},
            {"id": "hay_congestion", "type": "toggle", "label": "Nasal Congestion / Blockage?", "required": True},
            {"id": "hay_itch_nose", "type": "toggle", "label": "Nasal Itching?", "required": True},
            {"id": "hay_itch_eyes", "type": "toggle", "label": "Itchy / Watery Eyes?", "required": True},
            {"id": "hay_palate_itch", "type": "toggle", "label": "Palate / Ear Itching?", "required": False},
            {"id": "hay_cough", "type": "toggle", "label": "Post-nasal Drip / Cough?", "required": False},
            {"id": "hay_anosmia", "type": "toggle", "label": "Loss of Smell?", "required": False},
            {"id": "hay_asthma", "type": "toggle", "label": "Associated Asthma / Wheeze?", "required": True},
            {"id": "hay_eczema", "type": "toggle", "label": "Eczema / Atopy?", "required": True},
            {"id": "hay_severity", "type": "single_select", "label": "Impact on Daily Life", "required": True, "options": ["Mild - no impact", "Moderate - bothersome, affects sleep/work", "Severe - significant impact, cannot function"]}
        ]},
        {"title": "Examination", "section_type": "examination", "questions": [
            {"id": "hay_nasal_exam", "type": "single_select", "label": "Nasal Examination", "required": False, "options": ["Normal", "Pale, boggy turbinates (allergic)", "Erythematous (non-allergic/infective)", "Polyps visible - RED FLAG", "Not examined"]},
            {"id": "hay_eyes", "type": "single_select", "label": "Eye Examination", "required": False, "options": ["Normal", "Conjunctival injection", "Chemosis (swelling)", "Not examined"]},
            {"id": "hay_allergic_salute", "type": "toggle", "label": "Allergic Salute? (Nasal crease from rubbing)", "required": False},
            {"id": "hay_polyps", "type": "toggle", "label": "Nasal Polyps?", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Unilateral polyp or mass = ?malignancy. ENT referral. Bilateral polyps = consider ENT referral.", "red_flag_negative": ""}
        ]},
        {"title": "Red Flags", "section_type": "history", "questions": [
            {"id": "hay_unilateral", "type": "toggle", "label": "Unilateral Symptoms?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Unilateral nasal symptoms = ?tumour, foreign body. Urgent ENT referral.", "red_flag_negative": ""},
            {"id": "hay_bloody_discharge", "type": "toggle", "label": "Blood-Stained Nasal Discharge?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Blood-stained discharge = ?malignancy. Urgent ENT referral.", "red_flag_negative": ""},
            {"id": "hay_crusting", "type": "toggle", "label": "Nasal Crusting / Pain?", "required": False},
            {"id": "hay_visual", "type": "toggle", "label": "Visual Disturbance / Diplopia?", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Visual symptoms + nasal symptoms = ?sinonasal tumour extending to orbit. Urgent ENT.", "red_flag_negative": ""}
        ]},
        {"title": "Assessment", "section_type": "assessment", "differentials": ["Seasonal Allergic Rhinitis (Hayfever - pollen, grass, tree)", "Perennial Allergic Rhinitis (dust mite, pet dander, mould)", "Non-Allergic Rhinitis (vasomotor, irritant-induced)", "Chronic Rhinosinusitis (with/without polyps)", "Drug-induced (ACEi, alpha-blockers, cocaine)", "Occupational Rhinitis", "Pregnancy rhinitis"], "questions": [
            {"id": "hay_diagnosis", "type": "single_select", "label": "Diagnosis", "required": True, "options": ["Seasonal Allergic Rhinitis", "Perennial Allergic Rhinitis", "Non-Allergic Rhinitis", "Chronic Rhinosinusitis", "Mixed allergic + non-allergic"]}
        ]},
        {"title": "Management", "section_type": "plan", "safety_netting": "Stepwise approach: 1) Non-sedating antihistamine (cetirizine, loratadine, fexofenadine), 2) Add intranasal corticosteroid (fluticasone, mometasone - BD for moderate-severe), 3) Add antihistamine eye drops (sodium cromoglicate, olopatadine), 4) Consider short course oral steroids (prednisolone 20mg 5 days) if severe. Allergen avoidance: keep windows closed, shower after being outdoors, wrap-around sunglasses, Vaseline around nostrils. Nasal saline irrigation helpful. Refer to immunology/allergy clinic if: severe despite maximal therapy, considering immunotherapy, diagnostic uncertainty. Return if: unilateral symptoms, bloody discharge, visual changes, or not improving after 4 weeks of maximal therapy.", "questions": [
            {"id": "hay_plan", "type": "multi_select", "label": "Management", "required": True, "options": ["Oral antihistamine (Cetirizine 10mg OD)", "Intranasal steroid (Fluticasone/Mometasone BD)", "Antihistamine eye drops (Olopatadine/Sodium Cromoglicate)", "Nasal saline irrigation", "Short course oral prednisolone (severe)", "Allergen avoidance advice", "Refer allergy/immunology", "Refer ENT"]},
            {"id": "hay_prescription", "type": "text", "label": "Prescription", "required": False, "placeholder": "e.g., Fexofenadine 180mg OD + Mometasone nasal spray BD"},
            {"id": "hay_advice", "type": "toggle", "label": "Allergen Avoidance Advice Given?", "required": True},
            {"id": "hay_nasal_technique", "type": "toggle", "label": "Nasal Spray Technique Demonstrated?", "required": False},
            {"id": "hay_followup", "type": "text", "label": "Follow-up", "required": True, "placeholder": "e.g., Review in 4 weeks if not controlled, seasonal - start treatment 2 weeks before pollen season"}
        ]}
    ]}, is_public=True, created_by=admin.id)
    db.add(t); db.commit(); print(f"✅ {title}"); db.close()

if __name__ == "__main__": seed_hayfever()
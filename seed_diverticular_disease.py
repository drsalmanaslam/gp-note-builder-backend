from app.database import SessionLocal
from app.models import User, Template

def seed_diverticular_disease():
    db = SessionLocal()
    admin = db.query(User).filter(User.role == "admin").first()
    if not admin: print("❌ No admin!"); db.close(); return

    title = "Diverticular Disease"
    existing = db.query(Template).filter(Template.title == title).first()
    if existing: db.delete(existing); db.commit()

    t = Template(title=title, description="Assessment of diverticular disease covering acute diverticulitis vs symptomatic diverticular disease, red flags, antibiotic stewardship, and dietary management.", category="Gastroenterology", content={"sections": [
        {"title": "History", "section_type": "history", "questions": [
            {"id": "div_pain_site", "type": "single_select", "label": "Pain Location", "required": True, "options": ["Left iliac fossa (classic)", "Suprapubic", "Right iliac fossa", "Generalised", "Other"]},
            {"id": "div_pain_onset", "type": "single_select", "label": "Onset", "required": True, "options": ["Acute (hours-days)", "Gradual (weeks)", "Chronic intermittent"]},
            {"id": "div_pain_severity", "type": "number", "label": "Pain Score (0-10)", "required": True, "placeholder": "e.g., 6"},
            {"id": "div_fever", "type": "toggle", "label": "Fever / Rigors?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Fever = ?acute diverticulitis with systemic features. May need admission.", "red_flag_negative": ""},
            {"id": "div_bowel_habit", "type": "single_select", "label": "Bowel Habit Change", "required": True, "options": ["Normal", "Constipation", "Diarrhoea", "Alternating", "Blood in stool"]},
            {"id": "div_pr_bleeding", "type": "toggle", "label": "PR Bleeding?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: PR bleeding = ?diverticular bleed, colitis, malignancy. Needs investigation.", "red_flag_negative": ""},
            {"id": "div_nausea", "type": "toggle", "label": "Nausea / Vomiting?", "required": False},
            {"id": "div_previous_diverticulitis", "type": "toggle", "label": "Previous Diverticulitis Episodes?", "required": True},
            {"id": "div_previous_diagnosis", "type": "toggle", "label": "Known Diverticulosis? (Previous colonoscopy/CT)", "required": True},
            {"id": "div_antibiotics_recent", "type": "toggle", "label": "Recent Antibiotics?", "required": False}
        ]},
        {"title": "Red Flags - Complicated Diverticulitis", "section_type": "history", "questions": [
            {"id": "div_generalised_pain", "type": "toggle", "label": "Generalised Peritonitic Pain? (?Perforation)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Generalised peritonitis = ?perforation. EMERGENCY admission.", "red_flag_negative": ""},
            {"id": "div_obstruction", "type": "toggle", "label": "Absolute Constipation + Distension? (?Obstruction)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Bowel obstruction = urgent surgical admission.", "red_flag_negative": ""},
            {"id": "div_sepsis", "type": "toggle", "label": "Signs of Sepsis? (Confusion, tachycardia, hypotension)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Sepsis = emergency admission for IV antibiotics.", "red_flag_negative": ""},
            {"id": "div_weight_loss", "type": "toggle", "label": "Unintentional Weight Loss?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Weight loss + bowel symptoms = ?colorectal cancer. 2WW referral.", "red_flag_negative": ""}
        ]},
        {"title": "Examination", "section_type": "examination", "questions": [
            {"id": "div_temp", "type": "text", "label": "Temperature (°C)", "required": False, "placeholder": "e.g., 38.1"},
            {"id": "div_hr", "type": "text", "label": "Heart Rate", "required": False, "placeholder": "e.g., 92"},
            {"id": "div_bp", "type": "text", "label": "Blood Pressure", "required": False, "placeholder": "e.g., 110/70"},
            {"id": "div_abdo_tenderness", "type": "single_select", "label": "Abdominal Tenderness", "required": True, "options": ["Localised LIF tenderness", "Generalised tenderness", "Rebound/guarding - RED FLAG", "Non-tender"]},
            {"id": "div_mass", "type": "toggle", "label": "Palpable Mass?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Palpable mass = ?abscess, phlegmon, malignancy. Urgent CT + surgical referral.", "red_flag_negative": ""},
            {"id": "div_distension", "type": "toggle", "label": "Abdominal Distension?", "required": False}
        ]},
        {"title": "Assessment", "section_type": "assessment", "differentials": ["Acute Uncomplicated Diverticulitis", "Acute Complicated Diverticulitis (abscess, perforation, obstruction)", "Symptomatic Diverticular Disease (no acute inflammation)", "Irritable Bowel Syndrome", "Colorectal Cancer (RED FLAG)", "Inflammatory Bowel Disease", "Infective Colitis"], "questions": [
            {"id": "div_diagnosis", "type": "single_select", "label": "Diagnosis", "required": True, "options": ["Acute Uncomplicated Diverticulitis", "Acute Complicated Diverticulitis - ADMIT", "Symptomatic Diverticular Disease", "Suspected Malignancy - 2WW"]},
            {"id": "div_severity", "type": "single_select", "label": "Severity", "required": True, "options": ["Mild - manage at home", "Moderate - oral antibiotics at home", "Severe - admission for IV antibiotics", "Emergency - perforation/obstruction/sepsis"]},
            {"id": "div_ct_required", "type": "toggle", "label": "CT Abdomen Required?", "required": False},
            {"id": "div_colonoscopy", "type": "toggle", "label": "Colonoscopy Required? (6-8 weeks after acute episode)", "required": False}
        ]},
        {"title": "Management", "section_type": "plan", "safety_netting": "Return immediately or attend A&E if: severe worsening pain, generalised abdominal pain, vomiting, absolute constipation, fever >38.5°C, or feeling very unwell. Mild diverticulitis: may not need antibiotics (NICE NG160). If antibiotics: Co-amoxiclav 625mg TDS 5 days (or Metronidazole 400mg TDS + Cefalexin 500mg TDS if penicillin allergic). Clear fluids for 2-3 days, then soft diet. Simple analgesia (paracetamol, avoid NSAIDs/opioids due to constipation). Colonoscopy 6-8 weeks after acute episode to exclude malignancy (if not done within 2 years). Long-term: high-fibre diet (once acute episode resolved), adequate hydration, avoid constipation.", "questions": [
            {"id": "div_treatment", "type": "multi_select", "label": "Management", "required": True, "options": ["No antibiotics (mild, NICE guidance)", "Co-amoxiclav 625mg TDS 5 days", "Metronidazole + Cefalexin (penicillin allergy)", "Admit for IV antibiotics", "Surgical referral", "Clear fluids 2-3 days", "Simple analgesia (paracetamol)", "High-fibre diet advice (once resolved)"]},
            {"id": "div_antibiotic", "type": "text", "label": "Antibiotic Prescribed", "required": False, "placeholder": "e.g., Co-amoxiclav 625mg TDS 5 days"},
            {"id": "div_colonoscopy_plan", "type": "toggle", "label": "Colonoscopy Booked (6-8 weeks)?", "required": False},
            {"id": "div_safety", "type": "toggle", "label": "Red Flag Warning Given?", "required": True},
            {"id": "div_followup", "type": "text", "label": "Follow-up", "required": True, "placeholder": "e.g., Return if worsening, colonoscopy 6-8 weeks, routine GP review"}
        ]}
    ]}, is_public=True, created_by=admin.id)
    db.add(t); db.commit(); print(f"✅ {title}"); db.close()

if __name__ == "__main__": seed_diverticular_disease()
from app.database import SessionLocal
from app.models import User, Template

def seed_peptic_ulcer():
    db = SessionLocal()
    admin = db.query(User).filter(User.role == "admin").first()
    if not admin: print("❌ No admin!"); db.close(); return

    title = "Peptic Ulcer Disease / H.pylori"
    existing = db.query(Template).filter(Template.title == title).first()
    if existing: db.delete(existing); db.commit()

    t = Template(title=title, description="Assessment of dyspepsia and suspected peptic ulcer covering H.pylori testing, PPI trial, alarm symptoms, and NICE CG184 management.", category="Gastroenterology", content={"sections": [
        {"title": "History", "section_type": "history", "questions": [
            {"id": "pud_epigastric_pain", "type": "toggle", "label": "Epigastric Pain/Burning?", "required": True},
            {"id": "pud_pain_timing", "type": "single_select", "label": "Pain Timing", "required": True, "options": ["Before meals (duodenal ulcer)", "After meals (gastric ulcer)", "Nocturnal (waking from sleep)", "No clear pattern", "Constant"]},
            {"id": "pud_relieved_food", "type": "toggle", "label": "Relieved by Food/Antacids?", "required": False},
            {"id": "pud_nausea", "type": "toggle", "label": "Nausea / Vomiting?", "required": False},
            {"id": "pud_bloating", "type": "toggle", "label": "Bloating / Early Satiety?", "required": False},
            {"id": "pud_duration", "type": "text", "label": "Duration of Symptoms", "required": True, "placeholder": "e.g., 4 weeks"},
            {"id": "pud_nsaids", "type": "toggle", "label": "NSAID Use? (Including OTC)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: NSAID-induced ulcer risk. Stop NSAID if possible. Consider PPI cover if must continue.", "red_flag_negative": ""},
            {"id": "pud_aspirin", "type": "toggle", "label": "Aspirin / Antiplatelet?", "required": False},
            {"id": "pud_ppi_trial", "type": "toggle", "label": "Previous PPI Trial? (Response?)", "required": True},
            {"id": "pud_smoking", "type": "toggle", "label": "Smoker?", "required": True},
            {"id": "pud_alcohol", "type": "single_select", "label": "Alcohol", "required": True, "options": ["None", "Within limits", "Excess"]}
        ]},
        {"title": "Alarm Symptoms (Red Flags)", "section_type": "history", "questions": [
            {"id": "pud_dysphagia", "type": "toggle", "label": "Dysphagia?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Dysphagia = urgent OGD (2WW). ?Malignancy.", "red_flag_negative": ""},
            {"id": "pud_weight_loss", "type": "toggle", "label": "Unintentional Weight Loss?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Weight loss + dyspepsia = urgent 2WW OGD.", "red_flag_negative": ""},
            {"id": "pud_melaena", "type": "toggle", "label": "Melaena / Haematemesis?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: GI bleeding = emergency admission.", "red_flag_negative": ""},
            {"id": "pud_anaemia", "type": "toggle", "label": "Iron Deficiency Anaemia?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: IDA + dyspepsia = urgent OGD.", "red_flag_negative": ""},
            {"id": "pud_mass", "type": "toggle", "label": "Epigastric Mass?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Epigastric mass = urgent 2WW OGD.", "red_flag_negative": ""},
            {"id": "pud_age_55", "type": "toggle", "label": "Age >55 with New-Onset Dyspepsia?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Age >55 + new dyspepsia = urgent OGD per NICE.", "red_flag_negative": ""}
        ]},
        {"title": "Examination", "section_type": "examination", "questions": [
            {"id": "pud_epigastric_tenderness", "type": "toggle", "label": "Epigastric Tenderness?", "required": True},
            {"id": "pud_mass_palpable", "type": "toggle", "label": "Mass Palpable?", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Palpable mass = urgent 2WW.", "red_flag_negative": ""},
            {"id": "pud_succession_splash", "type": "toggle", "label": "Succession Splash? (?Gastric Outlet Obstruction)", "required": False}
        ]},
        {"title": "Assessment", "section_type": "assessment", "differentials": ["Functional Dyspepsia (most common)", "Peptic Ulcer Disease (H.pylori or NSAID-induced)", "GORD", "Gastric Cancer (RED FLAG)", "Oesophageal Cancer (RED FLAG)", "Gallstone Disease", "Pancreatitis"], "questions": [
            {"id": "pud_diagnosis", "type": "single_select", "label": "Likely Diagnosis", "required": True, "options": ["Functional Dyspepsia", "Peptic Ulcer - H.pylori likely", "Peptic Ulcer - NSAID-induced", "GORD", "Suspected Malignancy - URGENT"]},
            {"id": "pud_hpylori_test", "type": "toggle", "label": "H.pylori Stool Antigen / Breath Test Requested?", "required": True},
            {"id": "pud_oga", "type": "toggle", "label": "OGD Requested?", "required": False},
            {"id": "pud_2ww", "type": "toggle", "label": "2WW Referral Made?", "required": False}
        ]},
        {"title": "Management", "section_type": "plan", "safety_netting": "Return immediately if: vomiting blood, black tarry stools, severe abdominal pain, or difficulty swallowing. First-line: Full-dose PPI (Omeprazole 20mg BD or Lansoprazole 30mg BD) for 4-8 weeks. If H.pylori positive: 7-day triple therapy (PPI + Amoxicillin 1g BD + Clarithromycin 500mg BD or Metronidazole 400mg BD if penicillin allergic). Re-test for H.pylori 4 weeks after treatment (stool antigen). Stop NSAIDs if possible. Smoking cessation and alcohol reduction. If alarm symptoms: urgent 2WW OGD within 2 weeks.", "questions": [
            {"id": "pud_treatment", "type": "multi_select", "label": "Management", "required": True, "options": ["Full-dose PPI (4-8 weeks)", "H.pylori test-and-treat", "H.pylori eradication therapy", "Stop NSAIDs", "Stop aspirin (if safe)", "OGD requested", "2WW referral", "Lifestyle advice"]},
            {"id": "pud_ppi", "type": "text", "label": "PPI Prescribed", "required": False, "placeholder": "e.g., Omeprazole 20mg BD 4 weeks"},
            {"id": "pud_hpylori_rx", "type": "text", "label": "H.pylori Treatment", "required": False, "placeholder": "e.g., PPI + Amox 1g BD + Clarithromycin 500mg BD 7 days"},
            {"id": "pud_followup", "type": "text", "label": "Follow-up", "required": True, "placeholder": "e.g., Review 4 weeks, H.pylori test of cure, OGD if no response"}
        ]}
    ]}, is_public=True, created_by=admin.id)
    db.add(t); db.commit(); print(f"✅ {title}"); db.close()

if __name__ == "__main__": seed_peptic_ulcer()
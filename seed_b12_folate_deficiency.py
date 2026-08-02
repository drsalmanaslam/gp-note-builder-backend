from app.database import SessionLocal
from app.models import User, Template

def seed_b12_folate_deficiency():
    db = SessionLocal()
    admin = db.query(User).filter(User.role == "admin").first()
    if not admin: print("❌ No admin!"); db.close(); return

    title = "B12 & Folate Deficiency - Management"
    existing = db.query(Template).filter(Template.title == title).first()
    if existing: db.delete(existing); db.commit()

    t = Template(title=title, description="Management of vitamin B12 and folate deficiency covering investigations, replacement protocols, monitoring, and identifying underlying causes per NICE and BSH guidelines.", category="Abnormal Labs/Investigations", content={"sections": [
        {"title": "Blood Results", "section_type": "assessment", "questions": [
            {"id": "b12_b12_level", "type": "number", "label": "Serum B12 (ng/L)", "required": True, "placeholder": "e.g., 120"},
            {"id": "b12_folate_level", "type": "number", "label": "Serum Folate (µg/L)", "required": False, "placeholder": "e.g., 3.2"},
            {"id": "b12_hb", "type": "number", "label": "Haemoglobin (g/L)", "required": False, "placeholder": "e.g., 105"},
            {"id": "b12_mcv", "type": "number", "label": "MCV (fL)", "required": False, "placeholder": "e.g., 102"},
            {"id": "b12_ferritin", "type": "number", "label": "Ferritin (µg/L) - concurrent IDA?", "required": False, "placeholder": "e.g., 25"},
            {"id": "b12_if_antibodies", "type": "toggle", "label": "Intrinsic Factor Antibodies Checked?", "required": False},
            {"id": "b12_ifab_positive", "type": "toggle", "label": "IF Antibodies Positive? (Pernicious Anaemia)", "required": False}
        ]},
        {"title": "Symptoms & History", "section_type": "history", "questions": [
            {"id": "b12_symptoms", "type": "multi_select", "label": "Symptoms", "required": True, "options": ["Fatigue/lethargy", "SOB on exertion", "Palpitations", "Pallor", "Glossitis (sore tongue)", "Paraesthesia (pins and needles)", "Numbness", "Balance problems/ataxia", "Memory/cognitive issues", "Mood changes", "None - incidental finding"]},
            {"id": "b12_neuro_symptoms", "type": "toggle", "label": "Neurological Symptoms? (Paraesthesia, ataxia, cognitive)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Neurological symptoms + low B12 = treat urgently with IM hydroxocobalamin to prevent irreversible neurological damage.", "red_flag_negative": ""},
            {"id": "b12_diet", "type": "single_select", "label": "Diet", "required": True, "options": ["Omnivore", "Vegetarian", "Vegan", "Poor diet/elderly"]},
            {"id": "b12_alcohol", "type": "single_select", "label": "Alcohol Intake", "required": True, "options": ["None", "Within limits", "Excess"]},
            {"id": "b12_ppis", "type": "toggle", "label": "On PPIs? (Long-term reduces B12 absorption)", "required": True},
            {"id": "b12_metformin", "type": "toggle", "label": "On Metformin? (Reduces B12 absorption)", "required": True},
            {"id": "b12_gi_surgery", "type": "toggle", "label": "GI Surgery? (Gastrectomy, bypass, ileal resection)", "required": True},
            {"id": "b12_coeliac", "type": "toggle", "label": "Known/Suspected Coeliac Disease?", "required": True},
            {"id": "b12_autoimmune", "type": "toggle", "label": "Other Autoimmune Disease? (Thyroid, vitiligo, T1DM)", "required": False},
            {"id": "b12_pregnancy", "type": "toggle", "label": "Pregnant / Planning? (Folate critical for neural tube)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Pregnancy + low folate = urgent folic acid 5mg OD. Risk of neural tube defects.", "red_flag_negative": ""}
        ]},
        {"title": "Examination", "section_type": "examination", "questions": [
            {"id": "b12_pallor", "type": "toggle", "label": "Pallor?", "required": False},
            {"id": "b12_glossitis", "type": "toggle", "label": "Glossitis (Smooth, Red Tongue)?", "required": False},
            {"id": "b12_neuro_exam", "type": "single_select", "label": "Neurological Examination", "required": True, "options": ["Normal", "Reduced vibration/proprioception", "Peripheral neuropathy", "Ataxic gait / Romberg positive", "Not examined"]},
            {"id": "b12_jaundice", "type": "toggle", "label": "Mild Jaundice? (Haemolysis from ineffective erythropoiesis)", "required": False}
        ]},
        {"title": "Assessment", "section_type": "assessment", "differentials": ["Dietary B12 deficiency (vegan, vegetarian, poor diet)", "Pernicious Anaemia (autoimmune - IF antibodies positive)", "Food-B12 malabsorption (PPIs, metformin, atrophic gastritis)", "GI surgery / disease (gastrectomy, ileal resection, Crohn's)", "Folate deficiency (dietary, alcohol, pregnancy, methotrexate)", "Combined B12 + Folate deficiency", "Myelodysplasia (if macrocytosis without B12/folate deficiency)", "Haemolysis (if jaundice + anaemia)"], "questions": [
            {"id": "b12_cause", "type": "single_select", "label": "Likely Cause", "required": True, "options": ["Dietary (vegan/vegetarian)", "Pernicious Anaemia", "Drug-induced (PPI/Metformin)", "GI surgery/malabsorption", "Alcohol-related", "Pregnancy (folate)", "Unknown - investigate"]},
            {"id": "b12_severity", "type": "single_select", "label": "Severity", "required": True, "options": ["Mild (B12 150-200, asymptomatic)", "Moderate (B12 100-150, anaemia)", "Severe (B12 <100, neurological symptoms)"]}
        ]},
        {"title": "Management", "section_type": "plan", "safety_netting": "B12 replacement: If neurological symptoms present: IM hydroxocobalamin 1mg alternate days until no further improvement, then 1mg every 2 months. If no neurological symptoms (dietary): oral cyanocobalamin 50-150mcg daily OR IM hydroxocobalamin 1mg every 3 months. Pernicious anaemia or malabsorption: IM hydroxocobalamin 1mg every 3 months LIFELONG. Folate deficiency: Folic acid 5mg OD for 4 months (always check B12 first - treating folate without B12 can worsen SACD). Dietary advice: B12 sources (meat, fish, eggs, dairy, fortified foods). Return if: neurological symptoms worsen, new paraesthesia, balance problems, or symptoms not improving after 4 weeks of treatment.", "questions": [
            {"id": "b12_treatment", "type": "single_select", "label": "B12 Replacement Regime", "required": True, "options": ["IM hydroxocobalamin - loading (neuro symptoms)", "IM hydroxocobalamin 1mg every 3 months (maintenance)", "Oral cyanocobalamin 50-150mcg OD (dietary)", "Folic acid 5mg OD (folate deficiency)", "Combined B12 + folate replacement"]},
            {"id": "b12_im_schedule", "type": "text", "label": "Injection Schedule", "required": False, "placeholder": "e.g., 1mg alternate days for 2 weeks, then every 3 months"},
            {"id": "b12_oral_dose", "type": "text", "label": "Oral Dose", "required": False, "placeholder": "e.g., Cyanocobalamin 100mcg OD"},
            {"id": "b12_folic_acid", "type": "text", "label": "Folic Acid Dose", "required": False, "placeholder": "e.g., Folic acid 5mg OD for 4 months"},
            {"id": "b12_diet_advice", "type": "toggle", "label": "Dietary Advice Given?", "required": True},
            {"id": "b12_monitor", "type": "text", "label": "Monitoring Plan", "required": True, "placeholder": "e.g., Repeat FBC + B12 in 3 months, annual B12 if on IM maintenance"}
        ]}
    ]}, is_public=True, created_by=admin.id)
    db.add(t); db.commit(); print(f"✅ {title}"); db.close()

if __name__ == "__main__": seed_b12_folate_deficiency()
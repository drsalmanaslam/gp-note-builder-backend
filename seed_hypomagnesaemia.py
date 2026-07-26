from app.database import SessionLocal
from app.models import User, Template, Category

def seed_hypomagnesaemia():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Abnormal Labs/Investigations").first()
    if not category: category = Category(name="Abnormal Labs/Investigations"); db.add(category); db.commit()

    t = {
        "title": "Low Magnesium / Hypomagnesaemia Assessment",
        "description": "Focused assessment for hypomagnesaemia covering severity triage, PPI/diuretic/digoxin drug interactions, and Maalox outpatient replacement protocol.",
        "category": "Abnormal Labs/Investigations",
        "content": {"sections": [
            {
                "title": "RED FLAG - Severity Triage",
                "section_type": "history",
                "questions": [
                    {"id": "hypomg_level", "type": "number", "label": "Magnesium Level (mmol/L) - NR: 0.7-1.0", "required": True, "placeholder": "e.g., 0.4", "is_red_flag": True, "red_flag_positive": "RED FLAG: Significantly low Mg or severe symptoms = HOSPITAL ADMISSION for IV replacement. Do NOT manage as outpatient.", "red_flag_negative": ""},
                    {"id": "hypomg_severe_symptoms", "type": "toggle", "label": "Severe Symptoms? (Arrhythmia, Seizures, Tetany, Severe Weakness)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Severe symptoms = HOSPITAL ADMISSION for IV Mg. Do NOT manage as outpatient.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "History & Medication Review",
                "section_type": "history",
                "questions": [
                    {"id": "hypomg_symptoms", "type": "multi_select", "label": "Symptoms (Mild/Moderate)", "required": True, "options": ["Muscle cramps / twitching", "Paraesthesia", "Fatigue / weakness", "Nausea", "None - asymptomatic"]},
                    {"id": "hypomg_digoxin", "type": "toggle", "label": "On Digoxin? (Hypomagnesaemia + Hypokalaemia = Increased Digoxin Toxicity Risk)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Hypomagnesaemia increases digoxin toxicity risk. Check digoxin level + ECG urgently.", "red_flag_negative": ""},
                    {"id": "hypomg_diuretics", "type": "toggle", "label": "On Diuretics? (Loop / Thiazide)", "required": True},
                    {"id": "hypomg_ppi", "type": "toggle", "label": "On PPI? (Recognised Cause of Hypomagnesaemia - Also Can Cause Hypokalaemia + Hypocalcaemia)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: PPIs are recognised cause of hypomagnesaemia. Consider stopping/reducing PPI if possible.", "red_flag_negative": ""},
                    {"id": "hypomg_ppi_duration", "type": "text", "label": "PPI Duration", "required": False, "placeholder": "e.g., >1 year (Risk increases with long-term use)"}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "Drug-Induced Hypomagnesaemia (PPI - Most Common, Diuretics)",
                    "Dietary Deficiency / Malabsorption",
                    "Alcohol Excess",
                    "GI Losses (Diarrhoea, Vomiting)",
                    "Renal Losses (Diuretics, Hypercalcaemia)",
                    "Diabetes Mellitus (Osmotic Diuresis)",
                    "Refeeding Syndrome"
                ],
                "questions": [
                    {"id": "hypomg_diagnosis", "type": "single_select", "label": "Clinical Impression", "required": True, "options": ["Mild Hypomagnesaemia - PPI-Related", "Mild Hypomagnesaemia - Diuretic-Related", "Mild Hypomagnesaemia - Asymptomatic", "Severe Hypomagnesaemia - REQUIRES HOSPITAL ADMISSION"]}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Severe symptoms or significantly low Mg = HOSPITAL ADMISSION for IV replacement. Do NOT manage as outpatient. Outpatient replacement (mild, asymptomatic): Target 24mmol Mg replacement over 4 days (mnemonic: 24 = 24 hours in a day). Maalox 10ml TDS for 1 week (Maalox contains 3.95mmol Mg per 5ml - 10ml TDS ≈ 24mmol/day). Alternative: Magnesium Verla sachets 5mmol per sachet - typically requires 5 sachets daily to reach target (patients often find these poorly tolerated). Repeat Mg level after 1 week of treatment. If PPI-related: consider stopping/reducing PPI or switching to H2RA. Hypomagnesaemia + hypokalaemia increases digoxin toxicity risk - check ECG + digoxin level if on digoxin. Reference: BNF, NICE, SPS NHS.",
                "questions": [
                    {"id": "hypomg_maalox", "type": "toggle", "label": "Maalox 10ml TDS for 1 Week Prescribed? (3.95mmol/5ml - ~24mmol/Day)", "required": False},
                    {"id": "hypomg_verla", "type": "toggle", "label": "Magnesium Verla Sachets? (5mmol/Sachet - Requires 5/Day - Often Poorly Tolerated)", "required": False},
                    {"id": "hypomg_ppi_review", "type": "toggle", "label": "PPI Reviewed? (Consider Stopping/Reducing or Switching to H2RA)", "required": False},
                    {"id": "hypomg_digoxin_check", "type": "toggle", "label": "Digoxin Level + ECG Checked? (If on Digoxin)", "required": False},
                    {"id": "hypomg_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., Repeat Mg after 1 week of treatment"}
                ]
            }
        ]},
        "is_public": True
    }

    existing = db.query(Template).filter(Template.title == t["title"], Template.created_by == admin.id).first()
    if existing: db.delete(existing); db.commit()
    new_t = Template(title=t["title"], description=t["description"], category=t["category"], content=t["content"], is_public=True, created_by=admin.id, version=1)
    db.add(new_t); db.commit()
    print(f"Template '{t['title']}' created with {len(t['content']['sections'])} sections!"); db.close()

if __name__ == "__main__":
    seed_hypomagnesaemia()
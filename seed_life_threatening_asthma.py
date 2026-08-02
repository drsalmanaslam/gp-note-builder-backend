from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_life_threatening_asthma():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Respiratory").first()
    if not category: category = Category(name="Respiratory"); db.add(category); db.commit()

    t = {
        "title": "Life-Threatening Asthma Attack - EMERGENCY",
        "description": "Critical emergency template for life-threatening asthma attack covering immediate recognition criteria, emergency management, and urgent hospital admission pathway.",
        "category": "Respiratory",
        "content": {"sections": [
            {
                "title": "Life-Threatening Criteria (Any ONE Confirms)",
                "section_type": "examination",
                "questions": [
                    {"id": "lta_pefr", "type": "single_select", "label": "PEFR", "required": True, "options": ["<33% best/predicted - LIFE-THREATENING", "33-50% (SEVERE)", "50-75% (MODERATE)", "Unable to perform"], "is_red_flag": True, "red_flag_positive": "RED FLAG: PEFR <33% = LIFE-THREATENING. Immediate hospital admission. Do NOT delay.", "red_flag_negative": ""},
                    {"id": "lta_spo2", "type": "single_select", "label": "SpO2 / Cyanosis", "required": True, "options": ["<92% or cyanosis - LIFE-THREATENING", "≥92% (MODERATE/SEVERE)"], "is_red_flag": True, "red_flag_positive": "RED FLAG: SpO2 <92% or cyanosis = LIFE-THREATENING. Start O2 immediately.", "red_flag_negative": ""},
                    {"id": "lta_chest", "type": "single_select", "label": "Respiratory Effort / Chest Signs", "required": True, "options": ["Silent chest / feeble respiratory effort - LIFE-THREATENING", "Wheeze present (MODERATE/SEVERE)", "Poor air entry (SEVERE)"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Silent chest = NO air entry. LIFE-THREATENING. Call 999 immediately.", "red_flag_negative": ""},
                    {"id": "lta_cvs", "type": "single_select", "label": "Cardiovascular Status", "required": True, "options": ["Hypotension / arrhythmia / bradycardia - LIFE-THREATENING", "Tachycardia ≥110 (SEVERE)", "Normal (MODERATE)"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Hypotension/arrhythmia/bradycardia = cardiovascular collapse imminent. LIFE-THREATENING. Call 999.", "red_flag_negative": ""},
                    {"id": "lta_neuro", "type": "single_select", "label": "Neurological Status", "required": True, "options": ["Exhaustion / confusion / altered consciousness / coma - LIFE-THREATENING", "Agitated (SEVERE)", "Alert (MODERATE)"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Altered consciousness/confusion/coma = LIFE-THREATENING. Call 999. ICU required.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Severity Classification",
                "section_type": "assessment",
                "differentials": [
                    "Life-Threatening Asthma (PEFR <33%, SpO2 <92%, silent chest, cyanosis, exhaustion, bradycardia, hypotension, confusion, coma)",
                    "Near-Fatal Asthma (rising PaCO2 or requiring mechanical ventilation)",
                    "Severe Asthma (PEFR 33-50%, can't complete sentences, RR ≥25, HR ≥110)",
                    "Moderate Asthma (PEFR 50-75%, normal speech, SpO2 >92%)"
                ],
                "questions": [
                    {"id": "lta_severity", "type": "single_select", "label": "Severity Classification", "required": True, "options": ["LIFE-THREATENING - EMERGENCY 999", "NEAR-FATAL - CRITICAL CARE", "SEVERE (manage as per severe pathway)"]}
                ]
            },
            {
                "title": "Emergency Management",
                "section_type": "plan",
                "safety_netting": "LIFE-THREATENING ASTHMA = EMERGENCY. Call 999/112 immediately. Do NOT delay transfer for investigations. While awaiting ambulance: High flow oxygen to maintain SpO2 94-98%. Salbutamol 5mg nebulised via O2 + Ipratropium 0.5mg nebulised via O2 (may repeat every 15-30 min). Prednisolone 40mg PO (if able to swallow) OR Hydrocortisone 100mg IV. If severe/life-threatening features persist: consider IV Magnesium Sulphate 2g over 20 minutes (requires ECG monitoring). Consider IV Salbutamol 250mcg slow IV bolus (requires cardiac monitoring). Emergency hospital admission - no community follow-up applicable. After recovery: review medications, step up treatment, ensure written asthma action plan, arrange respiratory follow-up.",
                "questions": [
                    {"id": "lta_disposition", "type": "toggle", "label": "EMERGENCY - Admit to Hospital Immediately? (999/112)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: DO NOT DELAY. Life-threatening asthma requires immediate hospital admission. Call 999.", "red_flag_negative": ""},
                    {"id": "lta_oxygen", "type": "toggle", "label": "High Flow O2 - Titrate to SpO2 94-98%?", "required": True},
                    {"id": "lta_bronchodilator", "type": "toggle", "label": "Salbutamol 5mg + Ipratropium 0.5mg Nebulised via O2?", "required": True},
                    {"id": "lta_steroids", "type": "single_select", "label": "Steroid Therapy", "required": True, "options": ["Prednisolone 40mg PO (if able to swallow)", "Hydrocortisone 100mg IV", "Both (IV + PO if partial swallow)"]},
                    {"id": "lta_magnesium", "type": "toggle", "label": "IV Magnesium Sulphate 2g Over 20 Min? (If persisting severe features)", "required": False},
                    {"id": "lta_iv_salbutamol", "type": "toggle", "label": "IV Salbutamol 250mcg Slow Bolus? (If no response - requires cardiac monitoring)", "required": False},
                    {"id": "lta_followup", "type": "text", "label": "Post-Admission Plan", "required": False, "placeholder": "e.g., After recovery: step up treatment, written action plan, respiratory follow-up"}
                ]
            }
        ]},
        "is_public": True
    }

    existing = db.query(Template).filter(Template.title == t["title"], Template.created_by == admin.id).first()
    
    if existing:
        print(f"⏭️  SKIPPED: {title} already exists (ID={existing.id})")
        db.close()
        return
    new_t = Template(title=t["title"], description=t["description"], category=t["category"], content=t["content"], is_public=True, created_by=admin.id, version=1)
    db.add(new_t); db.commit()
    print(f"Template '{t['title']}' created with {len(t['content']['sections'])} sections!"); db.close()

if __name__ == "__main__":
    seed_life_threatening_asthma()
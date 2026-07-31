from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_acute_asthma():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Respiratory").first()
    if not category: category = Category(name="Respiratory"); db.add(category); db.commit()

    t = {
        "title": "Acute Moderate Asthma",
        "description": "Emergency-focused template for acute moderate asthma attack covering severity classification, PEFR, bronchodilator therapy, steroid dosing, and admission criteria.",
        "category": "Respiratory",
        "content": {"sections": [
            {
                "title": "Initial Assessment",
                "section_type": "examination",
                "questions": [
                    {"id": "ama_speech", "type": "single_select", "label": "Speech", "required": True, "options": ["Normal - able to complete sentences (MODERATE)", "Unable to complete sentences (SEVERE)", "Unable to speak (LIFE-THREATENING)"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Unable to complete sentences = SEVERE asthma. Unable to speak = LIFE-THREATENING. Emergency admission.", "red_flag_negative": ""},
                    {"id": "ama_pefr", "type": "single_select", "label": "PEFR (% Best or Predicted)", "required": True, "options": ["50-75% best/predicted (MODERATE)", "33-50% (SEVERE)", "<33% (LIFE-THREATENING)", "Not able to perform"], "is_red_flag": True, "red_flag_positive": "RED FLAG: PEFR <50% = severe. PEFR <33% = life-threatening. Emergency admission.", "red_flag_negative": ""},
                    {"id": "ama_spo2", "type": "single_select", "label": "Oxygen Saturation (SpO2)", "required": True, "options": [">92% (MODERATE)", "<92% (SEVERE/LIFE-THREATENING)"], "is_red_flag": True, "red_flag_positive": "RED FLAG: SpO2 <92% = severe/life-threatening. Emergency admission + O2.", "red_flag_negative": ""},
                    {"id": "ama_rr", "type": "single_select", "label": "Respiratory Rate", "required": True, "options": ["<25/min (MODERATE)", "≥25/min (SEVERE)", "Bradycardia / exhaustion (LIFE-THREATENING)"], "is_red_flag": True, "red_flag_positive": "RED FLAG: RR ≥25 = severe. Exhaustion/bradycardia = life-threatening. Emergency.", "red_flag_negative": ""},
                    {"id": "ama_hr", "type": "single_select", "label": "Pulse (bpm)", "required": True, "options": ["<110 bpm (MODERATE)", "≥110 bpm (SEVERE)", "Bradycardia / arrhythmia (LIFE-THREATENING)"], "is_red_flag": True, "red_flag_positive": "RED FLAG: HR ≥110 = severe. Bradycardia/arrhythmia = life-threatening. Emergency.", "red_flag_negative": ""},
                    {"id": "ama_chest", "type": "single_select", "label": "Chest Auscultation", "required": True, "options": ["Wheeze - expiratory (MODERATE)", "Wheeze - inspiratory + expiratory (SEVERE)", "Silent chest (LIFE-THREATENING)"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Silent chest = LIFE-THREATENING. No wheeze = no air entry. EMERGENCY.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Severity Classification",
                "section_type": "assessment",
                "differentials": [
                    "Acute Asthma - MODERATE (PEFR 50-75%, normal speech, SpO2 >92%, RR <25, HR <110)",
                    "Acute Asthma - SEVERE (PEFR 33-50%, can't complete sentences, SpO2 <92%, RR ≥25, HR ≥110)",
                    "Acute Asthma - LIFE-THREATENING (PEFR <33%, SpO2 <92%, silent chest, cyanosis, exhaustion, bradycardia, hypotension, confusion, coma)",
                    "Near-Fatal Asthma (rising PaCO2 or requiring mechanical ventilation)"
                ],
                "questions": [
                    {"id": "ama_severity", "type": "single_select", "label": "Severity Classification (BTS/SIGN)", "required": True, "options": ["MODERATE Asthma Attack", "SEVERE Asthma Attack - URGENT", "LIFE-THREATENING Asthma Attack - EMERGENCY ADMISSION", "Near-Fatal Asthma - CRITICAL"]}
                ]
            },
            {
                "title": "Management - Moderate Attack",
                "section_type": "plan",
                "safety_netting": "MODERATE ATTACK: Salbutamol via spacer - 10 puffs (each puff inhaled separately). If no improvement: Salbutamol nebuliser 5mg via oxygen. Prednisolone 40mg PO OD for 5 days or until recovery. No oxygen required in moderate attack. Review response today. Review in 48 hours. Step up treatment plan. Admit if deteriorating. SEVERE ATTACK: Salbutamol nebuliser 5mg (may repeat every 15-30 min). Ipratropium bromide 0.5mg nebuliser (added to salbutamol). Prednisolone 40mg PO (or IV hydrocortisone 200mg if unable to take PO). Oxygen to maintain SpO2 94-98%. Urgent hospital admission. LIFE-THREATENING: EMERGENCY - call 999. Oxygen, nebulised bronchodilators, IV steroids, consider IV magnesium sulphate, urgent ICU admission.",
                "questions": [
                    {"id": "ama_bronchodilator", "type": "single_select", "label": "Initial Bronchodilator (Moderate)", "required": False, "options": ["Salbutamol via spacer - 10 puffs", "Salbutamol nebuliser 5mg via O2 (if no improvement)", "Salbutamol nebuliser 5mg + Ipratropium 0.5mg (severe)"]},
                    {"id": "ama_steroids", "type": "single_select", "label": "Steroid Therapy", "required": False, "options": ["Prednisolone 40mg PO OD for 5 days or until recovery", "IV Hydrocortisone 200mg (if unable to take PO)", "Not indicated"]},
                    {"id": "ama_oxygen", "type": "single_select", "label": "Oxygen Therapy", "required": False, "options": ["Not required (moderate attack, SpO2 >92%)", "Required - maintain SpO2 94-98%", "High flow O2 (severe/life-threatening)"]},
                    {"id": "ama_medication_review", "type": "toggle", "label": "Review Medications - Step Up Treatment?", "required": True},
                    {"id": "ama_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., Review response today, review in 48 hours, admit if deteriorating"}
                ]
            }
        ]},
        "is_public": True
    }

    existing = db.query(Template).filter(Template.title == t["title"], Template.created_by == admin.id).first()
    
    if existing:
        # Update existing template instead of deleting
        existing.description = t["description"]
        existing.content = t["content"]
        existing.category = t["category"]
        existing.is_public = t["is_public"]
        existing.updated_at = datetime.now(timezone.utc)
        db.commit()
        print(f"🔄 Updated: {t['title']}")
    new_t = Template(title=t["title"], description=t["description"], category=t["category"], content=t["content"], is_public=True, created_by=admin.id, version=1)
    db.add(new_t); db.commit()
    print(f"Template '{t['title']}' created with {len(t['content']['sections'])} sections!"); db.close()

if __name__ == "__main__":
    seed_acute_asthma()
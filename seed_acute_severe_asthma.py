from app.database import SessionLocal
from app.models import User, Template, Category

def seed_acute_severe_asthma():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Respiratory").first()
    if not category: category = Category(name="Respiratory"); db.add(category); db.commit()

    t = {
        "title": "Acute Severe Asthma",
        "description": "Emergency template for acute severe asthma covering BTS/SIGN severity criteria, nebulised bronchodilator protocol, steroid therapy, and A&E referral pathway.",
        "category": "Respiratory",
        "content": {"sections": [
            {
                "title": "Initial Assessment",
                "section_type": "history",
                "questions": [
                    {"id": "asa_symptoms", "type": "multi_select", "label": "Presenting Symptoms", "required": True, "options": ["Wheeze", "Shortness of breath", "Increased respiratory rate"]},
                    {"id": "asa_speech", "type": "single_select", "label": "Speech", "required": True, "options": ["Unable to complete a sentence in one breath (SEVERE)", "Normal speech (MODERATE)", "Unable to speak (LIFE-THREATENING)"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Unable to complete sentences = SEVERE. Unable to speak = LIFE-THREATENING. Call 999.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Severity Criteria (Any ONE Confirms Severe)",
                "section_type": "examination",
                "questions": [
                    {"id": "asa_rr", "type": "number", "label": "Respiratory Rate (/min)", "required": True, "placeholder": "e.g., 28", "is_red_flag": True, "red_flag_positive": "RED FLAG: RR ≥25 = SEVERE asthma criterion met. Start nebulisers + steroids.", "red_flag_negative": ""},
                    {"id": "asa_hr", "type": "number", "label": "Pulse (bpm)", "required": True, "placeholder": "e.g., 115", "is_red_flag": True, "red_flag_positive": "RED FLAG: HR ≥110 = SEVERE asthma criterion met. Start nebulisers + steroids.", "red_flag_negative": ""},
                    {"id": "asa_pefr", "type": "number", "label": "PEFR (% Best or Predicted)", "required": True, "placeholder": "e.g., 40%", "is_red_flag": True, "red_flag_positive": "RED FLAG: PEFR ≤50% = SEVERE asthma criterion met. Use % of best PEFR in preference to % predicted.", "red_flag_negative": ""},
                    {"id": "asa_spo2", "type": "number", "label": "SpO2 (%)", "required": True, "placeholder": "e.g., 91%", "is_red_flag": True, "red_flag_positive": "RED FLAG: SpO2 <92% = severe/life-threatening. Start O2 immediately.", "red_flag_negative": ""},
                    {"id": "asa_chest", "type": "single_select", "label": "Respiratory Examination", "required": True, "options": ["Decreased air entry B/L + expiratory polyphonic wheeze", "Silent chest - LIFE-THREATENING", "Other finding"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Silent chest = NO air entry. LIFE-THREATENING. Emergency 999.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Severity Classification",
                "section_type": "assessment",
                "differentials": [
                    "Acute Asthma - MODERATE (PEFR 50-75%, normal speech, SpO2 >92%, RR <25, HR <110)",
                    "Acute Asthma - SEVERE (Any 1 of: PEFR ≤50%, can't complete sentences, RR ≥25, HR ≥110, SpO2 <92%)",
                    "Acute Asthma - LIFE-THREATENING (PEFR <33%, SpO2 <92%, silent chest, cyanosis, exhaustion, bradycardia, hypotension, confusion, coma)",
                    "Near-Fatal Asthma (rising PaCO2 or requiring mechanical ventilation)"
                ],
                "questions": [
                    {"id": "asa_severity", "type": "single_select", "label": "Severity Classification (BTS/SIGN)", "required": True, "options": ["MODERATE - Manage in Primary Care", "SEVERE - Urgent A&E Referral", "LIFE-THREATENING - EMERGENCY 999", "Near-Fatal - CRITICAL CARE"]}
                ]
            },
            {
                "title": "Management - Severe Attack",
                "section_type": "plan",
                "safety_netting": "SEVERE ATTACK: Oxygen to maintain SpO2 94-98%. Salbutamol 5mg nebulised (may repeat every 15-30 min) OR Salbutamol via spacer 12 puffs. Ipratropium (Atrovent) 0.5mg nebulised (add to salbutamol). Prednisolone 40mg PO OD for 5 days (or IV Hydrocortisone 200mg if unable to take PO). Antibiotics ONLY if evidence of infection. Refer A&E for ongoing management. Reassess response to nebulisers prior to transfer. LIFE-THREATENING: Call 999. High flow O2. Salbutamol + Ipratropium nebulised. IV Hydrocortisone 200mg. Consider IV Magnesium Sulphate 2g over 20 minutes. Urgent ICU admission. Do NOT delay transfer for investigations.",
                "questions": [
                    {"id": "asa_oxygen", "type": "toggle", "label": "Oxygen - Titrate to Keep SpO2 94-98%?", "required": True},
                    {"id": "asa_beta_agonist", "type": "single_select", "label": "Beta-2 Agonist", "required": True, "options": ["Salbutamol 5mg nebulised (repeat every 15-30 min)", "Salbutamol via spacer - 12 puffs"]},
                    {"id": "asa_anticholinergic", "type": "toggle", "label": "Ipratropium (Atrovent) 0.5mg Nebulised Added?", "required": True},
                    {"id": "asa_steroids", "type": "single_select", "label": "Steroid Therapy", "required": True, "options": ["Prednisolone 40mg PO OD for 5 days", "IV Hydrocortisone 200mg (if unable to take PO)", "Not indicated"]},
                    {"id": "asa_antibiotics", "type": "single_select", "label": "Antibiotics", "required": False, "options": ["Only if evidence of infection", "Not indicated"]},
                    {"id": "asa_referral", "type": "single_select", "label": "Referral", "required": True, "options": ["Refer A&E for ongoing management", "EMERGENCY 999 (life-threatening)", "Admit for observation"]},
                    {"id": "asa_followup", "type": "text", "label": "Transfer Plan", "required": True, "placeholder": "e.g., Emergency transfer to A&E, reassess response to nebulisers prior to transfer"}
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
    seed_acute_severe_asthma()
from app.database import SessionLocal
from app.models import User, Template, Category

def seed_egfr_ckd():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin: print("Admin not found."); db.close(); return
    category = db.query(Category).filter(Category.name == "Urology").first()
    if not category: category = Category(name="Urology"); db.add(category); db.commit()

    t = {
        "title": "eGFR 45-60 / CKD Stage 3a",
        "description": "Management of eGFR 45-60 (CKD Stage 3a). Includes monitoring frequency, BP targets, statin therapy, nephrology referral criteria, and NICE CKD guideline recommendations.",
        "category": "Urology",
        "content": {"sections": [
            {"title": "History", "questions": [
                {"id": "ckd_egfr_current", "type": "number", "label": "Current eGFR (ml/min/1.73m²)", "required": True, "placeholder": "e.g., 52"},
                {"id": "ckd_egfr_date", "type": "date", "label": "Date of Test", "required": True},
                {"id": "ckd_egfr_previous", "type": "number", "label": "Previous eGFR (>3 months ago)", "required": True, "placeholder": "e.g., 54"},
                {"id": "ckd_acr", "type": "number", "label": "Urine ACR (mg/mmol)", "required": True, "placeholder": "e.g., 5"},
                {"id": "ckd_diabetes", "type": "toggle", "label": "Diabetes?", "required": True},
                {"id": "ckd_hypertension", "type": "toggle", "label": "Hypertension?", "required": True},
                {"id": "ckd_fatigue", "type": "toggle", "label": "Fatigue/Nausea/Vomiting/Pruritis?", "required": True},
                {"id": "ckd_restless", "type": "toggle", "label": "Restless Legs?", "required": False},
                {"id": "ckd_anorexia", "type": "toggle", "label": "Anorexia/Weight Loss?", "required": False},
                {"id": "ckd_oedema", "type": "toggle", "label": "Ankle Oedema/SOB/Orthopnoea/PND?", "required": True},
                {"id": "ckd_haematuria", "type": "toggle", "label": "Haematuria (Visible or Persistent Invisible)?", "required": True},
                {"id": "ckd_urinary", "type": "toggle", "label": "Urinary Incontinence or Retention?", "required": False},
                {"id": "ckd_smoking", "type": "single_select", "label": "Smoking Status", "required": True, "options": ["Never", "Ex-Smoker", "Current"]},
                {"id": "ckd_family", "type": "toggle", "label": "Family History Kidney Disease/Polycystic Kidney Disease?", "required": True},
                {"id": "ckd_autoimmune", "type": "toggle", "label": "Autoimmune Disorders?", "required": False},
                {"id": "ckd_arthralgia", "type": "toggle", "label": "Arthralgia/Rashes (Vasculitis)?", "required": False}
            ]},
            {"title": "Examination", "questions": [
                {"id": "ckd_bp_systolic", "type": "number", "label": "BP Systolic (mmHg) - Target <140/90", "required": True, "placeholder": "e.g., 130"},
                {"id": "ckd_bp_diastolic", "type": "number", "label": "BP Diastolic (mmHg)", "required": True, "placeholder": "e.g., 80"},
                {"id": "ckd_hr", "type": "number", "label": "Heart Rate (bpm)", "required": False},
                {"id": "ckd_abdo", "type": "single_select", "label": "Abdominal Examination", "required": True, "options": ["SNT - No Masses/Palpable Bladder", "Abnormal - Masses/Palpable Bladder"]},
                {"id": "ckd_resp", "type": "single_select", "label": "Respiratory Examination", "required": True, "options": ["Clear - Vesicular Breath Sounds", "Crackles/Pulmonary Oedema", "Other"]},
                {"id": "ckd_oedema_exam", "type": "toggle", "label": "Ankle Oedema Present?", "required": True}
            ]},
            {"title": "Investigations & Assessment", "red_flag_threshold": 1, "questions": [
                {"id": "ckd_acr_category", "type": "single_select", "label": "ACR Category", "required": True, "options": ["A1 (<3) - Normal", "A2 (3-30) - Moderately Increased", "A3 (>30) - Severely Increased"]},
                {"id": "ckd_stage", "type": "single_select", "label": "CKD Stage", "required": True, "options": ["Stage 3a (eGFR 45-59)", "Stage 3b (eGFR 30-44)", "Other"]},
                {"id": "ckd_rapid_decline", "type": "toggle", "label": "🔴 Rapid Decline? (≥15ml/min/year or ≥25% in 1 year)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Accelerated CKD progression. Urgent nephrology referral and renal ultrasound.", "red_flag_negative": "Stable eGFR."},
                {"id": "ckd_nephrology", "type": "toggle", "label": "5-Year Renal Replacement Risk >5%? (Check kidneyfailurerisk.com)", "required": True},
                {"id": "ckd_bloods", "type": "multi_select", "label": "Bloods to Check", "required": True, "options": ["FBC", "Ferritin", "Renal Function (U&E)", "HbA1c", "Lipids"]},
                {"id": "ckd_hb", "type": "number", "label": "Hb (g/L)", "required": False},
                {"id": "ckd_hba1c", "type": "number", "label": "HbA1c (mmol/mol)", "required": False}
            ]},
            {"title": "Management Plan", "safety_netting": "If you develop reduced urine output, severe swelling, confusion, nausea/vomiting, or feel systemically unwell, seek urgent medical attention. During episodes of gastroenteritis/dehydration, temporarily stop ACEi/ARB/metformin/nitrofurantoin/gliflozin.", "questions": [
                {"id": "ckd_explanation", "type": "textarea", "label": "Explanation Given to Patient", "required": True, "placeholder": "e.g., Explained CKD Stage 3a is common - occurs in 30% of people in their 70s (TILDA study). eGFR naturally declines with age..."},
                {"id": "ckd_lifestyle", "type": "textarea", "label": "Lifestyle Advice", "required": True, "placeholder": "e.g., Weight loss if appropriate, DASH diet (low salt), avoid NSAIDs..."},
                {"id": "ckd_vaccines", "type": "toggle", "label": "Pneumococcal & Annual Flu Vaccine Advised?", "required": True},
                {"id": "ckd_statin", "type": "single_select", "label": "Atorvastatin 20mg Indicated? (CKD Stage 3-4 for CV risk)", "required": True, "options": ["Yes - Start Atorvastatin 20mg", "Already on Statin", "Contraindicated", "Patient Declined"]},
                {"id": "ckd_bp_target", "type": "single_select", "label": "BP Target", "required": True, "options": ["<140/90 (Standard)", "<130/80 (If ACR >70 or Diabetes)"]},
                {"id": "ckd_acei", "type": "toggle", "label": "ACEi (Ramipril)/ARB Started or Optimised?", "required": True},
                {"id": "ckd_gliflozin", "type": "toggle", "label": "SGLT2i (Dapagliflozin) Indicated? (ACR >30 + Diabetes)", "required": False},
                {"id": "ckd_ultrasound", "type": "toggle", "label": "Renal Ultrasound Indicated?", "required": True},
                {"id": "ckd_avoid_nsaids", "type": "toggle", "label": "Advised to Avoid NSAIDs?", "required": True},
                {"id": "ckd_sick_day", "type": "toggle", "label": "Sick Day Rules Explained? (Hold ACEi/ARB/Metformin during illness)", "required": True},
                {"id": "ckd_monitoring", "type": "single_select", "label": "Monitoring Frequency (NICE CG182)", "required": True, "options": ["6-12 Monthly (Stage 3)", "4-6 Monthly (Stage 4)", "3 Monthly (Stage 5)"]},
                {"id": "ckd_meat_advice", "type": "toggle", "label": "Advised: No Meat 12hrs Before eGFR Test?", "required": False},
                {"id": "ckd_notes", "type": "textarea", "label": "Additional Notes", "required": False}
            ]}
        ]}, "is_public": True
    }

    existing = db.query(Template).filter(Template.title == t["title"], Template.created_by == admin.id).first()
    if existing: db.delete(existing); db.commit()
    new_t = Template(title=t["title"], description=t["description"], category=t["category"], content=t["content"], is_public=True, created_by=admin.id, version=1)
    db.add(new_t); db.commit()
    print(f"Template '{t['title']}' created!"); db.close()

if __name__ == "__main__":
    seed_egfr_ckd()
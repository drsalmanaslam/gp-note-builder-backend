from app.database import SessionLocal
from app.models import User, Template

def seed_gout_review():
    db = SessionLocal()
    admin = db.query(User).filter(User.role == "admin").first()
    if not admin: print("❌ No admin!"); db.close(); return

    title = "Gout - Long-Term Review & Urate-Lowering Therapy"
    existing = db.query(Template).filter(Template.title == title).first()
    if existing: db.delete(existing); db.commit()

    t = Template(title=title, description="Long-term gout management covering urate-lowering therapy (allopurinol/febuxostat), treat-to-target approach, flare prophylaxis, and cardiovascular risk per BSR guidelines.", category="Musculoskeletal", content={"sections": [
        {"title": "Current Status", "section_type": "history", "questions": [
            {"id": "gr_flares_since_last", "type": "number", "label": "Number of Flares Since Last Review", "required": True, "placeholder": "e.g., 2"},
            {"id": "gr_last_flare", "type": "text", "label": "Date of Last Flare", "required": False, "placeholder": "e.g., 3 weeks ago"},
            {"id": "gr_flare_severity", "type": "single_select", "label": "Flare Severity", "required": True, "options": ["Mild - managed at home", "Moderate - needed GP visit", "Severe - A&E/hospital"]},
            {"id": "gr_current_pain", "type": "number", "label": "Current Pain (0-10)", "required": True, "placeholder": "e.g., 0"},
            {"id": "gr_tophi", "type": "toggle", "label": "Tophi Present?", "required": True},
            {"id": "gr_joints_affected", "type": "multi_select", "label": "Joints Affected (Ever)", "required": True, "options": ["1st MTP (podagra)", "Ankle", "Knee", "Elbow", "Wrist", "Finger", "Olecranon bursa"]}
        ]},
        {"title": "Urate-Lowering Therapy (ULT)", "section_type": "history", "questions": [
            {"id": "gr_on_ult", "type": "toggle", "label": "On Urate-Lowering Therapy?", "required": True},
            {"id": "gr_ult_drug", "type": "text", "label": "ULT Drug & Dose", "required": False, "placeholder": "e.g., Allopurinol 300mg OD"},
            {"id": "gr_ult_duration", "type": "text", "label": "Duration on ULT", "required": False, "placeholder": "e.g., 6 months"},
            {"id": "gr_urate_level", "type": "number", "label": "Latest Urate Level (µmol/L)", "required": True, "placeholder": "e.g., 320"},
            {"id": "gr_urate_date", "type": "text", "label": "Date of Urate Test", "required": False, "placeholder": "e.g., 2 weeks ago"},
            {"id": "gr_urate_target", "type": "toggle", "label": "Urate at Target? (<360 µmol/L, or <300 if tophi/severe)", "required": True},
            {"id": "gr_adherence", "type": "single_select", "label": "ULT Adherence", "required": True, "options": ["Excellent - daily without fail", "Good - misses occasionally", "Poor - frequently misses", "Stopped taking"]},
            {"id": "gr_side_effects", "type": "toggle", "label": "ULT Side Effects? (Rash, GI upset)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Rash on allopurinol = ?allopurinol hypersensitivity syndrome (DRESS/SJS). STOP immediately. Never rechallenge.", "red_flag_negative": ""}
        ]},
        {"title": "Flare Prophylaxis", "section_type": "history", "questions": [
            {"id": "gr_prophylaxis", "type": "toggle", "label": "On Flare Prophylaxis? (Colchicine/NSAID/Prednisolone)", "required": True},
            {"id": "gr_prophylaxis_drug", "type": "text", "label": "Prophylaxis Drug & Dose", "required": False, "placeholder": "e.g., Colchicine 500mcg BD"},
            {"id": "gr_prophylaxis_duration", "type": "text", "label": "Duration of Prophylaxis So Far", "required": False, "placeholder": "e.g., 4 months"},
            {"id": "gr_prophylaxis_continue", "type": "toggle", "label": "Continue Prophylaxis? (Until urate at target + 6 months no flares)", "required": True}
        ]},
        {"title": "Comorbidities & Lifestyle", "section_type": "history", "questions": [
            {"id": "gr_ckd", "type": "toggle", "label": "CKD? (eGFR - important for allopurinol dosing)", "required": True},
            {"id": "gr_egfr", "type": "number", "label": "Latest eGFR", "required": False, "placeholder": "e.g., 55"},
            {"id": "gr_htn", "type": "toggle", "label": "Hypertension?", "required": True},
            {"id": "gr_dm", "type": "toggle", "label": "Diabetes?", "required": True},
            {"id": "gr_diuretics", "type": "toggle", "label": "On Diuretics? (Increase urate)", "required": True},
            {"id": "gr_weight", "type": "number", "label": "Weight (kg)", "required": False},
            {"id": "gr_alcohol", "type": "single_select", "label": "Alcohol", "required": True, "options": ["None", "Within limits", "Excess - beer/spirits"]},
            {"id": "gr_diet", "type": "toggle", "label": "Dietary Advice Followed? (Reduce purines, red meat, shellfish)", "required": True}
        ]},
        {"title": "Assessment", "section_type": "assessment", "differentials": ["Gout - at target urate, stable", "Gout - not at target, needs ULT optimisation", "Gout - poor adherence", "Gout - treatment-resistant/severe (consider febuxostat or rheumatology referral)", "Pseudogout (CPPD)", "Septic arthritis (always consider in single hot joint)"], "questions": [
            {"id": "gr_control", "type": "single_select", "label": "Gout Control", "required": True, "options": ["Well-controlled - target urate, no flares", "Partially controlled - flares still occurring", "Poorly controlled - frequent flares, tophi", "Not on ULT - needs initiation"]},
            {"id": "gr_ult_plan", "type": "single_select", "label": "ULT Plan", "required": True, "options": ["Continue current dose - at target", "Increase allopurinol dose (not at target)", "Switch to febuxostat (allopurinol intolerant/resistant)", "Start ULT (first presentation)", "Refer rheumatology"]}
        ]},
        {"title": "Management", "section_type": "plan", "safety_netting": "ULT is lifelong treatment. Never stop during acute flare (continue ULT while treating flare). Target urate: <360 µmol/L (standard) or <300 µmol/L (tophi, severe, frequent flares). Allopurinol: start 100mg OD (50mg if eGFR <60), titrate up every 4 weeks by 100mg until target reached (max 900mg). Colchicine prophylaxis: 500mcg BD for 6 months after starting ULT (reduce to OD if eGFR 30-60, avoid if eGFR <30). Flare treatment: NSAID (Naproxen) or Colchicine 500mcg TDS or Prednisolone 30mg OD 5 days. STOP if rash develops on allopurinol - never rechallenge. Return if: severe flare, rash, or signs of infection (red hot joint + fever = ?septic arthritis).", "questions": [
            {"id": "gr_plan", "type": "multi_select", "label": "Management", "required": True, "options": ["Continue current ULT", "Increase allopurinol dose", "Start allopurinol (new initiation)", "Continue colchicine prophylaxis", "Stop colchicine prophylaxis (6 months + at target)", "Check urate in 4 weeks", "Repeat urate + U&E", "Dietary/lifestyle advice", "Rheumatology referral"]},
            {"id": "gr_new_dose", "type": "text", "label": "New ULT Dose", "required": False, "placeholder": "e.g., Allopurinol 300mg OD"},
            {"id": "gr_prophylaxis_plan", "type": "text", "label": "Prophylaxis Plan", "required": False, "placeholder": "e.g., Colchicine 500mcg BD for further 2 months"},
            {"id": "gr_flare_plan", "type": "toggle", "label": "Flare Action Plan Given? (NSAID/Colchicine/Prednisolone to keep at home)", "required": True},
            {"id": "gr_followup", "type": "text", "label": "Follow-up", "required": True, "placeholder": "e.g., Check urate in 4 weeks after dose change, review in 2 months"}
        ]}
    ]}, is_public=True, created_by=admin.id)
    db.add(t); db.commit(); print(f"✅ {title}"); db.close()

if __name__ == "__main__": seed_gout_review()
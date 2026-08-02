from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_gout():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Musculoskeletal").first()
    if not category: category = Category(name="Musculoskeletal"); db.add(category); db.commit()

    t = {
        "title": "Gout - Acute & Long-Term Management",
        "description": "Comprehensive gout management covering acute attack treatment (Colchicine/NSAIDs/Prednisolone), urate-lowering therapy (Allopurinol/Febuxostat), prophylaxis, and cardiovascular risk management.",
        "category": "Musculoskeletal",
        "content": {"sections": [
            {
                "title": "History",
                "section_type": "history",
                "questions": [
                    {"id": "gout_presenting_complaint", "type": "text", "label": "Presenting Complaint", "required": True, "placeholder": "e.g., Sudden severe pain in right big toe for 24 hours"},
                    {"id": "gout_duration", "type": "text", "label": "Duration", "required": True, "placeholder": "e.g., 1 day - came on within 24 hours"},
                    {"id": "gout_site", "type": "single_select", "label": "Affected Joint", "required": True, "options": ["1st MTP (Podagra - Most Common)", "Ankle", "Knee", "Wrist", "Elbow", "Other"]},
                    {"id": "gout_severity", "type": "single_select", "label": "Severity", "required": True, "options": ["Difficulty Putting on Sock/Shoe", "Pain When Sheets Rub Against It", "Unable to Weight Bear", "Severe - Cannot Touch"]},
                    {"id": "gout_itch_preceding", "type": "toggle", "label": "Preceded by Itch? (Prodromal Symptom)", "required": False},
                    {"id": "gout_tophi", "type": "toggle", "label": "Fleshy Swellings on Fingers/Elbows/Ears? (Tophi)", "required": False},
                    {"id": "gout_trauma", "type": "toggle", "label": "Recent Trauma?", "required": False},
                    {"id": "gout_alcohol", "type": "text", "label": "Alcohol Intake (Units/Week)", "required": False, "placeholder": "e.g., 3"},
                    {"id": "gout_fever", "type": "toggle", "label": "Fever or Polyarthropathy?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Fever + polyarthropathy = ?septic arthritis. Urgent aspiration + orthopaedics.", "red_flag_negative": ""},
                    {"id": "gout_thiazide", "type": "toggle", "label": "Taking Thiazide Diuretic? (Raises Uric Acid)", "required": True},
                    {"id": "gout_previous_episodes", "type": "number", "label": "Number of Episodes in Past Year", "required": False, "placeholder": "e.g., 2 (>2/year = Consider Urate-Lowering Therapy)"}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "gout_hr", "type": "number", "label": "Pulse (bpm)", "required": False, "placeholder": "e.g., 80"},
                    {"id": "gout_temp", "type": "number", "label": "Temperature (°C)", "required": False, "placeholder": "e.g., 37"},
                    {"id": "gout_joint", "type": "single_select", "label": "Affected Joint Appearance", "required": True, "options": ["Tender, Inflamed, Warm - No Erythema", "Tender, Inflamed, Warm + Erythema", "Tophi Present", "Normal"]},
                    {"id": "gout_tophi_exam", "type": "multi_select", "label": "Tophi on Examination", "required": True, "options": ["Helix of Ears", "Elbows", "Fingers", "Tendons", "None"]}
                ]
            },
            {
                "title": "Acute Attack - Treatment (GP Evidence)",
                "section_type": "plan",
                "safety_netting": "Return tomorrow if NOT 50% better. If on Colchicine + not improving = add Naproxen 500mg BD OR Prednisolone 40mg OD for 5 days. Naproxen and Prednisolone NOT to be given together. Bloods: Uric Acid, FBC, Renal Profile, Fasting Lipids, Glucose, Ferritin, HbA1c - today or in 2 weeks (wait for acute attack to settle for accurate urate). BP check - if ≥140/90 arrange 24h BP monitoring. Explain link with BP and CV risk. Patient leaflets: HSE Gout, Arthritis Ireland, Versus Arthritis. GP Evidence: https://gpevidence.org/conditions/gout/",
                "questions": [
                    {"id": "gout_acute_rx", "type": "single_select", "label": "Acute Treatment (First-Line)", "required": True, "options": ["Colchicine 500mcg QDS (BD if >65 Years)", "Naproxen 500mg BD (If eGFR >30, No Ulcers/Asthma)", "Ibuprofen 400mg TDS", "Prednisolone 40mg OD for 5 Days"]},
                    {"id": "gout_second_line", "type": "single_select", "label": "If Not 50% Better Tomorrow (Add if on Colchicine)", "required": False, "options": ["Add Naproxen 500mg BD", "Add Prednisolone 40mg OD for 5 Days", "Not Applicable - Already on NSAID/Steroid", "Not Applicable - Reviewing Tomorrow"]},
                    {"id": "gout_diet", "type": "toggle", "label": "Healthy Balanced Diet Advised?", "required": False}
                ]
            },
            {
                "title": "Urate-Lowering Therapy (If >2 Episodes/Year + Uric Acid >360 µmol/L)",
                "section_type": "plan",
                "questions": [
                    {"id": "gout_ult_indicated", "type": "toggle", "label": "Urate-Lowering Therapy Indicated? (>2 Episodes/Year + Uric Acid >360 µmol/L)", "required": False},
                    {"id": "gout_allopurinol", "type": "single_select", "label": "Allopurinol (Titrate: 100mg→300mg Over 6 Weeks)", "required": False, "options": ["Start 100mg OD - Titrate Up Over 6 Weeks to 300mg", "Already on Allopurinol - Continue", "Not Indicated / Contraindicated", "Not Starting Yet - Awaiting Uric Acid"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Warn to return IMMEDIATELY if rash develops (Stevens-Johnson risk). Caution with Azathioprine - reduce Azathioprine to 1/4 dose + monitor FBC.", "red_flag_negative": ""},
                    {"id": "gout_febuxostat", "type": "single_select", "label": "Febuxostat (If Normal LFT + No IHD/CCF/Creatinine >177)", "required": False, "options": ["Start 80mg OD - Increase to 120mg if Urate >357 After 3 Weeks", "Not Indicated", "Contraindicated (IHD/CCF/Renal/LFT)"]},
                    {"id": "gout_prophylaxis", "type": "single_select", "label": "Prophylaxis During ULT Initiation (Colchicine for 6 Months: 0.5mg BD x2mo → 0.5mg OD x2mo → 0.5mg Alt Days x2mo)", "required": False, "options": ["Colchicine 0.5mg BD (2 Months)", "Naproxen Cover", "Not Started - No ULT Yet", "Not Required - Already on ULT >6 Months"]},
                    {"id": "gout_ult_lifelong", "type": "toggle", "label": "ULT is LIFELONG - Do NOT Discontinue if Flare During Treatment?", "required": False}
                ]
            },
            {
                "title": "Monitoring & Follow-Up",
                "section_type": "plan",
                "questions": [
                    {"id": "gout_bloods", "type": "multi_select", "label": "Bloods Ordered", "required": False, "options": ["Uric Acid", "FBC", "Renal Profile (U&E, eGFR)", "Fasting Lipids", "Fasting Glucose / HbA1c", "Ferritin", "LFTs (If Starting Febuxostat)"]},
                    {"id": "gout_bp", "type": "toggle", "label": "BP Check - If ≥140/90 Arrange 24h BP Monitor? (Link with CV Risk)", "required": False},
                    {"id": "gout_leaflets", "type": "multi_select", "label": "Patient Information Given", "required": False, "options": ["HSE Gout (hse.ie/conditions/gout)", "Arthritis Ireland Leaflet", "Versus Arthritis"]},
                    {"id": "gout_monitoring", "type": "text", "label": "Monitoring Plan (Urate, LFT, Renal - 6 Monthly in 1st Year, Then Annually)", "required": False, "placeholder": "e.g., 6-monthly urate + renal + LFT for 1st year"},
                    {"id": "gout_xray", "type": "toggle", "label": "X-Ray? (If Ongoing Pain - ?Chondrocalcinosis/Pseudogout)", "required": False},
                    {"id": "gout_diagnosis", "type": "single_select", "label": "Impression", "required": True, "options": ["Acute Gout - First Episode", "Acute Gout - Recurrent", "Gout - Starting ULT", "Suspected Septic Arthritis - URGENT", "?Pseudogout"]},
                    {"id": "gout_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., Review tomorrow if not 50% better, 2 weeks for bloods, 6-monthly if on ULT"}
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
    seed_gout()
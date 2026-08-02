from app.database import SessionLocal
from app.models import User, Template

def seed_sick_note():
    db = SessionLocal()
    admin = db.query(User).filter(User.role == "admin").first()
    if not admin: print("❌ No admin!"); db.close(); return

    title = "Sick Note / Fit Note (MED3)"
    existing = db.query(Template).filter(Template.title == title).first()
    if existing: db.delete(existing); db.commit()

    t = Template(title=title, description="Structured consultation for issuing fit notes (MED3) covering assessment of fitness for work, phased return, workplace adjustments, and may-be-fit options.", category="General Practice", content={"sections": [
        {"title": "Patient Details & Reason", "section_type": "history", "questions": [
            {"id": "sn_diagnosis", "type": "text", "label": "Clinical Diagnosis / Reason for Sick Note", "required": True, "placeholder": "e.g., Acute LBP with sciatica, Post-operative recovery"},
            {"id": "sn_duration_off", "type": "text", "label": "Duration Already Off Work", "required": False, "placeholder": "e.g., Self-certified 5 days, now day 7"},
            {"id": "sn_occupation", "type": "text", "label": "Patient's Occupation", "required": True, "placeholder": "e.g., Warehouse operative - heavy lifting"},
            {"id": "sn_employer", "type": "text", "label": "Employer (optional)", "required": False, "placeholder": "e.g., Amazon, Tesco"},
            {"id": "sn_self_employed", "type": "toggle", "label": "Self-Employed?", "required": False}
        ]},
        {"title": "Functional Assessment", "section_type": "history", "questions": [
            {"id": "sn_mobility", "type": "single_select", "label": "Mobility", "required": True, "options": ["Fully mobile", "Reduced mobility - cannot walk far", "Requires walking aid", "Bedbound/housebound"]},
            {"id": "sn_sitting", "type": "toggle", "label": "Can Sit Comfortably? (Desk job)", "required": False},
            {"id": "sn_standing", "type": "toggle", "label": "Can Stand for Prolonged Periods? (Retail/manual)", "required": False},
            {"id": "sn_lifting", "type": "toggle", "label": "Can Lift/Carry? (Manual work)", "required": False},
            {"id": "sn_driving", "type": "toggle", "label": "Can Drive Safely? (DVLA rules)", "required": False},
            {"id": "sn_concentration", "type": "toggle", "label": "Concentration Affected? (Safety-critical roles)", "required": False},
            {"id": "sn_infection_risk", "type": "toggle", "label": "Infection Risk to Others? (Food handling, healthcare, childcare)", "required": False}
        ]},
        {"title": "Fit Note Decision", "section_type": "assessment", "questions": [
            {"id": "sn_decision", "type": "single_select", "label": "Fitness for Work Decision", "required": True, "options": ["Not Fit for Work", "May Be Fit for Work (with adjustments)"]},
            {"id": "sn_period_from", "type": "text", "label": "From (Date)", "required": True, "placeholder": "e.g., Today or start of illness"},
            {"id": "sn_period_to", "type": "text", "label": "To (Date)", "required": True, "placeholder": "e.g., 2 weeks from now"},
            {"id": "sn_may_be_fit", "type": "multi_select", "label": "If 'May Be Fit' - Workplace Adjustments", "required": False, "options": ["Phased return (reduced hours)", "Amended duties (no heavy lifting)", "Altered hours (flexible start/finish)", "Workplace adaptations (special chair, parking)", "Avoid night shifts", "Avoid driving/operating machinery", "Work from home"]},
            {"id": "sn_phased_return_detail", "type": "text", "label": "Phased Return Details", "required": False, "placeholder": "e.g., Week 1: 4h/day, Week 2: 6h/day, Week 3: full-time"},
            {"id": "sn_reassessment", "type": "toggle", "label": "Needs Reassessment Before Return?", "required": True}
        ]},
        {"title": "Additional Information", "section_type": "assessment", "questions": [
            {"id": "sn_occupational_health", "type": "toggle", "label": "Occupational Health Referral Needed?", "required": False},
            {"id": "sn_physio", "type": "toggle", "label": "Physiotherapy/Rehab Referral?", "required": False},
            {"id": "sn_counselling", "type": "toggle", "label": "Counselling / Mental Health Support?", "required": False},
            {"id": "sn_benefits_advice", "type": "toggle", "label": "Benefits Advice Needed? (ESA, PIP, Universal Credit)", "required": False},
            {"id": "sn_dvla", "type": "toggle", "label": "DVLA Notification Required?", "required": False}
        ]},
        {"title": "Management", "section_type": "plan", "safety_netting": "Fit notes are legal documents. Self-certification covers first 7 calendar days (including weekends). Fit note required from day 8 onwards. Fit notes can be backdated if medically appropriate. 'May be fit for work' requires employer agreement to implement adjustments - if employer cannot accommodate, the note defaults to 'not fit for work'. Patients can return to work before fit note expires if they feel able. If condition worsens or new symptoms develop, patient should seek review before fit note expiry. Sick pay entitlement: Statutory Sick Pay (SSP) from employer for up to 28 weeks (check eligibility).", "questions": [
            {"id": "sn_med3_issued", "type": "toggle", "label": "MED3 Fit Note Issued?", "required": True},
            {"id": "sn_first_note", "type": "toggle", "label": "First Fit Note for This Episode?", "required": True},
            {"id": "sn_treatment_plan", "type": "text", "label": "Treatment/Rehab Plan During Sick Leave", "required": False, "placeholder": "e.g., Physio weekly, analgesia, GP review in 2 weeks"},
            {"id": "sn_followup", "type": "text", "label": "Follow-up / Review Before Return", "required": True, "placeholder": "e.g., Review in 2 weeks, reassess fitness, extend fit note if needed"}
        ]}
    ]}, is_public=True, created_by=admin.id)
    db.add(t); db.commit(); print(f"✅ {title}"); db.close()

if __name__ == "__main__": seed_sick_note()
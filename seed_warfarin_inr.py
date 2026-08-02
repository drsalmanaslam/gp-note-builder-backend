from app.database import SessionLocal
from app.models import User, Template

def seed_warfarin_inr():
    db = SessionLocal()
    admin = db.query(User).filter(User.role == "admin").first()
    if not admin: print("❌ No admin!"); db.close(); return

    title = "Warfarin / INR Management"
    existing = db.query(Template).filter(Template.title == title).first()
    if existing: db.delete(existing); db.commit()

    t = Template(title=title, description="Warfarin monitoring and INR management covering target ranges, dose adjustment, bleeding risk assessment, bridging, and switching to DOAC per NICE NG196.", category="Cardiovascular", content={"sections": [
        {"title": "Current Treatment", "section_type": "history", "questions": [
            {"id": "inr_indication", "type": "single_select", "label": "Indication for Anticoagulation", "required": True, "options": ["Atrial Fibrillation", "DVT/PE (acute - first 3 months)", "DVT/PE (extended - 3-6 months)", "DVT/PE (long-term)", "Mechanical heart valve", "Antiphospholipid syndrome", "Other"]},
            {"id": "inr_target", "type": "single_select", "label": "Target INR Range", "required": True, "options": ["2.0 - 3.0 (AF, DVT/PE)", "2.5 - 3.5 (Mechanical mitral valve, recurrent DVT/PE on warfarin)"]},
            {"id": "inr_current", "type": "number", "label": "Current INR", "required": True, "placeholder": "e.g., 2.4"},
            {"id": "inr_date", "type": "text", "label": "Date of INR Test", "required": True, "placeholder": "e.g., Today"},
            {"id": "inr_previous", "type": "text", "label": "Previous INR & Date", "required": False, "placeholder": "e.g., 2.6 (2 weeks ago)"},
            {"id": "inr_current_dose", "type": "text", "label": "Current Warfarin Dose", "required": True, "placeholder": "e.g., 5mg OD (3mg Mon/Wed/Fri, 5mg other days)"},
            {"id": "inr_stability", "type": "single_select", "label": "INR Stability (Time in Therapeutic Range - TTR)", "required": True, "options": ["Good control (TTR >65%)", "Moderate control (TTR 50-65%)", "Poor control (TTR <50%)", "Labile - erratic INRs"]},
            {"id": "inr_duration_therapy", "type": "text", "label": "Duration on Warfarin", "required": False, "placeholder": "e.g., 3 years"}
        ]},
        {"title": "Bleeding Risk Assessment", "section_type": "history", "questions": [
            {"id": "inr_bleeding_any", "type": "toggle", "label": "Any Bleeding? (Gums, nose, bruising, PR, haematuria)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Active bleeding on warfarin = URGENT. Check INR stat, consider admission.", "red_flag_negative": ""},
            {"id": "inr_melaena", "type": "toggle", "label": "Melaena / Haematemesis?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: GI bleeding = EMERGENCY. Stop warfarin, admit. Consider vitamin K + prothrombin complex.", "red_flag_negative": ""},
            {"id": "inr_head_injury", "type": "toggle", "label": "Recent Head Injury/Fall?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Head injury on warfarin = CT head even with normal exam. Admit for observation.", "red_flag_negative": ""},
            {"id": "inr_bruising", "type": "single_select", "label": "Easy Bruising?", "required": True, "options": ["None", "Mild - occasional", "Significant - large/spontaneous"]},
            {"id": "inr_anticoagulant_card", "type": "toggle", "label": "Yellow Anticoagulant Card Issued?", "required": True}
        ]},
        {"title": "Drug Interactions & Lifestyle", "section_type": "history", "questions": [
            {"id": "inr_new_meds", "type": "toggle", "label": "New Medications? (Antibiotics, NSAIDs, amiodarone, statins)", "required": True},
            {"id": "inr_alcohol", "type": "single_select", "label": "Alcohol Intake", "required": True, "options": ["None", "Within limits (≤14 units/week)", "Excess / Binge drinking", "Recent change"]},
            {"id": "inr_diet_change", "type": "toggle", "label": "Diet Change? (Vitamin K - green leafy veg, cranberry)", "required": True},
            {"id": "inr_herbal", "type": "toggle", "label": "Herbal/OTC Preparations? (St John's Wort, ginkgo, glucosamine)", "required": False},
            {"id": "inr_consider_doac", "type": "toggle", "label": "Consider Switching to DOAC? (If AF/DVT/PE, TTR <65%, no mechanical valve/APS)", "required": True}
        ]},
        {"title": "INR Interpretation & Dose Adjustment", "section_type": "assessment", "questions": [
            {"id": "inr_in_range", "type": "toggle", "label": "INR Within Target Range?", "required": True},
            {"id": "inr_action", "type": "single_select", "label": "Dose Adjustment Required", "required": True, "options": ["No change - INR in range, stable", "Increase warfarin dose (INR below target)", "Decrease warfarin dose (INR above target)", "Withhold warfarin (INR significantly high)", "Stop warfarin + vitamin K (INR >8 or bleeding)", "Switch to DOAC"]},
            {"id": "inr_new_dose", "type": "text", "label": "New Warfarin Regime", "required": False, "placeholder": "e.g., Increase to 6mg OD"},
            {"id": "inr_next_check", "type": "text", "label": "Next INR Check", "required": True, "placeholder": "e.g., 1 week (stable), 3 days (dose change)"}
        ]},
        {"title": "Management", "section_type": "plan", "safety_netting": "Seek urgent medical attention if: any bleeding that doesn't stop, black/tarry stools, vomiting blood, unexplained bruising, severe headache, or head injury. Maintain consistent diet (vitamin K foods in moderation - do NOT avoid completely). Limit alcohol to ≤2 drinks/day. Avoid NSAIDs. Report any new medications. Always inform all healthcare providers you take warfarin. Attend INR checks regularly. If switching to DOAC: stop warfarin, start DOAC when INR <2.0.", "questions": [
            {"id": "inr_safety_advice", "type": "toggle", "label": "Bleeding Risk & Safety Advice Given?", "required": True},
            {"id": "inr_new_card", "type": "toggle", "label": "Anticoagulant Card Updated?", "required": False},
            {"id": "inr_doac_switch", "type": "text", "label": "DOAC Switch Plan", "required": False, "placeholder": "e.g., Stop warfarin, start Apixaban 5mg BD when INR <2.0"},
            {"id": "inr_followup", "type": "text", "label": "Follow-up", "required": True, "placeholder": "e.g., INR in 1 week, GP review monthly, consider DOAC switch at next review"}
        ]}
    ]}, is_public=True, created_by=admin.id)
    db.add(t); db.commit(); print(f"✅ {title}"); db.close()

if __name__ == "__main__": seed_warfarin_inr()
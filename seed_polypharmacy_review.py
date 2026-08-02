from app.database import SessionLocal
from app.models import User, Template

def seed_dementia_review():
    db = SessionLocal()
    admin = db.query(User).filter(User.role == "admin").first()
    if not admin: print("❌ No admin!"); db.close(); return

    title = "Dementia Annual Review"
    existing = db.query(Template).filter(Template.title == title).first()
    if existing: db.delete(existing); db.commit()

    t = Template(title=title, description="Annual dementia review covering cognitive assessment, BPSD screening, carer support, medication review (cholinesterase inhibitors), advanced care planning, and QOF requirements.", category="Elderly Care", content={"sections": [
        {"title": "Cognitive Assessment", "section_type": "examination", "questions": [
            {"id": "dem_cognitive_test", "type": "single_select", "label": "Cognitive Test Used", "required": True, "options": ["MMSE", "MoCA", "AMTS (10-point)", "GPCOG", "6-CIT"]},
            {"id": "dem_score", "type": "number", "label": "Score", "required": True, "placeholder": "e.g., MMSE 22/30"},
            {"id": "dem_previous_score", "type": "text", "label": "Previous Score & Date", "required": False, "placeholder": "e.g., MMSE 24/30 (12 months ago)"},
            {"id": "dem_decline", "type": "toggle", "label": "Significant Decline? (>3 points MMSE/year)", "required": True},
            {"id": "dem_memory", "type": "single_select", "label": "Memory (Subjective)", "required": True, "options": ["Stable", "Mild decline", "Moderate decline", "Severe decline"]},
            {"id": "dem_communication", "type": "single_select", "label": "Communication", "required": True, "options": ["Normal", "Word-finding difficulty", "Reduced comprehension", "Non-verbal"]},
            {"id": "dem_orientation", "type": "single_select", "label": "Orientation", "required": True, "options": ["Fully oriented", "Disoriented to time", "Disoriented to place", "Disoriented to person"]}
        ]},
        {"title": "BPSD (Behavioural & Psychological Symptoms)", "section_type": "history", "questions": [
            {"id": "dem_agitation", "type": "toggle", "label": "Agitation / Aggression?", "required": True},
            {"id": "dem_psychosis", "type": "toggle", "label": "Hallucinations / Delusions?", "required": True},
            {"id": "dem_anxiety", "type": "toggle", "label": "Anxiety / Depression?", "required": True},
            {"id": "dem_sleep", "type": "toggle", "label": "Sleep Disturbance / Sundowning?", "required": True},
            {"id": "dem_wandering", "type": "toggle", "label": "Wandering / Getting Lost?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Wandering = safety risk. Consider GPS tracker, door alarms, Herbert Protocol.", "red_flag_negative": ""},
            {"id": "dem_apathy", "type": "toggle", "label": "Apathy / Withdrawal?", "required": False},
            {"id": "dem_disinhibition", "type": "toggle", "label": "Disinhibition / Socially Inappropriate?", "required": False}
        ]},
        {"title": "Functional Assessment", "section_type": "history", "questions": [
            {"id": "dem_adls", "type": "single_select", "label": "Activities of Daily Living", "required": True, "options": ["Independent", "Needs prompting", "Needs assistance", "Fully dependent"]},
            {"id": "dem_personal_care", "type": "toggle", "label": "Personal Care: Needs Help?", "required": True},
            {"id": "dem_meals", "type": "toggle", "label": "Meals: Needs Help?", "required": True},
            {"id": "dem_incontinence", "type": "toggle", "label": "Incontinence? (Urinary/Faecal)", "required": True},
            {"id": "dem_mobility", "type": "single_select", "label": "Mobility", "required": True, "options": ["Independent", "Uses stick/frame", "Needs assistance", "Bedbound/chairbound"]},
            {"id": "dem_falls", "type": "toggle", "label": "Falls in Last 12 Months?", "required": True},
            {"id": "dem_driving", "type": "toggle", "label": "Still Driving? (DVLA + insurance MUST be informed)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Dementia + driving = DVLA must be informed. Legal requirement. Document advice given.", "red_flag_negative": ""}
        ]},
        {"title": "Carer Assessment", "section_type": "history", "questions": [
            {"id": "dem_carer", "type": "toggle", "label": "Has Carer?", "required": True},
            {"id": "dem_carer_relationship", "type": "text", "label": "Carer Relationship", "required": False, "placeholder": "e.g., Spouse, daughter"},
            {"id": "dem_carer_stress", "type": "single_select", "label": "Carer Stress / Burden", "required": False, "options": ["Coping well", "Moderate stress", "Significant stress - needs support", "Crisis - cannot continue"]},
            {"id": "dem_carer_assessment", "type": "toggle", "label": "Carer's Assessment Offered?", "required": False},
            {"id": "dem_respite", "type": "toggle", "label": "Respite Care Discussed?", "required": False},
            {"id": "dem_safeguarding", "type": "toggle", "label": "Safeguarding Concerns? (Neglect, financial abuse)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Safeguarding concern = adult safeguarding referral.", "red_flag_negative": ""}
        ]},
        {"title": "Medication Review", "section_type": "assessment", "questions": [
            {"id": "dem_cholinesterase", "type": "text", "label": "Cholinesterase Inhibitor / Memantine", "required": False, "placeholder": "e.g., Donepezil 10mg OD"},
            {"id": "dem_med_effective", "type": "single_select", "label": "Medication Effective? (Slowing decline)", "required": False, "options": ["Yes - appears to help", "Uncertain", "No clear benefit", "Side effects problematic"]},
            {"id": "dem_med_side_effects", "type": "multi_select", "label": "Side Effects", "required": False, "options": ["Nausea/Diarrhoea", "Bradycardia/Syncope", "Agitation", "Sleep disturbance", "None"]},
            {"id": "dem_antipsychotics", "type": "toggle", "label": "On Antipsychotics? (Only for severe BPSD, short-term)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Antipsychotics in dementia = increased stroke/death risk. Review regularly, aim to deprescribe.", "red_flag_negative": ""},
            {"id": "dem_polypharmacy", "type": "toggle", "label": "Polypharmacy Review Needed? (≥10 medications)", "required": True}
        ]},
        {"title": "Advance Care Planning", "section_type": "plan", "safety_netting": "Dementia is progressive. Discuss future care preferences early while patient has capacity. Advance Care Plan: preferred place of care/death, ceilings of treatment, DNACPR if appropriate. Lasting Power of Attorney (LPA) for health and welfare. Consider referral to palliative care in advanced dementia. Return if: sudden deterioration (delirium - infection, medication, constipation), aggression, psychosis, carer crisis, or safeguarding concerns. Community support: Alzheimer's Society, Admiral Nurses, social services, day centres.", "questions": [
            {"id": "dem_acp", "type": "toggle", "label": "Advance Care Plan Discussed?", "required": True},
            {"id": "dem_dnacpr", "type": "toggle", "label": "DNACPR Discussion?", "required": False},
            {"id": "dem_lpa", "type": "toggle", "label": "LPA for Health & Welfare in Place?", "required": False},
            {"id": "dem_preferred_place", "type": "text", "label": "Preferred Place of Care / Death", "required": False, "placeholder": "e.g., Home with care package, nursing home"}
        ]},
        {"title": "Management & Referrals", "section_type": "plan", "questions": [
            {"id": "dem_plan", "type": "multi_select", "label": "Management", "required": True, "options": ["Continue cholinesterase inhibitor", "Adjust dementia medication", "Deprescribe antipsychotics", "Polypharmacy review", "Carer support + assessment", "Social services referral", "Community mental health team (CMHT)", "Admiral Nurse referral", "Palliative care referral", "DVLA advice documented", "Safeguarding referral"]},
            {"id": "dem_followup", "type": "text", "label": "Follow-up", "required": True, "placeholder": "e.g., Annual dementia review, 6-month medication review, carer assessment, CMHT follow-up"}
        ]}
    ]}, is_public=True, created_by=admin.id)
    db.add(t); db.commit(); print(f"✅ {title}"); db.close()

if __name__ == "__main__": seed_dementia_review()
from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_bipolar():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin:
        print("Admin not found.")
        db.close()
        return

    category = db.query(Category).filter(Category.name == "Mental Health").first()
    if not category:
        category = Category(name="Mental Health")
        db.add(category)
        db.commit()

    t = {
        "title": "Bipolar Disorder — Shared Care",
        "description": "Shared care assessment for bipolar disorder. Covers mood monitoring, medication review (lithium, valproate, antipsychotics), physical health monitoring, and red flags for relapse.",
        "category": "Mental Health",
        "content": {"sections": [
            {
                "title": "Mood Assessment",
                "section_type": "history",
                "questions": [
                    {"id": "bp_current_mood", "type": "single_select", "label": "Current Mood State", "required": True, "options": ["Euthymic (stable)", "Mildly elevated / hypomanic", "Depressed", "Mixed features", "Rapid cycling"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Current hypomania/mania or severe depression = urgent psychiatry review. Risk of relapse.", "red_flag_negative": "", "output_phrase": "Mood: {value}"},
                    {"id": "bp_sleep", "type": "single_select", "label": "Sleep Pattern", "required": True, "options": ["Normal — 7-8h", "Reduced need — <5h (hypomania sign)", "Insomnia — can't sleep", "Hypersomnia — sleeping too much", "Variable"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Reduced need for sleep (<5h) + increased energy = hypomania/mania. Urgent psychiatry review.", "red_flag_negative": "", "output_phrase": "Sleep: {value}"},
                    {"id": "bp_risk", "type": "single_select", "label": "Risk to Self / Others", "required": True, "options": ["None", "Passive thoughts", "Active ideation — with plan", "Recent attempt / violence"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Active suicidal ideation or violence risk = emergency. Urgent psychiatric assessment. Do not leave alone.", "red_flag_negative": "", "output_phrase": "Risk: {value}"}
                ]
            },
            {
                "title": "Medication Review",
                "section_type": "history",
                "questions": [
                    {"id": "bp_meds", "type": "text", "label": "Current Medications + Doses", "required": True, "placeholder": "e.g., Lithium 800mg nocte, Quetiapine 300mg", "output_phrase": "Medications: {value}"},
                    {"id": "bp_adherence", "type": "single_select", "label": "Medication Adherence", "required": True, "options": ["Excellent — never misses", "Good — rarely misses", "Fair — occasionally misses", "Poor — frequently misses", "Stopped medications"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Stopped or poor adherence = high risk of relapse. Psychiatry review. Discuss reasons.", "red_flag_negative": "", "output_phrase": "Adherence: {value}"},
                    {"id": "bp_side_effects", "type": "multi_select", "label": "Side Effects", "required": True, "options": ["Weight gain", "Tremor", "Sedation / drowsiness", "Polyuria / polydipsia (?lithium toxicity)", "Gastrointestinal", "Sexual dysfunction", "None"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Polyuria/tremor/sedation = ?lithium toxicity. Check lithium level, U&E, TFTs urgently.", "red_flag_negative": "", "output_phrase": "Side effects: {value}"}
                ]
            },
            {
                "title": "Physical Health Monitoring",
                "section_type": "history",
                "questions": [
                    {"id": "bp_lithium_level", "type": "text", "label": "Last Lithium Level + Date (if on lithium)", "required": False, "placeholder": "e.g., 0.7 mmol/L — 2 months ago", "is_red_flag": True, "red_flag_positive": "RED FLAG: Lithium >1.0 mmol/L = toxicity risk. No level in >6 months = check urgently.", "red_flag_negative": "", "output_phrase": "Lithium: {value}"},
                    {"id": "bp_bmi", "type": "number", "label": "BMI (monitor — antipsychotics cause weight gain)", "required": False, "placeholder": "e.g., 31", "output_phrase": "BMI: {value}"},
                    {"id": "bp_smoking", "type": "single_select", "label": "Smoking", "required": True, "options": ["Non-smoker", "Ex-smoker", "Current smoker"], "output_phrase": "Smoking: {value}"}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": ["Bipolar I — stable", "Bipolar I — relapsing (manic/depressed/mixed)", "Bipolar II — stable", "Bipolar II — relapsing", "Schizoaffective Disorder", "Substance-induced mood disorder", "Borderline Personality Disorder (mood instability vs episodes)"],
                "questions": [
                    {"id": "bp_diagnosis", "type": "single_select", "label": "Assessment", "required": True, "options": ["Bipolar — stable, continue shared care", "Bipolar — mild mood disturbance, review soon", "Bipolar — relapse suspected, urgent psychiatry", "?Lithium toxicity — urgent bloods + psychiatry", "Other"], "output_phrase": "Assessment: {value}"}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Stable: Continue mood stabiliser/antipsychotic. Never abruptly stop — risk of rebound mania. Annual physical health check: BMI, BP, FBC, U&E, LFT, TFTs, HbA1c, lipids. Lithium: 3-monthly levels (target 0.6-0.8), 6-monthly U&E/TFTs. Valproate: Do NOT prescribe to women of childbearing age unless Pregnancy Prevention Programme in place. Driving: Must notify DVLA if unstable. Advance statement / crisis plan. Relapse signs: reduced sleep, increased energy, spending, grandiosity, irritability. If pregnant or planning: Urgent psychiatry referral — high risk of postpartum relapse. Safety-net: Contact crisis team if mood escalating or suicidal.",
                "questions": [
                    {"id": "bp_action", "type": "single_select", "label": "Action", "required": True, "options": ["Continue shared care — routine monitoring", "Adjust medication + review in 2 weeks", "Urgent psychiatry referral (relapse)", "Emergency — crisis team / hospital", "Physical health check ordered"], "output_phrase": "Action: {value}"},
                    {"id": "bp_bloods", "type": "toggle", "label": "Bloods Ordered? (Lithium level, U&E, TFTs, annual screen)", "required": False, "output_phrase": "Bloods: {value}"},
                    {"id": "bp_crisis_plan", "type": "toggle", "label": "Crisis Plan Reviewed? (contact numbers, early warning signs)", "required": True, "output_phrase": "Crisis plan: {value}"},
                    {"id": "bp_followup", "type": "text", "label": "Follow-up", "required": True, "placeholder": "e.g., Review in 3 months. Lithium level + U&E in 1 week. Annual physical health check.", "output_phrase": "Follow-up: {value}"}
                ]
            }
        ]},
        "is_public": True
    }

    existing = db.query(Template).filter(Template.title == t["title"], Template.created_by == admin.id).first()
    if existing:
        existing.description = t["description"]
        existing.content = t["content"]
        existing.category = t["category"]
        existing.is_public = t["is_public"]
        existing.updated_at = datetime.now(timezone.utc)
        db.commit()
        print(f"🔄 Updated: {t['title']}")
    else:
        new_t = Template(title=t["title"], description=t["description"], category=t["category"], content=t["content"], is_public=True, created_by=admin.id, version=1)
        db.add(new_t)
        db.commit()
        print(f"✅ Template '{t['title']}' created!")
    db.close()

if __name__ == "__main__":
    seed_bipolar()
from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_raised_troponin():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin:
        print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Abnormal Labs/Investigations").first()
    if not category:
        category = Category(name="Abnormal Labs/Investigations"); db.add(category); db.commit()

    t = {
        "title": "Raised Troponin (Non-Acute Setting)",
        "description": "Assessment of raised troponin in non-acute/incidental settings. Covers causes beyond ACS and when to refer cardiology.",
        "category": "Abnormal Labs/Investigations",
        "content": {"sections": [
            {
                "title": "Context",
                "section_type": "history",
                "questions": [
                    {"id": "trop_level", "type": "text", "label": "Troponin Level + Assay Type", "required": True, "placeholder": "e.g., hs-TnI 45 ng/L", "output_phrase": "Troponin: {value}"},
                    {"id": "trop_context", "type": "single_select", "label": "Clinical Context", "required": True, "options": ["Incidental finding on routine bloods", "Post-exercise / unwell at time", "During acute illness / sepsis", "CKD patient — baseline elevated", "Post-tachyarrhythmia / AF", "Chronic finding — no acute event"], "output_phrase": "Context: {value}"}
                ]
            },
            {
                "title": "Causes Beyond ACS",
                "section_type": "history",
                "questions": [
                    {"id": "trop_cardiac", "type": "multi_select", "label": "Cardiac Causes", "required": True, "options": ["Heart failure (acute or chronic)", "Myocarditis / pericarditis", "Tachyarrhythmia (AF, SVT)", "Cardiomyopathy", "Cardiac surgery / PCI", "None"], "output_phrase": "Cardiac: {value}"},
                    {"id": "trop_non_cardiac", "type": "multi_select", "label": "Non-Cardiac Causes", "required": True, "options": ["Sepsis / severe infection", "PE", "CKD (chronic elevation)", "Stroke / SAH", "Strenuous exercise", "None"], "output_phrase": "Non-cardiac: {value}"}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": ["ACS / MI (if acute chest pain — 999)", "Chronic Troponin Elevation — CKD, chronic HF, cardiomyopathy", "Demand Ischaemia — sepsis, anaemia, tachyarrhythmia", "Myocarditis / Pericarditis", "PE", "Strenuous Exercise", "False Positive (assay)"],
                "questions": [
                    {"id": "trop_diagnosis", "type": "single_select", "label": "Clinical Impression", "required": True, "options": ["?ACS — urgent cardiology / 999 if acute", "?Chronic HF — echo + cardiology", "?CKD-related — baseline, monitor", "?Demand ischaemia — treat underlying cause", "Incidental — likely benign"], "output_phrase": "Diagnosis: {value}"}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "If no acute chest pain + low pre-test probability: Likely non-ACS cause. Check ECG, echo, renal function. If CKD: Troponin often chronically elevated — note as baseline. If heart failure suspected: BNP + echo. Refer cardiology if: unexplained elevation, abnormal ECG/echo, or clinical concern. Safety-net: Return immediately if chest pain, SOB, palpitations, or collapse.",
                "questions": [
                    {"id": "trop_action", "type": "single_select", "label": "Action", "required": True, "options": ["Refer cardiology (unexplained)", "Echo + ECG + investigate cause", "Treat underlying cause (sepsis, HF)", "Note as baseline (CKD) + monitor", "Reassure (likely benign)"], "output_phrase": "Action: {value}"},
                    {"id": "trop_safety_net", "type": "toggle", "label": "Safety-Net Given?", "required": True, "output_phrase": "Safety-net: {value}"},
                    {"id": "trop_followup", "type": "text", "label": "Follow-up", "required": True, "placeholder": "e.g., Cardiology referral. ECG + echo. GP review in 2 weeks.", "output_phrase": "Follow-up: {value}"}
                ]
            }
        ]},
        "is_public": True
    }

    existing = db.query(Template).filter(Template.title == t["title"], Template.created_by == admin.id).first()
    if existing:
        existing.description = t["description"]; existing.content = t["content"]; existing.category = t["category"]; existing.is_public = t["is_public"]; existing.updated_at = datetime.now(timezone.utc)
        db.commit(); print(f"Updated: {t['title']}")
    else:
        new_t = Template(title=t["title"], description=t["description"], category=t["category"], content=t["content"], is_public=True, created_by=admin.id, version=1)
        db.add(new_t); db.commit(); print(f"Created: {t['title']}")
    db.close()

if __name__ == "__main__":
    seed_raised_troponin()
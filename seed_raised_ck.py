from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_raised_ck():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin:
        print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Abnormal Labs/Investigations").first()
    if not category:
        category = Category(name="Abnormal Labs/Investigations"); db.add(category); db.commit()

    t = {
        "title": "Raised CK (Creatine Kinase)",
        "description": "Assessment of elevated creatine kinase. Covers statin-related myopathy, muscle injury, myositis, and rhabdomyolysis.",
        "category": "Abnormal Labs/Investigations",
        "content": {"sections": [
            {
                "title": "Confirm & Level",
                "section_type": "history",
                "questions": [
                    {"id": "ck_level", "type": "text", "label": "CK Level (U/L)", "required": True, "placeholder": "e.g., 800", "is_red_flag": True, "red_flag_positive": "RED FLAG: CK >5000 or >10x ULN = risk of rhabdomyolysis. Check renal function. Urgent medical assessment.", "red_flag_negative": "", "output_phrase": "CK: {value} U/L"},
                    {"id": "ck_exercise", "type": "toggle", "label": "Recent Heavy Exercise / Gym / Marathon? (common cause)", "required": True, "output_phrase": "Exercise: {value}"}
                ]
            },
            {
                "title": "Causes",
                "section_type": "history",
                "questions": [
                    {"id": "ck_statins", "type": "toggle", "label": "On Statins? (especially if muscle pain/tenderness)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Statin + muscle symptoms + CK >10x ULN = statin-induced myopathy. Stop statin. Check renal function.", "red_flag_negative": "", "output_phrase": "Statins: {value}"},
                    {"id": "ck_trauma", "type": "toggle", "label": "Recent Trauma / Fall / Surgery / IM Injection?", "required": True, "output_phrase": "Trauma: {value}"},
                    {"id": "ck_seizures", "type": "toggle", "label": "Recent Seizure / Convulsion?", "required": True, "output_phrase": "Seizure: {value}"},
                    {"id": "ck_myositis", "type": "toggle", "label": "Proximal Muscle Weakness? (difficulty standing from chair, climbing stairs)", "required": True, "output_phrase": "Weakness: {value}"}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": ["Statin-Induced Myopathy", "Strenuous Exercise", "Rhabdomyolysis (CK >5000, renal impairment)", "Polymyositis / Dermatomyositis", "Trauma / IM Injection", "Hypothyroidism", "Alcohol", "Neuroleptic Malignant Syndrome (antipsychotics + fever + rigidity)"],
                "questions": [
                    {"id": "ck_diagnosis", "type": "single_select", "label": "Clinical Impression", "required": True, "options": ["?Exercise — repeat after rest", "?Statin-related — stop statin + monitor", "?Myositis — refer rheumatology", "?Rhabdomyolysis — urgent admission", "Mild elevation — likely benign"], "output_phrase": "Diagnosis: {value}"}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "If CK >5000 or renal impairment: Urgent admission (rhabdomyolysis). If statin-related + symptoms: Stop statin. Repeat CK in 2-4 weeks. Consider alternative (Pravastatin or Ezetimibe). If mild elevation + well: Likely exercise/benign. Repeat after 1 week rest. If proximal weakness: Check TFTs, autoantibodies, refer rheumatology. Safety-net: Return if dark urine, muscle swelling, weakness, or reduced urine output.",
                "questions": [
                    {"id": "ck_action", "type": "single_select", "label": "Action", "required": True, "options": ["Stop statin + repeat CK", "Repeat after rest (exercise)", "Refer rheumatology (myositis)", "Urgent admission (rhabdomyolysis)", "Reassure + observe"], "output_phrase": "Action: {value}"},
                    {"id": "ck_safety_net", "type": "toggle", "label": "Safety-Net Given?", "required": True, "output_phrase": "Safety-net: {value}"},
                    {"id": "ck_followup", "type": "text", "label": "Follow-up", "required": True, "placeholder": "e.g., Repeat CK in 1 week. Stop statin. Switch to Pravastatin if needed.", "output_phrase": "Follow-up: {value}"}
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
    seed_raised_ck()
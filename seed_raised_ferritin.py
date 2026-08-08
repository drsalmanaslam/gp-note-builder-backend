from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_raised_ferritin():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin:
        print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Abnormal Labs/Investigations").first()
    if not category:
        category = Category(name="Abnormal Labs/Investigations"); db.add(category); db.commit()

    t = {
        "title": "Raised Ferritin",
        "description": "Assessment of elevated ferritin. Differentiates inflammation, liver disease, metabolic syndrome, iron overload, and malignancy.",
        "category": "Abnormal Labs/Investigations",
        "content": {"sections": [
            {
                "title": "Confirm & Context",
                "section_type": "history",
                "questions": [
                    {"id": "ferr_level", "type": "text", "label": "Ferritin Level (ug/L)", "required": True, "placeholder": "e.g., 800", "output_phrase": "Ferritin: {value} ug/L"},
                    {"id": "ferr_crp", "type": "text", "label": "CRP (if checked)", "required": False, "placeholder": "e.g., 45", "output_phrase": "CRP: {value}"},
                    {"id": "ferr_transferrin_sat", "type": "text", "label": "Transferrin Saturation (%)", "required": False, "placeholder": "e.g., 55", "is_red_flag": True, "red_flag_positive": "RED FLAG: Transferrin sat >45% + raised ferritin = ?haemochromatosis. Check HFE gene.", "red_flag_negative": "", "output_phrase": "Transferrin sat: {value}%"}
                ]
            },
            {
                "title": "Causes — Systematic Enquiry",
                "section_type": "history",
                "questions": [
                    {"id": "ferr_inflammation", "type": "toggle", "label": "Active Infection / Inflammation / Autoimmune Disease?", "required": True, "output_phrase": "Inflammation: {value}"},
                    {"id": "ferr_liver", "type": "toggle", "label": "Known Liver Disease / Raised LFTs / Alcohol Excess?", "required": True, "output_phrase": "Liver: {value}"},
                    {"id": "ferr_metabolic", "type": "multi_select", "label": "Metabolic Features", "required": False, "options": ["Obesity / overweight", "Type 2 diabetes / prediabetes", "Hypertension", "Dyslipidaemia", "None"], "output_phrase": "Metabolic: {value}"},
                    {"id": "ferr_iron_overload", "type": "multi_select", "label": "Iron Overload Risk", "required": False, "options": ["Family history haemochromatosis", "Multiple transfusions", "Excess iron supplements", "None"], "output_phrase": "Iron overload risk: {value}"}
                ]
            },
            {
                "title": "Red Flags — ?Malignancy",
                "section_type": "history",
                "questions": [
                    {"id": "ferr_weight_loss", "type": "toggle", "label": "Unintentional Weight Loss / Night Sweats / Fatigue?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Constitutional symptoms + raised ferritin = ?malignancy. Urgent workup.", "red_flag_negative": "", "output_phrase": "Red flags: {value}"}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": ["Inflammation / Infection (acute phase reactant)", "Metabolic Syndrome / MASLD", "Alcohol / Liver Disease", "Hereditary Haemochromatosis (HFE gene)", "Iron Overload (transfusions, supplements)", "Malignancy", "Still's Disease / HLH (rare)"],
                "questions": [
                    {"id": "ferr_diagnosis", "type": "single_select", "label": "Clinical Impression", "required": True, "options": ["?Inflammatory — treat underlying cause + repeat", "?Metabolic — lifestyle + repeat LFTs", "?Haemochromatosis — HFE gene test", "?Malignancy — urgent workup", "Isolated — observe + repeat"], "output_phrase": "Diagnosis: {value}"}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "If CRP raised + ferritin raised: Likely reactive. Treat underlying cause. Repeat when well. If transferrin sat >45%: HFE gene test for haemochromatosis. If metabolic features: Lifestyle, weight loss, LFTs, repeat. If isolated mild elevation + well: Reassure, repeat in 3 months. Safety-net: Return if weight loss, night sweats, or new symptoms.",
                "questions": [
                    {"id": "ferr_action", "type": "single_select", "label": "Action", "required": True, "options": ["Repeat when well (likely reactive)", "HFE gene test (suspected haemochromatosis)", "Lifestyle + repeat LFTs (metabolic)", "Urgent 2-week wait (malignancy suspected)", "Reassure + repeat in 3 months"], "output_phrase": "Action: {value}"},
                    {"id": "ferr_safety_net", "type": "toggle", "label": "Safety-Net Given?", "required": True, "output_phrase": "Safety-net: {value}"},
                    {"id": "ferr_followup", "type": "text", "label": "Follow-up", "required": True, "placeholder": "e.g., Repeat ferritin + CRP in 3 months. HFE gene test if indicated.", "output_phrase": "Follow-up: {value}"}
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
    seed_raised_ferritin()
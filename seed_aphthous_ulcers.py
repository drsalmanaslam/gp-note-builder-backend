from app.database import SessionLocal
from app.models import User, Template, Category

def seed_aphthous_ulcers():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "ENT").first()
    if not category: category = Category(name="ENT"); db.add(category); db.commit()

    t = {
        "title": "Aphthous Mouth Ulcers",
        "description": "Focused assessment for aphthous ulcers covering Behçet's/Crohn's/HSV differential, topical steroid prescribing, and red flags for systemic disease.",
        "category": "ENT",
        "content": {"sections": [
            {
                "title": "Things NOT to Miss (Differential Screen)",
                "section_type": "history",
                "questions": [
                    {"id": "au_genital_anal", "type": "toggle", "label": "Genital or Anal Ulcers? (Behçet's / Crohn's)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Oral + genital ulcers = ?Behçet's disease, Crohn's. Urgent rheumatology/gastroenterology referral.", "red_flag_negative": ""},
                    {"id": "au_tingling", "type": "toggle", "label": "Tingling Before Ulcer or Blistering? (Herpes Simplex)", "required": True},
                    {"id": "au_hand_foot_spots", "type": "toggle", "label": "Spots on Hands/Feet? (Hand, Foot & Mouth Disease)", "required": True},
                    {"id": "au_eye_pain", "type": "toggle", "label": "Eye Pain? (Uveitis - Associated with Behçet's)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Oral ulcers + eye pain = ?Behçet's with uveitis. Urgent ophthalmology + rheumatology.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "History",
                "section_type": "history",
                "questions": [
                    {"id": "au_presenting_complaint", "type": "text", "label": "Presenting Complaint", "required": True, "placeholder": "e.g., Painful mouth ulcers for 5 days"},
                    {"id": "au_trauma", "type": "toggle", "label": "Preceding Trauma to the Area?", "required": False},
                    {"id": "au_pain", "type": "toggle", "label": "Pain?", "required": True},
                    {"id": "au_bleeding", "type": "toggle", "label": "Bleeding?", "required": False},
                    {"id": "au_gi_symptoms", "type": "multi_select", "label": "GI Symptoms", "required": True, "options": ["Blood or mucus in stool", "Weight loss", "None"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Blood/mucus + weight loss + oral ulcers = ?Crohn's. Urgent gastroenterology.", "red_flag_negative": ""},
                    {"id": "au_coeliac_screen", "type": "multi_select", "label": "Coeliac Screen", "required": False, "options": ["Pale stools, difficult to flush", "Related to eating rye/wheat/barley", "None"]},
                    {"id": "au_rash", "type": "toggle", "label": "Rash?", "required": False},
                    {"id": "au_systemic", "type": "multi_select", "label": "Systemic Symptoms", "required": False, "options": ["Fever", "Flu-like illness", "None"]},
                    {"id": "au_muscle_joint_pain", "type": "toggle", "label": "Muscle or Joint Pain?", "required": False}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "au_size", "type": "single_select", "label": "Ulcer Size", "required": True, "options": ["<10mm (Minor Aphthous)", "≥10mm (Major Aphthous)"]},
                    {"id": "au_appearance", "type": "text", "label": "Colour & Margins", "required": False, "placeholder": "e.g., Yellow-grey base, regular margins"},
                    {"id": "au_bleeding_exam", "type": "toggle", "label": "Bleeding on Examination?", "required": False},
                    {"id": "au_lymph", "type": "toggle", "label": "Localised Lymphadenopathy?", "required": False}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "Minor Aphthous Ulcer (<10mm, heal without scarring)",
                    "Major Aphthous Ulcer (≥10mm, may scar)",
                    "Herpes Simplex Virus (HSV) - preceding tingling, blistering",
                    "Behçet's Disease (oral + genital ulcers + uveitis)",
                    "Crohn's Disease (oral ulcers + GI symptoms)",
                    "Hand, Foot & Mouth Disease (Coxsackie - spots on hands/feet)",
                    "Coeliac Disease (pale stools, weight loss)",
                    "Erythema Multiforme",
                    "Oral Lichen Planus",
                    "Squamous Cell Carcinoma (non-healing, indurated - RED FLAG)"
                ],
                "questions": [
                    {"id": "au_diagnosis", "type": "single_select", "label": "Clinical Impression", "required": True, "options": ["Minor Aphthous Ulcer", "Major Aphthous Ulcer", "Suspected HSV", "Suspected Behçet's - URGENT REFERRAL", "Suspected Crohn's - URGENT REFERRAL", "Recurrent Aphthous Stomatitis"]}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Return if: ulcer persists >3 weeks without healing, becomes larger/indurated, new genital/anal ulcers develop, eye pain/visual symptoms, or GI symptoms (blood/mucus, weight loss). Minor aphthous ulcers heal within 10-14 days without scarring. Avoid spicy food. Use Sensodyne toothpaste (SLS-free may help). First-line topical: Orabase, Difflam spray, or Difflam rinse. If not settling: Prednisolone 5mg soluble tablet dissolved in small amount of water, applied topically or used as mouth rinse (half an eggcupful), OR Betamethasone 0.5mg mouth rinse (unlicensed). If recurrent/non-healing/red flags: FBC, haematinics (Ferritin, B12, Folate), ESR, CRP, coeliac screen (IgA TTG).",
                "questions": [
                    {"id": "au_topical", "type": "multi_select", "label": "Topical Symptom Relief", "required": False, "options": ["Orabase", "Difflam Spray", "Difflam Rinse", "None"]},
                    {"id": "au_steroid", "type": "single_select", "label": "Topical Steroid (If Not Settling)", "required": False, "options": ["Prednisolone 5mg Soluble Tablet - Dissolve in Water, Apply Topically or Mouth Rinse", "Betamethasone 0.5mg Mouth Rinse (Unlicensed)", "Not indicated"]},
                    {"id": "au_advice", "type": "multi_select", "label": "General Advice", "required": False, "options": ["Avoid spicy food", "Use Sensodyne / SLS-free toothpaste"]},
                    {"id": "au_investigations", "type": "multi_select", "label": "Investigations (If Recurrent / Non-Healing / Red Flags)", "required": False, "options": ["FBC", "Haematinics (Ferritin, B12, Folate)", "ESR / CRP", "Coeliac Screen (IgA TTG)", "None"]},
                    {"id": "au_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., Return if not healed in 2-3 weeks, sooner if red flags"}
                ]
            }
        ]},
        "is_public": True
    }

    existing = db.query(Template).filter(Template.title == t["title"], Template.created_by == admin.id).first()
    if existing: db.delete(existing); db.commit()
    new_t = Template(title=t["title"], description=t["description"], category=t["category"], content=t["content"], is_public=True, created_by=admin.id, version=1)
    db.add(new_t); db.commit()
    print(f"Template '{t['title']}' created with {len(t['content']['sections'])} sections!"); db.close()

if __name__ == "__main__":
    seed_aphthous_ulcers()
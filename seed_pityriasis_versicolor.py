from app.database import SessionLocal
from app.models import User, Template, Category

def seed_pityriasis_versicolor():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Dermatology").first()
    if not category: category = Category(name="Dermatology"); db.add(category); db.commit()

    t = {
        "title": "Pityriasis Versicolor Assessment",
        "description": "Focused assessment for pityriasis versicolor with topical and systemic treatment options and differentiation from other hypopigmented rashes.",
        "category": "Dermatology",
        "content": {"sections": [
            {
                "title": "Presentation",
                "section_type": "history",
                "questions": [
                    {"id": "pv_presenting_complaint", "type": "text", "label": "Presenting Complaint", "required": True, "placeholder": "e.g., Pale patches on back and chest, more noticeable after sun exposure"},
                    {"id": "pv_age", "type": "number", "label": "Age", "required": True, "placeholder": "e.g., 24"},
                    {"id": "pv_duration", "type": "text", "label": "Duration", "required": True, "placeholder": "e.g., 2 months"},
                    {"id": "pv_sites", "type": "multi_select", "label": "Affected Areas", "required": True, "options": ["Back", "Chest", "Neck", "Upper arms", "Abdomen", "Face", "Other"]},
                    {"id": "pv_appearance", "type": "single_select", "label": "Lesion Appearance", "required": True, "options": ["Hypopigmented (pale/lighter)", "Hyperpigmented (darker)", "Mixed hypo/hyperpigmented", "Pink/brown macules"]},
                    {"id": "pv_sun_noticeable", "type": "toggle", "label": "More Noticeable After Sun Exposure?", "required": True},
                    {"id": "pv_pruritus", "type": "single_select", "label": "Itching", "required": False, "options": ["None", "Mild", "Moderate", "Severe"]},
                    {"id": "pv_previous_episodes", "type": "toggle", "label": "Previous Episodes?", "required": False}
                ]
            },
            {
                "title": "RED FLAGS & Differentials",
                "section_type": "history",
                "questions": [
                    {"id": "pv_fever", "type": "toggle", "label": "Fever / Systemic Symptoms?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Systemic symptoms = ?disseminated infection in immunocompromised. Urgent assessment.", "red_flag_negative": ""},
                    {"id": "pv_immunosuppression", "type": "toggle", "label": "Known Immunosuppression? (HIV, transplant, chemotherapy)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Immunosuppressed + widespread rash = ?disseminated fungal infection. Urgent dermatology.", "red_flag_negative": ""},
                    {"id": "pv_mucosal", "type": "toggle", "label": "Mucosal Involvement? (Mouth, genitals)", "required": False},
                    {"id": "pv_plaque", "type": "toggle", "label": "Raised Plaques / Induration?", "required": False},
                    {"id": "pv_border", "type": "toggle", "label": "Raised Border / Central Clearing? (Tinea)", "required": False},
                    {"id": "pv_scale", "type": "single_select", "label": "Scaling", "required": True, "options": ["Fine scale (PV typical)", "Thick/silvery scale (Psoriasis)", "No scale", "Not assessed"]}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "pv_distribution", "type": "single_select", "label": "Distribution", "required": True, "options": ["Upper trunk (back + chest)", "Back only", "Chest only", "Widespread", "Face predominant"]},
                    {"id": "pv_morphology", "type": "multi_select", "label": "Morphology", "required": True, "options": ["Macules (flat)", "Patches", "Fine scale on scraping", "Well-demarcated borders", "Coalescing patches"]},
                    {"id": "pv_hypopigmented", "type": "toggle", "label": "Hypopigmented (Pale) Areas?", "required": True},
                    {"id": "pv_hyperpigmented", "type": "toggle", "label": "Hyperpigmented (Dark) Areas?", "required": False},
                    {"id": "pv_cellulitis", "type": "toggle", "label": "Signs of Cellulitis / Secondary Infection?", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Secondary bacterial infection = antibiotics + reassess.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "Pityriasis Versicolor (Malassezia furfur)",
                    "Tinea Corporis (Ringworm - raised border, central clearing)",
                    "Vitiligo (complete depigmentation, no scale)",
                    "Post-Inflammatory Hypopigmentation",
                    "Pityriasis Alba (face, children)",
                    "Seborrhoeic Dermatitis",
                    "Guttate Psoriasis",
                    "Tinea Versicolor (same condition, alternative name)"
                ],
                "questions": [
                    {"id": "pv_diagnosis", "type": "single_select", "label": "Working Diagnosis", "required": True, "options": ["Pityriasis Versicolor - typical", "Pityriasis Versicolor - widespread", "Suspected Tinea", "Suspected Vitiligo", "Uncertain - skin scraping needed"]}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Return if: rash spreads rapidly, becomes painful/inflamed/cellulitic, fails to respond to treatment after 4 weeks, or new systemic symptoms develop. Pigment changes (pale spots) persist for weeks/months after successful treatment - this is NORMAL and does not mean active infection. Sun exposure helps pigment return to normal. Relapse is common (50% within 1 year). For recurrence: resume ketoconazole shampoo twice weekly as prophylaxis. If frequent relapses or widespread resistant disease: consider oral itraconazole. Advise loose cotton clothing, avoid excessive sweating.",
                "questions": [
                    {"id": "pv_plan", "type": "single_select", "label": "Treatment", "required": True, "options": ["Topical ketoconazole shampoo (first-line)", "Topical selenium sulphide", "Oral itraconazole (widespread/resistant)", "Combination topical + reassurance", "Observation only (mild)"]},
                    {"id": "pv_ketoconazole", "type": "toggle", "label": "Ketoconazole Shampoo Prescribed? (Apply dry daily, leave 10-20 min, rinse)", "required": False},
                    {"id": "pv_prophylaxis", "type": "toggle", "label": "Relapse Prophylaxis Discussed? (Twice weekly shampoo)", "required": False},
                    {"id": "pv_itraconazole", "type": "toggle", "label": "Oral Itraconazole 200mg OD for 2 Weeks?", "required": False},
                    {"id": "pv_scraping", "type": "toggle", "label": "Skin Scraping for Mycology?", "required": False},
                    {"id": "pv_pigment_advice", "type": "toggle", "label": "Pigment Changes Explained? (Pale spots persist post-treatment - normal)", "required": True},
                    {"id": "pv_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., 4-6 weeks if not improved, or PRN"}
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
    seed_pityriasis_versicolor()
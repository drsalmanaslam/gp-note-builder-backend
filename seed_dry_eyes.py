from app.database import SessionLocal
from app.models import User, Template, Category

def seed_dry_eyes():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Ophthalmology").first()
    if not category: category = Category(name="Ophthalmology"); db.add(category); db.commit()

    t = {
        "title": "Dry Eyes",
        "description": "Focused assessment for dry eye syndrome covering environmental modifications, lubricant options, preservative-free indications, and red flags.",
        "category": "Ophthalmology",
        "content": {"sections": [
            {
                "title": "Presentation",
                "section_type": "history",
                "questions": [
                    {"id": "de_presenting_complaint", "type": "text", "label": "Presenting Complaint", "required": True, "placeholder": "e.g., Dry, gritty eyes for 3-4 months, worse with screen use"},
                    {"id": "de_age", "type": "number", "label": "Age", "required": True, "placeholder": "e.g., 52"},
                    {"id": "de_duration", "type": "text", "label": "Duration", "required": True, "placeholder": "e.g., 3-4 months"},
                    {"id": "de_side", "type": "single_select", "label": "Affected Eye(s)", "required": True, "options": ["Bilateral", "Right only", "Left only"]},
                    {"id": "de_symptoms", "type": "multi_select", "label": "Symptoms", "required": True, "options": ["Dryness", "Grittiness / foreign body sensation", "Burning", "Itching", "Intermittent blurring (blink clears)", "Watery eyes (reflex tearing)", "Tired eyes", "Stringy mucus"]},
                    {"id": "de_triggers", "type": "multi_select", "label": "Exacerbating Factors", "required": True, "options": ["Prolonged screen time", "Car heating/airflow", "Air conditioning", "Wind", "Contact lens wear", "Reading", "Driving at night", "None identified"]}
                ]
            },
            {
                "title": "RED FLAGS & Systemic",
                "section_type": "history",
                "questions": [
                    {"id": "de_eye_pain", "type": "toggle", "label": "Severe Eye Pain?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Severe pain = ?keratitis, corneal abrasion. Urgent ophthalmology.", "red_flag_negative": ""},
                    {"id": "de_photophobia", "type": "toggle", "label": "Photophobia?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Photophobia = ?keratitis, uveitis. Urgent ophthalmology.", "red_flag_negative": ""},
                    {"id": "de_discharge", "type": "toggle", "label": "Discharge? (Purulent/mucoid)", "required": True},
                    {"id": "de_visual_loss", "type": "toggle", "label": "Loss of Vision / Persistent Blurring?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Visual loss = urgent ophthalmology assessment.", "red_flag_negative": ""},
                    {"id": "de_dry_mouth", "type": "toggle", "label": "Severe Dry Mouth? (Sjögren's syndrome)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Dry eyes + dry mouth + arthralgia = ?Sjögren's. Check autoantibodies (ANA, Anti-Ro/La).", "red_flag_negative": ""},
                    {"id": "de_arthralgia", "type": "toggle", "label": "Joint Pains / Swelling? (Connective tissue disease)", "required": False},
                    {"id": "de_ra_sle", "type": "toggle", "label": "Known Rheumatoid Arthritis / SLE?", "required": False},
                    {"id": "de_rosacea", "type": "toggle", "label": "Rosacea? (Associated MGD)", "required": False},
                    {"id": "de_meds", "type": "multi_select", "label": "Medications That Cause Dry Eyes", "required": False, "options": ["Antihistamines", "Diuretics", "Beta-blockers", "Antidepressants (SSRIs/TCAs)", "Isotretinoin", "HRT", "None"]}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "de_va_right", "type": "text", "label": "Visual Acuity - Right", "required": True, "placeholder": "e.g., 6/9"},
                    {"id": "de_va_left", "type": "text", "label": "Visual Acuity - Left", "required": True, "placeholder": "e.g., 6/9"},
                    {"id": "de_conjunctiva", "type": "single_select", "label": "Conjunctiva", "required": True, "options": ["Normal - no injection", "Mild injection", "Significant injection"]},
                    {"id": "de_cornea", "type": "single_select", "label": "Cornea", "required": True, "options": ["Clear", "Punctate staining on fluorescein", "Corneal opacity - RED FLAG", "Not assessed"]},
                    {"id": "de_fluorescein", "type": "single_select", "label": "Fluorescein Staining", "required": False, "options": ["Negative (no uptake)", "Punctate erosions", "Not performed"]},
                    {"id": "de_lid_margins", "type": "single_select", "label": "Lid Margins / MGD", "required": False, "options": ["Normal", "MGD present (plugs/erythema)", "Blepharitis features", "Not assessed"]},
                    {"id": "de_fundoscopy", "type": "single_select", "label": "Fundoscopy", "required": False, "options": ["Normal", "Abnormal", "Not performed"]}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "Dry Eye Syndrome / Keratoconjunctivitis Sicca",
                    "Evaporative Dry Eye (Meibomian Gland Dysfunction)",
                    "Aqueous Tear Deficiency",
                    "Sjögren's Syndrome (Primary / Secondary)",
                    "Blepharitis / MGD",
                    "Allergic Conjunctivitis",
                    "Medication-Induced Dry Eye",
                    "Contact Lens-Associated Dryness",
                    "Vitamin A Deficiency (rare)",
                    "Corneal Abrasion / Keratitis"
                ],
                "questions": [
                    {"id": "de_diagnosis", "type": "single_select", "label": "Working Diagnosis", "required": True, "options": ["Dry eye syndrome - evaporative (MGD)", "Dry eye syndrome - aqueous deficiency", "Mixed dry eye", "Dry eye + blepharitis", "Suspected Sjögren's", "Medication-induced"]}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Return if: severe eye pain, photophobia, persistent loss of vision, or symptoms worsen despite regular lubrication. Screen breaks: 20-20-20 rule (every 20 minutes, look 20 feet away for 20 seconds). Conscious blinking during prolonged screen use. Direct car heating/airflow vents away from face. Humidifier in home/office if air is dry. If using drops >4 times daily: switch to preservative-free (BAK toxicity risk). If MGD co-exists: add warm compresses + lid hygiene. If refractory despite compliance: refer ophthalmology for consideration of punctal plugs, cyclosporine (Ikervis), or autologous serum drops.",
                "questions": [
                    {"id": "de_environmental", "type": "toggle", "label": "Environmental Modifications Advised? (Screen breaks, redirect vents, humidifier)", "required": True},
                    {"id": "de_daytime_drops", "type": "single_select", "label": "Daytime Lubricant Drops", "required": False, "options": ["None", "Thealoz Duo (preservative-free, GMS)", "Artelac SDU (preservative-free)", "Hyloforte", "Hyabak / Hylo-Dual", "Tears Naturale / Liquifilm", "Other"]},
                    {"id": "de_gel", "type": "toggle", "label": "Viscous Gel? (Geltears / Vidisic gel)", "required": False},
                    {"id": "de_night_ointment", "type": "single_select", "label": "Nighttime Ointment", "required": False, "options": ["None", "VitA-Pos (Hylo-Night) nocte", "Lacri-Lube nocte", "Vidisic gel nocte"]},
                    {"id": "de_preservative_free", "type": "toggle", "label": "Preservative-Free Advised? (If >4 applications/day)", "required": False},
                    {"id": "de_mgd", "type": "toggle", "label": "Warm Compresses + Lid Hygiene? (If MGD present)", "required": False},
                    {"id": "de_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., 4-6 weeks if not improving, sooner if red flags"}
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
    seed_dry_eyes()
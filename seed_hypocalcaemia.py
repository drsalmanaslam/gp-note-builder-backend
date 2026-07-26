from app.database import SessionLocal
from app.models import User, Template, Category

def seed_hypocalcaemia():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Abnormal Labs/Investigations").first()
    if not category: category = Category(name="Abnormal Labs/Investigations"); db.add(category); db.commit()

    t = {
        "title": "Low Calcium / Hypocalcaemia Assessment",
        "description": "Comprehensive hypocalcaemia assessment covering emergency threshold (<1.9mmol/L), Trousseau's/Chvostek's signs, PTH interpretation, and vitamin D/magnesium correction pathways.",
        "category": "Abnormal Labs/Investigations",
        "content": {"sections": [
            {
                "title": "RED FLAG - Emergency Threshold",
                "section_type": "history",
                "questions": [
                    {"id": "hypoca_corrected_ca", "type": "number", "label": "Corrected Calcium (mmol/L) - NR: 2.2-2.6", "required": True, "placeholder": "e.g., 1.85 (If <1.9 = A&E IMMEDIATELY)", "is_red_flag": True, "red_flag_positive": "RED FLAG: Corrected Calcium <1.9mmol/L = REFER TO A&E IMMEDIATELY. Do NOT manage in primary care.", "red_flag_negative": ""},
                    {"id": "hypoca_albumin", "type": "number", "label": "Albumin (g/L) - For Correction Calculation", "required": False, "placeholder": "e.g., 32 (Use MDCalc Calcium Correction)"}
                ]
            },
            {
                "title": "History",
                "section_type": "history",
                "questions": [
                    {"id": "hypoca_paraesthesia", "type": "toggle", "label": "Paraesthesia of Fingertips, Toes, or Perioral Region?", "required": True},
                    {"id": "hypoca_muscle_cramps", "type": "toggle", "label": "Muscle Cramps?", "required": True},
                    {"id": "hypoca_epigastric_pain", "type": "toggle", "label": "Epigastric Pain? (?Pancreatitis)", "required": False}
                ]
            },
            {
                "title": "Examination (If Symptomatic or Borderline)",
                "section_type": "examination",
                "questions": [
                    {"id": "hypoca_trousseau", "type": "single_select", "label": "Trousseau's Sign (Inflate BP Cuff >Systolic for 3 Min → Carpal Spasm?)", "required": False, "options": ["Positive - Carpal Spasm Present", "Negative", "Not performed"]},
                    {"id": "hypoca_chvostek", "type": "single_select", "label": "Chvostek's Sign (Tap Facial Nerve → Contraction Corner Mouth/Nose/Eye?)", "required": False, "options": ["Positive", "Negative", "Not performed"]}
                ]
            },
            {
                "title": "Investigations",
                "section_type": "assessment",
                "questions": [
                    {"id": "hypoca_renal_mg", "type": "toggle", "label": "Renal Profile + Magnesium Ordered? (Low Mg = PTH Resistance - Must Correct First)", "required": False},
                    {"id": "hypoca_lfts_alp", "type": "toggle", "label": "LFTs Ordered? (Raised ALP = ?Malignancy)", "required": False},
                    {"id": "hypoca_pth", "type": "number", "label": "PTH Level", "required": False, "placeholder": "e.g., 3.5 (Mid-low normal may still be inappropriate/blunted response)"},
                    {"id": "hypoca_pth_interpretation", "type": "single_select", "label": "PTH Interpretation", "required": False, "options": ["Appropriately Elevated (Secondary Hyperparathyroidism - Vit D Deficiency)", "Low / Inappropriately Normal (Hypoparathyroidism)", "Awaiting Result"]},
                    {"id": "hypoca_vit_d", "type": "number", "label": "Vitamin D (nmol/L) - Target >50", "required": False, "placeholder": "e.g., 18 (<25 = Severe Deficiency)"},
                    {"id": "hypoca_phosphate", "type": "number", "label": "Phosphate", "required": False, "placeholder": "e.g., 1.8 (High PO4 + Normal Renal Function = ?Hypoparathyroidism)"},
                    {"id": "hypoca_urine_ca_cr", "type": "toggle", "label": "Urine Calcium:Creatinine Ratio Ordered?", "required": False},
                    {"id": "hypoca_ecg", "type": "toggle", "label": "ECG Ordered? (QT Prolongation Risk)", "required": False}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "Vitamin D Deficiency (Most Common - PTH Appropriately Elevated)",
                    "Hypoparathyroidism (Low/Inappropriately Normal PTH, High PO4)",
                    "Pseudohypoparathyroidism (PTH Resistance - High PTH, High PO4)",
                    "Hypomagnesaemia (PTH Resistance - PPI/Diuretic Related)",
                    "Malignancy (Raised ALP, Bone Metastases)",
                    "Pancreatitis (Epigastric Pain, Raised Amylase)",
                    "Hypoalbuminaemia (Low Albumin - Corrected Ca May Be Normal)",
                    "Rhabdomyolysis (Raised CK)"
                ],
                "questions": [
                    {"id": "hypoca_diagnosis", "type": "single_select", "label": "Clinical Impression", "required": True, "options": ["Vitamin D Deficiency - Symptomatic", "Vitamin D Deficiency - Asymptomatic", "Suspected Hypoparathyroidism", "Suspected Hypomagnesaemia", "RED FLAG: Ca <1.9 - REFER A&E"]}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "If corrected calcium <1.9mmol/L: REFER TO A&E IMMEDIATELY. Do NOT manage in primary care. If low magnesium identified: correct magnesium FIRST - calcium will not normalise until magnesium is corrected. Consider PPI or diuretic use as contributing cause. If low vitamin D (<25 nmol/L): treat vitamin D deficiency, recheck calcium after 1 month. High phosphate with normal renal function = consider hypoparathyroidism or pseudohypoparathyroidism. Raised ALP = consider underlying malignancy. PTH should rise promptly in response to low calcium - a mid-to-low normal PTH may represent inappropriate (blunted) response and still be significant.",
                "questions": [
                    {"id": "hypoca_vit_d_rx", "type": "single_select", "label": "Vitamin D Replacement (If <25 nmol/L)", "required": False, "options": ["Altavita 25,000 IU Capsules: 50,000 IU/Week (2 Caps) x6-8 Weeks → 2 Caps/Month Maintenance", "Thorens 25,000 IU: 2 Bottles/Week x4 Weeks → 1 Bottle/Month Maintenance", "Desunin Tablets: 4,000 IU OD x10 Weeks → 800 IU OD Maintenance", "Dnord 255mcg Capsule: Once Monthly", "Not indicated"]},
                    {"id": "hypoca_mg_correction", "type": "toggle", "label": "Magnesium Correction Required? (Correct Before Calcium Will Normalise)", "required": False},
                    {"id": "hypoca_ppi_diuretic_review", "type": "toggle", "label": "PPI / Diuretic Use Reviewed? (Mg Depletion Causes)", "required": False},
                    {"id": "hypoca_referral", "type": "single_select", "label": "Referral", "required": False, "options": ["None - GP Managed", "Endocrinology (?Hypoparathyroidism)", "A&E (Ca <1.9)", "Gastroenterology (?Malignancy)"]},
                    {"id": "hypoca_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., Recheck Ca + Vit D after 1 month, endo referral if hypoparathyroidism"}
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
    seed_hypocalcaemia()
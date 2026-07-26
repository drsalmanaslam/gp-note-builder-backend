from app.database import SessionLocal
from app.models import User, Template, Category

def seed_raised_transferrin_sat():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Abnormal Labs/Investigations").first()
    if not category: category = Category(name="Abnormal Labs/Investigations"); db.add(category); db.commit()

    t = {
        "title": "Raised Fasting Transferrin Saturation (>45%) Assessment",
        "description": "Focused assessment for elevated transferrin saturation covering hereditary haemochromatosis HFE genetic testing, venesection triggers, and gastroenterology referral.",
        "category": "Abnormal Labs/Investigations",
        "content": {"sections": [
            {
                "title": "Results & History",
                "section_type": "history",
                "questions": [
                    {"id": "tsat_level", "type": "number", "label": "Fasting Transferrin Saturation (%)", "required": True, "placeholder": "e.g., 55 (>45% = Strongly Suggestive of HH)", "is_red_flag": True, "red_flag_positive": "RED FLAG: Transferrin saturation >45% = strongly suggestive of hereditary haemochromatosis. Proceed to HFE genetic testing.", "red_flag_negative": ""},
                    {"id": "tsat_fasting_confirmed", "type": "toggle", "label": "Fasting Sample Confirmed? (Non-Fasting Results Are Unreliable)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Non-fasting transferrin saturation is unreliable. Repeat as fasting sample if not confirmed.", "red_flag_negative": ""},
                    {"id": "tsat_ferritin", "type": "number", "label": "Ferritin Level (µg/L) - Guides Treatment Decision", "required": False, "placeholder": "e.g., 450 (Treatment guided by ferritin, not TSAT alone)"},
                    {"id": "tsat_family_hh", "type": "toggle", "label": "Family History of Haemochromatosis?", "required": True}
                ]
            },
            {
                "title": "HFE Genetic Testing",
                "section_type": "assessment",
                "questions": [
                    {"id": "tsat_hfe_ordered", "type": "toggle", "label": "HFE Genetic Test Ordered? (C282Y + H63D Mutations - 2 EDTA Bottles + Biochemistry Form + Signed Consent)", "required": True},
                    {"id": "tsat_hfe_result", "type": "single_select", "label": "HFE Genetic Result", "required": False, "options": ["C282Y Homozygous (Classic HH)", "C282Y/H63D Compound Heterozygous", "H63D Homozygous", "H63D Heterozygous Only", "No Mutations Detected", "Awaiting Result"]}
                ]
            },
            {
                "title": "Treatment Trigger",
                "section_type": "assessment",
                "questions": [
                    {"id": "tsat_venesection_indicated", "type": "toggle", "label": "Venesection Indicated? (Compound Heterozygous + High Ferritin + TSAT ≥49% → Aim Ferritin <50)", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Meets venesection criteria = refer gastroenterology for venesection. Target ferritin <50.", "red_flag_negative": ""},
                    {"id": "tsat_iron_safe", "type": "toggle", "label": "Iron Supplementation Safe if Indicated? (Compound Heterozygous Alone = NOT a Contraindication to Iron)", "required": False}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "Hereditary Haemochromatosis (HFE-Related - C282Y/C282Y or C282Y/H63D)",
                    "Non-HFE Haemochromatosis (Rare - HJV, HAMP, TFR2 Mutations)",
                    "Secondary Iron Overload (Multiple Transfusions, Chronic Liver Disease)",
                    "Alcohol-Related Liver Disease (Raised TSAT + Ferritin)",
                    "Metabolic Syndrome (Mildly Raised Ferritin, Normal TSAT)",
                    "Acute Phase Response (Raised Ferritin, Normal TSAT - Infection/Inflammation)"
                ],
                "questions": [
                    {"id": "tsat_diagnosis", "type": "single_select", "label": "Clinical Impression", "required": True, "options": ["?Hereditary Haemochromatosis - Awaiting HFE", "HH Confirmed - Venesection Indicated", "HH Confirmed - No Treatment Required (Ferritin Normal)", "Secondary Iron Overload", "Not HH (No HFE Mutation)"]}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Transferrin saturation >45% is strongly suggestive of HH but does NOT by itself indicate need for treatment - treatment is guided by ferritin level. HFE genetic test: 2 EDTA bottles sent with biochemistry form and signed consent form. Regional forms: CUH (Cork) or St James's (Dublin). Venesection indicated if: compound heterozygous for HH + high ferritin + TSAT ≥49% → aim for ferritin <50. Being compound heterozygous for HH is NOT a contraindication to iron - this genetic status alone does not preclude iron-containing treatment if otherwise indicated. Refer to Gastroenterology for venesection management. First-degree relatives should be screened.",
                "questions": [
                    {"id": "tsat_venesection", "type": "toggle", "label": "Venesection Arranged? (Refer Gastroenterology - Aim Ferritin <50)", "required": False},
                    {"id": "tsat_family_screening", "type": "toggle", "label": "First-Degree Relatives Advised to be Screened?", "required": False},
                    {"id": "tsat_referral", "type": "single_select", "label": "Referral", "required": False, "options": ["None - GP Managed (Mild / No Treatment Indicated)", "Gastroenterology (Venesection Indicated)", "Gastroenterology (Diagnostic Confirmation)"]},
                    {"id": "tsat_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., Await HFE result, refer gastro if venesection criteria met"}
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
    seed_raised_transferrin_sat()
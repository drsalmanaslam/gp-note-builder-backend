from app.database import SessionLocal
from app.models import User, Template, Category

def seed_medication_review():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "GP-Related Topics").first()
    if not category: category = Category(name="GP-Related Topics"); db.add(category); db.commit()

    t = {
        "title": "Medication Review - Safety & Optimisation",
        "description": "Comprehensive medication review covering renal dosing, ACB scoring, PPI stewardship, sick day rules, drug interactions, and monitoring schedules.",
        "category": "GP-Related Topics",
        "content": {"sections": [
            {
                "title": "Key Checks & Latest Results",
                "section_type": "history",
                "questions": [
                    {"id": "medrev_egfr", "type": "number", "label": "Current eGFR (mL/min/1.73m²) - Date", "required": True, "placeholder": "e.g., 48 (15/07/2026)"},
                    {"id": "medrev_egfr_action", "type": "single_select", "label": "Renal Dosing Action Required", "required": True, "options": ["eGFR <60: Avoid SGLT2i", "eGFR <50: Avoid NSAIDs", "eGFR <30: Stop Metformin, Max Digoxin 0.125mg, Max Apixaban 2.5mg BD, Max Allopurinol 50mg", "eGFR <15: Stop Factor Xa Inhibitors", "eGFR <10: Stop Colchicine", "No Action Required (eGFR ≥60)"]},
                    {"id": "medrev_acb_score", "type": "number", "label": "Anticholinergic Drug Burden (ACB) Score (≥4 Confers Harm: Confusion, Falls, Dementia)", "required": False, "placeholder": "e.g., 5", "is_red_flag": True, "red_flag_positive": "RED FLAG: ACB ≥4 = review medications for discontinuation/substitution.", "red_flag_negative": ""},
                    {"id": "medrev_acb_drugs", "type": "multi_select", "label": "ACB-Contributing Drugs", "required": False, "options": ["Score 1: Atenolol/BBs, Codeine/Opiates, Diazepam/BZDs, Digoxin, Furosemide", "Score 2: Cetirizine/Antihistamines, Baclofen, Carbamazepine, Stemetil", "Score 3: Amitriptyline/TCAs, Oxybutynin, Olanzapine, Chlorphenamine", "None"]},
                    {"id": "medrev_ppi_longterm", "type": "toggle", "label": "Long-Term PPI Without Valid Indication? (Review: Barrett's, Severe Oesophagitis, Stricture, Chronic NSAID, Bleeding Ulcer, Zollinger-Ellison)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: No valid indication = consider PPI dose reduction or discontinuation trial.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Latest Bloods & Vitals",
                "section_type": "assessment",
                "questions": [
                    {"id": "medrev_creatinine", "type": "number", "label": "Creatinine (µmol/L)", "required": False, "placeholder": "e.g., 125"},
                    {"id": "medrev_sodium", "type": "number", "label": "Sodium (mmol/L)", "required": False, "placeholder": "e.g., 139"},
                    {"id": "medrev_t4", "type": "number", "label": "Free T4 (pmol/L)", "required": False, "placeholder": "e.g., 15.5"},
                    {"id": "medrev_tsh", "type": "number", "label": "TSH (mU/L)", "required": False, "placeholder": "e.g., 2.1"},
                    {"id": "medrev_ast", "type": "number", "label": "AST (U/L)", "required": False, "placeholder": "e.g., 28"},
                    {"id": "medrev_ggt", "type": "number", "label": "GGT (U/L)", "required": False, "placeholder": "e.g., 35"},
                    {"id": "medrev_lithium", "type": "number", "label": "Lithium Level (If Applicable)", "required": False, "placeholder": "e.g., 0.6"},
                    {"id": "medrev_calcium", "type": "number", "label": "Corrected Ca²⁺ (If Applicable)", "required": False, "placeholder": "e.g., 2.35"},
                    {"id": "medrev_bp", "type": "text", "label": "Last BP (mmHg) + Date", "required": False, "placeholder": "e.g., 138/82 (15/07/2026)"}
                ]
            },
            {
                "title": "Sick Day Rules - STOP THE DAMN DRUGS",
                "section_type": "plan",
                "questions": [
                    {"id": "medrev_sick_day", "type": "multi_select", "label": "Medications to Temporarily STOP During Acute Illness/Dehydration", "required": False, "options": ["Diuretics", "ACEI/ARBs", "Metformin", "NSAIDs", "Lithium", "SGLT2 Inhibitors", "None - Not on Any", "Patient Leaflet Provided"]}
                ]
            },
            {
                "title": "Key Drug Interactions - Checklist",
                "section_type": "assessment",
                "questions": [
                    {"id": "medrev_interactions", "type": "multi_select", "label": "High-Risk Interactions Present?", "required": True, "options": ["Azathioprine + Allopurinol (Blood Dyscrasias)", "Azathioprine/MTX + Trimethoprim (Toxicity)", "Clarithromycin + Statins (Rhabdomyolysis)", "Clopidogrel + Omeprazole/Esomeprazole (Reduced Effect)", "Eltroxin + Iron (Reduced Absorption - Separate Dosing)", "Fusidic Acid (PO) + Statins (Can Be Fatal)", "SSRIs + Tramadol (Serotonin Syndrome)", "SSRIs + NSAIDs (7-Fold Bleeding Risk)", "Warfarin + Daktarin Gel (Increased INR)", "Domperidone + Amiodarone/Citalopram/Clarithromycin (Pro-Arrhythmic)", "None Identified"]}
                ]
            },
            {
                "title": "Drugs Requiring Regular Monitoring",
                "section_type": "assessment",
                "questions": [
                    {"id": "medrev_monitoring", "type": "multi_select", "label": "Monitoring Required for Current Drugs", "required": False, "options": ["ACEI/ARB: U&E Yearly", "Amiodarone: TFTs/U&E/LFTs 6-Monthly", "Azathioprine: FBC+LFTs 3-Monthly, U&E 6-Monthly", "Denosumab: Calcium Prior to Each Dose", "Eltroxin: TFTs Yearly (8-12 Weekly if Abnormal)", "Lithium: Levels 3-Monthly, TFTs/U&E/LFTs 6-Monthly", "Methotrexate: FBC/U&E/LFTs 3-Monthly", "NOACs: FBC/U&E/LFTs 6-Monthly", "PPIs: Mg, B12, U&E Before Starting + Yearly", "SGLT2i: U&E Before Starting + Yearly", "None Required"]}
                ]
            },
            {
                "title": "Review Actions & Plan",
                "section_type": "plan",
                "safety_netting": "PPI prescribing notes: take before food, effect plateaus after 3-7 days, prefer BD dosing over increasing dose. If stopping PPI: rebound acid hypersecretion for up to 2 weeks - cover with antacid. NSAIDs + Aspirin = 30% of ADR-related admissions (largest cause of ADR death). Diclofenac: caution if IHD/CVA/PVD/CCF. Naproxen + PPI is least-worst NSAID option (e.g., Vimovo). Ibuprofen second choice. Sick Day Rules: STOP Diuretics, ACEI/ARBs, Metformin, NSAIDs, SGLT2i during acute illness/dehydration.",
                "questions": [
                    {"id": "medrev_actions", "type": "multi_select", "label": "Actions Taken Today", "required": True, "options": ["Drugs + eGFR Checked", "Sick Day Rules Leaflet Provided", "Interactions Checked", "Bloods Acceptable", "Bloods Needed", "BP Needs Review", "High ACB → Medications Reviewed", "NSAIDs Reduced", "PPI Reduction Attempted", "Blister Pack (MDS) Considered", "Phased Dispensing Considered"]},
                    {"id": "medrev_reviewer", "type": "text", "label": "Reviewed By (Initials/Name)", "required": False, "placeholder": "e.g., Dr. Aslam"},
                    {"id": "medrev_date", "type": "text", "label": "Date of Review", "required": False, "placeholder": "e.g., 29/07/2026"},
                    {"id": "medrev_followup", "type": "text", "label": "Next Review / Actions", "required": True, "placeholder": "e.g., Repeat U&E in 2 weeks, annual medication review"}
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
    seed_medication_review()
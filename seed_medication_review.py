from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_medication_review():
    db = SessionLocal()
    
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin:
        admin = db.query(User).filter(User.role == "admin").first()
    if not admin:
        print("❌ No admin user found!")
        db.close()
        return

    category = db.query(Category).filter(Category.name == "GP-Related Topics").first()
    if not category:
        category = Category(name="GP-Related Topics")
        db.add(category)
        db.commit()

    title = "Medication Review - Safety & Optimisation"
    
    existing = db.query(Template).filter(Template.title == title).first()
    if existing:
        print(f"⏭️  SKIPPED: {title} already exists (ID={existing.id})")
        db.close()
        return

    template = Template(
        title=title,
        description="Comprehensive medication review covering renal dosing, ACB scoring, PPI stewardship, sick day rules, drug interactions, and monitoring schedules.",
        category="GP-Related Topics",
        content={"sections": [
            {
                "title": "Key Checks & Latest Results",
                "section_type": "history",
                "questions": [
                    {"id": "medrev_egfr", "type": "number", "label": "Current eGFR (mL/min/1.73m²)", "required": True, "placeholder": "e.g., 48"},
                    {"id": "medrev_egfr_action", "type": "single_select", "label": "Renal Dosing Action Required", "required": True, "options": ["eGFR <60: Avoid SGLT2i", "eGFR <50: Avoid NSAIDs", "eGFR <30: Stop Metformin, Max Digoxin 0.125mg", "eGFR <15: Stop Factor Xa Inhibitors", "No Action Required (eGFR ≥60)"]},
                    {"id": "medrev_acb_score", "type": "number", "label": "Anticholinergic Drug Burden (ACB) Score", "required": False, "placeholder": "e.g., 5", "is_red_flag": True, "red_flag_positive": "RED FLAG: ACB ≥4 = increased risk of confusion, falls, dementia. Review medications.", "red_flag_negative": ""},
                    {"id": "medrev_acb_drugs", "type": "multi_select", "label": "ACB-Contributing Drugs", "required": False, "options": ["Amitriptyline/TCAs (Score 3)", "Oxybutynin (Score 3)", "Codeine/Opiates (Score 1)", "Diazepam/BZDs (Score 1)", "Cetirizine (Score 2)", "None"]},
                    {"id": "medrev_ppi_longterm", "type": "toggle", "label": "Long-Term PPI Without Valid Indication?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: No valid indication = consider PPI dose reduction or discontinuation trial.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Latest Bloods & Vitals",
                "section_type": "assessment",
                "questions": [
                    {"id": "medrev_creatinine", "type": "number", "label": "Creatinine (µmol/L)", "required": False, "placeholder": "e.g., 125"},
                    {"id": "medrev_sodium", "type": "number", "label": "Sodium (mmol/L)", "required": False, "placeholder": "e.g., 139"},
                    {"id": "medrev_tsh", "type": "number", "label": "TSH (mU/L)", "required": False, "placeholder": "e.g., 2.1"},
                    {"id": "medrev_lithium", "type": "number", "label": "Lithium Level (if applicable)", "required": False, "placeholder": "e.g., 0.6"},
                    {"id": "medrev_bp", "type": "text", "label": "Last BP (mmHg)", "required": False, "placeholder": "e.g., 138/82"}
                ]
            },
            {
                "title": "Sick Day Rules",
                "section_type": "plan",
                "questions": [
                    {"id": "medrev_sick_day", "type": "multi_select", "label": "Medications to STOP During Acute Illness/Dehydration", "required": False, "options": ["Diuretics", "ACEI/ARBs", "Metformin", "NSAIDs", "SGLT2 Inhibitors", "None", "Patient Leaflet Provided"]}
                ]
            },
            {
                "title": "Key Drug Interactions",
                "section_type": "assessment",
                "questions": [
                    {"id": "medrev_interactions", "type": "multi_select", "label": "High-Risk Interactions Present?", "required": True, "options": ["Clarithromycin + Statins (Rhabdomyolysis)", "Clopidogrel + Omeprazole (Reduced Effect)", "SSRIs + Tramadol (Serotonin Syndrome)", "SSRIs + NSAIDs (Bleeding Risk)", "Warfarin + Daktarin Gel (Increased INR)", "Eltroxin + Iron (Reduced Absorption)", "None Identified"]}
                ]
            },
            {
                "title": "Drugs Requiring Monitoring",
                "section_type": "assessment",
                "questions": [
                    {"id": "medrev_monitoring", "type": "multi_select", "label": "Monitoring Required", "required": False, "options": ["ACEI/ARB: U&E Yearly", "Amiodarone: TFTs/U&E/LFTs 6-Monthly", "Lithium: Levels 3-Monthly", "Methotrexate: FBC/U&E/LFTs 3-Monthly", "NOACs: FBC/U&E/LFTs 6-Monthly", "PPIs: Mg, B12 Yearly", "SGLT2i: U&E Yearly", "None Required"]}
                ]
            },
            {
                "title": "Review Actions & Plan",
                "section_type": "plan",
                "safety_netting": "Sick Day Rules: STOP Diuretics, ACEI/ARBs, Metformin, NSAIDs, SGLT2i during acute illness/dehydration. NSAIDs + Aspirin = 30% of ADR-related admissions. Naproxen + PPI is safest NSAID option. If stopping PPI: rebound acid hypersecretion for up to 2 weeks - cover with antacid.",
                "questions": [
                    {"id": "medrev_actions", "type": "multi_select", "label": "Actions Taken", "required": True, "options": ["Drugs + eGFR Checked", "Sick Day Rules Leaflet Provided", "Interactions Checked", "Bloods Acceptable", "Bloods Needed", "High ACB → Reviewed", "PPI Reduction Attempted", "Blister Pack (MDS) Considered"]},
                    {"id": "medrev_followup", "type": "text", "label": "Next Review / Actions", "required": True, "placeholder": "e.g., Repeat U&E in 2 weeks, annual review"}
                ]
            }
        ]},
        is_public=True,
        created_by=admin.id
    )
    
    db.add(template)
    db.commit()
    print(f"✅ Created: {title}")
    db.close()

if __name__ == "__main__":
    seed_medication_review()
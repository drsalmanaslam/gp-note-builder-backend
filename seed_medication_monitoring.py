from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_medication_monitoring():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin:
        print("Admin not found.")
        db.close()
        return

    category = db.query(Category).filter(Category.name == "GP-Related Topics").first()
    if not category:
        category = Category(name="GP-Related Topics")
        db.add(category)
        db.commit()

    t = {
        "title": "Monitoring Bloods for Patients on Specific Medications",
        "description": "Quick-reference guide for blood monitoring requirements of commonly prescribed medications. Reflects NICE/BNF recommendations as mirrored in HSE primary care and shared-care guidance.",
        "category": "GP-Related Topics",
        "content": {"sections": [
            {
                "title": "Cardiovascular / Renal Drugs",
                "section_type": "plan",
                "questions": [
                    {"id": "mon_acei_arb", "type": "text", "label": "ACE Inhibitors / ARBs", "required": False, "placeholder": "U&E before starting; recheck 1-2 weeks after starting/dose increase; annually once stable. Check sooner if intercurrent illness, dehydration, or NSAID/diuretic co-prescribed.", "output_phrase": "ACEi/ARB: {value}"},
                    {"id": "mon_diuretics", "type": "text", "label": "Diuretics (Loop/Thiazide)", "required": False, "placeholder": "U&E before starting, 1-2 weeks after starting/dose change, then annually (more often in elderly or if on other nephrotoxic drugs).", "output_phrase": "Diuretics: {value}"},
                    {"id": "mon_spironolactone", "type": "text", "label": "Spironolactone / K+-Sparing Diuretics (esp. with ACEi/ARB)", "required": False, "placeholder": "U&E before starting, at 1 week, 1 month, then every 3-6 months once stable. Risk of hyperkalaemia.", "output_phrase": "Spironolactone: {value}"},
                    {"id": "mon_statins", "type": "text", "label": "Statins", "required": False, "placeholder": "LFTs before starting, at 3 months, and at 12 months. No routine ongoing LFTs. CK only if muscle symptoms.", "output_phrase": "Statins: {value}"},
                    {"id": "mon_amiodarone", "type": "text", "label": "Amiodarone", "required": False, "placeholder": "TFTs and LFTs before starting, then every 6 months. Also periodic U&E, CXR at baseline, annual ophthalmic/pulmonary review.", "output_phrase": "Amiodarone: {value}"},
                    {"id": "mon_digoxin", "type": "text", "label": "Digoxin", "required": False, "placeholder": "U&E (esp. potassium) periodically; digoxin level only if toxicity suspected or renal function changes (sample >=6h post-dose).", "output_phrase": "Digoxin: {value}"},
                    {"id": "mon_warfarin", "type": "text", "label": "Warfarin", "required": False, "placeholder": "INR per individual dosing schedule (initially frequent, then per stability, typically every 4-12 weeks once stable).", "output_phrase": "Warfarin: {value}"},
                    {"id": "mon_doac", "type": "text", "label": "DOACs (Apixaban, Rivaroxaban, Dabigatran, Edoxaban)", "required": False, "placeholder": "U&E/eGFR before starting; at least annually; more frequently (every 6 months) if eGFR 30-60, elderly, or frail. Consider LFTs at baseline.", "output_phrase": "DOACs: {value}"}
                ]
            },
            {
                "title": "Diabetes Drugs",
                "section_type": "plan",
                "questions": [
                    {"id": "mon_metformin", "type": "text", "label": "Metformin", "required": False, "placeholder": "U&E/eGFR before starting, then annually; more frequently if eGFR declining or elderly. B12 periodically with long-term use (risk of deficiency).", "output_phrase": "Metformin: {value}"},
                    {"id": "mon_sulfonylureas", "type": "text", "label": "Sulfonylureas (e.g. Gliclazide)", "required": False, "placeholder": "U&E/renal function periodically; HbA1c every 3-6 months.", "output_phrase": "Sulfonylureas: {value}"},
                    {"id": "mon_sglt2", "type": "text", "label": "SGLT2 Inhibitors", "required": False, "placeholder": "Renal function before starting and periodically; watch for DKA risk factors.", "output_phrase": "SGLT2i: {value}"}
                ]
            },
            {
                "title": "Psychiatric Drugs",
                "section_type": "plan",
                "questions": [
                    {"id": "mon_lithium", "type": "text", "label": "Lithium", "required": False, "placeholder": "Weekly levels until stable, then every 3 months for first year. After year 1: every 6 months if stable (or every 3 months in higher-risk). U&E, eGFR, calcium, TFTs every 6 months. Sample 12h post-dose.", "output_phrase": "Lithium: {value}"},
                    {"id": "mon_valproate", "type": "text", "label": "Sodium Valproate", "required": False, "placeholder": "LFTs and FBC at baseline, then periodically (esp. first 6 months). Levels not routinely required unless adherence/toxicity concern.", "output_phrase": "Valproate: {value}"},
                    {"id": "mon_carbamazepine", "type": "text", "label": "Carbamazepine", "required": False, "placeholder": "FBC, LFTs, U&E (sodium - risk of hyponatraemia) at baseline, then periodically, especially in first few months.", "output_phrase": "Carbamazepine: {value}"},
                    {"id": "mon_clozapine", "type": "text", "label": "Clozapine", "required": False, "placeholder": "FBC (with differential) mandatory: weekly for 18 weeks, then fortnightly to 1 year, then monthly indefinitely under mandatory monitoring service.", "output_phrase": "Clozapine: {value}"},
                    {"id": "mon_antipsychotics", "type": "text", "label": "Antipsychotics (General, incl. Second-Generation)", "required": False, "placeholder": "Baseline weight/BMI, HbA1c/fasting glucose, lipid profile; repeat at 3 months then annually. Prolactin if clinically indicated.", "output_phrase": "Antipsychotics: {value}"}
                ]
            },
            {
                "title": "Rheumatology / Immunosuppressants",
                "section_type": "plan",
                "questions": [
                    {"id": "mon_methotrexate", "type": "text", "label": "Methotrexate", "required": False, "placeholder": "FBC, U&E, LFTs before starting; every 2 weeks until stable dose for 6 weeks; then monthly for 3 months; then every 3 months.", "output_phrase": "Methotrexate: {value}"},
                    {"id": "mon_azathioprine", "type": "text", "label": "Azathioprine", "required": False, "placeholder": "TPMT (and consider NUDT15) activity before starting. FBC weekly for first 4 weeks, then every 2-3 months once stable; LFTs periodically.", "output_phrase": "Azathioprine: {value}"},
                    {"id": "mon_sulfasalazine", "type": "text", "label": "Sulfasalazine", "required": False, "placeholder": "FBC and LFTs before starting, then every 2-4 weeks for first 3 months, then every 3 months.", "output_phrase": "Sulfasalazine: {value}"},
                    {"id": "mon_leflunomide", "type": "text", "label": "Leflunomide", "required": False, "placeholder": "FBC, LFTs before starting; every 2 weeks for first 6 months, then every 8 weeks.", "output_phrase": "Leflunomide: {value}"}
                ]
            },
            {
                "title": "Other Commonly Monitored Drugs",
                "section_type": "plan",
                "questions": [
                    {"id": "mon_isotretinoin", "type": "text", "label": "Isotretinoin", "required": False, "placeholder": "LFTs and lipid profile at baseline and periodically; pregnancy test monthly in patients of childbearing potential.", "output_phrase": "Isotretinoin: {value}"},
                    {"id": "mon_corticosteroids", "type": "text", "label": "Long-Term Corticosteroids", "required": False, "placeholder": "Glucose/HbA1c periodically; bone health assessment if long-term use; U&E if high dose.", "output_phrase": "Corticosteroids: {value}"},
                    {"id": "mon_ppi", "type": "text", "label": "Long-Term PPIs", "required": False, "placeholder": "Magnesium and B12 periodically with prolonged use (>1 year), especially in older patients.", "output_phrase": "PPIs: {value}"},
                    {"id": "mon_allopurinol", "type": "text", "label": "Allopurinol", "required": False, "placeholder": "U&E/renal function and uric acid before starting and periodically; start dose adjusted for renal function.", "output_phrase": "Allopurinol: {value}"},
                    {"id": "mon_bisphosphonates", "type": "text", "label": "Bisphosphonates", "required": False, "placeholder": "Calcium, vitamin D, and renal function before starting and periodically; correct hypocalcaemia before initiation.", "output_phrase": "Bisphosphonates: {value}"},
                    {"id": "mon_phenytoin", "type": "text", "label": "Phenytoin", "required": False, "placeholder": "FBC, LFTs, and phenytoin levels (if toxicity/adherence concern or interacting drugs); levels not needed routinely if clinically stable.", "output_phrase": "Phenytoin: {value}"}
                ]
            },
            {
                "title": "Notes on Medication Monitoring",
                "section_type": "plan",
                "safety_netting": "Always check current BNF/BNF-NI, local shared-care agreement, or HSE medicines management guidance before initiating monitoring. Many drugs (lithium, clozapine, methotrexate, DMARDs) are initiated in secondary care with formal shared-care agreement before GP takes over monitoring — confirm responsibility is clearly documented. Build monitoring into recall/practice system to avoid missed tests. Document rationale if extending or reducing standard monitoring intervals for an individual patient.",
                "questions": []
            }
        ]},
        "is_public": True
    }

    existing = db.query(Template).filter(Template.title == t["title"], Template.created_by == admin.id).first()
    if existing:
        existing.description = t["description"]
        existing.content = t["content"]
        existing.category = t["category"]
        existing.is_public = t["is_public"]
        existing.updated_at = datetime.now(timezone.utc)
        db.commit()
        print(f"🔄 Updated: {t['title']}")
    else:
        new_t = Template(title=t["title"], description=t["description"], category=t["category"], content=t["content"], is_public=True, created_by=admin.id, version=1)
        db.add(new_t)
        db.commit()
        print(f"✅ Template '{t['title']}' created with {len(t['content']['sections'])} sections!")
    db.close()

if __name__ == "__main__":
    seed_medication_monitoring()
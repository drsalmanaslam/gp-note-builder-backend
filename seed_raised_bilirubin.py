from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_raised_bilirubin():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Abnormal Labs/Investigations").first()
    if not category: category = Category(name="Abnormal Labs/Investigations"); db.add(category); db.commit()

    t = {
        "title": "Raised Bilirubin",
        "description": "Focused assessment for raised bilirubin covering Gilbert's syndrome vs haemolysis vs hepatobiliary causes, fractionated bilirubin interpretation, and stepwise investigation.",
        "category": "Abnormal Labs/Investigations",
        "content": {"sections": [
            {
                "title": "Results & History",
                "section_type": "history",
                "questions": [
                    {"id": "bili_total", "type": "number", "label": "Total Bilirubin (µmol/L)", "required": True, "placeholder": "e.g., 38 (Note lab reference range)"},
                    {"id": "bili_itch", "type": "toggle", "label": "Itch / Pruritus? (Obstructive Jaundice)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Itch + raised bilirubin = ?obstructive jaundice. Urgent US liver.", "red_flag_negative": ""},
                    {"id": "bili_general", "type": "single_select", "label": "General Wellbeing", "required": True, "options": ["Well - Asymptomatic (?Gilbert's)", "Unwell - ?Pathological Cause"]},
                    {"id": "bili_meds", "type": "multi_select", "label": "Hepatotoxic Medications", "required": True, "options": ["Methotrexate", "Azathioprine", "Nitrofurantoin", "Statins", "Terbinafine", "Carbamazepine", "None of the above"]}
                ]
            },
            {
                "title": "Step 1 - Fractionated Bilirubin",
                "section_type": "assessment",
                "questions": [
                    {"id": "bili_fractionated", "type": "toggle", "label": "Repeat LFTs with Fractionated Bilirubin Ordered? (Unconjugated + Conjugated)", "required": True},
                    {"id": "bili_unconjugated", "type": "number", "label": "Unconjugated (Indirect) Bilirubin", "required": False, "placeholder": "e.g., 30 (≥80% Total = ?Gilbert's)"},
                    {"id": "bili_conjugated", "type": "number", "label": "Conjugated (Direct) Bilirubin", "required": False, "placeholder": "e.g., 5"},
                    {"id": "bili_unconjugated_percent", "type": "number", "label": "Unconjugated % of Total", "required": False, "placeholder": "e.g., 86% (≥80% = Gilbert's Pattern)"}
                ]
            },
            {
                "title": "Step 1 Interpretation",
                "section_type": "assessment",
                "questions": [
                    {"id": "bili_pattern", "type": "single_select", "label": "Bilirubin Pattern", "required": False, "options": ["Predominantly UNCONJUGATED (≥80% Total) → ?Gilbert's Syndrome", "Predominantly CONJUGATED → ?Hepatobiliary Cause", "Mixed", "Awaiting Result"]},
                    {"id": "bili_gilberts_explained", "type": "toggle", "label": "Gilbert's Explained? (Harmless Liver Condition, No Long-Term Consequences, Bilirubin Rises with Fasting/Stress/Illness)", "required": False},
                    {"id": "bili_haemolysis_workup", "type": "multi_select", "label": "Haemolysis Workup (If Clinically Indicated)", "required": False, "options": ["LDH", "Reticulocyte Count", "Haptoglobin", "Blood Film", "Not indicated"]}
                ]
            },
            {
                "title": "Step 2 - If Conjugated / Significantly Raised",
                "section_type": "assessment",
                "questions": [
                    {"id": "bili_hepatobiliary_workup", "type": "multi_select", "label": "Hepatobiliary Investigation (If Conjugated Bilirubin Raised)", "required": False, "options": ["Ultrasound Liver + Biliary Tree", "Viral Hepatitis Serology (B/C)", "Ferritin / Iron Studies", "Caeruloplasmin (Wilson's)", "Alpha-1 Antitrypsin", "Liver Autoantibody Profile (ANA, SMA, LKM, AMA)", "Not indicated"]}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "Gilbert's Syndrome (Unconjugated ≥80%, Asymptomatic, Well) - Most Common",
                    "Haemolysis (Unconjugated, Anaemia, Raised LDH, Low Haptoglobin)",
                    "Drug-Induced (Statins, Methotrexate, etc.)",
                    "Viral Hepatitis (Conjugated, Unwell, Raised ALT/AST)",
                    "Obstructive Jaundice (Conjugated, Itch, Pale Stools, Dark Urine)",
                    "Dubin-Johnson / Rotor Syndrome (Conjugated - Rare)",
                    "Wilson's Disease (Young, Conjugated, Low Caeruloplasmin)",
                    "Autoimmune Hepatitis (Conjugated, ANA/SMA Positive)"
                ],
                "questions": [
                    {"id": "bili_diagnosis", "type": "single_select", "label": "Clinical Impression", "required": True, "options": ["?Gilbert's Syndrome (Likely - Asymptomatic, Unconjugated ≥80%)", "?Haemolysis", "?Hepatobiliary Cause (Conjugated Bilirubin)", "?Drug-Induced", "Uncertain - Awaiting Fractionated Bilirubin"]}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Gilbert's syndrome: harmless liver condition where liver doesn't process bilirubin as efficiently as usual. No long-term health consequences. Bilirubin may rise with fasting, stress, illness, or alcohol. No treatment required. No restrictions on lifestyle or medications. If predominantly unconjugated (≥80% total) + asymptomatic + well = likely Gilbert's. Consider haemolysis workup (LDH, reticulocyte count, haptoglobin) if clinically indicated (anaemia, jaundice, gallstones). If predominantly conjugated or significantly raised: investigate hepatobiliary cause (US liver, viral hepatitis serology, ferritin, caeruloplasmin, alpha-1 antitrypsin, liver autoantibody profile).",
                "questions": [
                    {"id": "bili_no_treatment", "type": "toggle", "label": "No Treatment Required Explained? (Gilbert's - Harmless, No Long-Term Consequences)", "required": False},
                    {"id": "bili_triggers", "type": "toggle", "label": "Triggers Explained? (Fasting, Stress, Illness, Alcohol Can Raise Bilirubin)", "required": False},
                    {"id": "bili_referral", "type": "single_select", "label": "Referral", "required": False, "options": ["None - GP Managed (Gilbert's / Drug-Induced)", "Gastroenterology / Hepatology (Conjugated / Significantly Raised)", "Haematology (?Haemolysis)"]},
                    {"id": "bili_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., No follow-up if Gilbert's confirmed, further investigation if conjugated"}
                ]
            }
        ]},
        "is_public": True
    }

    existing = db.query(Template).filter(Template.title == t["title"], Template.created_by == admin.id).first()
    
    if existing:
        print(f"⏭️  SKIPPED: {title} already exists (ID={existing.id})")
        db.close()
        return
    new_t = Template(title=t["title"], description=t["description"], category=t["category"], content=t["content"], is_public=True, created_by=admin.id, version=1)
    db.add(new_t); db.commit()
    print(f"Template '{t['title']}' created with {len(t['content']['sections'])} sections!"); db.close()

if __name__ == "__main__":
    seed_raised_bilirubin()
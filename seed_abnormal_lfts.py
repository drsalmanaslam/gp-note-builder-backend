from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_abnormal_lfts():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin:
        print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Abnormal Labs/Investigations").first()
    if not category:
        category = Category(name="Abnormal Labs/Investigations"); db.add(category); db.commit()

    t = {
        "title": "Abnormal LFTs — General Approach",
        "description": "Systematic approach to abnormal liver function tests. Pattern recognition (hepatitic, cholestatic, mixed), common causes, and investigation pathway.",
        "category": "Abnormal Labs/Investigations",
        "content": {"sections": [
            {
                "title": "Pattern Recognition",
                "section_type": "history",
                "questions": [
                    {"id": "lft_pattern", "type": "single_select", "label": "LFT Pattern", "required": True, "options": ["Hepatitic — ALT/AST raised > ALP", "Cholestatic — ALP/GGT raised > ALT", "Mixed — both ALT and ALP raised", "Isolated GGT", "Isolated bilirubin"], "output_phrase": "Pattern: {value}"},
                    {"id": "lft_alt", "type": "text", "label": "ALT (U/L)", "required": False, "placeholder": "e.g., 120", "output_phrase": "ALT: {value}"},
                    {"id": "lft_alp", "type": "text", "label": "ALP (U/L)", "required": False, "placeholder": "e.g., 180", "output_phrase": "ALP: {value}"},
                    {"id": "lft_ggt", "type": "text", "label": "GGT (U/L)", "required": False, "placeholder": "e.g., 250", "output_phrase": "GGT: {value}"}
                ]
            },
            {
                "title": "Causes — Systematic Enquiry",
                "section_type": "history",
                "questions": [
                    {"id": "lft_alcohol", "type": "single_select", "label": "Alcohol Intake", "required": True, "options": ["None", "Within limits", "Excess", "Heavy"], "output_phrase": "Alcohol: {value}"},
                    {"id": "lft_drugs", "type": "multi_select", "label": "Hepatotoxic Drugs", "required": True, "options": ["Paracetamol", "Statins", "Amoxicillin/clavulanate", "NSAIDs", "Methotrexate", "Valproate", "None"], "output_phrase": "Drugs: {value}"},
                    {"id": "lft_metabolic", "type": "multi_select", "label": "Metabolic Risk Factors", "required": True, "options": ["Obesity / overweight", "Type 2 diabetes", "Dyslipidaemia", "Hypertension", "None"], "output_phrase": "Metabolic: {value}"},
                    {"id": "lft_viral", "type": "toggle", "label": "Risk Factors for Viral Hepatitis? (travel, IVDU, tattoos, transfusion)", "required": True, "output_phrase": "Viral risk: {value}"}
                ]
            },
            {
                "title": "Red Flags",
                "section_type": "history",
                "questions": [
                    {"id": "lft_jaundice", "type": "toggle", "label": "Jaundice / Ascites / Encephalopathy?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Signs of decompensated liver disease = urgent gastroenterology referral.", "red_flag_negative": "", "output_phrase": "Decompensation: {value}"},
                    {"id": "lft_weight_loss", "type": "toggle", "label": "Weight Loss / Night Sweats? (?malignancy)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Constitutional symptoms + deranged LFTs = ?malignancy. Urgent imaging.", "red_flag_negative": "", "output_phrase": "?Malignancy: {value}"}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": ["MASLD / NAFLD (commonest cause of mild ALT rise)", "Alcohol-Related Liver Disease", "Viral Hepatitis (A, B, C, EBV)", "Drug-Induced Liver Injury", "Gilbert Syndrome (isolated bilirubin)", "Haemochromatosis", "Autoimmune Hepatitis", "Primary Biliary Cholangitis", "Malignancy (primary or metastatic)"],
                "questions": [
                    {"id": "lft_diagnosis", "type": "single_select", "label": "Clinical Impression", "required": True, "options": ["?MASLD — lifestyle + repeat", "?Alcohol — brief intervention + repeat", "?Drug-induced — stop agent + repeat", "?Viral — hepatitis screen", "?Serious — urgent gastro referral"], "output_phrase": "Diagnosis: {value}"}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "First-line: Repeat LFTs in 2-4 weeks with full liver screen (hepatitis B/C, EBV, CMV, ANA, ASMA, AMA, immunoglobulins, ferritin, caeruloplasmin if <40, alpha-1 antitrypsin). Liver ultrasound. If MASLD: Weight loss 10%, exercise, repeat. If alcohol: Brief intervention. If LFTs persistently >2x normal: Refer gastroenterology. Safety-net: Return if jaundice, ascites, confusion, or bleeding.",
                "questions": [
                    {"id": "lft_action", "type": "single_select", "label": "Action", "required": True, "options": ["Repeat LFTs + liver screen", "Liver ultrasound", "Lifestyle + repeat (mild MASLD)", "Stop drug + repeat", "Urgent gastro referral"], "output_phrase": "Action: {value}"},
                    {"id": "lft_safety_net", "type": "toggle", "label": "Safety-Net Given?", "required": True, "output_phrase": "Safety-net: {value}"},
                    {"id": "lft_followup", "type": "text", "label": "Follow-up", "required": True, "placeholder": "e.g., Repeat LFTs + liver screen in 2 weeks. Ultrasound booked.", "output_phrase": "Follow-up: {value}"}
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
    seed_abnormal_lfts()
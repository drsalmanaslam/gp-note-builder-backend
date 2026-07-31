from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_diarrhoea():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Gastroenterology").first()
    if not category: category = Category(name="Gastroenterology"); db.add(category); db.commit()

    t = {
        "title": "Diarrhoea",
        "description": "Focused assessment for diarrhoea covering infective vs inflammatory causes, red flags, stool testing, safety-netting, and school/work exclusion advice.",
        "category": "Gastroenterology",
        "content": {"sections": [
            {
                "title": "Bowel History",
                "section_type": "history",
                "questions": [
                    {"id": "diar_presenting_complaint", "type": "text", "label": "Presenting Complaint", "required": True, "placeholder": "e.g., Diarrhoea for 2 weeks, 5 times daily including at night"},
                    {"id": "diar_duration", "type": "text", "label": "Duration of Symptoms", "required": True, "placeholder": "e.g., 2 weeks", "is_red_flag": True, "red_flag_positive": "RED FLAG: Diarrhoea >7 days = send stool for molecular enterics + C. diff. >4 weeks = ?IBD, coeliac, thyrotoxicosis.", "red_flag_negative": ""},
                    {"id": "diar_frequency", "type": "number", "label": "Stool Frequency (per day)", "required": True, "placeholder": "e.g., 5"},
                    {"id": "diar_nocturnal", "type": "toggle", "label": "Nocturnal Symptoms? (Waking from sleep)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Nocturnal diarrhoea = ?IBD (not IBS). Investigate.", "red_flag_negative": ""},
                    {"id": "diar_pain", "type": "single_select", "label": "Associated Abdominal Pain", "required": True, "options": ["Mild pain, relieved by passing bowel motion (?IBS)", "Pain not relieved by defaecation (?IBD)", "No pain"]},
                    {"id": "diar_steatorrhoea", "type": "toggle", "label": "Steatorrhoea? (Pale, bulky, difficult to flush)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Steatorrhoea = ?coeliac disease, pancreatic insufficiency. Check coeliac screen + faecal elastase.", "red_flag_negative": ""},
                    {"id": "diar_blood", "type": "toggle", "label": "Blood in Stool?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Blood + diarrhoea = ?IBD, infective colitis, malignancy. Stool sample + investigate.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Associated Symptoms & Screening",
                "section_type": "history",
                "questions": [
                    {"id": "diar_upper_gi", "type": "multi_select", "label": "Upper GI Symptoms", "required": False, "options": ["Nausea", "Vomiting", "Haematemesis", "Fever", "None present"]},
                    {"id": "diar_ibd_screen", "type": "multi_select", "label": "IBD Screen", "required": True, "options": ["Mouth ulcers", "Fever", "Weight loss", "Loss of appetite", "Eye symptoms", "None present"], "is_red_flag": True, "red_flag_positive": "RED FLAG: IBD red flags present = urgent gastroenterology referral.", "red_flag_negative": ""},
                    {"id": "diar_ibs", "type": "toggle", "label": "Bloating with Relief After Passing Stool? (IBS-type)", "required": False},
                    {"id": "diar_thyrotoxicosis", "type": "multi_select", "label": "Thyrotoxicosis Screen", "required": False, "options": ["Heat intolerance", "Sweating", "Tremor", "Irritability", "None present"]},
                    {"id": "diar_anorectal", "type": "multi_select", "label": "Anorectal Symptoms", "required": False, "options": ["Tenesmus", "Anal sex (receptive - ?LGV)", "Neither"]},
                    {"id": "diar_gu", "type": "toggle", "label": "Genitourinary Symptoms?", "required": False}
                ]
            },
            {
                "title": "Exposure & Risk Factors",
                "section_type": "history",
                "questions": [
                    {"id": "diar_exposure", "type": "multi_select", "label": "Infective / Exposure History", "required": True, "options": ["Unwell contacts", "Suspicious food (BBQ/buffet/takeaway)", "Recent travel (specify)", "None"]},
                    {"id": "diar_pmh_family", "type": "multi_select", "label": "Past / Family History", "required": False, "options": ["IBD", "Thyroid disease", "Coeliac disease", "None"]},
                    {"id": "diar_diet_change", "type": "toggle", "label": "Recent Dietary Change?", "required": False},
                    {"id": "diar_hepatobiliary", "type": "multi_select", "label": "Hepatobiliary Screen", "required": False, "options": ["Pale stool", "Jaundice", "Neither present"]},
                    {"id": "diar_occupation", "type": "multi_select", "label": "Occupational / Exposure Risk (Public Health)", "required": True, "options": ["Food handler", "Healthcare worker", "Education worker", "Farm animal exposure", "Contaminated water exposure", "None of the above"]},
                    {"id": "diar_meds", "type": "text", "label": "Recent New Medication? (e.g., Valsartan, metformin, antibiotics)", "required": False, "placeholder": "Specify drug or 'None'"}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "diar_vitals", "type": "text", "label": "Vital Signs", "required": True, "placeholder": "e.g., HR 80, Temp 36°C, SpO2 99%"},
                    {"id": "diar_hydration", "type": "single_select", "label": "Hydration Status", "required": True, "options": ["Moist mucous membranes - well hydrated", "Signs of dehydration - RED FLAG"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Dehydrated = ?need admission for IV fluids. Especially elderly/children.", "red_flag_negative": ""},
                    {"id": "diar_abdo", "type": "single_select", "label": "Abdominal Examination", "required": True, "options": ["Soft, non-tender, BS present, no masses", "Tenderness present", "Mass palpated", "Organomegaly", "Abnormal bowel sounds"]},
                    {"id": "diar_thyroid", "type": "single_select", "label": "Thyroid Examination", "required": False, "options": ["Normal", "Abnormal"]}
                ]
            },
            {
                "title": "Investigations",
                "section_type": "assessment",
                "differentials": [
                    "Viral Gastroenteritis (most common)",
                    "Bacterial Gastroenteritis (Campylobacter, Salmonella, Shigella, E. coli)",
                    "C. difficile Colitis (recent antibiotics, hospitalisation)",
                    "IBD (Crohn's / Ulcerative Colitis)",
                    "Coeliac Disease",
                    "Hyperthyroidism",
                    "Irritable Bowel Syndrome (IBS-D)",
                    "Medication-Induced (metformin, antibiotics, ARBs, SSRIs)",
                    "Lactose Intolerance",
                    "Lymphogranuloma Venereum (LGV - receptive anal sex + tenesmus)",
                    "Colorectal Cancer (RED FLAG)"
                ],
                "questions": [
                    {"id": "diar_bloods", "type": "multi_select", "label": "Bloods Ordered", "required": False, "options": ["FBC (WCC)", "TFTs", "U&Es", "Coeliac screen (IgA TTG)", "ESR / CRP", "LFTs", "Haematinics", "None"]},
                    {"id": "diar_urine", "type": "toggle", "label": "Urine Dipstick Performed?", "required": False},
                    {"id": "diar_stool", "type": "single_select", "label": "Stool Sample (Molecular Enterics + C. diff)", "required": False, "options": ["Sent - persistent diarrhoea >7 days", "Sent - blood in stool", "Not indicated at this stage"]}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Return if: no improvement after 48-72 hours, blood in stool develops, signs of dehydration (dizziness, reduced urine, dry mouth), severe abdominal pain, or fever >38°C. Loperamide: 4mg stat then 1 tablet TDS. Only for symptom control (travel/events). Do NOT use with fever or suspected C. difficile. Not recommended in viral gastroenteritis. Codant (codeine phosphate) 30mg QDS for 4 days as second-line. Hold diuretics/ACEi/NSAIDs if dehydrated. School/work exclusion: 48 hours after last episode of diarrhoea/vomiting. Food handlers, healthcare workers, education staff must be excluded.",
                "questions": [
                    {"id": "diar_diagnosis", "type": "single_select", "label": "Clinical Impression", "required": True, "options": ["Likely viral gastroenteritis", "Bacterial gastroenteritis suspected", "IBD suspected", "Coeliac disease suspected", "Thyrotoxicosis suspected", "Medication-induced", "Other"]},
                    {"id": "diar_loperamide", "type": "single_select", "label": "Loperamide (Symptom Control Only)", "required": False, "options": ["4mg stat then 1 tablet TDS", "Not prescribed - fever / ?C. diff", "Not prescribed - clinical judgement"]},
                    {"id": "diar_codant", "type": "toggle", "label": "Codant (Codeine Phosphate) 30mg QDS for 4 Days?", "required": False},
                    {"id": "diar_meds_hold", "type": "multi_select", "label": "Medications to Hold", "required": False, "options": ["Diuretic", "ACE Inhibitor", "NSAID", "Not applicable"]},
                    {"id": "diar_exclusion", "type": "multi_select", "label": "School/Work Exclusion Group", "required": False, "options": ["Child attending school/nursery", "School/nursery teacher", "Food handler", "Healthcare worker", "Not applicable"]},
                    {"id": "diar_exclusion_advised", "type": "toggle", "label": "48 Hours Post-Last Episode Exclusion Advised?", "required": False},
                    {"id": "diar_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., Return if not improving, review with results, or refer if persistent"}
                ]
            }
        ]},
        "is_public": True
    }

    existing = db.query(Template).filter(Template.title == t["title"], Template.created_by == admin.id).first()
    
    if existing:
        # Update existing template instead of deleting
        existing.description = t["description"]
        existing.content = t["content"]
        existing.category = t["category"]
        existing.is_public = t["is_public"]
        existing.updated_at = datetime.now(timezone.utc)
        db.commit()
        print(f"🔄 Updated: {t['title']}")
    new_t = Template(title=t["title"], description=t["description"], category=t["category"], content=t["content"], is_public=True, created_by=admin.id, version=1)
    db.add(new_t); db.commit()
    print(f"Template '{t['title']}' created with {len(t['content']['sections'])} sections!"); db.close()

if __name__ == "__main__":
    seed_diarrhoea()
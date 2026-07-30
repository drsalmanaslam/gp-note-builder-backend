from app.database import SessionLocal
from app.models import User, Template, Category

def seed_pruritis_ani():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Gastroenterology").first()
    if not category: category = Category(name="Gastroenterology"); db.add(category); db.commit()

    t = {
        "title": "Pruritis Ani",
        "description": "Focused assessment for pruritis ani covering threadworm, dermatological, and hygiene-related causes with structured management advice.",
        "category": "Gastroenterology",
        "content": {"sections": [
            {
                "title": "Symptom Profile",
                "section_type": "history",
                "questions": [
                    {"id": "pa_presenting_complaint", "type": "text", "label": "Presenting Complaint", "required": True, "placeholder": "e.g., Persistent anal itching, worse at night"},
                    {"id": "pa_pattern", "type": "single_select", "label": "Symptom Pattern", "required": True, "options": ["Intermittent", "Persistent"]},
                    {"id": "pa_nocturnal", "type": "toggle", "label": "Worse at Night? (Threadworm - Enterobius vermicularis)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Nocturnal itch = ?threadworm infestation. Treat with Mebendazole. Treat whole family.", "red_flag_negative": ""},
                    {"id": "pa_aggravating", "type": "multi_select", "label": "Aggravating Factors", "required": False, "options": ["Spicy food", "Post-defaecation", "Stress", "Clothing (tight/synthetic)"]},
                    {"id": "pa_relieving", "type": "multi_select", "label": "Relieving Factors", "required": False, "options": ["Emollients", "Anaesthetic cream", "None identified"]}
                ]
            },
            {
                "title": "Hygiene & Risk Factors",
                "section_type": "history",
                "questions": [
                    {"id": "pa_hygiene", "type": "single_select", "label": "Hygiene Practices", "required": True, "options": ["Excessive washing / over-cleaning", "Does not wash excessively", "Uses soaps / perfumes / wipes"]},
                    {"id": "pa_gi_symptoms", "type": "multi_select", "label": "GI Symptoms", "required": True, "options": ["Constipation", "Worms visible in stool", "Piles / haemorrhoids", "Pain on passing stool", "None present"]},
                    {"id": "pa_anorectal", "type": "multi_select", "label": "Anorectal Symptoms", "required": True, "options": ["PR bleeding", "Pain", "Straining", "Hard stools", "Diarrhoea", "Piles", "Mucus", "Fevers", "None present"]},
                    {"id": "pa_contacts", "type": "multi_select", "label": "Contact / Transmission History", "required": False, "options": ["Other family members itchy", "Anal sex", "Neither"]},
                    {"id": "pa_dermatological", "type": "multi_select", "label": "Dermatological History", "required": False, "options": ["Psoriasis", "Eczema", "Urticaria", "None"]}
                ]
            },
            {
                "title": "Red Flags",
                "section_type": "history",
                "questions": [
                    {"id": "pa_red_flags", "type": "multi_select", "label": "Red Flag Screen", "required": True, "options": ["Tenesmus", "Weight loss", "Neither present"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Tenesmus + weight loss + itch = ?colorectal cancer. Urgent 2WW referral.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "pa_inspection", "type": "multi_select", "label": "Perianal Inspection", "required": True, "options": ["Perianal rash / erythema", "Skin tags / sentinel pile", "Excoriation (scratch marks)", "Neither present"]},
                    {"id": "pa_dre", "type": "single_select", "label": "DRE", "required": False, "options": ["No rectal wall abnormalities", "Abnormality noted", "Not performed"]}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "Idiopathic Pruritis Ani",
                    "Threadworm Infestation (Enterobius vermicularis - nocturnal itch)",
                    "Contact Dermatitis (soaps, wipes, perfumes)",
                    "Haemorrhoids",
                    "Anal Fissure",
                    "Psoriasis / Eczema (perianal)",
                    "Candidiasis",
                    "Diabetes Mellitus (HbA1c)",
                    "Colorectal Cancer (RED FLAG - tenesmus, weight loss)",
                    "Faecal Incontinence / Soiling"
                ],
                "questions": [
                    {"id": "pa_diagnosis", "type": "single_select", "label": "Clinical Impression", "required": True, "options": ["Pruritis Ani - idiopathic / hygiene-related", "Threadworm infestation suspected", "Dermatological cause suspected", "Haemorrhoids contributing", "Diabetes-related (pending HbA1c)", "Suspected malignancy - URGENT 2WW"]}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Return if not improving after 2-4 weeks of conservative measures, or if red flags develop (tenesmus, weight loss, bleeding). Hygiene: wash anus after bowel movement with wet toilet paper (not dry), avoid rubbing, avoid soaps/wipes/perfumes, wear cotton underwear, avoid bio washing powders, avoid scratching, cut nails short. Diet: avoid spicy/chilli foods, tomatoes, decrease caffeine. Pharmacotherapy: Instillagel (lidocaine + chlorhexidine) for symptomatic relief. If threadworm suspected: Mebendazole 100mg stat, repeat at 2 weeks. Treat all family members. Check HbA1c if diabetes suspected.",
                "questions": [
                    {"id": "pa_hygiene_advice", "type": "multi_select", "label": "Hygiene Advice", "required": False, "options": ["Wash anus after bowel movement with wet toilet paper", "Avoid rubbing", "Avoid soaps / wipes / perfumes", "Wear cotton underwear", "Avoid bio washing powders", "Avoid scratching", "Cut nails short"]},
                    {"id": "pa_diet", "type": "multi_select", "label": "Dietary Advice", "required": False, "options": ["Avoid spicy / chilli foods", "Avoid tomatoes", "Decrease caffeine intake"]},
                    {"id": "pa_rx", "type": "single_select", "label": "Pharmacotherapy", "required": False, "options": ["Instillagel (Lidocaine + Chlorhexidine)", "Mebendazole 100mg stat + repeat 2 weeks (threadworm)", "Mild hydrocortisone 1% (short course)", "None"]},
                    {"id": "pa_hba1c", "type": "toggle", "label": "HbA1c Ordered? (If diabetes suspected)", "required": False},
                    {"id": "pa_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., Review in 2-4 weeks if not improving, sooner if red flags"}
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
    seed_pruritis_ani()
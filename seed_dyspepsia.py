from app.database import SessionLocal
from app.models import User, Template, Category

def seed_dyspepsia():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Gastroenterology").first()
    if not category: category = Category(name="Gastroenterology"); db.add(category); db.commit()

    t = {
        "title": "Dyspepsia / GORD",
        "description": "Focused assessment for dyspepsia and GORD covering symptom differentiation, alarm features for malignancy, PPI therapy, H. pylori testing, and lifestyle advice.",
        "category": "Gastroenterology",
        "content": {"sections": [
            {
                "title": "Symptom Profile",
                "section_type": "history",
                "questions": [
                    {"id": "dysp_presenting_complaint", "type": "text", "label": "Presenting Complaint", "required": True, "placeholder": "e.g., Epigastric burning and bloating for 1 week"},
                    {"id": "dysp_duration", "type": "text", "label": "Duration of Symptoms", "required": True, "placeholder": "e.g., 1 week"},
                    {"id": "dysp_symptoms", "type": "multi_select", "label": "Presenting Symptoms", "required": True, "options": ["Epigastric pain / burning", "Retrosternal discomfort (heartburn)", "Bloating", "Burping", "Bad taste in mouth", "Waterbrash (excess salivation)"]},
                    {"id": "dysp_aggravating", "type": "multi_select", "label": "Aggravating Factors", "required": False, "options": ["Spicy food", "Alcohol", "Hot caffeinated drinks", "Lying down", "Bending over", "None identified"]},
                    {"id": "dysp_relieving", "type": "single_select", "label": "Relieving Factors", "required": False, "options": ["Milk", "Antacids", "No relieving factor identified"]}
                ]
            },
            {
                "title": "Cardiac & Peptic Ulcer Screening",
                "section_type": "history",
                "questions": [
                    {"id": "dysp_cardiac", "type": "multi_select", "label": "Cardiac / Respiratory Screen", "required": True, "options": ["Chest pain", "Shortness of breath", "Palpitations", "None present"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Chest pain + dyspepsia = ?cardiac. ECG + troponin if acute. Do NOT assume GORD.", "red_flag_negative": ""},
                    {"id": "dysp_exertion", "type": "toggle", "label": "Symptoms Related to Exertion? (Cardiac vs GORD)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Exertional symptoms = ?angina. Cardiac workup before assuming GORD.", "red_flag_negative": ""},
                    {"id": "dysp_ulcer_red_flags", "type": "multi_select", "label": "Peptic Ulcer Red Flags", "required": True, "options": ["Pain radiating to back (?posterior ulcer)", "Black tarry stools (melaena) - RED FLAG", "Neither present"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Melaena = upper GI bleed. Urgent A&E. Pain radiating to back = ?posterior duodenal ulcer.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Malignancy Red Flags & Risk Factors",
                "section_type": "history",
                "questions": [
                    {"id": "dysp_alarm", "type": "multi_select", "label": "Alarm Features (NICE NG12 - 2WW Referral)", "required": True, "options": ["Weight loss", "PR bleeding / melaena", "Dysphagia (difficulty swallowing)", "Vomiting", "None present"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Any alarm feature + dyspepsia = urgent 2WW OGD. Do NOT trial PPI first.", "red_flag_negative": ""},
                    {"id": "dysp_alcohol", "type": "text", "label": "Alcohol Intake (units/week)", "required": False, "placeholder": "e.g., 10"},
                    {"id": "dysp_smoking", "type": "single_select", "label": "Smoking Status", "required": True, "options": ["Current smoker", "Ex-smoker", "Non-smoker"]},
                    {"id": "dysp_family", "type": "multi_select", "label": "Family History", "required": False, "options": ["Gastric / oesophageal cancer", "Peptic ulcer disease", "None"]},
                    {"id": "dysp_pmh_endoscopy", "type": "toggle", "label": "Previous Endoscopy?", "required": False}
                ]
            },
            {
                "title": "Medication Review",
                "section_type": "history",
                "questions": [
                    {"id": "dysp_meds", "type": "multi_select", "label": "Ulcerogenic / GORD-Aggravating Drugs", "required": True, "options": ["NSAIDs (Ibuprofen, Naproxen, Diclofenac)", "SSRIs", "Opioids", "Bisphosphonates (Alendronate)", "Steroids (Prednisolone)", "Calcium Channel Antagonists", "None of the above"], "is_red_flag": True, "red_flag_positive": "RED FLAG: NSAIDs + dyspepsia = stop NSAID + PPI. Consider H. pylori testing.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "dysp_abdo", "type": "single_select", "label": "Abdominal Examination", "required": True, "options": ["Epigastric tenderness on deep palpation, BS present, no masses", "Normal", "Other finding"]}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "Gastro-Oesophageal Reflux Disease (GORD)",
                    "Functional Dyspepsia",
                    "Peptic Ulcer Disease (gastric / duodenal)",
                    "H. pylori-Associated Dyspepsia",
                    "Oesophagitis",
                    "Barrett's Oesophagus",
                    "Gastric / Oesophageal Cancer (RED FLAG)",
                    "Cardiac Chest Pain (RED FLAG - ECG + troponin)",
                    "Gallstone Disease",
                    "Pancreatitis"
                ],
                "questions": [
                    {"id": "dysp_diagnosis", "type": "single_select", "label": "Clinical Impression", "required": True, "options": ["GORD", "Dyspepsia - uninvestigated", "Peptic ulcer disease suspected", "Red flag features present - URGENT 2WW OGD"]}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Return if: no improvement after 4 weeks of PPI, alarm features develop (weight loss, dysphagia, vomiting, melaena), or symptoms worsen. PPI: take 30 minutes before breakfast for optimal effect. 1-month trial then review. H. pylori breath test: book morning appointment. Fast for 6 hours before. Avoid antibiotics for 4 weeks and PPIs for 2 weeks before test. Lifestyle: elevate head of bed, sleep on left side, avoid late eating (<3h before bed), smaller meals, avoid fatty foods, reduce alcohol/caffeine/spicy foods, weight reduction, stop smoking.",
                "questions": [
                    {"id": "dysp_ppi", "type": "single_select", "label": "PPI Therapy", "required": False, "options": ["Pantoprazole 20mg OD 30 min before breakfast for 1 month", "Omeprazole 20mg OD for 1 month", "Lansoprazole 30mg OD for 1 month", "Esomeprazole 20mg OD for 1 month", "Not prescribed"]},
                    {"id": "dysp_alginate", "type": "single_select", "label": "Alginate / Antacid", "required": False, "options": ["Acidex 10ml TDS after food + before bed", "Gaviscon 10ml TDS", "None"]},
                    {"id": "dysp_lifestyle", "type": "multi_select", "label": "Lifestyle Advice", "required": False, "options": ["Elevate head of bed", "Sleep on left side", "Avoid late eating (<3h before bed)", "Smaller meals", "Avoid fatty foods", "Weight reduction", "Reduce smoking", "Reduce alcohol", "Reduce caffeine", "Reduce orange juice", "Chew gum (increases saliva/bicarbonate)"]},
                    {"id": "dysp_hpylori", "type": "toggle", "label": "H. pylori Breath Test Arranged? (If no improvement at 4 weeks)", "required": False},
                    {"id": "dysp_hpylori_prep", "type": "toggle", "label": "Preparation Instructions Given? (Fast 6h, no abx 4/52, no PPI 2/52)", "required": False},
                    {"id": "dysp_investigations", "type": "multi_select", "label": "Investigations (If No Improvement)", "required": False, "options": ["FBC", "CRP", "Coeliac screen", "Bone/Liver profile", "H. pylori breath test", "OGD (endoscopy)", "None"]},
                    {"id": "dysp_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., Review at 4 weeks if no improvement, sooner if red flags"}
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
    seed_dyspepsia()
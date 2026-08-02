from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_anal_fissure():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Gastroenterology").first()
    if not category: category = Category(name="Gastroenterology"); db.add(category); db.commit()

    t = {
        "title": "Anal Fissure",
        "description": "Focused assessment for anal fissure covering differentiation from haemorrhoids, examination findings, and stepwise management from conservative to surgical.",
        "category": "Gastroenterology",
        "content": {"sections": [
            {
                "title": "Presenting Symptoms",
                "section_type": "history",
                "questions": [
                    {"id": "af_presenting_complaint", "type": "text", "label": "Presenting Complaint", "required": True, "placeholder": "e.g., Severe sharp pain on defaecation with bright red blood on wiping"},
                    {"id": "af_symptoms", "type": "multi_select", "label": "Presenting Symptoms", "required": True, "options": ["Anal discomfort", "Bright red blood on toilet paper on wiping", "Acute severe pain on defaecation (like passing glass)", "Dragging sensation throughout the day (?haemorrhoids)"]},
                    {"id": "af_pain_pattern", "type": "single_select", "label": "Pain Pattern", "required": True, "options": ["Acute, severe, sharp pain on defaecation, subsiding 1-2 hours after (FISSURE)", "Constant / dragging sensation (?HAEMORRHOIDS)", "Painless bleeding only"]}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "af_abdo", "type": "single_select", "label": "Abdominal Examination", "required": False, "options": ["Soft, non-tender, no organomegaly, BS present", "Abnormal finding"]},
                    {"id": "af_pr_tolerated", "type": "single_select", "label": "PR Examination", "required": True, "options": ["Too painful for full PR exam", "PR exam tolerated"]},
                    {"id": "af_pr_findings", "type": "multi_select", "label": "Visualised / Palpated Findings", "required": False, "options": ["Area of induration at 6 o'clock", "Area of induration at 12 o'clock", "Sentinel skin tag present", "Fissure directly visualised", "Tenderness on palpation"]}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "Anal Fissure (acute - <6 weeks)",
                    "Anal Fissure (chronic - >6 weeks)",
                    "Haemorrhoids (dragging sensation, painless bleeding)",
                    "Perianal Abscess",
                    "Fistula-in-Ano",
                    "Anorectal Malignancy (RED FLAG - atypical location, mass)",
                    "Crohn's Disease (atypical fissures - lateral, painless)",
                    "Sexually Transmitted Proctitis"
                ],
                "questions": [
                    {"id": "af_diagnosis", "type": "single_select", "label": "Clinical Impression", "required": True, "options": ["Anal Fissure - Acute", "Anal Fissure - Chronic", "Haemorrhoids", "Other anorectal pathology"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Lateral fissure or atypical location = ?Crohn's, malignancy, STI. Urgent colorectal referral.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Return in 4-6 weeks for PR exam if not resolved. Sooner if worsening symptoms or new bleeding. Mechanism: fissures caused by increased pressure from hard stool passage → reduced local blood flow → impaired healing. First-line: stool softeners (Macrogols) + topical treatment (Anusol / Proctosedyl). Second-line (if not resolving at 4-6 weeks): Rectogesic (GTN) BD for 6 weeks (warn re headaches) OR Diltiazem cream (Anoheal) for 6 weeks (similar efficacy 60-70%, more expensive, fridge storage). If topical treatment fails: refer for Botox injection or surgical sphincterotomy (risk of continence problems).",
                "questions": [
                    {"id": "af_mechanism_explained", "type": "toggle", "label": "Mechanism Explained? (Hard stool → increased pressure → reduced blood flow)", "required": True},
                    {"id": "af_stool_softener", "type": "single_select", "label": "Stool Softener", "required": False, "options": ["Macrogols PO (e.g., Movicol)", "Lactulose", "None"]},
                    {"id": "af_topical_first_line", "type": "multi_select", "label": "Topical Treatment (First-Line)", "required": False, "options": ["Anusol ointment", "Proctosedyl suppository", "None"]},
                    {"id": "af_topical_second_line", "type": "single_select", "label": "Second-Line (If Not Resolving at 4-6 Weeks)", "required": False, "options": ["Rectogesic (GTN) BD for 6 weeks - warn re headaches", "Diltiazem cream (Anoheal) for 6 weeks - fridge storage", "Not yet - continue first-line"]},
                    {"id": "af_escalation", "type": "single_select", "label": "Escalation (If Topical Treatment Fails)", "required": False, "options": ["Continue topical treatment", "Refer for Botox injection", "Refer for surgical sphincterotomy", "Refer colorectal surgery"]},
                    {"id": "af_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., 4-6 weeks for PR exam, sooner if worsening"}
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
    seed_anal_fissure()
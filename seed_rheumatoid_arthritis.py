from app.database import SessionLocal
from app.models import User, Template, Category

def seed_rheumatoid_arthritis():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Musculoskeletal").first()
    if not category: category = Category(name="Musculoskeletal"); db.add(category); db.commit()

    t = {
        "title": "Rheumatoid Arthritis - Initial",
        "description": "Comprehensive RA assessment covering diagnostic criteria (>6 weeks, bilateral small joints), immunopathology workup, rheumatology referral pathway, and DMARD monitoring protocols.",
        "category": "Musculoskeletal",
        "content": {"sections": [
            {
                "title": "History",
                "section_type": "history",
                "questions": [
                    {"id": "ra_duration", "type": "single_select", "label": "Duration of Symptoms (Must Be >6 Weeks - Key Distinguishing Feature)", "required": True, "options": [">6 Weeks - Consistent with Inflammatory Arthritis", "<6 Weeks - May Be Self-Limiting / Reactive"], "is_red_flag": True, "red_flag_positive": "RED FLAG: >6 weeks = consistent with RA. <6 weeks = may be viral/reactive.", "red_flag_negative": ""},
                    {"id": "ra_distribution", "type": "multi_select", "label": "Joint Distribution", "required": True, "options": ["Bilateral", "Small Joints of Hands (MCP, PIP)", "Wrists", "Feet (MTP)", "Knees", "Shoulders"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Bilateral small joint involvement = classic RA pattern.", "red_flag_negative": ""},
                    {"id": "ra_recent_infection", "type": "toggle", "label": "Recent Infective Illness? (?Reactive Arthritis)", "required": False},
                    {"id": "ra_morning_stiffness", "type": "text", "label": "Morning Stiffness Duration (Typically ≥30 Min to Loosen Out in Inflammatory Arthritis)", "required": True, "placeholder": "e.g., 60 minutes"},
                    {"id": "ra_functional", "type": "toggle", "label": "Difficulty with Fine Motor Tasks? (Buttons, Jar Lids)", "required": True},
                    {"id": "ra_axial", "type": "toggle", "label": "Back Pain or Stiffness? (?Axial Involvement)", "required": False},
                    {"id": "ra_sjogrens", "type": "multi_select", "label": "Sjögren's Screen", "required": True, "options": ["Dry Eyes", "Dry Mouth", "None"]},
                    {"id": "ra_associated", "type": "multi_select", "label": "Extra-Articular / Associated Conditions", "required": True, "options": ["Personal History Psoriasis", "Family History Psoriasis", "Colitis / IBD", "Uveitis", "None"]}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "ra_temp", "type": "number", "label": "Temperature (°C)", "required": False, "placeholder": "e.g., 37.1"},
                    {"id": "ra_hr", "type": "number", "label": "Pulse (bpm)", "required": False, "placeholder": "e.g., 78"},
                    {"id": "ra_grip", "type": "toggle", "label": "Able to Make a Fist?", "required": True},
                    {"id": "ra_mcp_squeeze", "type": "single_select", "label": "Metacarpal Squeeze Test", "required": True, "options": ["Positive (Tender) - Inflammatory", "Negative"]},
                    {"id": "ra_synovitis", "type": "toggle", "label": "Boggy Swelling / Synovitis in Small Joints of Hands?", "required": True},
                    {"id": "ra_psoriasis", "type": "toggle", "label": "Psoriasis on Skin?", "required": False},
                    {"id": "ra_nodules", "type": "toggle", "label": "Firm/Hard Nodules on Extensor Surfaces? (Rheumatoid Nodules)", "required": False},
                    {"id": "ra_lymph", "type": "multi_select", "label": "Lymphadenopathy", "required": False, "options": ["Axillary", "Inguinal", "Cervical", "None"]}
                ]
            },
            {
                "title": "Investigations",
                "section_type": "assessment",
                "differentials": [
                    "Rheumatoid Arthritis (Bilateral, Small Joints, >6 Weeks, RF/anti-CCP Positive)",
                    "Psoriatic Arthritis (Psoriasis, DIP Joints, Nail Changes)",
                    "Reactive Arthritis (Recent Infection, Asymmetrical, Self-Limiting)",
                    "Gout / Pseudogout (Acute Monoarthritis, Tophi, Crystals)",
                    "SLE / Connective Tissue Disease (ANA Positive, Multi-System)",
                    "Osteoarthritis (DIP/PIP, Heberden's/Bouchard's Nodes, No Synovitis)",
                    "Polymyalgia Rheumatica (Shoulder/Pelvic Girdle, Age >50, Raised ESR)"
                ],
                "questions": [
                    {"id": "ra_bloods", "type": "multi_select", "label": "Immunopathology Form - Annotate '?Inflammatory Arthritis'", "required": False, "options": ["Rheumatoid Factor (RF - Positive in ~70% RA, Negative Does NOT Exclude)", "Anti-CCP (Anti-Cyclic Citrullinated Peptide - More Specific)", "CRP / ESR", "ANA / ANF", "ANCA", "Renal / Bone Profile", "FBC", "Haematinics / Iron Studies", "Uric Acid"]},
                    {"id": "ra_xray", "type": "toggle", "label": "X-Ray Hands + Feet Requested?", "required": True},
                    {"id": "ra_rf_note", "type": "toggle", "label": "Note: RF Positive in ~70% RA - Negative Does NOT Exclude Diagnosis", "required": False}
                ]
            },
            {
                "title": "Referral & Symptomatic Management",
                "section_type": "plan",
                "safety_netting": "Refer to rheumatology using ISR referral form: https://www.isr.ie/wp-content/uploads/2018/02/attachment_ISR_Interactive_Referral_Form1.pdf. Symptomatic management pending referral: NSAID for symptom control (Naproxen/Ibuprofen if no CI). Tears Naturale or Lacrilube if dry eyes present. Lifestyle: Mediterranean diet, smoking cessation. RAISE app - helps patients monitor RA symptoms. Specialist treatment pathway: combination methotrexate + another DMARD (sulfasalazine, hydroxychloroquine, or azathioprine) + oral prednisolone. Biologics first-line if: erosive arthropathy on X-ray, OR high CRP, OR high ESR. Azathioprine protocol: check TPMT before starting, 50mg OD week 1 → 50mg BD if bloods normal. Reduce to 1/3 if starting allopurinol. Avoid trimethoprim. Monitor FBC + LFT weekly x6 weeks → fortnightly x6 weeks → monthly → 2-3 monthly once stable.",
                "questions": [
                    {"id": "ra_diagnosis", "type": "single_select", "label": "Impression", "required": True, "options": ["Inflammatory Arthritis - ?RA (Consistent History + Exam)", "?Psoriatic Arthritis", "?Reactive Arthritis", "?SLE / Connective Tissue Disease", "Awaiting Investigations"]},
                    {"id": "ra_referral", "type": "toggle", "label": "Rheumatology Referral Sent? (ISR Form)", "required": True},
                    {"id": "ra_nsaid", "type": "toggle", "label": "NSAID for Symptom Control? (Pending Rheumatology)", "required": False},
                    {"id": "ra_dry_eyes", "type": "toggle", "label": "Tears Naturale / Lacrilube if Dry Eyes?", "required": False},
                    {"id": "ra_lifestyle", "type": "multi_select", "label": "Lifestyle Advice", "required": False, "options": ["Mediterranean Diet", "Smoking Cessation", "RAISE App for Symptom Monitoring"]},
                    {"id": "ra_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., Await rheumatology OPD, review with bloods + X-ray results"}
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
    seed_rheumatoid_arthritis()
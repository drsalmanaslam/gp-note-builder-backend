from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_vertigo_dizziness():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "ENT").first()
    if not category: category = Category(name="ENT"); db.add(category); db.commit()

    t = {
        "title": "Vertigo / Dizziness (HINTS Exam)",
        "description": "Comprehensive dizziness assessment covering dizziness vs vertigo differentiation, HINTS examination for central causes, and posterior circulation stroke exclusion.",
        "category": "ENT",
        "content": {"sections": [
            {
                "title": "KEY DISTINCTION - Dizziness vs Vertigo",
                "section_type": "history",
                "questions": [
                    {"id": "vert_type", "type": "single_select", "label": "What Is the Patient Describing?", "required": True, "options": ["Dizziness - Unsteadiness / Light-Headedness (No Spinning)", "Vertigo - Sensation Everything Is Spinning (Debilitating)"]}
                ]
            },
            {
                "title": "RED FLAGS - Central / Stroke Features (Screen First)",
                "section_type": "history",
                "questions": [
                    {"id": "vert_visual_blurring", "type": "toggle", "label": "Visual Blurring / Diplopia?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Visual symptoms + vertigo = ?posterior circulation stroke. URGENT A&E.", "red_flag_negative": ""},
                    {"id": "vert_dysarthria", "type": "toggle", "label": "Dysarthria (Slurred Speech)?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Dysarthria + vertigo = ?brainstem stroke. URGENT A&E.", "red_flag_negative": ""},
                    {"id": "vert_numbness", "type": "toggle", "label": "Numbness / Paraesthesia?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Focal neurology + vertigo = ?CVA. URGENT A&E.", "red_flag_negative": ""},
                    {"id": "vert_dysphagia", "type": "toggle", "label": "Dysphagia?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Dysphagia + vertigo = ?brainstem stroke. URGENT A&E.", "red_flag_negative": ""},
                    {"id": "vert_ataxia", "type": "toggle", "label": "Unsteadiness / Ataxia?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Ataxia + vertigo = ?cerebellar stroke. URGENT A&E.", "red_flag_negative": ""},
                    {"id": "vert_vomiting", "type": "toggle", "label": "Severe Vomiting?", "required": False}
                ]
            },
            {
                "title": "History",
                "section_type": "history",
                "questions": [
                    {"id": "vert_presenting_complaint", "type": "text", "label": "Presenting Complaint", "required": True, "placeholder": "e.g., Sudden spinning sensation lasting hours"},
                    {"id": "vert_onset", "type": "single_select", "label": "Onset", "required": True, "options": ["Sudden (Seconds/Minutes)", "Gradual (Hours/Days)"]},
                    {"id": "vert_character", "type": "single_select", "label": "Character of Spinning", "required": False, "options": ["Horizontal", "Vertical (RED FLAG - Central)", "Rotatory / Torsional", "Uncertain"]},
                    {"id": "vert_severity", "type": "single_select", "label": "Severity (0-10)", "required": True, "options": ["Mild (1-3)", "Moderate (4-6)", "Severe (7-9)", "Debilitating (10)"]},
                    {"id": "vert_pattern", "type": "single_select", "label": "Pattern", "required": True, "options": ["Continuous (Hours-Days) - ?Vestibular Neuritis", "Intermittent / Episodic - Each Episode", "Seconds (<30 sec) - ?BPPV", "Minutes-Hours - ?Ménière's", "Days - ?Labyrinthitis"]},
                    {"id": "vert_eyes_closed", "type": "single_select", "label": "Effect of Sitting Still with Eyes Closed", "required": False, "options": ["Improves (Peripheral)", "No change (Central Concern)"]},
                    {"id": "vert_preceding_urti", "type": "toggle", "label": "Preceding URTI?", "required": False},
                    {"id": "vert_cardiac", "type": "multi_select", "label": "Cardiac / Autonomic Screen", "required": True, "options": ["Pre-syncope / light-headedness", "Warmth / diaphoresis", "Nausea", "Palpitations", "Chest pain", "Dyspnoea", "None"]},
                    {"id": "vert_postural_instability", "type": "toggle", "label": "Postural Instability?", "required": True},
                    {"id": "vert_otological", "type": "multi_select", "label": "Otological Symptoms", "required": True, "options": ["Hearing loss", "Ear discharge", "Tinnitus", "Ear fullness", "None"]},
                    {"id": "vert_headache", "type": "toggle", "label": "Headache? (?Migrainous Vertigo)", "required": False},
                    {"id": "vert_migraine_history", "type": "toggle", "label": "History of Migraine?", "required": False},
                    {"id": "vert_head_trauma", "type": "toggle", "label": "Recent Head Trauma?", "required": False},
                    {"id": "vert_positional_trigger", "type": "toggle", "label": "Provoked by Position Changes? (?BPPV)", "required": True},
                    {"id": "vert_occupational_driving", "type": "toggle", "label": "Occupational Driving? (Bus Driver etc. - Relevant to Driving Advice)", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Must advise NOT to drive until symptoms fully resolve. Inform DVLA if relevant.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "vert_gait", "type": "single_select", "label": "Gait", "required": True, "options": ["Normal", "Abnormal / unsteady - RED FLAG", "Unable to stand unaided - RED FLAG"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Unable to stand = ?cerebellar stroke. URGENT A&E.", "red_flag_negative": ""},
                    {"id": "vert_romberg", "type": "single_select", "label": "Romberg's Test", "required": False, "options": ["Negative (Steady)", "Positive (Falls) - RED FLAG"]},
                    {"id": "vert_cn", "type": "single_select", "label": "Cranial Nerves", "required": True, "options": ["Normal", "Abnormal - RED FLAG"], "is_red_flag": True, "red_flag_positive": "RED FLAG: CN deficit = ?brainstem lesion. URGENT A&E.", "red_flag_negative": ""},
                    {"id": "vert_cerebellar", "type": "single_select", "label": "Cerebellar Exam", "required": True, "options": ["Normal", "Abnormal - RED FLAG"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Cerebellar signs = ?cerebellar stroke. URGENT A&E.", "red_flag_negative": ""},
                    {"id": "vert_pronator_drift", "type": "toggle", "label": "Pronator Drift?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Pronator drift = ?CVA. URGENT A&E.", "red_flag_negative": ""},
                    {"id": "vert_nystagmus", "type": "single_select", "label": "Nystagmus", "required": True, "options": ["None", "Unidirectional - Peripheral", "Bidirectional - RED FLAG (Central)", "Vertical - RED FLAG (Central)"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Bidirectional or vertical nystagmus = CENTRAL cause. URGENT A&E.", "red_flag_negative": ""},
                    {"id": "vert_fundoscopy", "type": "single_select", "label": "Fundoscopy", "required": False, "options": ["Normal", "Abnormal"]},
                    {"id": "vert_tm", "type": "single_select", "label": "Tympanic Membranes", "required": False, "options": ["Normal B/L", "Abnormal", "Cholesteatoma Present"]}
                ]
            },
            {
                "title": "HINTS Examination (Acute Continuous Vertigo + Nystagmus Only)",
                "section_type": "examination",
                "questions": [
                    {"id": "vert_hints_head_impulse", "type": "single_select", "label": "Head Impulse Test", "required": False, "options": ["Abnormal (Corrective Saccade) → PERIPHERAL", "Normal → CENTRAL Concern (Proceed to Nystagmus + Skew)", "Not performed (Episodic Vertigo)"]},
                    {"id": "vert_hints_nystagmus", "type": "single_select", "label": "Nystagmus Direction", "required": False, "options": ["Unidirectional → PERIPHERAL (Reassuring)", "Bidirectional → CENTRAL (Highly Specific)", "Not applicable"]},
                    {"id": "vert_hints_skew", "type": "single_select", "label": "Test of Skew", "required": False, "options": ["Negative → PERIPHERAL (Reassuring)", "Positive → CENTRAL (Highly Specific - Often with Vertical Diplopia)", "Not performed"]},
                    {"id": "vert_hints_interpretation", "type": "single_select", "label": "HINTS Interpretation", "required": False, "options": ["PERIPHERAL: Abnormal Head Impulse + Unidirectional Nystagmus + Skew Negative", "CENTRAL: Normal Head Impulse + Nystagmus OR Bidirectional Nystagmus OR Positive Skew → ESCALATE", "Not applicable (Episodic / Non-Continuous Vertigo)"]}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "BPPV (Brief <30 sec, Positional, Dix-Hallpike Positive)",
                    "Vestibular Neuritis (Continuous Days, Preceding URTI, Abnormal Head Impulse)",
                    "Labyrinthitis (Vestibular Neuritis + Hearing Loss)",
                    "Ménière's Disease (Triad: Vertigo + Hearing Loss + Tinnitus, 20 Min-Hours)",
                    "Vestibular Migraine (Headache, Photophobia, Migraine History)",
                    "Posterior Circulation Stroke / TIA (RED FLAG - Central HINTS, Focal Neurology)",
                    "Cerebellar Stroke (RED FLAG - Ataxia, Unable to Stand)",
                    "Brainstem Stroke (RED FLAG - Dysarthria, Dysphagia, Diplopia)",
                    "Orthostatic Hypotension",
                    "Acoustic Neuroma (Unilateral Hearing Loss + Tinnitus)"
                ],
                "questions": [
                    {"id": "vert_diagnosis", "type": "single_select", "label": "Clinical Impression", "required": True, "options": ["Likely Peripheral - BPPV", "Likely Peripheral - Vestibular Neuritis / Labyrinthitis", "Likely Peripheral - Ménière's", "Suspected Central Cause - URGENT A&E (CVA)", "Dizziness (Non-Vertiginous) - ?Cardiac / Orthostatic", "Vestibular Migraine"]}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Return immediately or attend A&E if: visual blurring/diplopia, slurred speech, numbness/weakness, dysphagia, unsteadiness/ataxia, or severe vomiting. Red flags discussed. Do NOT drive until symptoms fully resolve - especially if occupational driving (bus/taxi/HGV). Peripheral causes: BPPV = Epley manoeuvre + Brandt-Daroff exercises. Vestibular neuritis = Prochlorperazine (Stemetil) + reassurance (resolves over days-weeks). Ménière's = Betahistine trial + avoid caffeine/alcohol. Central causes on HINTS = URGENT A&E for CT/MRI brain. If non-vertiginous dizziness: check lying/standing BP, ECG, consider cardiac cause.",
                "questions": [
                    {"id": "vert_driving_advice", "type": "toggle", "label": "Driving Advice Given? (Do NOT Drive Until Symptoms Resolve)", "required": True},
                    {"id": "vert_medication", "type": "single_select", "label": "Medication (Peripheral Cause)", "required": False, "options": ["Prochlorperazine (Stemetil) 5mg TDS PRN", "Betahistine 16mg TDS (Ménière's)", "Cyclizine 50mg TDS PRN", "None"]},
                    {"id": "vert_epley", "type": "toggle", "label": "Epley Manoeuvre Performed? (If BPPV)", "required": False},
                    {"id": "vert_referral", "type": "single_select", "label": "Referral", "required": False, "options": ["None - GP Managed", "ENT (Routine - Persistent Peripheral)", "ENT (Urgent - Unilateral Hearing Loss / Tinnitus)", "A&E (Urgent - Central HINTS / Focal Neurology)"]},
                    {"id": "vert_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., Return if no improvement, ENT referral if persistent, emergency if central signs"}
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
    seed_vertigo_dizziness()
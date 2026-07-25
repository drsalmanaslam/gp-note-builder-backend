from app.database import SessionLocal
from app.models import User, Template, Category

def seed_vertigo_bppv():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "ENT").first()
    if not category: category = Category(name="ENT"); db.add(category); db.commit()

    t = {
        "title": "Vertigo / BPPV Assessment",
        "description": "Focused assessment for acute vertigo with Dix-Hallpike testing, Epley manoeuvre, and red flags for central causes.",
        "category": "ENT",
        "content": {"sections": [
            {
                "title": "Presentation",
                "section_type": "history",
                "questions": [
                    {"id": "vert_presenting_complaint", "type": "text", "label": "Presenting Complaint", "required": True, "placeholder": "e.g., Brief episodes of spinning sensation when turning in bed"},
                    {"id": "vert_age", "type": "number", "label": "Age", "required": True, "placeholder": "e.g., 52"},
                    {"id": "vert_duration_episode", "type": "single_select", "label": "Duration of Each Episode", "required": True, "options": ["<30 seconds (BPPV)", "30 sec - few minutes", "Minutes to hours", "Hours to days", "Constant"]},
                    {"id": "vert_onset", "type": "single_select", "label": "Onset", "required": True, "options": ["Acute (days)", "Subacute (weeks)", "Chronic (months)"]},
                    {"id": "vert_triggers", "type": "multi_select", "label": "Triggers", "required": True, "options": ["Head turns", "Turning over in bed", "Looking up (top shelf)", "Bending forward", "Standing up (orthostatic)", "Spontaneous", "Worse in mornings"]},
                    {"id": "vert_nature", "type": "single_select", "label": "Nature of Vertigo", "required": True, "options": ["Rotational / spinning (true vertigo)", "Lightheaded / floating", "Unsteadiness / imbalance"]}
                ]
            },
            {
                "title": "RED FLAGS - Central & Neurological",
                "section_type": "history",
                "questions": [
                    {"id": "vert_hearing_loss", "type": "toggle", "label": "Hearing Loss?", "required": True},
                    {"id": "vert_tinnitus", "type": "toggle", "label": "Tinnitus?", "required": True},
                    {"id": "vert_ear_fullness", "type": "toggle", "label": "Ear Fullness / Pressure?", "required": False},
                    {"id": "vert_headache", "type": "toggle", "label": "Headache?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Headache + vertigo = ?posterior circulation stroke, migraine. Urgent neurological assessment.", "red_flag_negative": ""},
                    {"id": "vert_focal_weakness", "type": "toggle", "label": "Focal Weakness / Numbness?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Focal neurology + vertigo = ?stroke/TIA. Emergency A&E referral.", "red_flag_negative": ""},
                    {"id": "vert_dysarthria", "type": "toggle", "label": "Dysarthria (Slurred Speech)?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Dysarthria + vertigo = ?brainstem stroke. Emergency.", "red_flag_negative": ""},
                    {"id": "vert_diplopia", "type": "toggle", "label": "Diplopia (Double Vision)?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Diplopia + vertigo = ?brainstem/cerebellar stroke. Emergency.", "red_flag_negative": ""},
                    {"id": "vert_vomiting", "type": "toggle", "label": "Severe Vomiting?", "required": False},
                    {"id": "vert_gait_instability", "type": "toggle", "label": "Gait Instability / Unable to Walk?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Unable to walk + vertigo = ?cerebellar stroke. Emergency A&E.", "red_flag_negative": ""},
                    {"id": "vert_head_injury", "type": "toggle", "label": "Recent Head Injury?", "required": False}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "vert_otoscopy", "type": "single_select", "label": "Otoscopy", "required": True, "options": ["B/L tympanic membranes normal", "Right abnormal", "Left abnormal", "Not examined"]},
                    {"id": "vert_nystagmus_spontaneous", "type": "single_select", "label": "Spontaneous Nystagmus", "required": True, "options": ["None", "Horizontal", "Vertical", "Rotatory/Torsional"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Spontaneous vertical nystagmus = central cause (brainstem/cerebellar). Urgent neurology.", "red_flag_negative": ""},
                    {"id": "vert_dix_hallpike", "type": "single_select", "label": "Dix-Hallpike Test", "required": True, "options": ["Not performed", "POSITIVE - geotropic torsional nystagmus + latency", "POSITIVE - other pattern", "NEGATIVE"]},
                    {"id": "vert_dix_hallpike_side", "type": "single_select", "label": "Positive Side", "required": False, "options": ["Right", "Left", "B/L", "Not applicable"]},
                    {"id": "vert_gait", "type": "single_select", "label": "Gait", "required": True, "options": ["Normal", "Unsteady - cerebellar", "Unable to walk - RED FLAG"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Unable to walk = ?cerebellar stroke. Emergency.", "red_flag_negative": ""},
                    {"id": "vert_romberg", "type": "single_select", "label": "Romberg Test", "required": False, "options": ["Negative (steady)", "Positive (falls) - RED FLAG", "Not tested"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Positive Romberg = ?central or proprioceptive cause.", "red_flag_negative": ""},
                    {"id": "vert_cranial_nerves", "type": "toggle", "label": "Cranial Nerves Intact?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Cranial nerve deficit = ?stroke/TIA. Emergency A&E.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "Benign Paroxysmal Positional Vertigo (BPPV) - Most Common",
                    "Vestibular Neuritis / Labyrinthitis",
                    "Meniere's Disease (triad: vertigo + tinnitus + hearing loss)",
                    "Vestibular Migraine",
                    "Posterior Circulation Stroke / TIA (RED FLAG)",
                    "Brainstem / Cerebellar Stroke (RED FLAG)",
                    "Acoustic Neuroma (vestibular schwannoma)",
                    "Orthostatic Hypotension",
                    "Cervicogenic Dizziness"
                ],
                "questions": [
                    {"id": "vert_diagnosis", "type": "single_select", "label": "Working Diagnosis", "required": True, "options": ["BPPV - posterior canal", "BPPV - horizontal canal", "Vestibular neuritis", "Meniere's disease", "Vestibular migraine", "Suspected central cause - REFER EMERGENCY", "Uncertain"]}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Return immediately if: severe vomiting, new neurological symptoms (weakness, numbness, speech difficulty, diplopia), gait unsteadiness / unable to walk, or severe headache. After Epley: avoid sudden head posture changes for 24-48 hours. Sleep with head raised on 2-3 pillows tonight. Do not drive if feeling dizzy. Brandt-Daroff exercises: perform 3 times daily for 2 weeks. If symptoms persist >4 weeks despite exercises - refer ENT/Audiology for further assessment. BPPV often recurs - teach self-Epley for future episodes.",
                "questions": [
                    {"id": "vert_epley", "type": "toggle", "label": "Epley Manoeuvre Performed Today?", "required": True},
                    {"id": "vert_epley_tolerated", "type": "toggle", "label": "Epley Tolerated Well?", "required": False},
                    {"id": "vert_brandt_daroff", "type": "toggle", "label": "Brandt-Daroff Exercises Explained?", "required": True},
                    {"id": "vert_post_epley_advice", "type": "toggle", "label": "Post-Epley Advice Given? (Avoid head movement, sleep upright)", "required": False},
                    {"id": "vert_medication", "type": "single_select", "label": "Medication (if needed)", "required": False, "options": ["None", "Prochlorperazine (Stemetil) 5mg TDS PRN", "Betahistine 16mg TDS (Meniere's)", "Cinnarizine 15mg TDS PRN"]},
                    {"id": "vert_referral", "type": "single_select", "label": "Referral", "required": False, "options": ["None", "ENT / Audiology (if persistent >4 weeks)", "Neurology (urgent - central cause)", "A&E (emergency - ?stroke)"]},
                    {"id": "vert_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., 4 weeks if not resolved, sooner if red flags"}
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
    seed_vertigo_bppv()
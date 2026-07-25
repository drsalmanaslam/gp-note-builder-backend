from app.database import SessionLocal
from app.models import User, Template, Category

def seed_ear_wax():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "ENT").first()
    if not category: category = Category(name="ENT"); db.add(category); db.commit()

    t = {
        "title": "Ear Wax / Impacted Cerumen Assessment",
        "description": "Focused assessment for ear wax impaction with otoscopy findings, red flags for perforation, and management including microsuction/irrigation criteria.",
        "category": "ENT",
        "content": {"sections": [
            {
                "title": "Presentation",
                "section_type": "history",
                "questions": [
                    {"id": "wax_presenting_complaint", "type": "text", "label": "Presenting Complaint", "required": True, "placeholder": "e.g., Ear pressure/fullness and reduced hearing in right ear"},
                    {"id": "wax_age", "type": "number", "label": "Age", "required": True, "placeholder": "e.g., 45"},
                    {"id": "wax_side", "type": "single_select", "label": "Affected Ear", "required": True, "options": ["Right", "Left", "Both"]},
                    {"id": "wax_duration", "type": "text", "label": "Duration", "required": True, "placeholder": "e.g., 2 weeks"},
                    {"id": "wax_symptoms", "type": "multi_select", "label": "Symptoms", "required": True, "options": ["Ear pressure/fullness", "Conductive hearing loss (mild)", "Muffled hearing", "Itching", "Tinnitus (mild)", "None - incidental finding"]},
                    {"id": "wax_cotton_buds", "type": "toggle", "label": "Using Cotton Buds / Inserting Objects?", "required": True}
                ]
            },
            {
                "title": "RED FLAGS - Must Exclude",
                "section_type": "history",
                "questions": [
                    {"id": "wax_otalgia", "type": "toggle", "label": "Otalgia (Ear Pain)?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Ear pain = ?otitis externa/media. Examine for infection before irrigation.", "red_flag_negative": ""},
                    {"id": "wax_otorrhoea", "type": "toggle", "label": "Active Otorrhoea / Discharge?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Discharge = ?infection or perforation. Do NOT irrigate. Treat infection first.", "red_flag_negative": ""},
                    {"id": "wax_bleeding", "type": "toggle", "label": "Bleeding from Ear?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Bleeding = ?trauma, perforation, or tumour. Do NOT irrigate. Urgent ENT.", "red_flag_negative": ""},
                    {"id": "wax_sudden_hearing_loss", "type": "toggle", "label": "Sudden Sensorineural Hearing Loss?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Sudden hearing loss = ENT EMERGENCY. Same-day referral. Not wax-related.", "red_flag_negative": ""},
                    {"id": "wax_vertigo", "type": "toggle", "label": "Vertigo / Dizziness?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Vertigo + ear symptoms = ?labyrinthitis, Meniere's, or cholesteatoma. ENT referral.", "red_flag_negative": ""},
                    {"id": "wax_tinnitus_new", "type": "toggle", "label": "New Onset Tinnitus? (Especially unilateral/pulsatile)", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Unilateral tinnitus = ?acoustic neuroma. ENT referral if persistent.", "red_flag_negative": ""},
                    {"id": "wax_facial_weakness", "type": "toggle", "label": "Facial Nerve Weakness?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Facial weakness = ?cholesteatoma, malignancy, Ramsay Hunt. Urgent ENT.", "red_flag_negative": ""},
                    {"id": "wax_previous_surgery", "type": "toggle", "label": "Previous Ear Surgery? (Mastoidectomy, grommets, tympanoplasty)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Previous ear surgery = do NOT irrigate. Refer ENT for microsuction.", "red_flag_negative": ""},
                    {"id": "wax_perforation_history", "type": "toggle", "label": "History of TM Perforation?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Known/suspected perforation = do NOT irrigate. Water in middle ear = infection risk. ENT for microsuction.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "wax_otoscopy_right", "type": "single_select", "label": "Otoscopy - Right Ear", "required": True, "options": ["Normal - no wax", "Partial wax occlusion", "Complete wax occlusion (TM not visible)", "TM visible - normal", "TM visible - abnormal", "Not examined"]},
                    {"id": "wax_otoscopy_left", "type": "single_select", "label": "Otoscopy - Left Ear", "required": True, "options": ["Normal - no wax", "Partial wax occlusion", "Complete wax occlusion (TM not visible)", "TM visible - normal", "TM visible - abnormal", "Not examined"]},
                    {"id": "wax_tm_perforation", "type": "toggle", "label": "TM Perforation Visible? (If canal partially visible)", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: TM perforation visible = do NOT irrigate. ENT referral.", "red_flag_negative": ""},
                    {"id": "wax_otitis_externa", "type": "toggle", "label": "Signs of Otitis Externa? (Erythema, swelling, debris)", "required": False},
                    {"id": "wax_mastoid", "type": "toggle", "label": "Mastoid Tenderness / Erythema / Swelling?", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Mastoid tenderness = ?mastoiditis. Urgent ENT.", "red_flag_negative": ""},
                    {"id": "wax_pinna", "type": "toggle", "label": "Pinna Displacement / Swelling?", "required": False}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "Impacted Cerumen (Ear Wax)",
                    "Otitis Externa",
                    "Otitis Media with Effusion (Glue Ear)",
                    "Chronic Suppurative Otitis Media",
                    "Tympanic Membrane Perforation",
                    "Cholesteatoma",
                    "External Auditory Canal Stenosis / Exostosis",
                    "Foreign Body",
                    "Sensorineural Hearing Loss (non-wax related)"
                ],
                "questions": [
                    {"id": "wax_diagnosis", "type": "single_select", "label": "Working Diagnosis", "required": True, "options": ["Impacted cerumen - bilateral", "Impacted cerumen - right", "Impacted cerumen - left", "Wax + otitis externa", "Normal ears - no wax impaction"]}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Return if: severe pain, foul discharge, bleeding, dizziness, or worsening hearing loss develops. Do NOT use cotton buds or insert any objects into ear canal (compacts wax and risks TM perforation). Use softening drops as directed. If irrigation/microsuction planned: ensure no contraindications (perforation, surgery, infection). After irrigation: keep ears dry for 24-48 hours. If wax recurrent: use olive oil drops 1-2 times weekly as prophylaxis.",
                "questions": [
                    {"id": "wax_drops", "type": "single_select", "label": "Wax Softening Drops", "required": False, "options": ["None", "Olive oil 3-5 drops BD for 3-5 days", "Sodium bicarbonate drops BD for 3-5 days", "Cerumol drops BD for 3-5 days"]},
                    {"id": "wax_irrigation", "type": "toggle", "label": "Ear Irrigation Planned? (If no contraindications)", "required": False},
                    {"id": "wax_microsuction", "type": "toggle", "label": "Microsuction Referral? (If irrigation contraindicated)", "required": False},
                    {"id": "wax_cotton_bud_advice", "type": "toggle", "label": "No Cotton Buds / Objects Advised?", "required": True},
                    {"id": "wax_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., 1 week after drops if not cleared, or attend for irrigation"}
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
    seed_ear_wax()
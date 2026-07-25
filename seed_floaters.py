from app.database import SessionLocal
from app.models import User, Template, Category

def seed_floaters():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Ophthalmology").first()
    if not category: category = Category(name="Ophthalmology"); db.add(category); db.commit()

    t = {
        "title": "Floaters & Flashes Assessment",
        "description": "Emergency-focused assessment for floaters and flashes with red flags for retinal detachment, PVD, and vitreous haemorrhage.",
        "category": "Ophthalmology",
        "content": {"sections": [
            {
                "title": "Presentation",
                "section_type": "history",
                "questions": [
                    {"id": "fl_presenting_complaint", "type": "text", "label": "Presenting Complaint", "required": True, "placeholder": "e.g., Small black dots/lines in vision for 2 months, worse against bright backgrounds"},
                    {"id": "fl_age", "type": "number", "label": "Age", "required": True, "placeholder": "e.g., 58"},
                    {"id": "fl_duration", "type": "text", "label": "Duration", "required": True, "placeholder": "e.g., 2 months"},
                    {"id": "fl_onset", "type": "single_select", "label": "Onset", "required": True, "options": ["Gradual (weeks-months)", "Sudden (hours-days) - RED FLAG", "Sudden shower of floaters - RED FLAG"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Sudden onset or shower of floaters = ?retinal tear/detachment, vitreous haemorrhage. Urgent ophthalmology same-day.", "red_flag_negative": ""},
                    {"id": "fl_appearance", "type": "multi_select", "label": "Appearance of Floaters", "required": True, "options": ["Small black dots", "Lines/cobwebs", "Fly/insect shape", "Ring/Weiss ring (PVD)", "Haze/cloud", "Dots + flashes"]},
                    {"id": "fl_triggers", "type": "single_select", "label": "More Noticeable When", "required": False, "options": ["Reading", "Bright backgrounds (sky/screen)", "Both", "All the time"]},
                    {"id": "fl_move_with_gaze", "type": "toggle", "label": "Move Away on Gaze Shift?", "required": True}
                ]
            },
            {
                "title": "RED FLAGS - Retinal Detachment & Haemorrhage",
                "section_type": "history",
                "questions": [
                    {"id": "fl_curtain_shadow", "type": "toggle", "label": "Dark Shadow / 'Curtain' Moving Across Vision?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Curtain/shadow = RETINAL DETACHMENT until proven otherwise. EMERGENCY - same-day ophthalmology/Eye Casualty.", "red_flag_negative": ""},
                    {"id": "fl_sudden_increase", "type": "toggle", "label": "Sudden Dramatic Increase in Floaters?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Sudden shower of floaters = ?retinal tear, vitreous haemorrhage. Urgent ophthalmology within 24h.", "red_flag_negative": ""},
                    {"id": "fl_flashes", "type": "single_select", "label": "Flashes of Light (Photopsia)", "required": True, "options": ["None", "White flashes in dark/movement - RED FLAG", "Coloured/zigzag (migrainous)", "Brief occasional"], "is_red_flag": True, "red_flag_positive": "RED FLAG: White flashes + floaters = ?PVD with retinal tear. Urgent dilated fundus exam within 24-48h.", "red_flag_negative": ""},
                    {"id": "fl_visual_loss", "type": "toggle", "label": "Sudden Visual Loss / Blurring?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Visual loss = ?retinal detachment, vitreous haemorrhage, central retinal artery occlusion. EMERGENCY.", "red_flag_negative": ""},
                    {"id": "fl_peripheral_loss", "type": "toggle", "label": "Peripheral Vision Loss?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Peripheral loss = ?retinal detachment. Same-day ophthalmology.", "red_flag_negative": ""},
                    {"id": "fl_eye_pain", "type": "toggle", "label": "Eye Pain?", "required": False}
                ]
            },
            {
                "title": "Risk Factors",
                "section_type": "history",
                "questions": [
                    {"id": "fl_myopia", "type": "toggle", "label": "Myopia (Short-Sightedness)? Especially high myopia", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: High myopia (>-6D) = significantly increased risk of retinal detachment. Lower threshold for urgent referral.", "red_flag_negative": ""},
                    {"id": "fl_trauma", "type": "toggle", "label": "Recent Ocular Trauma?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Trauma + floaters = ?retinal tear/detachment. Urgent ophthalmology.", "red_flag_negative": ""},
                    {"id": "fl_previous_surgery", "type": "toggle", "label": "Previous Cataract Surgery / Eye Surgery?", "required": True},
                    {"id": "fl_previous_detachment", "type": "toggle", "label": "Previous Retinal Detachment? (Other eye)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Previous detachment = high risk in fellow eye. Urgent assessment for any new symptoms.", "red_flag_negative": ""},
                    {"id": "fl_diabetes", "type": "toggle", "label": "Diabetes Mellitus? (Proliferative retinopathy risk)", "required": True},
                    {"id": "fl_family_detachment", "type": "toggle", "label": "Family History Retinal Detachment?", "required": False},
                    {"id": "fl_inflammatory", "type": "toggle", "label": "Sarcoidosis / IBD / Uveitis History?", "required": False}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "fl_va_right", "type": "text", "label": "Visual Acuity - Right", "required": True, "placeholder": "e.g., 6/6"},
                    {"id": "fl_va_left", "type": "text", "label": "Visual Acuity - Left", "required": True, "placeholder": "e.g., 6/6"},
                    {"id": "fl_visual_fields", "type": "single_select", "label": "Visual Fields (Confrontation)", "required": True, "options": ["Normal B/L", "Deficit - Right", "Deficit - Left", "Superior quadrant defect (inferior RD)"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Visual field defect = ?retinal detachment. Same-day ophthalmology.", "red_flag_negative": ""},
                    {"id": "fl_red_reflex", "type": "single_select", "label": "Red Reflex", "required": True, "options": ["B/L symmetrical + present", "Absent/diminished Right", "Absent/diminished Left", "Absent B/L - RED FLAG"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Absent red reflex = ?vitreous haemorrhage, large retinal detachment. Urgent ophthalmology.", "red_flag_negative": ""},
                    {"id": "fl_weiss_ring", "type": "toggle", "label": "Weiss Ring Visible? (PVD pathognomonic)", "required": False},
                    {"id": "fl_fundoscopy", "type": "single_select", "label": "Fundoscopy", "required": False, "options": ["Normal (as far as visible)", "Abnormal", "Not performed - needs dilated exam", "Not assessed"]}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "Posterior Vitreous Detachment (PVD) - Most Common (85%)",
                    "Vitreous Liquefaction (Age-Related)",
                    "Retinal Tear (RED FLAG - needs urgent laser)",
                    "Retinal Detachment (RED FLAG - surgical emergency)",
                    "Vitreous Haemorrhage (RED FLAG - diabetes, trauma, tear)",
                    "Posterior Uveitis / Retinitis",
                    "Migraine with Visual Aura (coloured/zigzag)",
                    "Optic Neuritis",
                    "Central Retinal Artery Occlusion (RED FLAG)"
                ],
                "questions": [
                    {"id": "fl_diagnosis", "type": "single_select", "label": "Working Diagnosis", "required": True, "options": ["Likely benign PVD", "Floaters - needs dilated exam", "Suspected retinal tear - URGENT", "Suspected retinal detachment - EMERGENCY", "Suspected vitreous haemorrhage - URGENT", "Migrainous visual aura", "Uncertain"]}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "EMERGENCY - attend Eye Casualty/Emergency Department IMMEDIATELY if: dark shadow or 'curtain' moving across vision (peripheral or central), sudden dramatic increase in floaters (shower), new or worsening flashes of light, or any sudden drop/blurring in visual acuity. These are RED FLAGS for retinal detachment which can cause permanent blindness if not treated within 24-48 hours. Any patient with acute/new onset floaters or photopsia requires dilated fundus examination (via Optometry or Ophthalmology within 24-48 hours) - GP examination alone cannot exclude peripheral retinal tears. If no red flags: routine optician/optometry referral for dilated examination.",
                "questions": [
                    {"id": "fl_plan", "type": "single_select", "label": "Management", "required": True, "options": ["Reassurance + routine optometry referral", "Urgent optometry (dilated exam within 24-48h)", "Same-day ophthalmology (suspected tear/detachment)", "Emergency Eye Casualty (retinal detachment)", "Observation + safety-net"]},
                    {"id": "fl_dilated_exam", "type": "toggle", "label": "Dilated Fundus Exam Arranged? (Optometry/Ophthalmology)", "required": True},
                    {"id": "fl_reassurance", "type": "toggle", "label": "Benign PVD Nature Explained? (85% benign, gel liquefaction)", "required": False},
                    {"id": "fl_curtain_warning", "type": "toggle", "label": "Curtain/Shadow RED FLAG Warning Given?", "required": True},
                    {"id": "fl_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., Optometry this week, return immediately if red flags"}
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
    seed_floaters()
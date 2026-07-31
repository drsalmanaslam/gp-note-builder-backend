from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_2week_check():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Paediatrics").first()
    if not category: category = Category(name="Paediatrics"); db.add(category); db.commit()

    t = {
        "title": "2-Week Mother & Baby Check",
        "description": "Combined 2-week infant examination and postnatal maternal check covering newborn red flags, feeding, and maternal wellbeing.",
        "category": "Paediatrics",
        "content": {"sections": [
            {
                "title": "Baby - History",
                "section_type": "history",
                "questions": [
                    {"id": "w2_sex", "type": "single_select", "label": "Sex", "required": True, "options": ["Male", "Female"]},
                    {"id": "w2_gestation", "type": "single_select", "label": "Gestation at Birth", "required": True, "options": ["Term (≥37 weeks)", "Preterm (34-36 weeks)", "Preterm (32-33 weeks)", "Preterm (<32 weeks)"]},
                    {"id": "w2_delivery_method", "type": "single_select", "label": "Method of Delivery", "required": True, "options": ["SVD (Normal vaginal)", "Assisted vaginal (Ventouse/Forceps)", "Elective C-section", "Emergency C-section"]},
                    {"id": "w2_birthweight", "type": "number", "label": "Birthweight (kg)", "required": True, "placeholder": "e.g., 3.4"},
                    {"id": "w2_perinatal_issues", "type": "toggle", "label": "Any Prenatal / Perinatal / Postnatal Issues?", "required": True},
                    {"id": "w2_perinatal_detail", "type": "textarea", "label": "Perinatal Details", "required": False, "placeholder": "e.g., NICU stay, jaundice needing phototherapy, sepsis..."},
                    {"id": "w2_feeding", "type": "single_select", "label": "Feeding Method", "required": True, "options": ["Breastfeeding", "Formula feeding", "Combination (breast + formula)"]},
                    {"id": "w2_latch", "type": "single_select", "label": "Latching / Feeding", "required": True, "options": ["Good - feeding well", "Fair - some difficulty", "Poor - significant issues"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Poor feeding = risk of dehydration, weight loss, hypoglycaemia. Urgent assessment.", "red_flag_negative": ""},
                    {"id": "w2_crying", "type": "toggle", "label": "Incessant Crying / Irritability?", "required": False},
                    {"id": "w2_phn_visit", "type": "toggle", "label": "Public Health Nurse Visited?", "required": True},
                    {"id": "w2_phn_concerns", "type": "toggle", "label": "Any PHN Concerns?", "required": False},
                    {"id": "w2_maternal_concerns", "type": "textarea", "label": "Other Concerns (Mother)", "required": False, "placeholder": "Any other worries about baby..."}
                ]
            },
            {
                "title": "Baby - Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "w2_general", "type": "single_select", "label": "General Appearance", "required": True, "options": ["Well - good activity, posture, cry", "Mildly unwell", "Lethargic / Ill-appearing - RED FLAG"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Lethargic/ill-appearing = urgent paediatric assessment.", "red_flag_negative": ""},
                    {"id": "w2_weight", "type": "number", "label": "Weight (kg)", "required": True, "placeholder": "e.g., 3.6"},
                    {"id": "w2_hc", "type": "number", "label": "Head Circumference (cm)", "required": True, "placeholder": "e.g., 35"},
                    {"id": "w2_length", "type": "number", "label": "Length (cm)", "required": False, "placeholder": "e.g., 51"},
                    {"id": "w2_hydration", "type": "single_select", "label": "Hydration / CRT", "required": True, "options": ["Well hydrated, CRT <2 sec", "Dehydrated - RED FLAG"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Dehydration = urgent paediatric assessment.", "red_flag_negative": ""},
                    {"id": "w2_skin", "type": "single_select", "label": "Skin", "required": True, "options": ["Normal colour/texture", "Jaundice", "Rash", "Birthmarks noted", "Pallor"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Jaundice at 2 weeks (especially if prolonged) = check conjugated/unconjugated bilirubin. Pallor = check Hb.", "red_flag_negative": ""},
                    {"id": "w2_scfat_muscle", "type": "toggle", "label": "Good Subcutaneous Fat & Muscle Bulk?", "required": False},
                    {"id": "w2_fontanelles", "type": "single_select", "label": "Fontanelles", "required": True, "options": ["Anterior + posterior soft & flat", "Tense/bulging - RED FLAG", "Sunken - RED FLAG"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Abnormal fontanelles = urgent assessment.", "red_flag_negative": ""},
                    {"id": "w2_face_symmetry", "type": "toggle", "label": "Normal Facial Symmetry?", "required": True},
                    {"id": "w2_ears_nose_neck", "type": "toggle", "label": "Ears, Nose, Neck Normal?", "required": False},
                    {"id": "w2_palate", "type": "single_select", "label": "Palate", "required": True, "options": ["Intact", "Cleft / abnormality - RED FLAG"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Cleft palate = refer cleft team urgently.", "red_flag_negative": ""},
                    {"id": "w2_thrush", "type": "toggle", "label": "Oral Thrush?", "required": False},
                    {"id": "w2_red_reflex", "type": "single_select", "label": "Red Reflex", "required": True, "options": ["B/L present", "Absent/abnormal - RED FLAG"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Absent/abnormal red reflex = urgent ophthalmology referral.", "red_flag_negative": ""},
                    {"id": "w2_sclera", "type": "toggle", "label": "Sclera Clear? (No jaundice/icterus)", "required": False},
                    {"id": "w2_opacities", "type": "toggle", "label": "Corneal/Lens Opacities?", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Corneal/lens opacity = ?congenital cataract. Urgent ophthalmology.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Baby - Cardiovascular & Respiratory",
                "section_type": "examination",
                "questions": [
                    {"id": "w2_hr", "type": "number", "label": "Heart Rate (bpm)", "required": True, "placeholder": "e.g., 140 (NR: 110-160)"},
                    {"id": "w2_heart_sounds", "type": "single_select", "label": "Heart Sounds", "required": True, "options": ["HS 1+2 Normal, No Murmurs", "Murmur Present", "Gallop/Abnormal - RED FLAG"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Abnormal heart sounds = paediatric cardiology referral.", "red_flag_negative": ""},
                    {"id": "w2_femoral_pulses", "type": "single_select", "label": "Femoral Pulses", "required": True, "options": ["B/L normal volume", "Weak/Absent - RED FLAG"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Weak femoral pulses = ?coarctation. Urgent paediatric cardiology.", "red_flag_negative": ""},
                    {"id": "w2_rr", "type": "number", "label": "Respiratory Rate (/min)", "required": True, "placeholder": "e.g., 35 (NR: 25-50)"},
                    {"id": "w2_chest", "type": "single_select", "label": "Chest", "required": True, "options": ["Clear B/L, No Distress", "Crackles/Wheeze", "Recessions - RED FLAG"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Respiratory distress = urgent paediatric assessment.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Baby - Abdomen, GU, Hips, Neuro",
                "section_type": "examination",
                "questions": [
                    {"id": "w2_abdomen", "type": "single_select", "label": "Abdomen", "required": True, "options": ["Soft, No Organomegaly/Masses", "Distended", "Mass"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Abdominal mass/distension = urgent paediatric assessment.", "red_flag_negative": ""},
                    {"id": "w2_umbilicus", "type": "single_select", "label": "Umbilicus", "required": True, "options": ["Clean/dry / small crusted remnant", "Infection/erythema", "Hernia"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Umbilical infection (omphalitis) = urgent antibiotics. May need admission.", "red_flag_negative": ""},
                    {"id": "w2_genitalia", "type": "single_select", "label": "Genitalia", "required": True, "options": ["Normal for gender", "Ambiguous - RED FLAG", "Hypospadias noted", "Testes undescended"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Ambiguous genitalia = urgent paediatric endocrinology. Hypospadias = refer urology.", "red_flag_negative": ""},
                    {"id": "w2_anus", "type": "toggle", "label": "Anus Patent?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Imperforate anus = surgical emergency.", "red_flag_negative": ""},
                    {"id": "w2_hips", "type": "single_select", "label": "Barlow & Ortolani", "required": True, "options": ["B/L Negative", "Positive - RED FLAG"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Positive = ?DDH. Urgent hip USS + orthopaedic referral.", "red_flag_negative": ""},
                    {"id": "w2_talipes", "type": "toggle", "label": "Talipes / Foot Deformity?", "required": False},
                    {"id": "w2_limbs", "type": "toggle", "label": "Limbs/Hands/Feet Symmetrical & Well-Proportioned?", "required": True},
                    {"id": "w2_spine", "type": "toggle", "label": "Spinal Dimple / Sinus / Hair Tuft?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Spinal abnormality = ?spina bifida occulta. Paediatric referral.", "red_flag_negative": ""},
                    {"id": "w2_tone", "type": "single_select", "label": "Tone & Movement", "required": True, "options": ["Normal tone + posture + movements", "Hypotonic (floppy) - RED FLAG", "Hypertonic (stiff) - RED FLAG"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Abnormal tone = neurological concern. Paediatric neurology referral.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Baby - Assessment & Plan",
                "section_type": "assessment",
                "differentials": [
                    "Normal 2-Week Infant - Well Child",
                    "Feeding Difficulty / Poor Weight Gain",
                    "Neonatal Jaundice (Prolonged/Pathological)",
                    "Congenital Heart Disease",
                    "Developmental Dysplasia of Hip (DDH)",
                    "Congenital Cataract / Retinoblastoma",
                    "Cleft Palate",
                    "Umbilical Infection (Omphalitis)",
                    "Ambiguous Genitalia",
                    "Spina Bifida Occulta",
                    "Neurological / Tone Abnormality"
                ],
                "questions": [
                    {"id": "w2_impression", "type": "single_select", "label": "Baby Impression", "required": True, "options": ["Well 2-week infant - normal examination", "Minor finding - monitor", "Significant finding - refer"]},
                    {"id": "w2_vitamin_d", "type": "toggle", "label": "Vitamin D3 5mcg Daily Advised?", "required": True},
                    {"id": "w2_resources", "type": "toggle", "label": "Parent Resources Given? (HSE / Cuidiú)", "required": False},
                    {"id": "w2_baby_followup", "type": "text", "label": "Baby Follow-up", "required": True, "placeholder": "e.g., 6-week check in 4 weeks"}
                ]
            },
            {
                "title": "Mother - Postnatal Check",
                "section_type": "history",
                "questions": [
                    {"id": "w2_mum_gravida_para", "type": "text", "label": "Gravida / Para", "required": True, "placeholder": "e.g., G1P1"},
                    {"id": "w2_mum_delivery_complications", "type": "toggle", "label": "Any Delivery Complications?", "required": True},
                    {"id": "w2_mum_mood", "type": "single_select", "label": "Mood", "required": True, "options": ["Good - well supported", "Low mood / tearful", "Significant low mood / ?postnatal depression", "Suicidal thoughts / psychosis - RED FLAG"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Severe depression/suicidal thoughts/psychosis = urgent psychiatric assessment. Same-day referral.", "red_flag_negative": ""},
                    {"id": "w2_mum_support", "type": "toggle", "label": "Adequate Support at Home?", "required": True},
                    {"id": "w2_mum_feeding", "type": "toggle", "label": "Feeding Going Well?", "required": True},
                    {"id": "w2_mum_breast_issues", "type": "toggle", "label": "Breast Issues? (Mastitis, cracked nipples, engorgement)", "required": False},
                    {"id": "w2_mum_perineum", "type": "toggle", "label": "Perineal Healing? (If vaginal delivery)", "required": False},
                    {"id": "w2_mum_wound", "type": "toggle", "label": "Wound Healing? (If C-section)", "required": False},
                    {"id": "w2_mum_bleeding", "type": "toggle", "label": "PV Bleeding? (Lochia - normal vs heavy)", "required": False},
                    {"id": "w2_mum_contraception", "type": "toggle", "label": "Contraception Discussed?", "required": True},
                    {"id": "w2_mum_contraception_plan", "type": "text", "label": "Contraception Plan", "required": False, "placeholder": "e.g., Will decide by 6-week check. Mirena timing: 6 weeks baseline +2 weeks if BF +2 weeks if C-section."},
                    {"id": "w2_mum_concerns", "type": "textarea", "label": "Any Maternal Concerns?", "required": False, "placeholder": "Physical, emotional, or social concerns..."}
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
    seed_2week_check()
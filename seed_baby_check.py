from app.database import SessionLocal
from app.models import User, Template, Category

def seed_baby_check():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Paediatrics").first()
    if not category: category = Category(name="Paediatrics"); db.add(category); db.commit()

    t = {
        "title": "6-Week Baby Check",
        "description": "Structured 6-week infant physical examination covering growth, development, red flags, and vaccination planning.",
        "category": "Paediatrics",
        "content": {"sections": [
            {
                "title": "General & Maternal Concerns",
                "section_type": "history",
                "questions": [
                    {"id": "bc_sex", "type": "single_select", "label": "Sex", "required": True, "options": ["Male", "Female"]},
                    {"id": "bc_maternal_concerns", "type": "toggle", "label": "Any Maternal Concerns?", "required": True},
                    {"id": "bc_maternal_concerns_detail", "type": "textarea", "label": "Maternal Concerns Details", "required": False, "placeholder": "e.g., Feeding, crying, rash, breathing..."},
                    {"id": "bc_feeding", "type": "single_select", "label": "Feeding Method", "required": True, "options": ["Breastfeeding", "Formula feeding", "Mixed"]},
                    {"id": "bc_feeding_well", "type": "toggle", "label": "Feeding Well?", "required": True},
                    {"id": "bc_bowel_motions", "type": "single_select", "label": "Bowel Motions", "required": False, "options": ["Normal", "Constipated", "Diarrhoea", "Not reported"]},
                    {"id": "bc_wet_nappies", "type": "toggle", "label": "6+ Wet Nappies Daily?", "required": False}
                ]
            },
            {
                "title": "Developmental Milestones",
                "section_type": "history",
                "questions": [
                    {"id": "bc_fixes_follows", "type": "toggle", "label": "Fixes & Follows Face/Objects? (Visual tracking)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Absent visual fixing/following = possible visual impairment or neurological issue. Refer ophthalmology/paediatrics.", "red_flag_negative": ""},
                    {"id": "bc_social_smile", "type": "toggle", "label": "Social Smile Present? (By 6-8 weeks)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Absent social smile by 8 weeks = possible developmental delay or neurodevelopmental disorder.", "red_flag_negative": ""},
                    {"id": "bc_startles_sound", "type": "toggle", "label": "Startles to Loud Sound?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: No startle response = possible hearing impairment. Refer audiology urgently.", "red_flag_negative": ""},
                    {"id": "bc_head_control", "type": "toggle", "label": "Good Head Control? (When held upright)", "required": False},
                    {"id": "bc_vocalisation", "type": "toggle", "label": "Cooing / Vocalising?", "required": False}
                ]
            },
            {
                "title": "Growth Measurements",
                "section_type": "examination",
                "questions": [
                    {"id": "bc_weight", "type": "number", "label": "Weight (kg)", "required": True, "placeholder": "e.g., 4.8"},
                    {"id": "bc_weight_centile", "type": "text", "label": "Weight Centile", "required": False, "placeholder": "e.g., 50th"},
                    {"id": "bc_hc", "type": "number", "label": "Head Circumference (cm)", "required": True, "placeholder": "e.g., 38.5", "is_red_flag": True, "red_flag_positive": "RED FLAG: Abnormal HC (crossing centiles, microcephaly, macrocephaly) = needs paediatric assessment.", "red_flag_negative": ""},
                    {"id": "bc_hc_centile", "type": "text", "label": "HC Centile", "required": False, "placeholder": "e.g., 50th"},
                    {"id": "bc_length", "type": "number", "label": "Length (cm)", "required": False, "placeholder": "e.g., 56"},
                    {"id": "bc_length_centile", "type": "text", "label": "Length Centile", "required": False, "placeholder": "e.g., 50th"}
                ]
            },
            {
                "title": "HEENT - Head, Eyes, Ears, Nose, Throat",
                "section_type": "examination",
                "questions": [
                    {"id": "bc_fontanelles", "type": "single_select", "label": "Fontanelles", "required": True, "options": ["Anterior + posterior normal (flat, soft)", "Tense/bulging - RED FLAG", "Sunken - RED FLAG"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Tense/bulging = ?raised ICP. Sunken = ?dehydration. Urgent assessment.", "red_flag_negative": ""},
                    {"id": "bc_palate", "type": "single_select", "label": "Palate", "required": True, "options": ["Intact", "Cleft lip/palate noted", "Submucous cleft suspected", "Membranous cleft noted"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Cleft palate = refer Cleft Lip & Palate Team. Feeding assessment needed.", "red_flag_negative": ""},
                    {"id": "bc_red_reflex", "type": "single_select", "label": "Red Reflex", "required": True, "options": ["B/L present + symmetrical", "Absent Right", "Absent Left", "Absent B/L", "Abnormal/white reflex - RED FLAG"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Absent/abnormal red reflex = ?congenital cataract, retinoblastoma. Urgent ophthalmology referral (within 2 weeks).", "red_flag_negative": ""},
                    {"id": "bc_irises", "type": "toggle", "label": "Irises Complete & Normal?", "required": True},
                    {"id": "bc_ears", "type": "single_select", "label": "Ears", "required": False, "options": ["Normal position + shape", "Low-set ears", "Pre-auricular tags/pits", "Not examined"]}
                ]
            },
            {
                "title": "Cardiovascular",
                "section_type": "examination",
                "questions": [
                    {"id": "bc_hr", "type": "number", "label": "Heart Rate (bpm)", "required": True, "placeholder": "e.g., 130 (NR: 100-160)"},
                    {"id": "bc_heart_sounds", "type": "single_select", "label": "Heart Sounds", "required": True, "options": ["HS 1+2 Normal, No Murmurs", "Murmur Present (describe)", "Gallop / Abnormal"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Murmur/gallop = refer paediatric cardiology. Significant murmurs need echocardiogram.", "red_flag_negative": ""},
                    {"id": "bc_femoral_pulses", "type": "single_select", "label": "Femoral Pulses", "required": True, "options": ["B/L palpable + normal volume", "Weak/absent Right", "Weak/absent Left", "Weak/absent B/L - RED FLAG"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Weak/absent femoral pulses = ?coarctation of the aorta. Urgent paediatric cardiology.", "red_flag_negative": ""},
                    {"id": "bc_brachial_pulses", "type": "single_select", "label": "Brachial Pulses", "required": True, "options": ["B/L palpable + normal", "Abnormal"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Abnormal brachial pulses = ?coarctation. Check 4-limb BP. Urgent cardiology.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Respiratory",
                "section_type": "examination",
                "questions": [
                    {"id": "bc_rr", "type": "number", "label": "Respiratory Rate (/min)", "required": True, "placeholder": "e.g., 30 (NR: 25-40)"},
                    {"id": "bc_chest", "type": "single_select", "label": "Chest Auscultation", "required": True, "options": ["Clear B/L, No Distress", "Crackles/Wheeze", "Reduced Air Entry", "Recessions/Distress - RED FLAG"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Respiratory distress/recessions = urgent paediatric assessment.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Abdomen & Gastrointestinal",
                "section_type": "examination",
                "questions": [
                    {"id": "bc_abdomen", "type": "single_select", "label": "Abdominal Examination", "required": True, "options": ["Soft, Non-tender, No Masses", "Distended", "Mass palpable", "Tender"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Abdominal mass/distension = ?pyloric stenosis, obstruction. Urgent paediatric assessment.", "red_flag_negative": ""},
                    {"id": "bc_bowel_sounds", "type": "single_select", "label": "Bowel Sounds", "required": False, "options": ["Present + Normal", "Absent/Reduced", "Not assessed"]},
                    {"id": "bc_anus", "type": "toggle", "label": "Anus Patent? (Passage of meconium/stool)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Imperforate anus / no meconium = surgical emergency. Immediate paediatric surgical referral.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Genitourinary - Male",
                "section_type": "examination",
                "questions": [
                    {"id": "bc_testes", "type": "single_select", "label": "Testes (if male)", "required": False, "options": ["Descended B/L", "Undescended Right", "Undescended Left", "Undescended B/L", "Not applicable (female)"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Undescended testes = refer paediatrics if not descended by 3-6 months. May need orchidopexy.", "red_flag_negative": ""},
                    {"id": "bc_hypospadias", "type": "toggle", "label": "Hypospadias?", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Hypospadias = refer paediatric urology. Do NOT circumcise (foreskin needed for repair).", "red_flag_negative": ""},
                    {"id": "bc_inguinal_hernia", "type": "toggle", "label": "Inguinal Hernia?", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Inguinal hernia in infant = refer paediatric surgery (high risk of incarceration).", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Hips & Musculoskeletal",
                "section_type": "examination",
                "questions": [
                    {"id": "bc_barlow", "type": "single_select", "label": "Barlow Test (Hips)", "required": True, "options": ["Negative B/L", "Positive Right", "Positive Left", "Positive B/L - RED FLAG"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Positive Barlow = ?DDH (Developmental Dysplasia of Hip). Urgent hip USS + orthopaedic referral within 2 weeks.", "red_flag_negative": ""},
                    {"id": "bc_ortolani", "type": "single_select", "label": "Ortolani Test (Hips)", "required": True, "options": ["Negative B/L", "Positive Right", "Positive Left", "Positive B/L - RED FLAG"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Positive Ortolani = DDH. Urgent hip USS + orthopaedic referral.", "red_flag_negative": ""},
                    {"id": "bc_galeazzi", "type": "single_select", "label": "Galeazzi Sign (Leg Length)", "required": True, "options": ["Negative - Equal B/L", "Positive - Right shorter", "Positive - Left shorter"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Positive Galeazzi = ?DDH or hip dislocation. Urgent hip USS.", "red_flag_negative": ""},
                    {"id": "bc_talipes", "type": "toggle", "label": "Talipes / Foot Deformity?", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Talipes = refer orthopaedics for Ponseti casting.", "red_flag_negative": ""},
                    {"id": "bc_hands_palms", "type": "single_select", "label": "Hands & Palms", "required": False, "options": ["Normal", "Single palmar crease", "Extra digits", "Other abnormality"]}
                ]
            },
            {
                "title": "Spine & Neurological",
                "section_type": "examination",
                "questions": [
                    {"id": "bc_tone_ventral", "type": "single_select", "label": "Tone - Ventral Suspension", "required": True, "options": ["Normal", "Hypotonic (floppy) - RED FLAG", "Hypertonic (stiff) - RED FLAG"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Abnormal tone = ?cerebral palsy, neurological disorder. Urgent paediatric neurology referral.", "red_flag_negative": ""},
                    {"id": "bc_tone_upright", "type": "single_select", "label": "Tone - Upright Position", "required": True, "options": ["Normal head control", "Poor head control - RED FLAG", "Stiff/arching - RED FLAG"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Poor head control or stiff/arching = neurological concern. Paediatric referral.", "red_flag_negative": ""},
                    {"id": "bc_spine", "type": "toggle", "label": "Spinal Dimples / Sinus / Hair Tuft?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Spinal dimple above natal cleft, sinus, or hair tuft = ?spina bifida occulta or tethered cord. Paediatric referral.", "red_flag_negative": ""},
                    {"id": "bc_reflexes", "type": "single_select", "label": "Primitive Reflexes", "required": True, "options": ["All normal (Moro, rooting, grasp, stepping, fencing)", "Abnormal/reduced - RED FLAG", "Asymmetrical - RED FLAG"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Absent/asymmetrical reflexes = neurological concern. Paediatric neurology referral.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "Normal 6-Week Infant - Well Child",
                    "Developmental Dysplasia of Hip (DDH)",
                    "Congenital Heart Disease (murmur, abnormal pulses)",
                    "Congenital Cataract / Retinoblastoma",
                    "Cleft Palate",
                    "Undescended Testes",
                    "Hypospadias",
                    "Talipes / Foot Deformity",
                    "Cerebral Palsy / Neurodevelopmental Concern",
                    "Spina Bifida Occulta / Tethered Cord",
                    "Hearing Impairment",
                    "Visual Impairment",
                    "Inguinal Hernia",
                    "Failure to Thrive"
                ],
                "questions": [
                    {"id": "bc_impression", "type": "single_select", "label": "Overall Impression", "required": True, "options": ["Well 6-week infant - normal examination", "Minor finding - monitor in community", "Significant finding - needs referral", "Multiple concerns - urgent paediatric referral"]},
                    {"id": "bc_redflags_assessed", "type": "toggle", "label": "All Red Flags Specifically Assessed?", "required": True}
                ]
            },
            {
                "title": "Plan",
                "section_type": "plan",
                "safety_netting": "Return immediately if: poor feeding (< half normal), fewer than 4 wet nappies daily, lethargy/difficult to wake, breathing difficulty/grunting, fever, or any new parental concerns. 2-month vaccinations: 6-in-1 (DTaP/IPV/Hib/HepB) + PCV13 + MenB + Rotavirus (oral). Give paracetamol post-MenB vaccine. Vitamin D: 5mcg (200 IU) daily if breastfeeding. Maternal health: discuss contraception (barrier methods, POP, implant - COCP avoided if breastfeeding), pelvic floor exercises, postnatal depression screening. Next routine check: 3-4 months for 2-month vaccines. If any red flags found: refer appropriately (ophthalmology, orthopaedics, cardiology, neurology, paediatrics).",
                "questions": [
                    {"id": "bc_plan", "type": "multi_select", "label": "Plan", "required": False, "options": ["Reassure - normal examination", "Book 2-month vaccines", "Vitamin D 5mcg daily advised", "Contraception discussed", "Postnatal depression screen", "Refer ophthalmology (red reflex/vision)", "Refer orthopaedics (DDH/talipes)", "Refer cardiology (murmur/pulses)", "Refer audiology (hearing)", "Refer paediatrics (general)", "Refer paediatric neurology", "Refer cleft team"]},
                    {"id": "bc_vaccines_discussed", "type": "toggle", "label": "2-Month Vaccines Discussed & Consented?", "required": True},
                    {"id": "bc_vitamin_d", "type": "toggle", "label": "Vitamin D 5mcg Daily Advised? (If breastfed)", "required": False},
                    {"id": "bc_maternal_contraception", "type": "toggle", "label": "Maternal Contraception Discussed?", "required": False},
                    {"id": "bc_maternal_mental_health", "type": "toggle", "label": "Postnatal Depression Screening Done?", "required": False},
                    {"id": "bc_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., 2-month vaccines with practice nurse, next GP check at 3-4 months"}
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
    seed_baby_check()
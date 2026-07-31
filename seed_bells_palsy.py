from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_bells_palsy():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Neurology").first()
    if not category: category = Category(name="Neurology"); db.add(category); db.commit()

    t = {
        "title": "Bell's Palsy",
        "description": "Emergency-focused assessment for acute facial palsy covering CVA exclusion, Ramsay Hunt screening, prednisolone prescribing, and eye protection priorities.",
        "category": "Neurology",
        "content": {"sections": [
            {
                "title": "RED FLAGS - Exclude CVA First",
                "section_type": "history",
                "questions": [
                    {"id": "bp_limb_weakness", "type": "toggle", "label": "Upper or Lower Limb Weakness?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Limb weakness + facial palsy = STROKE (CVA) until proven otherwise. EMERGENCY referral. Do NOT use Bell's palsy pathway.", "red_flag_negative": ""},
                    {"id": "bp_speech_vision", "type": "toggle", "label": "New Speech or Vision Problems?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Speech/vision changes + facial palsy = STROKE. EMERGENCY referral. Do NOT use Bell's palsy pathway.", "red_flag_negative": ""},
                    {"id": "bp_brow_sparing", "type": "toggle", "label": "Able to Raise Eyebrow on Affected Side? (Brow Sparing = UMN Lesion = ?CVA)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Brow sparing (able to raise eyebrow) = UPPER MOTOR NEURON lesion. Investigate as CVA, NOT Bell's palsy. EMERGENCY referral.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "History",
                "section_type": "history",
                "questions": [
                    {"id": "bp_presenting_complaint", "type": "text", "label": "Presenting Complaint", "required": True, "placeholder": "e.g., Sudden right-sided facial droop for 6 hours"},
                    {"id": "bp_side", "type": "single_select", "label": "Side Affected", "required": True, "options": ["Right", "Left"]},
                    {"id": "bp_duration", "type": "text", "label": "Duration", "required": True, "placeholder": "e.g., 6 hours (Steroids most effective within 72 hours)"},
                    {"id": "bp_smile", "type": "toggle", "label": "Unable to Smile Properly on Affected Side?", "required": True},
                    {"id": "bp_eyebrow", "type": "toggle", "label": "Unable to Raise Eyebrow on Affected Side? (Must be present for Bell's)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: If able to raise eyebrow = UMN lesion = ?CVA. If unable = LMN (Bell's).", "red_flag_negative": ""},
                    {"id": "bp_chewing", "type": "toggle", "label": "Difficulty Chewing Food?", "required": False},
                    {"id": "bp_taste_loss", "type": "toggle", "label": "Loss of Taste - Anterior 2/3 Tongue, Same Side?", "required": False},
                    {"id": "bp_drooling", "type": "toggle", "label": "Drooling? (Parasympathetic Salivary Involvement)", "required": False},
                    {"id": "bp_eye_closure", "type": "toggle", "label": "Able to Close Affected Eye Fully?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: If unable to close eye fully = risk of exposure keratopathy. Eye protection is ESSENTIAL.", "red_flag_negative": ""},
                    {"id": "bp_hyperacusis", "type": "toggle", "label": "Hyperacusis? (Stapedius Muscle Involvement)", "required": False},
                    {"id": "bp_recurrence", "type": "toggle", "label": "First Episode or Recurrence?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Recurrence = requires further investigation to rule out alternative diagnosis.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Lyme & Ramsay Hunt Screening",
                "section_type": "history",
                "questions": [
                    {"id": "bp_lyme", "type": "multi_select", "label": "Lyme Disease Screen", "required": True, "options": ["Tick bites", "Rash (erythema migrans)", "Arthralgia", "Fever", "Headache", "None"]},
                    {"id": "bp_ramsay_hunt", "type": "toggle", "label": "Severe Ear Pain? (Ramsay Hunt - mild/moderate post-auricular pain can occur in Bell's)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Severe ear pain + vesicles = ?Ramsay Hunt syndrome (Herpes Zoster Oticus). Urgent ENT + antivirals.", "red_flag_negative": ""},
                    {"id": "bp_head_injury", "type": "toggle", "label": "Head Injury?", "required": False},
                    {"id": "bp_cough_sob", "type": "toggle", "label": "Cough / Shortness of Breath?", "required": False}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "bp_cn7_forehead", "type": "toggle", "label": "Unable to Wrinkle Forehead / Raise Eyebrow on Affected Side?", "required": True},
                    {"id": "bp_cn7_smile", "type": "toggle", "label": "Unable to Smile on Affected Side?", "required": True},
                    {"id": "bp_cn7_whistle", "type": "toggle", "label": "Unable to Whistle or Blow Out Cheek?", "required": False},
                    {"id": "bp_bell_phenomenon", "type": "toggle", "label": "Able to Close Affected Eye Fully? (Bell's Phenomenon)", "required": True},
                    {"id": "bp_ent_tonsil", "type": "toggle", "label": "Oropharynx / Ipsilateral Tonsil Asymmetry? (CN IX - suggests alternative cause)", "required": False},
                    {"id": "bp_ent_parotid", "type": "toggle", "label": "Parotid Swelling? (Parotid Gland Lesion)", "required": False},
                    {"id": "bp_ent_tm", "type": "toggle", "label": "Tympanic Membrane Vesicles? (Ramsay Hunt - Check Ipsilateral Ear)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Vesicles on TM/ear canal = Ramsay Hunt syndrome. Urgent ENT + antivirals + steroids.", "red_flag_negative": ""},
                    {"id": "bp_neuro_cn", "type": "single_select", "label": "Cranial Nerves (Other Than VII)", "required": True, "options": ["Normal", "Abnormal - RED FLAG"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Other CN involvement = ?brainstem lesion, not Bell's. Urgent neurology.", "red_flag_negative": ""},
                    {"id": "bp_neuro_limbs", "type": "single_select", "label": "Peripheral Nervous System (Tone, Power, Reflexes, Coordination, Sensation)", "required": True, "options": ["Normal in All 4 Limbs", "Abnormal - RED FLAG"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Limb neurology abnormal = ?CVA. Emergency referral.", "red_flag_negative": ""},
                    {"id": "bp_neuro_cerebellar", "type": "single_select", "label": "Cerebellar Exam (SPINDAR)", "required": False, "options": ["Normal", "Abnormal - RED FLAG"]},
                    {"id": "bp_neuro_speech", "type": "single_select", "label": "Speech", "required": True, "options": ["Normal", "Abnormal - RED FLAG"]},
                    {"id": "bp_pronator_drift", "type": "toggle", "label": "Pronator Drift?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Pronator drift = ?CVA. Emergency referral.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "Bell's Palsy (LMN CN VII - viral aetiology, self-limiting, ~70% full recovery in 4-6 months)",
                    "Stroke / CVA (UMN - brow sparing, limb weakness, speech/vision changes) - EMERGENCY",
                    "Ramsay Hunt Syndrome (Herpes Zoster Oticus - severe ear pain, vesicles) - URGENT ENT",
                    "Lyme Disease (tick bite, erythema migrans, arthralgia)",
                    "Parotid Gland Tumour",
                    "Acoustic Neuroma",
                    "Guillain-Barré Syndrome (bilateral, ascending)",
                    "Myasthenia Gravis (fluctuating, bilateral)",
                    "Sarcoidosis (Heerfordt's syndrome)"
                ],
                "questions": [
                    {"id": "bp_diagnosis", "type": "single_select", "label": "Clinical Impression (Diagnosis of Exclusion)", "required": True, "options": ["Bell's Palsy - Confirmed (CVA + Ramsay Hunt Excluded)", "Suspected CVA - EMERGENCY REFERRAL", "Suspected Ramsay Hunt - URGENT ENT", "Recurrent Bell's - Requires Investigation", "Alternative Diagnosis"]}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Return immediately if: limb weakness, speech/vision changes, or symptoms worsen. Bell's palsy: acute unilateral LMN facial palsy, fully evolving within 72 hours. ~70% complete recovery within 4-6 months. Steroids most effective within 72 hours of onset. Prednisolone 60mg OD for 5 days, then reduce by 10mg/day. Severe palsy/complete paralysis: add Valaciclovir 500-1000mg BD-TDS for 5-7 days. EYE PROTECTION IS PRIORITY: Do NOT use eye patch (eye may open underneath = corneal abrasion risk). Daytime: glasses + artificial tears. Night-time: ocular lubricating ointment + tape eyelid closed. Review in 2 weeks. If no improvement or recurrence: investigate further (MRI, neuro referral).",
                "questions": [
                    {"id": "bp_steroids", "type": "single_select", "label": "Prednisolone (Start Within 72 Hours)", "required": True, "options": ["Prednisolone 60mg OD for 5 Days, Then Reduce by 10mg/Day", "Not started - >72 hours since onset", "Not indicated"]},
                    {"id": "bp_antiviral", "type": "single_select", "label": "Valaciclovir (Severe Palsy / Complete Paralysis)", "required": False, "options": ["Valaciclovir 500-1000mg BD-TDS for 5-7 Days", "Not indicated - mild/moderate palsy"]},
                    {"id": "bp_eye_day", "type": "toggle", "label": "Daytime Eye Protection: Glasses + Artificial Tears Advised?", "required": True},
                    {"id": "bp_eye_night", "type": "toggle", "label": "Night-Time: Ocular Lubricating Ointment + Tape Eyelid Closed Advised?", "required": True},
                    {"id": "bp_no_eye_patch", "type": "toggle", "label": "NO Eye Patch Warning Given? (Corneal Abrasion Risk)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Do NOT use eye patch - eye may open underneath, risking corneal abrasion.", "red_flag_negative": ""},
                    {"id": "bp_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., Review in 2 weeks, sooner if worsening"}
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
    seed_bells_palsy()
from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_developmental_milestones():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Paediatrics").first()
    if not category: category = Category(name="Paediatrics"); db.add(category); db.commit()

    t = {
        "title": "Paediatric Developmental Milestones",
        "description": "Comprehensive developmental assessment covering gross motor, fine motor, language, and social milestones with absolute red flag ages.",
        "category": "Paediatrics",
        "content": {"sections": [
            {
                "title": "Child Details",
                "section_type": "history",
                "questions": [
                    {"id": "dev_sex", "type": "single_select", "label": "Sex", "required": True, "options": ["Male", "Female"]},
                    {"id": "dev_age_months", "type": "number", "label": "Age (months)", "required": True, "placeholder": "e.g., 18 (use months for accuracy)"},
                    {"id": "dev_gestation", "type": "number", "label": "Gestation at Birth (weeks)", "required": True, "placeholder": "e.g., 40"},
                    {"id": "dev_corrected", "type": "toggle", "label": "Corrected for Prematurity? (If <2 years)", "required": False},
                    {"id": "dev_corrected_age", "type": "number", "label": "Corrected Age (months)", "required": False, "placeholder": "e.g., 15"},
                    {"id": "dev_concern", "type": "textarea", "label": "Parental / Professional Concern", "required": False, "placeholder": "e.g., Not walking yet, not talking as expected..."}
                ]
            },
            {
                "title": "Absolute RED FLAG Milestones (Prompt Referral if Missed)",
                "section_type": "history",
                "questions": [
                    {"id": "dev_smile_8wks", "type": "toggle", "label": "Smiling by 8 Weeks?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Not smiling by 8 weeks = ?visual impairment, neurological disorder, autism. Urgent paediatric referral.", "red_flag_negative": ""},
                    {"id": "dev_sit_9m", "type": "toggle", "label": "Sitting Independently by 9 Months?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Not sitting by 9 months = ?cerebral palsy, neuromuscular disorder. Paediatric referral.", "red_flag_negative": ""},
                    {"id": "dev_walk_18m", "type": "toggle", "label": "Walking Independently by 18 Months?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Not walking by 18 months = ?cerebral palsy, Duchenne (check CK in boys), neuromuscular. Urgent paediatric referral.", "red_flag_negative": ""},
                    {"id": "dev_words_18m", "type": "toggle", "label": "Words with Meaning by 18 Months?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: No words by 18 months = ?hearing impairment, autism, language disorder. Urgent audiology + paediatric referral.", "red_flag_negative": ""},
                    {"id": "dev_2word_24m", "type": "toggle", "label": "2-Word Phrases by 24 Months?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: No 2-word phrases by 24 months = ?language disorder, autism. Speech therapy + paediatric referral.", "red_flag_negative": ""},
                    {"id": "dev_regression", "type": "toggle", "label": "Loss of Previously Acquired Skills? (Regression)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Developmental regression = EMERGENCY. ?Metabolic, neurodegenerative, Rett syndrome, Landau-Kleffner. Urgent paediatric neurology.", "red_flag_negative": ""},
                    {"id": "dev_hand_preference", "type": "toggle", "label": "Persistent Hand Preference Before 12-18 Months?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Early hand preference = ?focal neurological deficit/hemiplegia (cerebral palsy). Paediatric referral.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Gross Motor Milestones",
                "section_type": "examination",
                "questions": [
                    {"id": "dev_gm_head_control", "type": "single_select", "label": "Head Control (4-6 months)", "required": False, "options": ["Achieved", "Not achieved - RED FLAG", "Not yet expected for age"]},
                    {"id": "dev_gm_roll", "type": "single_select", "label": "Rolls Over (5-6 months)", "required": False, "options": ["Achieved", "Not achieved", "Not yet expected"]},
                    {"id": "dev_gm_sit", "type": "single_select", "label": "Sits Independently (6-9 months)", "required": False, "options": ["Achieved", "Not achieved", "Not yet expected"]},
                    {"id": "dev_gm_crawl", "type": "single_select", "label": "Crawls (8-10 months)", "required": False, "options": ["Achieved", "Not achieved", "Not yet expected"]},
                    {"id": "dev_gm_pull_stand", "type": "single_select", "label": "Pulls to Stand (9-12 months)", "required": False, "options": ["Achieved", "Not achieved", "Not yet expected"]},
                    {"id": "dev_gm_walk", "type": "single_select", "label": "Walks Independently (12-18 months)", "required": False, "options": ["Achieved", "Not achieved", "Not yet expected"]},
                    {"id": "dev_gm_run", "type": "single_select", "label": "Runs (18-24 months)", "required": False, "options": ["Achieved", "Not achieved", "Not yet expected"]},
                    {"id": "dev_gm_jump", "type": "single_select", "label": "Jumps with Both Feet (2.5 years)", "required": False, "options": ["Achieved", "Not achieved", "Not yet expected"]},
                    {"id": "dev_gm_tricycle", "type": "single_select", "label": "Rides Tricycle (3 years)", "required": False, "options": ["Achieved", "Not achieved", "Not yet expected"]},
                    {"id": "dev_gm_hop", "type": "single_select", "label": "Hops on 1 Leg (4 years)", "required": False, "options": ["Achieved", "Not achieved", "Not yet expected"]}
                ]
            },
            {
                "title": "Fine Motor & Vision Milestones",
                "section_type": "examination",
                "questions": [
                    {"id": "dev_fm_fixes_follows", "type": "single_select", "label": "Fixes & Follows Face (6 weeks)", "required": False, "options": ["Achieved", "Not achieved - RED FLAG", "Not yet expected"]},
                    {"id": "dev_fm_reaches", "type": "single_select", "label": "Reaches for Objects (3-4 months)", "required": False, "options": ["Achieved", "Not achieved", "Not yet expected"]},
                    {"id": "dev_fm_transfers", "type": "single_select", "label": "Transfers Hand-to-Hand (6 months)", "required": False, "options": ["Achieved", "Not achieved", "Not yet expected"]},
                    {"id": "dev_fm_pincer", "type": "single_select", "label": "Mature Pincer Grip (10-12 months)", "required": False, "options": ["Achieved", "Not achieved", "Not yet expected"]},
                    {"id": "dev_fm_scribbles", "type": "single_select", "label": "Scribbles (18 months)", "required": False, "options": ["Achieved", "Not achieved", "Not yet expected"]},
                    {"id": "dev_fm_tower", "type": "single_select", "label": "Tower of Cubes (age-appropriate)", "required": False, "options": ["Achieved (age-appropriate)", "Not achieved", "Not assessed"]},
                    {"id": "dev_fm_circle", "type": "single_select", "label": "Draws Circle (3 years)", "required": False, "options": ["Achieved", "Not achieved", "Not yet expected"]},
                    {"id": "dev_fm_cross", "type": "single_select", "label": "Draws Cross (4 years)", "required": False, "options": ["Achieved", "Not achieved", "Not yet expected"]}
                ]
            },
            {
                "title": "Language & Hearing Milestones",
                "section_type": "examination",
                "questions": [
                    {"id": "dev_lh_startle", "type": "single_select", "label": "Startles to Loud Sound (birth)", "required": False, "options": ["Achieved", "Not achieved - REFER AUDIOLOGY", "Not assessed"]},
                    {"id": "dev_lh_coos", "type": "single_select", "label": "Vocalises / Coos (6 weeks-3 months)", "required": False, "options": ["Achieved", "Not achieved", "Not yet expected"]},
                    {"id": "dev_lh_babble", "type": "single_select", "label": "Polysyllabic Babble (6-9 months)", "required": False, "options": ["Achieved", "Not achieved", "Not yet expected"]},
                    {"id": "dev_lh_dada_mama", "type": "single_select", "label": "Specific Sounds 'dada/mama' (8-10 months)", "required": False, "options": ["Achieved", "Not achieved", "Not yet expected"]},
                    {"id": "dev_lh_first_words", "type": "single_select", "label": "2-3 Words with Meaning (12 months)", "required": False, "options": ["Achieved", "Not achieved", "Not yet expected"]},
                    {"id": "dev_lh_10_words", "type": "single_select", "label": "10+ Words (18 months)", "required": False, "options": ["Achieved", "Not achieved", "Not yet expected"]},
                    {"id": "dev_lh_2word", "type": "single_select", "label": "Links 2 Words (24 months)", "required": False, "options": ["Achieved", "Not achieved", "Not yet expected"]},
                    {"id": "dev_lh_3word", "type": "single_select", "label": "3-Word Sentences (2.5 years)", "required": False, "options": ["Achieved", "Not achieved", "Not yet expected"]},
                    {"id": "dev_lh_speech_clear", "type": "single_select", "label": "Speech 100% Clear (4 years)", "required": False, "options": ["Achieved", "Not achieved", "Not yet expected"]}
                ]
            },
            {
                "title": "Personal & Social Milestones",
                "section_type": "examination",
                "questions": [
                    {"id": "dev_ps_social_smile", "type": "single_select", "label": "Social Smile (6-8 weeks)", "required": False, "options": ["Achieved", "Not achieved - RED FLAG", "Not yet expected"]},
                    {"id": "dev_ps_stranger_anxiety", "type": "single_select", "label": "Stranger Anxiety (7-8 months)", "required": False, "options": ["Achieved", "Not achieved", "Not yet expected"]},
                    {"id": "dev_ps_peekaboo", "type": "single_select", "label": "Peek-a-Boo / Waves Bye-Bye (9-10 months)", "required": False, "options": ["Achieved", "Not achieved", "Not yet expected"]},
                    {"id": "dev_ps_feeds_self", "type": "single_select", "label": "Feeds Self Finger Foods (6-9 months)", "required": False, "options": ["Achieved", "Not achieved", "Not yet expected"]},
                    {"id": "dev_ps_drinks_cup", "type": "single_select", "label": "Drinks from Cup (15 months)", "required": False, "options": ["Achieved", "Not achieved", "Not yet expected"]},
                    {"id": "dev_ps_spoon", "type": "single_select", "label": "Spoon Feeds (18 months)", "required": False, "options": ["Achieved", "Not achieved", "Not yet expected"]},
                    {"id": "dev_ps_toilet", "type": "single_select", "label": "Toilet Trained by Day (2.5-3 years)", "required": False, "options": ["Achieved", "Not achieved", "Not yet expected"]},
                    {"id": "dev_ps_dresses", "type": "single_select", "label": "Dresses Self (3-4 years)", "required": False, "options": ["Achieved", "Not achieved", "Not yet expected"]},
                    {"id": "dev_ps_play", "type": "single_select", "label": "Interactive / Cooperative Play (3-4 years)", "required": False, "options": ["Achieved", "Not achieved", "Not yet expected"]}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "Normal Development - Age Appropriate",
                    "Constitutional Delay (late bloomer)",
                    "Global Developmental Delay",
                    "Gross Motor Delay (?Cerebral Palsy, Duchenne, neuromuscular)",
                    "Fine Motor Delay (?Visual impairment, neurological)",
                    "Speech & Language Delay (?Hearing impairment, autism, language disorder)",
                    "Autism Spectrum Disorder (social + language + repetitive behaviours)",
                    "Hearing Impairment",
                    "Visual Impairment",
                    "Developmental Regression (RED FLAG - metabolic, neurodegenerative)"
                ],
                "questions": [
                    {"id": "dev_impression", "type": "single_select", "label": "Overall Development", "required": True, "options": ["Age-appropriate across all domains", "Mild delay - monitor", "Significant delay - needs referral", "Multi-domain delay - urgent referral", "Regression - URGENT referral"]},
                    {"id": "dev_redflags_assessed", "type": "toggle", "label": "All Absolute Red Flag Milestones Assessed?", "required": True}
                ]
            },
            {
                "title": "Plan",
                "section_type": "plan",
                "safety_netting": "Return if: parents notice any loss of previously acquired skills (regression), lack of response to sound, delay in motor or speech milestones, or any new concerns. Absolute red flags for prompt referral: not smiling by 8 weeks, not sitting by 9 months, not walking by 18 months, no words by 18 months, no 2-word phrases by 24 months, persistent hand preference before 12-18 months, or any developmental regression. Early intervention is key - if in doubt, refer. Provide parent with written milestone guide. Next routine developmental check per national schedule.",
                "questions": [
                    {"id": "dev_referral", "type": "single_select", "label": "Referral", "required": False, "options": ["None - normal development", "Community Paediatrics / AMO", "Paediatric Neurology (regression/motor)", "Audiology (hearing concern)", "Ophthalmology (vision concern)", "Speech & Language Therapy", "Physiotherapy (motor delay)", "Occupational Therapy (fine motor)"]},
                    {"id": "dev_anticipatory_guidance", "type": "toggle", "label": "Anticipatory Guidance Given? (Safety, stimulation, next milestones)", "required": False},
                    {"id": "dev_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., Routine developmental check at next scheduled visit"}
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
    seed_developmental_milestones()
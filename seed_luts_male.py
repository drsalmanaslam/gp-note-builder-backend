from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_luts_male():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Men's Health").first()
    if not category: category = Category(name="Men's Health"); db.add(category); db.commit()

    t = {
        "title": "Lower Urinary Tract Symptoms (LUTS) - Male",
        "description": "Comprehensive male LUTS assessment covering IPSS scoring, voiding vs storage symptom differentiation, alpha-blocker therapy, and urology referral criteria.",
        "category": "Men's Health",
        "content": {"sections": [
            {
                "title": "RED FLAGS - Prostate Cancer Screen",
                "section_type": "history",
                "questions": [
                    {"id": "luts_haematuria", "type": "toggle", "label": "Haematuria?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Haematuria + LUTS = ?prostate/bladder cancer. Urgent urology referral.", "red_flag_negative": ""},
                    {"id": "luts_pain", "type": "toggle", "label": "Pain? (Pelvic/Perineal)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Pain + LUTS = ?prostatitis, advanced prostate cancer.", "red_flag_negative": ""},
                    {"id": "luts_bone_pain", "type": "toggle", "label": "Bone Pain? (Especially Back/Pelvis)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Bone pain + LUTS = ?metastatic prostate cancer. Urgent PSA + urology.", "red_flag_negative": ""},
                    {"id": "luts_weight_loss", "type": "toggle", "label": "Unexplained Weight Loss?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Weight loss + LUTS = ?malignancy.", "red_flag_negative": ""},
                    {"id": "luts_back_pain", "type": "toggle", "label": "Back Pain?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Back pain + LUTS = ?spinal metastases from prostate cancer.", "red_flag_negative": ""},
                    {"id": "luts_fh_prostate", "type": "toggle", "label": "Family History of Prostate Cancer?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: FHx prostate cancer = increased risk. Lower threshold for PSA.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Symptom Classification",
                "section_type": "history",
                "questions": [
                    {"id": "luts_voiding", "type": "multi_select", "label": "Voiding Symptoms (Bladder Outflow Obstruction - BPH)", "required": True, "options": ["Urgency", "Hesitancy", "Straining", "Slow Stream", "Intermittency", "Terminal Dribbling", "Feeling of Incomplete Emptying", "None"]},
                    {"id": "luts_storage", "type": "multi_select", "label": "Storage Symptoms (Overactive Bladder / OAB)", "required": True, "options": ["Daytime Frequency", "Nocturia", "Urgency", "Urinary Incontinence", "None"]},
                    {"id": "luts_incontinence_frequency", "type": "text", "label": "Incontinence Frequency + Triggers", "required": False, "placeholder": "e.g., Once a month, associated with alcohol"},
                    {"id": "luts_post_micturition", "type": "multi_select", "label": "Post-Micturition Symptoms", "required": True, "options": ["Post-Micturition Dribble", "Sensation of Incomplete Emptying", "None"]},
                    {"id": "luts_stress_incontinence", "type": "toggle", "label": "Stress Incontinence? (Leakage on Coughing/Sneezing/Valsalva)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Stress incontinence = NOT typical of prostatic LUTS. Refer urology separately.", "red_flag_negative": ""},
                    {"id": "luts_predominant", "type": "single_select", "label": "Predominant Symptom Pattern", "required": True, "options": ["Voiding (Bladder Outflow Obstruction)", "Storage (OAB)", "Mixed Voiding + Storage", "Post-Micturition Only"]}
                ]
            },
            {
                "title": "IPSS (International Prostate Symptom Score)",
                "section_type": "assessment",
                "questions": [
                    {"id": "luts_ipss_score", "type": "number", "label": "IPSS Score (0-35) - https://www.ruh.nhs.uk/patients/urology/documents/patient_leaflets/form_ipss.pdf", "required": False, "placeholder": "e.g., 13"},
                    {"id": "luts_ipss_category", "type": "single_select", "label": "IPSS Severity", "required": False, "options": ["Mild (0-7)", "Moderate (8-19)", "Severe (20-35)"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Score and bother don't always correlate. Treatment based on patient's own perception of bother, not just score.", "red_flag_negative": ""},
                    {"id": "luts_bother", "type": "single_select", "label": "Patient's Perception of Bother", "required": True, "options": ["Not Bothered - Would Accept Watchful Waiting", "Mildly Bothered - Would Like Treatment", "Significantly Bothered - Affecting QoL"]}
                ]
            },
            {
                "title": "Other Relevant History",
                "section_type": "history",
                "questions": [
                    {"id": "luts_caffeine", "type": "toggle", "label": "Caffeine Intake?", "required": True},
                    {"id": "luts_diuretics", "type": "toggle", "label": "Diuretic Use?", "required": True},
                    {"id": "luts_recurrent_uti", "type": "toggle", "label": "Recurrent UTIs?", "required": False},
                    {"id": "luts_pelvic_surgery", "type": "toggle", "label": "Previous Pelvic Surgery or Irradiation?", "required": False},
                    {"id": "luts_ed", "type": "toggle", "label": "Erectile Problems?", "required": False},
                    {"id": "luts_bowel_change", "type": "toggle", "label": "Change in Bowel Habit?", "required": False}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "luts_abdo_mass", "type": "toggle", "label": "Abdominal Mass?", "required": False},
                    {"id": "luts_bladder_distension", "type": "toggle", "label": "Bladder Distension?", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Palpable bladder = chronic retention. Check renal function + refer urology.", "red_flag_negative": ""},
                    {"id": "luts_dre_size", "type": "single_select", "label": "DRE: Prostate Size", "required": False, "options": ["Normal", "Enlarged", "Not Examined"]},
                    {"id": "luts_dre_consistency", "type": "single_select", "label": "DRE: Consistency", "required": False, "options": ["Smooth", "Irregular / Nodular - RED FLAG", "Rubbery", "Hard - RED FLAG", "Not Examined"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Irregular/hard prostate = ?cancer. Urgent PSA + urology.", "red_flag_negative": ""},
                    {"id": "luts_dre_symmetry", "type": "single_select", "label": "DRE: Symmetry", "required": False, "options": ["Symmetrical", "Asymmetrical - RED FLAG", "Not Examined"]},
                    {"id": "luts_urine_dip", "type": "text", "label": "Urine Dipstick Findings", "required": False, "placeholder": "e.g., Normal / Leucocytes+ / Blood+"}
                ]
            },
            {
                "title": "Investigations",
                "section_type": "assessment",
                "differentials": [
                    "Benign Prostatic Hyperplasia (BPH) - Voiding Symptoms",
                    "Overactive Bladder (OAB) - Storage Symptoms",
                    "Mixed BPH + OAB",
                    "Chronic Prostatitis",
                    "Prostate Cancer (RED FLAG)",
                    "Urinary Tract Infection",
                    "Bladder Cancer (RED FLAG - Haematuria)",
                    "Neurogenic Bladder",
                    "Urethral Stricture"
                ],
                "questions": [
                    {"id": "luts_msu", "type": "toggle", "label": "MSU (Mid-Stream Urine) - Via Nurse Follow-Up?", "required": False},
                    {"id": "luts_renal", "type": "toggle", "label": "Renal Function? (Only if Palpable Bladder, Nocturnal Enuresis, or Recurrent UTI)", "required": False},
                    {"id": "luts_psa", "type": "toggle", "label": "PSA? (Only Based on Patient Preference or Clinical Judgement - NOT Routine)", "required": False}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Return if: haematuria, pain, weight loss, bone pain, or symptoms worsen. BPH: benign prostatic enlargement due to increased stromal + epithelial cells in peri-urethral area causing voiding symptoms (NICE 2018). OAB: urinary urgency with frequency + nocturia. First-line conservative: weight loss, reduce smoking/alcohol, voiding diary, bladder retraining, manage evening fluid intake, decrease caffeine. Voiding symptoms: Tamsulosin 400mcg OD / Silodosin 8mg OD / Doxazosin 1mg OD (limited efficacy, review IPSS at 6 months). If hypotensive concern: Dutasteride or Finasteride. No improvement: Dutasteride + Tamsulosin (Dutasteride takes ≥3 months for effect). Storage/OAB: Solifenacin + Tamsulosin. If OAB persists despite anticholinergic: Mirabegron (if BP <160/100). Stress incontinence: refer urology separately. If conservative + medical management not effective: refer urology for TURP.",
                "questions": [
                    {"id": "luts_diagnosis", "type": "single_select", "label": "Impression", "required": True, "options": ["BPH - Voiding Predominant", "OAB - Storage Predominant", "Mixed BPH + OAB", "Red Flags Present - Urgent Urology", "Stress Incontinence - Separate Urology Referral"]},
                    {"id": "luts_lifestyle", "type": "multi_select", "label": "Lifestyle Advice", "required": False, "options": ["Weight Loss", "Reduce Smoking", "Reduce Alcohol", "Voiding Diary / Bladder Diary", "Bladder Retraining", "Manage Evening Fluid Intake", "Decrease Caffeine"]},
                    {"id": "luts_alpha_blocker", "type": "single_select", "label": "Alpha-Blocker (Voiding Symptoms)", "required": False, "options": ["Tamsulosin 400mcg OD", "Silodosin 8mg OD", "Doxazosin 1mg OD", "Not Indicated"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Alpha-blockers have limited efficacy. Review with repeat IPSS at 6 months.", "red_flag_negative": ""},
                    {"id": "luts_5ari", "type": "toggle", "label": "Dutasteride / Finasteride? (If Hypotensive Concern + Enlarged Prostate)", "required": False},
                    {"id": "luts_combination", "type": "single_select", "label": "Combination Therapy (If Monotherapy Fails)", "required": False, "options": ["Dutasteride + Tamsulosin (≥3 Months for Effect)", "Solifenacin + Tamsulosin (Storage Symptoms)", "Mirabegron (If OAB Persists + BP <160/100)", "Not Indicated"]},
                    {"id": "luts_referral", "type": "single_select", "label": "Referral", "required": False, "options": ["None - GP Managed", "Urology - Routine (Failed Medical Management / TURP)", "Urology - Urgent (Red Flags / Haematuria)", "Urology - Stress Incontinence"]},
                    {"id": "luts_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., 6 months with repeat IPSS, sooner if red flags"}
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
    seed_luts_male()
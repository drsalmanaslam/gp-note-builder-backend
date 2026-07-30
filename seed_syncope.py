from app.database import SessionLocal
from app.models import User, Template, Category

def seed_syncope():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Cardiovascular").first()
    if not category: category = Category(name="Cardiovascular"); db.add(category); db.commit()

    t = {
        "title": "Syncope / Transient Loss of Consciousness",
        "description": "Focused assessment for syncope covering vasovagal vs cardiac vs seizure differentiation, orthostatic BP screening, ECG red flags, and driving advice.",
        "category": "Cardiovascular",
        "content": {"sections": [
            {
                "title": "Event Characteristics",
                "section_type": "history",
                "questions": [
                    {"id": "sync_presenting_complaint", "type": "text", "label": "Presenting Complaint", "required": True, "placeholder": "e.g., Collapsed yesterday - brief loss of consciousness"},
                    {"id": "sync_age", "type": "number", "label": "Age", "required": True, "placeholder": "e.g., 28"},
                    {"id": "sync_onset", "type": "single_select", "label": "Onset", "required": True, "options": ["Rapid (seconds)", "Gradual"]},
                    {"id": "sync_duration", "type": "single_select", "label": "Duration of LOC", "required": True, "options": ["<1 minute (syncope)", "1-5 minutes", ">5 minutes (?seizure)"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Prolonged LOC >5 min = ?seizure. Urgent neurology.", "red_flag_negative": ""},
                    {"id": "sync_recovery", "type": "single_select", "label": "Recovery", "required": True, "options": ["Immediate, complete, spontaneous", "Slow/prolonged (?seizure)", "With confusion/post-ictal (?seizure)"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Prolonged recovery/post-ictal confusion = ?seizure. Neurology referral.", "red_flag_negative": ""},
                    {"id": "sync_prodrome", "type": "multi_select", "label": "Prodromal Symptoms", "required": True, "options": ["Weakness", "Dizziness", "Blurred vision", "Nausea", "Sweating", "Palpitations", "None"], "is_red_flag": True, "red_flag_positive": "RED FLAG: NO prodrome (sudden collapse) = ?cardiogenic (arrhythmia). Urgent cardiology.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "RED FLAGS - Cardiac Syncope",
                "section_type": "history",
                "questions": [
                    {"id": "sync_exertional", "type": "toggle", "label": "Syncope DURING Exertion?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Exertional syncope = ?HOCM, aortic stenosis, VT. URGENT cardiology. Do NOT drive.", "red_flag_negative": ""},
                    {"id": "sync_supine", "type": "toggle", "label": "Syncope While Supine / Lying Down?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Supine syncope = ?arrhythmia (VT, complete heart block). Urgent cardiology.", "red_flag_negative": ""},
                    {"id": "sync_chest_pain", "type": "toggle", "label": "Chest Pain Before Syncope?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Chest pain + syncope = ?ACS, PE, aortic dissection. EMERGENCY A&E.", "red_flag_negative": ""},
                    {"id": "sync_palpitations", "type": "toggle", "label": "Palpitations Before Syncope?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Palpitations preceding syncope = ?arrhythmia. Urgent cardiology + Holter.", "red_flag_negative": ""},
                    {"id": "sync_family_scd", "type": "toggle", "label": "Family History Sudden Cardiac Death (<40)?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: FHx SCD = ?Brugada, LQTS, HOCM. Urgent cardiology + ECG.", "red_flag_negative": ""},
                    {"id": "sync_structural_hd", "type": "toggle", "label": "Known Structural Heart Disease?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Structural HD + syncope = high-risk cardiogenic. Urgent cardiology.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Seizure vs Syncope Differentiation",
                "section_type": "history",
                "questions": [
                    {"id": "sync_tongue_bite", "type": "single_select", "label": "Tongue Biting?", "required": True, "options": ["No", "Tip of tongue (syncope possible)", "Lateral tongue (SEIZURE) - RED FLAG"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Lateral tongue biting = seizure. Neurology referral.", "red_flag_negative": ""},
                    {"id": "sync_jerking", "type": "toggle", "label": "Limb Jerking / Myoclonus?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Prolonged rhythmic jerking = seizure. Brief myoclonus can occur in syncope.", "red_flag_negative": ""},
                    {"id": "sync_incontinence", "type": "toggle", "label": "Urinary Incontinence?", "required": True},
                    {"id": "sync_postictal", "type": "toggle", "label": "Post-Ictal Confusion / Prolonged Recovery?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Post-ictal state = seizure. Syncope recovery is immediate + complete.", "red_flag_negative": ""},
                    {"id": "sync_situational", "type": "multi_select", "label": "Situational Triggers?", "required": True, "options": ["Coughing", "Micturition", "Defecation", "Swallowing", "Pain/fear", "Prolonged standing", "Hot environment", "None"]}
                ]
            },
            {
                "title": "Examination & Orthostatic BP",
                "section_type": "examination",
                "questions": [
                    {"id": "sync_hr", "type": "number", "label": "Heart Rate (bpm)", "required": True, "placeholder": "e.g., 70"},
                    {"id": "sync_rhythm", "type": "single_select", "label": "Rhythm", "required": True, "options": ["Regular", "Irregular (AF)", "Irregularly irregular"]},
                    {"id": "sync_sitting_bp", "type": "text", "label": "Sitting BP (mmHg)", "required": True, "placeholder": "e.g., 120/80"},
                    {"id": "sync_standing_bp", "type": "text", "label": "3-Min Standing BP (mmHg)", "required": True, "placeholder": "e.g., 120/80"},
                    {"id": "sync_orthostatic", "type": "toggle", "label": "Orthostatic Hypotension? (SBP drop ≥20 or DBP ≥10)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Orthostatic hypotension = ?autonomic dysfunction, hypovolaemia, medications. Investigate cause.", "red_flag_negative": ""},
                    {"id": "sync_heart_sounds", "type": "single_select", "label": "Heart Sounds", "required": True, "options": ["HS 1+2 Normal", "Murmur (AS/HOCM) - RED FLAG", "Not assessed"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Murmur + syncope = ?AS/HOCM. Urgent echo.", "red_flag_negative": ""},
                    {"id": "sync_cn", "type": "toggle", "label": "Cranial Nerves II-XII Intact?", "required": False},
                    {"id": "sync_neuro", "type": "toggle", "label": "Full Neurological Exam Normal?", "required": False}
                ]
            },
            {
                "title": "ECG & Investigations",
                "section_type": "assessment",
                "differentials": [
                    "Reflex / Vasovagal Syncope (most common, benign)",
                    "Situational Syncope (cough, micturition, defecation)",
                    "Orthostatic Hypotension",
                    "Cardiac Syncope (arrhythmia - VT, complete HB, SSS)",
                    "Cardiac Syncope (structural - AS, HOCM)",
                    "Seizure / Epilepsy",
                    "TIA / Stroke (rarely causes isolated TLOC)",
                    "Psychogenic Pseudosyncope"
                ],
                "questions": [
                    {"id": "sync_ecg", "type": "single_select", "label": "12-Lead ECG", "required": True, "options": ["Normal sinus rhythm", "AF / Flutter", "Delta waves (WPW) - RED FLAG", "Long QTc - RED FLAG", "Brugada pattern - RED FLAG", "Heart block / BBB", "LVH / ST-T changes", "Not done"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Abnormal ECG = urgent cardiology. Do NOT diagnose vasovagal without normal ECG.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Return immediately / attend ED if: syncope occurs during exertion, while supine, associated with chest pain/palpitations, or without prodrome (sudden collapse). Do NOT drive if high-risk features present (exertional syncope, no prodrome, abnormal ECG, cardiac history). For simple vasovagal: reassurance, physical counter-pressure manoeuvres (hand/arm tensing, leg crossing, squatting at prodrome onset), adequate hydration (2-2.5L/day), avoid prolonged standing/hot environments/sudden standing. Consider thigh-high compression stockings if recurrent. If recurrent despite measures or if ECG abnormal: refer cardiology for echo/Holter/event recorder. If head trauma or new neuro deficit: CT brain + neurology.",
                "questions": [
                    {"id": "sync_diagnosis", "type": "single_select", "label": "Impression", "required": True, "options": ["Vasovagal Syncope (Simple Faint) - Low Risk", "Situational Syncope", "Orthostatic Hypotension", "Suspected Cardiac Syncope - URGENT", "Suspected Seizure - Neurology", "Uncertain - Needs Investigation"]},
                    {"id": "sync_pcm", "type": "toggle", "label": "Physical Counter-Pressure Manoeuvres Taught?", "required": False},
                    {"id": "sync_hydration", "type": "toggle", "label": "Hydration + Trigger Avoidance Advised?", "required": True},
                    {"id": "sync_driving", "type": "toggle", "label": "Driving Advice Given?", "required": True},
                    {"id": "sync_referral", "type": "single_select", "label": "Referral", "required": False, "options": ["None", "Cardiology (urgent - cardiac features)", "Cardiology (routine - Holter/echo)", "Neurology (?seizure)", "A&E (emergency)"]},
                    {"id": "sync_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., PRN if single episode, 4 weeks if recurrent"}
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
    seed_syncope()
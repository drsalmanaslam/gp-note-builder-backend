from app.database import SessionLocal
from app.models import Template, User

def seed_adhd_assessment():
    db = SessionLocal()
    
    title = "ADHD Assessment (Adult)"
    existing = db.query(Template).filter(Template.title == title).first()
    if existing:
        print(f"⏭️  SKIPPED: {title} already exists (ID={existing.id})")
        db.close()
        return
    
    template = Template(
        title=title,
        description="Adult ADHD assessment covering ASRS screening, childhood history, functional impairment, differential diagnosis, and referral pathway per NICE NG87.",
        category="Mental Health",
        content={
            "sections": [
                {
                    "title": "ASRS v1.1 Screening (6 Questions)",
                    "section_type": "history",
                    "questions": [
                        {"id": "adhd_asrs1", "type": "single_select", "label": "Trouble wrapping up final details of a project?", "required": True, "options": ["Never", "Rarely", "Sometimes", "Often", "Very Often"]},
                        {"id": "adhd_asrs2", "type": "single_select", "label": "Difficulty getting things in order when task requires organisation?", "required": True, "options": ["Never", "Rarely", "Sometimes", "Often", "Very Often"]},
                        {"id": "adhd_asrs3", "type": "single_select", "label": "Problems remembering appointments or obligations?", "required": True, "options": ["Never", "Rarely", "Sometimes", "Often", "Very Often"]},
                        {"id": "adhd_asrs4", "type": "single_select", "label": "Avoid or delay starting tasks that require lots of thought?", "required": True, "options": ["Never", "Rarely", "Sometimes", "Often", "Very Often"]},
                        {"id": "adhd_asrs5", "type": "single_select", "label": "Fidget or squirm with hands/feet when sitting for long time?", "required": True, "options": ["Never", "Rarely", "Sometimes", "Often", "Very Often"]},
                        {"id": "adhd_asrs6", "type": "single_select", "label": "Feel overly active and compelled to do things, as if driven by a motor?", "required": True, "options": ["Never", "Rarely", "Sometimes", "Often", "Very Often"]},
                        {"id": "adhd_asrs_score", "type": "text", "label": "ASRS Score (≥4/6 positive = screen positive)", "required": True, "placeholder": "e.g., 5/6"}
                    ]
                },
                {
                    "title": "Childhood History (Symptoms Before Age 12)",
                    "section_type": "history",
                    "questions": [
                        {"id": "adhd_childhood_school", "type": "text", "label": "School Reports / Teacher Comments", "required": False, "placeholder": "e.g., Easily distracted, could do better, disruptive"},
                        {"id": "adhd_childhood_hyperactive", "type": "toggle", "label": "Hyperactive/Restless as Child?", "required": True},
                        {"id": "adhd_childhood_inattentive", "type": "toggle", "label": "Difficulty Concentrating as Child?", "required": True},
                        {"id": "adhd_childhood_impulsive", "type": "toggle", "label": "Impulsive Behaviour as Child?", "required": True},
                        {"id": "adhd_childhood_support", "type": "toggle", "label": "Educational Support / SEN?", "required": False},
                        {"id": "adhd_family_history", "type": "toggle", "label": "Family History of ADHD?", "required": True}
                    ]
                },
                {
                    "title": "Current Functional Impairment",
                    "section_type": "history",
                    "questions": [
                        {"id": "adhd_work_impact", "type": "single_select", "label": "Impact on Work/Education", "required": True, "options": ["None", "Mild", "Moderate", "Severe - at risk of losing job/failing"]},
                        {"id": "adhd_relationship_impact", "type": "single_select", "label": "Impact on Relationships", "required": True, "options": ["None", "Mild", "Moderate", "Severe"]},
                        {"id": "adhd_daily_impact", "type": "text", "label": "Daily Life Examples", "required": True, "placeholder": "e.g., Loses keys daily, misses bills, can't complete tasks"},
                        {"id": "adhd_coping", "type": "text", "label": "Coping Strategies Used", "required": False, "placeholder": "e.g., Multiple alarms, lists, partner helps"}
                    ]
                },
                {
                    "title": "Differential & Comorbidity Screen",
                    "section_type": "history",
                    "questions": [
                        {"id": "adhd_anxiety", "type": "toggle", "label": "Anxiety Symptoms?", "required": True},
                        {"id": "adhd_depression", "type": "toggle", "label": "Depression / Low Mood?", "required": True},
                        {"id": "adhd_bipolar", "type": "toggle", "label": "Past Mania / Hypomania? (Screen for Bipolar)", "required": True},
                        {"id": "adhd_autism", "type": "toggle", "label": "ASD Traits?", "required": False},
                        {"id": "adhd_substance", "type": "single_select", "label": "Substance Use", "required": True, "options": ["None", "Occasional", "Regular", "Problematic - self-medicating"]},
                        {"id": "adhd_sleep", "type": "single_select", "label": "Sleep Pattern", "required": True, "options": ["Normal", "Difficulty falling asleep", "Restless sleep", "Delayed sleep phase"]},
                        {"id": "adhd_thyroid", "type": "toggle", "label": "Thyroid Symptoms?", "required": False},
                        {"id": "adhd_head_injury", "type": "toggle", "label": "History of Head Injury / Epilepsy?", "required": False}
                    ]
                },
                {
                    "title": "Physical Examination",
                    "section_type": "examination",
                    "questions": [
                        {"id": "adhd_bp", "type": "text", "label": "Blood Pressure", "required": True, "placeholder": "e.g., 120/80"},
                        {"id": "adhd_hr", "type": "text", "label": "Heart Rate", "required": True, "placeholder": "e.g., 72 bpm"},
                        {"id": "adhd_bmi", "type": "number", "label": "BMI", "required": True, "placeholder": "e.g., 24"},
                        {"id": "adhd_heart", "type": "single_select", "label": "Cardiovascular Exam", "required": True, "options": ["Normal", "Murmur", "Irregular pulse", "Not assessed"]},
                        {"id": "adhd_neuro", "type": "single_select", "label": "Brief Neurological", "required": False, "options": ["Normal", "Abnormal", "Not assessed"]}
                    ]
                },
                {
                    "title": "Assessment & Referral",
                    "section_type": "assessment",
                    "differentials": [
                        "Adult ADHD (Inattentive type)",
                        "Adult ADHD (Hyperactive-impulsive type)",
                        "Adult ADHD (Combined type)",
                        "Anxiety disorder mimicking ADHD",
                        "Bipolar disorder",
                        "Substance-induced attention problems",
                        "Sleep disorder causing cognitive impairment"
                    ],
                    "questions": [
                        {"id": "adhd_diagnosis", "type": "single_select", "label": "Likely Diagnosis", "required": True, "options": ["Probable ADHD - refer", "Possible ADHD - investigate further", "Unlikely ADHD - consider other diagnosis", "Requires specialist assessment"]},
                        {"id": "adhd_referral", "type": "single_select", "label": "Referral Pathway", "required": True, "options": ["Refer to Adult ADHD Service", "Refer to General Psychiatry", "Refer to Psychology for CBT", "Manage in primary care with advice", "Right to Choose (England)"]},
                        {"id": "adhd_bloods", "type": "multi_select", "label": "Bloods Ordered", "required": False, "options": ["FBC", "TFTs", "LFTs", "U&E", "None"]},
                        {"id": "adhd_ecg", "type": "toggle", "label": "ECG Done? (Required before stimulants)", "required": False}
                    ]
                },
                {
                    "title": "Management & Safety Netting",
                    "section_type": "plan",
                    "safety_netting": "ADHD assessment is specialist-led. While awaiting referral, provide psychoeducation and signpost to resources (ADHD UK, ADDISS). If starting medication, monitor BP, pulse, weight, and mood regularly. Stimulants carry risk of diversion and misuse. Report chest pain, palpitations, or severe mood changes immediately. Consider occupational health referral for workplace adjustments.",
                    "questions": [
                        {"id": "adhd_psychoeducation", "type": "toggle", "label": "Psychoeducation Provided?", "required": True},
                        {"id": "adhd_resources", "type": "toggle", "label": "Signposted to ADHD UK / Support Groups?", "required": False},
                        {"id": "adhd_occupational", "type": "toggle", "label": "Occupational Health Referral?", "required": False},
                        {"id": "adhd_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., Review after specialist assessment, check waiting list status in 4 weeks"}
                    ]
                }
            ]
        },
        is_public=True,
        created_by=admin.id
    )
    
    db.add(template)
    db.commit()
    print(f"✅ Created: {title}")
    db.close()

if __name__ == "__main__":
    seed_adhd_assessment()
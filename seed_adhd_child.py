from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_adhd_child():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: 
        print("Admin not found.")
        db.close()
        return

    category = db.query(Category).filter(Category.name == "Paediatrics").first()
    if not category: 
        category = Category(name="Paediatrics")
        db.add(category)
        db.commit()

    t = {
        "title": "ADHD Assessment (Child)",
        "description": "Initial assessment for children presenting with possible ADHD symptoms, covering core features, functional impact, and red flags.",
        "category": "Paediatrics",
        "content": {"sections": [
            {
                "title": "History",
                "section_type": "history",
                "questions": [
                    {
                        "id": "adhd_presenting_complaint",
                        "type": "text",
                        "label": "Presenting Complaint",
                        "required": True,
                        "placeholder": "e.g., 'Teacher says he can't sit still'",
                        "output_phrase": "c/o: {value}"
                    },
                    {
                        "id": "adhd_age",
                        "type": "number",
                        "label": "Child's Age",
                        "required": True,
                        "placeholder": "e.g., 8",
                        "output_phrase": "Age: {value} years"
                    },
                    {
                        "id": "adhd_symptoms_onset",
                        "type": "text",
                        "label": "Age of Symptom Onset",
                        "required": True,
                        "placeholder": "e.g., Since age 4 (before age 12)",
                        "output_phrase": "Onset: {value}"
                    },
                    {
                        "id": "adhd_inattention",
                        "type": "multi_select",
                        "label": "Inattention Symptoms",
                        "required": True,
                        "options": ["Difficulty focusing", "Easily distracted", "Forgetful", "Loses things", "Doesn't listen", "Avoids tasks needing focus", "None"],
                        "output_phrase": "Inattention: {value}"
                    },
                    {
                        "id": "adhd_hyperactivity",
                        "type": "multi_select",
                        "label": "Hyperactivity/Impulsivity Symptoms",
                        "required": True,
                        "options": ["Fidgety", "Can't sit still", "Interrupts", "Talks excessively", "Blurts out answers", "Difficulty waiting turn", "None"],
                        "output_phrase": "Hyperactivity: {value}"
                    },
                    {
                        "id": "adhd_settings",
                        "type": "multi_select",
                        "label": "Settings Where Symptoms Occur",
                        "required": True,
                        "options": ["Home", "School", "Social settings", "Extracurricular", "All settings - RED FLAG"],
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Symptoms in all settings - consider formal assessment.",
                        "red_flag_negative": "",
                        "output_phrase": "Settings: {value}"
                    },
                    {
                        "id": "adhd_impact",
                        "type": "multi_select",
                        "label": "Functional Impact",
                        "required": True,
                        "options": ["Academic difficulties", "Social difficulties", "Behavioural issues", "Family stress", "Self-esteem issues", "None"],
                        "output_phrase": "Impact: {value}"
                    },
                    {
                        "id": "adhd_school_report",
                        "type": "textarea",
                        "label": "School Feedback/Concerns",
                        "required": False,
                        "placeholder": "e.g., Teacher concerns, report card, SEN involvement",
                        "output_phrase": "School: {value}"
                    },
                    {
                        "id": "adhd_red_flags",
                        "type": "multi_select",
                        "label": "Red Flag Screen",
                        "required": True,
                        "options": ["Aggression/violence - RED FLAG", "Self-harm/suicidal ideation - RED FLAG", "Extreme impulsivity risking safety", "Suspected learning disability", "Developmental regression", "None"],
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: {value} - urgent child psychiatry / crisis referral if violence or self-harm.",
                        "red_flag_negative": "",
                        "output_phrase": "Red flags: {value}"
                    },
                    {
                        "id": "adhd_fh",
                        "type": "toggle",
                        "label": "Family History of ADHD?",
                        "required": False,
                        "output_phrase": "Family history: {value}"
                    },
                    {
                        "id": "adhd_comorbidities",
                        "type": "multi_select",
                        "label": "Comorbid Conditions",
                        "required": False,
                        "options": ["Anxiety", "Depression", "Conduct disorder", "Learning difficulties", "Autism", "Tourettes", "Sleep disorder", "None"],
                        "output_phrase": "Comorbidities: {value}"
                    }
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {
                        "id": "adhd_vitals",
                        "type": "text",
                        "label": "Vital Signs & Growth",
                        "required": False,
                        "placeholder": "e.g., Height 120cm, Weight 22kg, BMI 15, BP 110/70",
                        "output_phrase": "Vitals: {value}"
                    },
                    {
                        "id": "adhd_neurological",
                        "type": "textarea",
                        "label": "Neurological Examination",
                        "required": False,
                        "placeholder": "e.g., Normal neuro, no tics, no dysmorphic features",
                        "output_phrase": "Neuro: {value}"
                    }
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "ADHD (combined type)",
                    "ADHD (inattentive type)",
                    "ADHD (hyperactive-impulsive type)",
                    "Anxiety disorder (overlap with inattention)",
                    "Oppositional Defiant Disorder",
                    "Conduct Disorder",
                    "Sleep deprivation (mimics ADHD)",
                    "Autism Spectrum Condition (overlap)",
                    "Learning difficulties",
                    "Environmental factors (family stress, trauma)",
                    "Normal developmental variation"
                ],
                "questions": [
                    {
                        "id": "adhd_diagnosis",
                        "type": "single_select",
                        "label": "Clinical Impression",
                        "required": True,
                        "options": ["ADHD suspected - refer to CAMHS", "ADHD unlikely - other cause", "ADHD likely - need formal diagnosis", "Reassurance - normal variation", "Other"],
                        "output_phrase": "Diagnosis: {value}"
                    },
                    {
                        "id": "adhd_severity",
                        "type": "single_select",
                        "label": "Functional Impact Severity",
                        "required": True,
                        "options": ["Mild", "Moderate - significant impact", "Severe - needs urgent support"],
                        "output_phrase": "Severity: {value}"
                    }
                ]
            },
            {
                "title": "Plan",
                "section_type": "plan",
                "safety_netting": "Return/urgent if: Child becomes aggressive, risk to self or others, new suicidal thoughts, extreme emotional distress, or school exclusion. If no improvement with strategies, follow up in 4-6 weeks.",
                "questions": [
                    {
                        "id": "adhd_parent_advice",
                        "type": "toggle",
                        "label": "Parent Strategies Discussed?",
                        "required": False,
                        "output_phrase": "Parent advice: {value}"
                    },
                    {
                        "id": "adhd_school",
                        "type": "toggle",
                        "label": "School Support Recommended?",
                        "required": False,
                        "output_phrase": "School support: {value}"
                    },
                    {
                        "id": "adhd_referral",
                        "type": "single_select",
                        "label": "Referral Plan",
                        "required": True,
                        "options": ["CAMHS referral (routine)", "CAMHS referral (urgent)", "Speech & Language", "Educational Psychology", "Watchful waiting", "None"],
                        "output_phrase": "Referral: {value}"
                    },
                    {
                        "id": "adhd_followup",
                        "type": "text",
                        "label": "Follow-up Plan",
                        "required": True,
                        "placeholder": "e.g., Review in 4-6 weeks, or after CAMHS assessment",
                        "output_phrase": "Follow-up: {value}"
                    }
                ]
            }
        ]},
        "is_public": True
    }

    existing = db.query(Template).filter(Template.title == t["title"], Template.created_by == admin.id).first()
    
    if existing:
        existing.description = t["description"]
        existing.content = t["content"]
        existing.category = t["category"]
        existing.is_public = t["is_public"]
        existing.updated_at = datetime.now(timezone.utc)
        db.commit()
        print(f"🔄 Updated: {t['title']}")
    else:
        new_t = Template(
            title=t["title"], 
            description=t["description"], 
            category=t["category"], 
            content=t["content"], 
            is_public=True, 
            created_by=admin.id, 
            version=1
        )
        db.add(new_t)
        db.commit()
        print(f"✅ Template '{t['title']}' created with {len(t['content']['sections'])} sections!")
    
    db.close()

if __name__ == "__main__":
    seed_adhd_child()
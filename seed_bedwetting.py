from app.database import SessionLocal
from app.models import User, Template, Category

def seed_bedwetting():
    db = SessionLocal()
    
    admin = db.query(User).filter(User.role == "admin").first()
    if not admin:
        print("❌ No admin found!")
        db.close()
        return

    title = "Bedwetting / Nocturnal Enuresis (Children)"
    existing = db.query(Template).filter(Template.title == title).first()
    if existing:
        print(f"⏭️  SKIPPED: {title} already exists (ID={existing.id})")
        db.close()
        return

    template = Template(
        title=title,
        description="Assessment and management of nocturnal enuresis in children per NICE CG111, covering daytime symptoms, fluid management, alarm therapy, and desmopressin.",
        category="Paediatrics",
        content={"sections": [
            {
                "title": "History",
                "section_type": "history",
                "questions": [
                    {"id": "bed_age", "type": "number", "label": "Age of Child", "required": True, "placeholder": "e.g., 7"},
                    {"id": "bed_frequency", "type": "single_select", "label": "Frequency", "required": True, "options": ["Every night", "Most nights (4-6/week)", "Some nights (2-3/week)", "Occasional (≤1/week)"]},
                    {"id": "bed_primary_secondary", "type": "single_select", "label": "Primary or Secondary?", "required": True, "options": ["Primary (never been dry)", "Secondary (previously dry ≥6 months)"]},
                    {"id": "bed_dry_ever", "type": "toggle", "label": "Ever Been Dry for 6+ Months?", "required": True},
                    {"id": "bed_daytime_symptoms", "type": "multi_select", "label": "Daytime Urinary Symptoms?", "required": True, "options": ["Frequency", "Urgency", "Daytime wetting", "Dribbling", "Straining", "None"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Daytime symptoms + bedwetting = ?overactive bladder, UTI, constipation. Treat daytime symptoms FIRST.", "red_flag_negative": ""},
                    {"id": "bed_constipation", "type": "toggle", "label": "Constipation?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Constipation is the #1 cause of treatment-resistant enuresis. Treat constipation aggressively FIRST.", "red_flag_negative": ""},
                    {"id": "bed_fluid_intake", "type": "text", "label": "Evening Fluid Intake Pattern", "required": True, "placeholder": "e.g., Drinks 500ml water before bed"},
                    {"id": "bed_toilet_before_bed", "type": "toggle", "label": "Child Voids Before Bed?", "required": True},
                    {"id": "bed_wakes", "type": "toggle", "label": "Wakes When Wet?", "required": True},
                    {"id": "bed_family_history", "type": "toggle", "label": "Family History of Bedwetting?", "required": True}
                ]
            },
            {
                "title": "Red Flag Screen",
                "section_type": "history",
                "questions": [
                    {"id": "bed_polydipsia", "type": "toggle", "label": "Excessive Thirst / Drinking? (?Diabetes)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Polydipsia + polyuria = ?T1DM. Urgent urine dipstick for glucose.", "red_flag_negative": ""},
                    {"id": "bed_weight_loss", "type": "toggle", "label": "Weight Loss / Failure to Thrive?", "required": True},
                    {"id": "bed_uti_symptoms", "type": "toggle", "label": "UTI Symptoms? (Dysuria, frequency, fever)", "required": True},
                    {"id": "bed_neuro", "type": "toggle", "label": "Neurological Symptoms? (Gait, lower limb)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Neurological signs = ?tethered cord, spina bifida. Urgent paediatric referral.", "red_flag_negative": ""},
                    {"id": "bed_emotional", "type": "toggle", "label": "Recent Emotional Stress? (Bullying, family change)", "required": True},
                    {"id": "bed_development", "type": "single_select", "label": "Development", "required": True, "options": ["Normal for age", "Mild delay", "Significant delay"]}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "bed_bp", "type": "text", "label": "Blood Pressure", "required": False, "placeholder": "e.g., 95/60"},
                    {"id": "bed_growth", "type": "single_select", "label": "Growth Parameters", "required": True, "options": ["Normal", "Below 2nd centile", "Above 98th centile"]},
                    {"id": "bed_abdo", "type": "toggle", "label": "Faecal Mass Palpable? (Constipation)", "required": True},
                    {"id": "bed_spine", "type": "toggle", "label": "Spinal Abnormalities? (Dimple, hair tuft, sacral agenesis)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Spinal abnormality = ?spina bifida occulta, tethered cord. Paediatric referral.", "red_flag_negative": ""},
                    {"id": "bed_urinalysis", "type": "single_select", "label": "Urine Dipstick", "required": True, "options": ["Normal", "Glucose present - RED FLAG", "Nitrites/Leukocytes (UTI)", "Blood/Protein", "Not done"]}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "Primary Nocturnal Enuresis (most common)",
                    "Secondary Enuresis (UTI, stress, diabetes, constipation)",
                    "Overactive Bladder",
                    "Constipation-associated enuresis",
                    "Type 1 Diabetes Mellitus",
                    "UTI",
                    "Neurogenic bladder (rare)"
                ],
                "questions": [
                    {"id": "bed_diagnosis", "type": "single_select", "label": "Diagnosis", "required": True, "options": ["Primary nocturnal enuresis - no daytime symptoms", "Enuresis with daytime symptoms - treat daytime first", "Secondary enuresis - investigate cause", "Constipation-associated - treat constipation first"]},
                    {"id": "bed_severity", "type": "single_select", "label": "Impact on Child/Family", "required": True, "options": ["Mild - not bothered", "Moderate - affecting sleepovers/social", "Severe - significant distress, school refusal"]}
                ]
            },
            {
                "title": "Management Plan (NICE CG111)",
                "section_type": "plan",
                "safety_netting": "Bedwetting is common and NOT the child's fault - never punish or shame. Most children outgrow it. Treat constipation FIRST before starting alarm or medication. Fluid management: adequate daytime fluids, reduce fluids 2 hours before bed, avoid caffeine/fizzy drinks. Reward systems for agreed behaviour (e.g., voiding before bed, helping change sheets) NOT for dry nights. Return if: daytime wetting, urinary symptoms, excessive thirst, weight loss, or no improvement after 3 months of treatment.",
                "questions": [
                    {"id": "bed_plan", "type": "multi_select", "label": "Initial Management (First-Line)", "required": True, "options": ["Reassurance + explanation", "Fluid management advice", "Treat constipation (Movicol if needed)", "Reward system (for behaviour, not dry nights)", "Lifting/waking NOT recommended", "Enuresis alarm (first-line if motivated family)", "Desmopressin (for short-term: sleepovers, holidays)", "Refer enuresis clinic"]},
                    {"id": "bed_alarm", "type": "toggle", "label": "Enuresis Alarm Offered?", "required": False},
                    {"id": "bed_desmopressin", "type": "text", "label": "Desmopressin Dose (if prescribed)", "required": False, "placeholder": "e.g., 200mcg sublingual at bedtime"},
                    {"id": "bed_desmopressin_warning", "type": "toggle", "label": "WARNED: Fluid restriction with desmopressin (hyponatraemia risk)", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Must restrict fluids 1 hour before + 8 hours after desmopressin. Risk of fatal hyponatraemia.", "red_flag_negative": ""},
                    {"id": "bed_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., Review in 4 weeks, check progress with alarm/medication"}
                ]
            }
        ]},
        is_public=True,
        created_by=admin.id
    )
    
    db.add(template)
    db.commit()
    print(f"✅ Created: {title}")
    db.close()

if __name__ == "__main__":
    seed_bedwetting()
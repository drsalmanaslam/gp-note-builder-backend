from app.database import SessionLocal
from app.models import Template, User

def seed_postnatal_depression():
    db = SessionLocal()
    
    title = "Postnatal Depression (EPDS Assessment)"
    existing = db.query(Template).filter(Template.title == title).first()
    if existing:
        db.delete(existing)
        db.commit()
    
    admin = db.query(User).filter(User.role == "admin").first()
    
    template = Template(
        title=title,
        description="Postnatal depression assessment using Edinburgh Postnatal Depression Scale (EPDS), suicide & infanticide risk screen, breastfeeding review, and management per NICE CG192.",
        category="Women's Health",
        content={
            "sections": [
                {
                    "title": "EPDS Screening (10 Questions)",
                    "section_type": "history",
                    "questions": [
                        {"id": "pnd_epds_total", "type": "number", "label": "EPDS Total Score (/30)", "required": True, "placeholder": "e.g., 16"},
                        {"id": "pnd_epds_q10", "type": "single_select", "label": "EPDS Q10 - Thoughts of self-harm? (Score 0-3)", "required": True, "options": ["0 - Never", "1 - Hardly ever", "2 - Sometimes", "3 - Yes, quite often"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Any score on Q10 = urgent risk assessment for suicide and infanticide. Consider emergency referral.", "red_flag_negative": ""},
                        {"id": "pnd_when_completed", "type": "single_select", "label": "Timing of EPDS", "required": True, "options": ["6-8 weeks postnatal", "3-4 months postnatal", "Other"]},
                        {"id": "pnd_onset", "type": "text", "label": "When Did Symptoms Start?", "required": True, "placeholder": "e.g., Since birth, gradually over 3 weeks"},
                        {"id": "pnd_baby_blues", "type": "toggle", "label": "Baby Blues Initially? (Resolved by day 10)", "required": True},
                        {"id": "pnd_previous_mh", "type": "toggle", "label": "Previous Mental Health History?", "required": True},
                        {"id": "pnd_previous_pnd", "type": "toggle", "label": "Previous Postnatal Depression?", "required": True},
                        {"id": "pnd_family_mh", "type": "toggle", "label": "Family History of Postnatal Mental Illness?", "required": True}
                    ]
                },
                {
                    "title": "Risk Assessment - CRITICAL",
                    "section_type": "history",
                    "questions": [
                        {"id": "pnd_suicide_risk", "type": "toggle", "label": "Active Suicidal Ideation?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Suicidal ideation = urgent psychiatric assessment. Consider admission to Mother & Baby Unit.", "red_flag_negative": ""},
                        {"id": "pnd_infanticide", "type": "toggle", "label": "Thoughts of Harming Baby?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Thoughts of harming baby = EMERGENCY. Immediate safeguarding referral and psychiatric assessment. Do NOT leave mother alone with baby.", "red_flag_negative": ""},
                        {"id": "pnd_psychosis", "type": "multi_select", "label": "Psychotic Symptoms?", "required": True, "options": ["Confusion", "Hallucinations", "Delusions", "Paranoia", "None"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Psychotic symptoms = ?Postpartum psychosis (psychiatric emergency). Same-day admission to Mother & Baby Unit.", "red_flag_negative": ""},
                        {"id": "pnd_support", "type": "single_select", "label": "Support Network", "required": True, "options": ["Strong partner/family support", "Some support", "Isolated / No support"]},
                        {"id": "pnd_safeguarding", "type": "toggle", "label": "Safeguarding Concerns for Baby?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Safeguarding concern = immediate referral to Children's Services.", "red_flag_negative": ""}
                    ]
                },
                {
                    "title": "Maternal & Baby Wellbeing",
                    "section_type": "history",
                    "questions": [
                        {"id": "pnd_sleep", "type": "single_select", "label": "Sleep (Excluding Baby Waking)", "required": True, "options": ["Getting adequate sleep", "Moderately sleep deprived", "Severely sleep deprived"]},
                        {"id": "pnd_breastfeeding", "type": "single_select", "label": "Feeding Method", "required": True, "options": ["Exclusively breastfeeding", "Mixed feeding", "Formula feeding"]},
                        {"id": "pnd_breastfeeding_difficulty", "type": "toggle", "label": "Breastfeeding Difficulties?", "required": False},
                        {"id": "pnd_baby_health", "type": "toggle", "label": "Baby Health Concerns?", "required": False},
                        {"id": "pnd_bonding", "type": "single_select", "label": "Bonding with Baby", "required": True, "options": ["Strong bond", "Some difficulty", "Significant difficulty", "Feeling detached"]},
                        {"id": "pnd_partner_support", "type": "toggle", "label": "Partner Supportive?", "required": False},
                        {"id": "pnd_domestic_abuse", "type": "toggle", "label": "Domestic Abuse? (Ask routinely)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Domestic abuse = safeguarding risk. Offer support and referral to IDVA.", "red_flag_negative": ""}
                    ]
                },
                {
                    "title": "Physical Health",
                    "section_type": "examination",
                    "questions": [
                        {"id": "pnd_bp", "type": "text", "label": "Blood Pressure", "required": False, "placeholder": "e.g., 120/80"},
                        {"id": "pnd_thyroid", "type": "toggle", "label": "Thyroid Symptoms? (Fatigue, weight change, hair loss)", "required": True},
                        {"id": "pnd_anaemia", "type": "toggle", "label": "Symptoms of Anaemia? (Pallor, SOB, palpitations)", "required": False},
                        {"id": "pnd_bloods", "type": "multi_select", "label": "Blood Tests", "required": False, "options": ["FBC", "TFTs", "Ferritin", "B12/Folate", "None"]},
                        {"id": "pnd_contraception", "type": "toggle", "label": "Contraception Discussed?", "required": False}
                    ]
                },
                {
                    "title": "Assessment & Diagnosis",
                    "section_type": "assessment",
                    "differentials": [
                        "Postnatal Depression (EPDS ≥10)",
                        "Baby Blues (resolved by day 10 - NOT depression)",
                        "Postpartum Psychosis (psychiatric emergency)",
                        "Adjustment Disorder",
                        "Thyroid Dysfunction (postpartum thyroiditis)",
                        "Anaemia causing fatigue",
                        "OCD (intrusive thoughts about baby without intent)"
                    ],
                    "questions": [
                        {"id": "pnd_diagnosis", "type": "single_select", "label": "Diagnosis", "required": True, "options": ["Mild PND (EPDS 10-12)", "Moderate PND (EPDS 13-18)", "Severe PND (EPDS ≥19)", "Postpartum Psychosis - EMERGENCY", "Not PND - Baby Blues / Adjustment"]},
                        {"id": "pnd_risk_level", "type": "single_select", "label": "Overall Risk Level", "required": True, "options": ["Low - manage in primary care", "Medium - involve Perinatal Mental Health Team", "High - urgent psychiatric assessment", "Emergency - same-day admission"]}
                    ]
                },
                {
                    "title": "Management Plan",
                    "section_type": "plan",
                    "safety_netting": "If you feel worse, have thoughts of harming yourself or your baby, or feel confused/hear voices, seek help IMMEDIATELY. Contact GP, Health Visitor, call 111, or attend A&E. Mother & Baby Units provide specialist inpatient care while keeping mother and baby together. Do not stop medication suddenly. Breastfeeding-safe antidepressants: Sertraline (first-line), Paroxetine. Most antidepressants are compatible with breastfeeding - discuss risks vs benefits. Continue treatment for at least 6-12 months after remission.",
                    "questions": [
                        {"id": "pnd_plan", "type": "multi_select", "label": "Management", "required": True, "options": ["Psychoeducation + support", "Health Visitor involvement", "Perinatal Mental Health Team referral", "Start antidepressant (Sertraline first-line)", "CBT / Counselling referral", "Mother & Baby Unit admission", "Crisis Team referral", "Children's Services referral"]},
                        {"id": "pnd_medication", "type": "text", "label": "Medication Prescribed", "required": False, "placeholder": "e.g., Sertraline 50mg OD (breastfeeding safe)"},
                        {"id": "pnd_hv_referral", "type": "toggle", "label": "Health Visitor Notified?", "required": True},
                        {"id": "pnd_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., Review in 2 weeks, repeat EPDS. HV to visit weekly."}
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
    seed_postnatal_depression()
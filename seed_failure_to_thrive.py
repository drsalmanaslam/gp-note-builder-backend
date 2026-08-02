from app.database import SessionLocal
from app.models import Template, User

def seed_failure_to_thrive():
    db = SessionLocal()
    
    title = "Failure to Thrive / Faltering Growth (Children)"
    existing = db.query(Template).filter(Template.title == title).first()
    if existing:
        db.delete(existing)
        db.commit()
    
    admin = db.query(User).filter(User.role == "admin").first()
    
    template = Template(
        title=title,
        description="Assessment of faltering growth in children covering growth chart interpretation, red flags, feeding history, organic vs non-organic causes, and safeguarding per RCPCH guidelines.",
        category="Paediatrics",
        content={
            "sections": [
                {
                    "title": "Growth Assessment",
                    "section_type": "history",
                    "questions": [
                        {"id": "ftt_age", "type": "text", "label": "Age of Child", "required": True, "placeholder": "e.g., 8 months"},
                        {"id": "ftt_weight_centile", "type": "text", "label": "Current Weight Centile", "required": True, "placeholder": "e.g., 0.4th"},
                        {"id": "ftt_previous_centile", "type": "text", "label": "Previous Weight Centile", "required": True, "placeholder": "e.g., 25th at 4 months"},
                        {"id": "ftt_height_centile", "type": "text", "label": "Height/Length Centile", "required": False, "placeholder": "e.g., 9th"},
                        {"id": "ftt_hc_centile", "type": "text", "label": "Head Circumference Centile", "required": False, "placeholder": "e.g., 25th"},
                        {"id": "ftt_birth_weight", "type": "text", "label": "Birth Weight & Gestation", "required": True, "placeholder": "e.g., 3.2kg at 39 weeks"},
                        {"id": "ftt_crossed_centiles", "type": "toggle", "label": "Crossed ≥2 Centile Lines?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Crossing ≥2 centile lines = significant faltering growth. Needs urgent investigation.", "red_flag_negative": ""},
                        {"id": "ftt_weight_loss", "type": "toggle", "label": "Actual Weight Loss?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Weight loss in infant/child = urgent assessment. Consider admission if <70% expected weight.", "red_flag_negative": ""}
                    ]
                },
                {
                    "title": "Feeding History",
                    "section_type": "history",
                    "questions": [
                        {"id": "ftt_feeding_method", "type": "single_select", "label": "Feeding Method", "required": True, "options": ["Breastfeeding", "Formula feeding", "Mixed", "Weaning/Solids"]},
                        {"id": "ftt_feed_frequency", "type": "text", "label": "Feeding Frequency & Duration", "required": True, "placeholder": "e.g., Every 3 hours, 20 mins per breast"},
                        {"id": "ftt_breastfeeding_issues", "type": "multi_select", "label": "Breastfeeding Issues", "required": False, "options": ["Poor latch", "Nipple pain", "Low milk supply", "Tongue-tie suspected", "None"]},
                        {"id": "ftt_formula_amount", "type": "text", "label": "Formula Amount (ml per 24h)", "required": False, "placeholder": "e.g., 600ml"},
                        {"id": "ftt_solids_intake", "type": "text", "label": "Solids Intake (if weaning)", "required": False, "placeholder": "e.g., Small amounts, refuses most foods"},
                        {"id": "ftt_feeding_difficulty", "type": "multi_select", "label": "Feeding Difficulties", "required": True, "options": ["Vomiting", "Choking/Coughing during feeds", "Refusing feeds", "Takes very long to feed", "Fussy eater", "None"]}
                    ]
                },
                {
                    "title": "Output & GI Symptoms",
                    "section_type": "history",
                    "questions": [
                        {"id": "ftt_wet_nappies", "type": "text", "label": "Wet Nappies per Day", "required": True, "placeholder": "e.g., 3-4"},
                        {"id": "ftt_stools", "type": "single_select", "label": "Bowel Movements", "required": True, "options": ["Normal - daily", "Constipation", "Diarrhoea", "Foul-smelling/greasy (malabsorption)", "Blood in stool"]},
                        {"id": "ftt_vomiting", "type": "toggle", "label": "Regular Vomiting / Reflux?", "required": True},
                        {"id": "ftt_proj_vomiting", "type": "toggle", "label": "Projectile Vomiting? (?Pyloric Stenosis)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Projectile vomiting in infant = ?pyloric stenosis. Urgent surgical referral.", "red_flag_negative": ""}
                    ]
                },
                {
                    "title": "Red Flag Symptoms",
                    "section_type": "history",
                    "questions": [
                        {"id": "ftt_dysmorphic", "type": "toggle", "label": "Dysmorphic Features?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Dysmorphic features = ?genetic syndrome. Refer paediatrics.", "red_flag_negative": ""},
                        {"id": "ftt_development", "type": "single_select", "label": "Developmental Milestones", "required": True, "options": ["Normal for age", "Mild delay", "Significant delay", "Regression"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Regression = neurological emergency. Urgent paediatric referral.", "red_flag_negative": ""},
                        {"id": "ftt_cardiac", "type": "toggle", "label": "Cyanosis / SOB / Murmur?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Cardiac symptoms = ?congenital heart disease. Urgent paediatric cardiology.", "red_flag_negative": ""},
                        {"id": "ftt_recurrent_infections", "type": "toggle", "label": "Recurrent Infections?", "required": False},
                        {"id": "ftt_alertness", "type": "single_select", "label": "Alertness / Interaction", "required": True, "options": ["Alert and interactive", "Lethargic / Poor interaction"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Lethargy = urgent assessment. Consider sepsis, metabolic disorder.", "red_flag_negative": ""}
                    ]
                },
                {
                    "title": "Social & Safeguarding",
                    "section_type": "history",
                    "questions": [
                        {"id": "ftt_parental_concern", "type": "text", "label": "Parental Concerns", "required": True, "placeholder": "e.g., Worried he's not gaining, feels he eats very little"},
                        {"id": "ftt_maternal_mh", "type": "toggle", "label": "Maternal Mental Health Concerns?", "required": True},
                        {"id": "ftt_social_support", "type": "single_select", "label": "Family Support", "required": True, "options": ["Good support", "Some concerns", "Significant concerns - safeguarding"]},
                        {"id": "ftt_safeguarding", "type": "toggle", "label": "Any Safeguarding Concerns?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Safeguarding concern = immediate referral to Children's Services per local protocol.", "red_flag_negative": ""}
                    ]
                },
                {
                    "title": "Assessment & Differential",
                    "section_type": "assessment",
                    "differentials": [
                        "Non-organic / Feeding difficulty (most common)",
                        "GORD / CMPA",
                        "Coeliac disease",
                        "Cystic Fibrosis",
                        "Congenital heart disease",
                        "Chronic renal disease",
                        "Genetic syndrome",
                        "Neglect / Safeguarding",
                        "Inborn error of metabolism"
                    ],
                    "questions": [
                        {"id": "ftt_severity", "type": "single_select", "label": "Severity", "required": True, "options": ["Mild - monitoring in community", "Moderate - paediatric outpatient referral", "Severe - urgent paediatric assessment", "Emergency - same-day admission"]},
                        {"id": "ftt_likely_cause", "type": "single_select", "label": "Likely Cause", "required": True, "options": ["Feeding/Non-organic", "Organic - GI", "Organic - Other", "Mixed", "Safeguarding concern"]}
                    ]
                },
                {
                    "title": "Management Plan",
                    "section_type": "plan",
                    "safety_netting": "Return immediately or attend A&E if: child becomes lethargic, stops feeding completely, has bilious (green) vomiting, shows signs of dehydration (dry mouth, sunken fontanelle, reduced wet nappies), or develops breathing difficulty. Weekly weight checks with Health Visitor. If breastfeeding: refer to lactation consultant / infant feeding team. If formula feeding: consider high-energy formula (e.g., SMA High Energy) on dietician advice. Health Visitor referral for ongoing monitoring.",
                    "questions": [
                        {"id": "ftt_plan", "type": "multi_select", "label": "Management", "required": True, "options": ["Health Visitor - weekly weights", "Dietician referral", "Paediatric referral", "Lactation consultant", "Trial of high-energy formula", "SALT if feeding difficulty", "Children's Services if safeguarding", "Admission for observation"]},
                        {"id": "ftt_investigations", "type": "multi_select", "label": "Investigations", "required": False, "options": ["FBC, CRP", "U&E, LFTs", "Coeliac screen", "TFTs", "Urine MCS", "Sweat test", "None - clinical monitoring"]},
                        {"id": "ftt_hv_notified", "type": "toggle", "label": "Health Visitor Notified?", "required": True},
                        {"id": "ftt_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., Weekly HV weights, paediatric clinic in 4 weeks, GP review in 2 weeks"}
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
    seed_failure_to_thrive()
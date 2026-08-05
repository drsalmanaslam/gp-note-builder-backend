from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone


def seed_sepsis_recognition():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin:
        print("Admin not found.")
        db.close()
        return

    category = db.query(Category).filter(Category.name == "Infectious Disease").first()
    if not category:
        category = Category(name="Infectious Disease")
        db.add(category)
        db.commit()

    t = {
        "title": "Sepsis Recognition (GP)",
        "description": "Urgent sepsis screening tool for general practice using NICE/SIRS criteria. Identifies red flags, risk factors, and guides immediate management including emergency referral.",
        "category": "Infectious Disease",
        "content": {
            "sections": [
                {
                    "title": "Suspected Source of Infection",
                    "section_type": "history",
                    "questions": [
                        {
                            "id": "sepsis_source",
                            "type": "single_select",
                            "label": "Likely Source of Infection",
                            "required": True,
                            "options": [
                                "Respiratory (pneumonia, LRTI)",
                                "Urinary tract (UTI, pyelonephritis)",
                                "Skin/soft tissue (cellulitis, wound)",
                                "Abdominal (perforation, cholecystitis, abscess)",
                                "Meningitis/CNS",
                                "Line-related / IV access",
                                "Post-surgical / procedure",
                                "Unknown source",
                                "Other"
                            ],
                            "output_phrase": "Suspected source: {value}"
                        },
                        {
                            "id": "sepsis_temp",
                            "type": "number",
                            "label": "Temperature (°C)",
                            "required": True,
                            "placeholder": "e.g., 38.5",
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Temperature <36°C or >38.3°C = SIRS criteria met. Hypothermia (<36°C) is particularly ominous.",
                            "red_flag_negative": "",
                            "output_phrase": "Temp: {value}°C"
                        }
                    ]
                },
                {
                    "title": "SIRS Criteria (≥2 = Sepsis Risk)",
                    "section_type": "examination",
                    "questions": [
                        {
                            "id": "sepsis_hr",
                            "type": "number",
                            "label": "Heart Rate (bpm)",
                            "required": True,
                            "placeholder": "e.g., 105",
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: HR >90 bpm = SIRS criterion met. Tachycardia is an early sign of sepsis.",
                            "red_flag_negative": "",
                            "output_phrase": "HR: {value} bpm"
                        },
                        {
                            "id": "sepsis_rr",
                            "type": "number",
                            "label": "Respiratory Rate (breaths/min)",
                            "required": True,
                            "placeholder": "e.g., 24",
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: RR >20/min = SIRS criterion met. Tachypnoea may be the earliest sign of deterioration.",
                            "red_flag_negative": "",
                            "output_phrase": "RR: {value}/min"
                        },
                        {
                            "id": "sepsis_bp_systolic",
                            "type": "number",
                            "label": "BP Systolic (mmHg)",
                            "required": True,
                            "placeholder": "e.g., 95",
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: SBP <100 mmHg or MAP <65 = hypotensive. Indicates septic shock if lactate >2 and vasopressors required.",
                            "red_flag_negative": "",
                            "output_phrase": "BP: {value}/"
                        },
                        {
                            "id": "sepsis_bp_diastolic",
                            "type": "number",
                            "label": "BP Diastolic (mmHg)",
                            "required": True,
                            "placeholder": "e.g., 60",
                            "output_phrase": "{value} mmHg"
                        },
                        {
                            "id": "sepsis_sats",
                            "type": "number",
                            "label": "O2 Saturations (%)",
                            "required": True,
                            "placeholder": "e.g., 94",
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: SpO2 <92% on air = severe hypoxaemia. Give high-flow O2 and urgent transfer.",
                            "red_flag_negative": "",
                            "output_phrase": "SpO2: {value}%"
                        }
                    ]
                },
                {
                    "title": "High-Risk Factors",
                    "section_type": "history",
                    "questions": [
                        {
                            "id": "sepsis_age_risk",
                            "type": "toggle",
                            "label": "Age >75?",
                            "required": True,
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Age >75 = high risk. Lower threshold for hospital admission and IV antibiotics.",
                            "red_flag_negative": "",
                            "output_phrase": "Age >75: {value}"
                        },
                        {
                            "id": "sepsis_immunocompromised",
                            "type": "toggle",
                            "label": "Immunocompromised? (chemo, steroids, transplant, HIV, asplenia)",
                            "required": True,
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Immunocompromised = high risk of overwhelming sepsis. Early IV antibiotics essential.",
                            "red_flag_negative": "",
                            "output_phrase": "Immunocompromised: {value}"
                        },
                        {
                            "id": "sepsis_comorbid",
                            "type": "multi_select",
                            "label": "Significant Comorbidities",
                            "required": True,
                            "options": [
                                "Diabetes",
                                "Chronic kidney disease",
                                "Chronic liver disease",
                                "COPD",
                                "Heart failure",
                                "Recent surgery (<6 weeks)",
                                "Indwelling catheter/lines",
                                "None"
                            ],
                            "output_phrase": "Comorbidities: {value}"
                        }
                    ]
                },
                {
                    "title": "Red Flag Signs (NICE NG51)",
                    "section_type": "examination",
                    "questions": [
                        {
                            "id": "sepsis_mental_state",
                            "type": "single_select",
                            "label": "Mental Status / Conscious Level",
                            "required": True,
                            "options": [
                                "Alert and orientated",
                                "Confused / altered mental state (new onset)",
                                "Drowsy / reduced GCS",
                                "Unresponsive"
                            ],
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Altered mental state = objective evidence of new altered mental state. Emergency admission. May indicate cerebral hypoperfusion.",
                            "red_flag_negative": "",
                            "output_phrase": "Mental status: {value}"
                        },
                        {
                            "id": "sepsis_mottled",
                            "type": "toggle",
                            "label": "Mottled/Ashen Appearance or Cyanosis?",
                            "required": True,
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Mottled/ashen/cyanotic = signs of poor perfusion/shock. Emergency admission.",
                            "red_flag_negative": "",
                            "output_phrase": "Mottled/cyanotic: {value}"
                        },
                        {
                            "id": "sepsis_urine_output",
                            "type": "single_select",
                            "label": "Urine Output (if available)",
                            "required": False,
                            "options": [
                                "Normal",
                                "Reduced (<0.5ml/kg/hr)",
                                "Anuric",
                                "Not assessed"
                            ],
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Oliguria/anuria = acute kidney injury. Sign of organ dysfunction in sepsis.",
                            "red_flag_negative": "",
                            "output_phrase": "Urine output: {value}"
                        },
                        {
                            "id": "sepsis_lactate",
                            "type": "single_select",
                            "label": "Lactate (if point-of-care available)",
                            "required": False,
                            "options": [
                                "Not available",
                                "<2 mmol/L",
                                "2-4 mmol/L",
                                ">4 mmol/L"
                            ],
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Lactate >2 mmol/L indicates tissue hypoperfusion. >4 mmol/L = severe sepsis with high mortality risk. Emergency admission.",
                            "red_flag_negative": "",
                            "output_phrase": "Lactate: {value}"
                        }
                    ]
                },
                {
                    "title": "Immediate Management",
                    "section_type": "assessment",
                    "differentials": [
                        "Sepsis (SIRS + confirmed/suspected infection)",
                        "Severe Sepsis (sepsis + organ dysfunction)",
                        "Septic Shock (sepsis + hypotension despite fluids + lactate >2)",
                        "Non-infective SIRS (pancreatitis, trauma, burns)",
                        "Anaphylaxis",
                        "Adrenal crisis"
                    ],
                    "questions": [
                        {
                            "id": "sepsis_diagnosis",
                            "type": "single_select",
                            "label": "Clinical Impression",
                            "required": True,
                            "options": [
                                "SIRS (≥2 criteria, no confirmed infection)",
                                "Sepsis (SIRS + suspected/confirmed infection)",
                                "Severe Sepsis (sepsis + organ dysfunction)",
                                "Septic Shock (hypotension + lactate >2)",
                                "Infection without SIRS",
                                "Non-infective cause"
                            ],
                            "output_phrase": "Diagnosis: {value}"
                        },
                        {
                            "id": "sepsis_qsofa",
                            "type": "single_select",
                            "label": "qSOFA Score (≥2 = high risk)",
                            "required": True,
                            "options": [
                                "0",
                                "1",
                                "2 - HIGH RISK",
                                "3 - HIGH RISK"
                            ],
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: qSOFA ≥2 + suspected infection = high mortality risk. Emergency admission for IV antibiotics and fluids within 1 hour.",
                            "red_flag_negative": "",
                            "output_phrase": "qSOFA: {value}"
                        }
                    ]
                },
                {
                    "title": "Management Plan",
                    "section_type": "plan",
                    "safety_netting": "If any RED FLAG or qSOFA ≥2: Call 999/112 immediately — arrange emergency transfer to hospital. If admission declined, document capacity assessment and safety-net rigorously. Give IM Benzylpenicillin 1.2g STAT (or Clarithromycin 500mg if penicillin-allergic) if meningococcal sepsis suspected and transfer delayed. If not for immediate admission: review within 4-6 hours, escalate if any deterioration. Advise family/carer to call 999 if: confusion, reduced consciousness, mottled skin, severe breathlessness, or patient becomes unresponsive. Document all observations and safety-netting clearly.",
                    "questions": [
                        {
                            "id": "sepsis_action",
                            "type": "single_select",
                            "label": "Action Taken",
                            "required": True,
                            "options": [
                                "999 ambulance — emergency transfer to hospital",
                                "Urgent referral to medical team (same day)",
                                "IM Benzylpenicillin given (suspected meningococcal sepsis)",
                                "Patient declined admission — capacity assessed and documented",
                                "Not septic — routine management"
                            ],
                            "output_phrase": "Action: {value}"
                        },
                        {
                            "id": "sepsis_antibiotics",
                            "type": "toggle",
                            "label": "IV/IM Antibiotics Given in Practice? (if transfer delayed)",
                            "required": False,
                            "output_phrase": "Antibiotics given: {value}"
                        },
                        {
                            "id": "sepsis_fluids",
                            "type": "toggle",
                            "label": "IV Fluids Started? (if transfer delayed and hypotensive)",
                            "required": False,
                            "output_phrase": "IV fluids: {value}"
                        },
                        {
                            "id": "sepsis_safety_net",
                            "type": "toggle",
                            "label": "Family/Carer Advised to Call 999 if Deterioration?",
                            "required": True,
                            "output_phrase": "Safety-net given: {value}"
                        },
                        {
                            "id": "sepsis_followup",
                            "type": "text",
                            "label": "Follow-up Plan",
                            "required": True,
                            "placeholder": "e.g., Admitted to hospital via ambulance. Will follow up post-discharge.",
                            "output_phrase": "Follow-up: {value}"
                        }
                    ]
                }
            ]
        },
        "is_public": True
    }

    existing = db.query(Template).filter(
        Template.title == t["title"],
        Template.created_by == admin.id
    ).first()

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
    seed_sepsis_recognition()
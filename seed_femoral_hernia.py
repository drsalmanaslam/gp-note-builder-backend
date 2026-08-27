from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_femoral_hernia():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: 
        print("Admin not found.")
        db.close()
        return

    category = db.query(Category).filter(Category.name == "General Surgery").first()
    if not category: 
        category = Category(name="General Surgery")
        db.add(category)
        db.commit()

    t = {
        "title": "Femoral Hernia Assessment",
        "description": "Practical GP assessment and management of femoral hernias. Femoral hernias deserve a lower threshold for surgical referral due to higher risk of incarceration/strangulation.",
        "category": "General Surgery",
        "content": {"sections": [
            {
                "title": "History",
                "section_type": "history",
                "questions": [
                    {
                        "id": "femoral_presenting_complaint",
                        "type": "text",
                        "label": "Presenting Complaint",
                        "required": True,
                        "placeholder": "e.g., Lump in right groin noticed 2 weeks ago",
                        "output_phrase": "c/o: {value}"
                    },
                    {
                        "id": "femoral_onset_duration",
                        "type": "text",
                        "label": "Onset and Duration",
                        "required": True,
                        "placeholder": "e.g., Noticed 2 weeks ago, gradually increasing",
                        "output_phrase": "Onset: {value}"
                    },
                    {
                        "id": "femoral_location",
                        "type": "single_select",
                        "label": "Location of Lump",
                        "required": True,
                        "options": ["Groin", "Upper medial thigh", "Groin + thigh", "Uncertain"],
                        "output_phrase": "Location: {value}"
                    },
                    {
                        "id": "femoral_side",
                        "type": "single_select",
                        "label": "Side",
                        "required": True,
                        "options": ["Right", "Left", "Bilateral", "Uncertain"],
                        "output_phrase": "Side: {value}"
                    },
                    {
                        "id": "femoral_size_change",
                        "type": "single_select",
                        "label": "Change in Size",
                        "required": True,
                        "options": ["Stable", "Increasing", "Intermittent", "Decreasing"],
                        "output_phrase": "Size change: {value}"
                    },
                    {
                        "id": "femoral_pain",
                        "type": "single_select",
                        "label": "Pain/Discomfort",
                        "required": True,
                        "options": ["None", "Mild discomfort", "Painful", "Severe pain - RED FLAG"],
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Severe pain - consider incarceration/strangulation.",
                        "red_flag_negative": "",
                        "output_phrase": "Pain: {value}"
                    },
                    {
                        "id": "femoral_aggravating",
                        "type": "multi_select",
                        "label": "Aggravating Factors",
                        "required": False,
                        "options": ["Standing", "Coughing", "Straining", "Lifting", "Exercise", "None"],
                        "output_phrase": "Aggravated by: {value}"
                    },
                    {
                        "id": "femoral_reducible",
                        "type": "single_select",
                        "label": "Reducible?",
                        "required": True,
                        "options": ["Yes - reducible", "No - not reducible - RED FLAG", "Yes - disappears when lying down", "Variable"],
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Irreducible femoral hernia - high risk of incarceration/strangulation.",
                        "red_flag_negative": "",
                        "output_phrase": "Reducible: {value}"
                    },
                    {
                        "id": "femoral_previous_irreducibility",
                        "type": "toggle",
                        "label": "Previous Episodes of Irreducibility?",
                        "required": False,
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Previous irreducibility - higher risk of complications.",
                        "red_flag_negative": "",
                        "output_phrase": "Previous irreducibility: {value}"
                    },
                    {
                        "id": "femoral_sudden_increase",
                        "type": "toggle",
                        "label": "Sudden Increase in Size?",
                        "required": False,
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Sudden increase in size - consider incarceration/strangulation.",
                        "red_flag_negative": "",
                        "output_phrase": "Sudden increase: {value}"
                    },
                    {
                        "id": "femoral_nausea",
                        "type": "toggle",
                        "label": "Nausea / Vomiting?",
                        "required": False,
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Nausea/vomiting - urgent surgical/ED assessment.",
                        "red_flag_negative": "",
                        "output_phrase": "Nausea/vomiting: {value}"
                    },
                    {
                        "id": "femoral_abdominal_pain",
                        "type": "toggle",
                        "label": "Abdominal Pain / Distension?",
                        "required": False,
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Abdominal pain/distension - consider obstruction.",
                        "red_flag_negative": "",
                        "output_phrase": "Abdominal pain: {value}"
                    },
                    {
                        "id": "femoral_constipation",
                        "type": "multi_select",
                        "label": "Bowel Symptoms",
                        "required": False,
                        "options": ["Constipation", "Obstipation (no passage of stool/flatus) - RED FLAG", "Change in bowel habit", "Normal"],
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Obstipation - urgent surgical assessment for obstruction.",
                        "red_flag_negative": "",
                        "output_phrase": "Bowel symptoms: {value}"
                    },
                    {
                        "id": "femoral_previous_surgery",
                        "type": "textarea",
                        "label": "Previous Hernia / Abdominal / Pelvic Surgery",
                        "required": False,
                        "placeholder": "e.g., Previous hernia repair, C-section, hysterectomy",
                        "output_phrase": "Previous surgery: {value}"
                    }
                ]
            },
            {
                "title": "Risk Factors",
                "section_type": "history",
                "questions": [
                    {
                        "id": "femoral_pregnancy",
                        "type": "single_select",
                        "label": "Pregnancy History (if female)",
                        "required": False,
                        "options": ["Not applicable", "Never pregnant", "Previous pregnancy", "Multiparous (≥3 pregnancies)", "Current pregnancy"],
                        "output_phrase": "Pregnancy: {value}"
                    },
                    {
                        "id": "femoral_bmi",
                        "type": "number",
                        "label": "BMI",
                        "required": False,
                        "placeholder": "e.g., 30",
                        "output_phrase": "BMI: {value}"
                    },
                    {
                        "id": "femoral_chronic_cough",
                        "type": "toggle",
                        "label": "Chronic Cough?",
                        "required": False,
                        "output_phrase": "Chronic cough: {value}"
                    },
                    {
                        "id": "femoral_constipation_risk",
                        "type": "toggle",
                        "label": "Chronic Constipation / Straining?",
                        "required": False,
                        "output_phrase": "Constipation: {value}"
                    },
                    {
                        "id": "femoral_heavy_lifting",
                        "type": "toggle",
                        "label": "Heavy Lifting / Occupation?",
                        "required": False,
                        "output_phrase": "Heavy lifting: {value}"
                    },
                    {
                        "id": "femoral_smoking",
                        "type": "single_select",
                        "label": "Smoking Status",
                        "required": False,
                        "options": ["Non-smoker", "Ex-smoker", "Current smoker"],
                        "output_phrase": "Smoking: {value}"
                    }
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {
                        "id": "femoral_abdomen_soft",
                        "type": "single_select",
                        "label": "Abdomen",
                        "required": True,
                        "options": ["Soft, non-tender", "Tender - RED FLAG", "Distended - RED FLAG", "Rigid/guarding - RED FLAG"],
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Tender/distended/rigid abdomen - urgent surgical/ED assessment.",
                        "red_flag_negative": "",
                        "output_phrase": "Abdomen: {value}"
                    },
                    {
                        "id": "femoral_scars",
                        "type": "text",
                        "label": "Previous Surgical Scars",
                        "required": False,
                        "placeholder": "e.g., PFANZ scar, midline laparotomy",
                        "output_phrase": "Scars: {value}"
                    },
                    {
                        "id": "femoral_groin_inspection",
                        "type": "textarea",
                        "label": "Groin Examination - Inspection (standing and supine)",
                        "required": True,
                        "placeholder": "e.g., Visible lump R groin below pubic tubercle, reduces on lying down",
                        "output_phrase": "Groin inspection: {value}"
                    },
                    {
                        "id": "femoral_location_pubic_tubercle",
                        "type": "single_select",
                        "label": "Location Relative to Pubic Tubercle",
                        "required": True,
                        "options": [
                            "Below and lateral - typical femoral hernia",
                            "Above and medial - likely inguinal",
                            "Uncertain - consider imaging/surgical assessment"
                        ],
                        "output_phrase": "Location (pubic tubercle): {value}"
                    },
                    {
                        "id": "femoral_cough_impulse",
                        "type": "single_select",
                        "label": "Cough Impulse",
                        "required": True,
                        "options": ["Present", "Absent", "Not assessed"],
                        "output_phrase": "Cough impulse: {value}"
                    },
                    {
                        "id": "femoral_size",
                        "type": "text",
                        "label": "Size",
                        "required": False,
                        "placeholder": "e.g., 3 cm",
                        "output_phrase": "Size: {value}"
                    },
                    {
                        "id": "femoral_tenderness_exam",
                        "type": "single_select",
                        "label": "Tenderness on Palpation",
                        "required": True,
                        "options": ["Non-tender", "Tender - RED FLAG", "Very tender - RED FLAG"],
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Tender femoral hernia - high risk of incarceration/strangulation.",
                        "red_flag_negative": "",
                        "output_phrase": "Tenderness: {value}"
                    },
                    {
                        "id": "femoral_consistency",
                        "type": "single_select",
                        "label": "Consistency",
                        "required": True,
                        "options": ["Soft", "Firm - RED FLAG", "Hard - RED FLAG", "Uncertain"],
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Firm/hard femoral hernia - consider incarceration/strangulation.",
                        "red_flag_negative": "",
                        "output_phrase": "Consistency: {value}"
                    },
                    {
                        "id": "femoral_reducible_exam",
                        "type": "single_select",
                        "label": "Reducible on Examination",
                        "required": True,
                        "options": ["Yes", "No - RED FLAG", "Partially"],
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Irreducible femoral hernia - urgent surgical/ED assessment.",
                        "red_flag_negative": "",
                        "output_phrase": "Reducible (exam): {value}"
                    },
                    {
                        "id": "femoral_skin",
                        "type": "single_select",
                        "label": "Overlying Skin",
                        "required": True,
                        "options": ["Normal", "Erythematous - RED FLAG", "Discoloured - RED FLAG", "Tense/shiny - RED FLAG"],
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Erythematous/discoloured/shiny skin - consider strangulation.",
                        "red_flag_negative": "",
                        "output_phrase": "Skin: {value}"
                    },
                    {
                        "id": "femoral_other_hernias",
                        "type": "single_select",
                        "label": "Other Inguinal/Femoral Hernias",
                        "required": False,
                        "options": ["None detected", "Inguinal hernia present", "Contralateral femoral hernia", "Other"],
                        "output_phrase": "Other hernias: {value}"
                    },
                    {
                        "id": "femoral_testes",
                        "type": "textarea",
                        "label": "Testes/Scrotum Examination (if male)",
                        "required": False,
                        "placeholder": "e.g., Normal, no masses",
                        "output_phrase": "Testes: {value}"
                    },
                    {
                        "id": "femoral_lymph_nodes",
                        "type": "single_select",
                        "label": "Lymph Nodes",
                        "required": False,
                        "options": ["Not palpable", "Palpable - non-tender", "Palpable - tender - consider infection/inflammation", "Not assessed"],
                        "output_phrase": "Lymph nodes: {value}"
                    }
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "Femoral hernia (high risk of incarceration/strangulation) - RED FLAG",
                    "Inguinal hernia (more common, lower risk)",
                    "Hydrocele (if male)",
                    "Inguinal lymphadenopathy",
                    "Lipoma",
                    "Femoral artery aneurysm (rare)",
                    "Saphena varix (venous swelling)",
                    "Abscess (tender, erythematous)",
                    "Hematoma",
                    "Metastasis (rare)"
                ],
                "questions": [
                    {
                        "id": "femoral_diagnosis",
                        "type": "single_select",
                        "label": "Clinical Diagnosis",
                        "required": True,
                        "options": [
                            "Femoral hernia - suspect confirmed - refer routinely",
                            "Femoral hernia - incarcerated - URGENT ED",
                            "Femoral hernia - strangulated - URGENT ED",
                            "Inguinal hernia - more likely",
                            "Lymphadenopathy - investigate",
                            "Uncertain - consider imaging/surgical assessment"
                        ],
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Femoral hernia - HIGH RISK of incarceration/strangulation. Low threshold for referral.",
                        "red_flag_negative": "",
                        "output_phrase": "Diagnosis: {value}"
                    },
                    {
                        "id": "femoral_risk_level",
                        "type": "single_select",
                        "label": "Risk Level",
                        "required": True,
                        "options": [
                            "High risk - femoral hernia regardless of symptoms",
                            "Moderate risk - symptomatic but reducible",
                            "Urgent - incarcerated/strangulated",
                            "Low - likely other diagnosis"
                        ],
                        "output_phrase": "Risk level: {value}"
                    }
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "URGENT ED/SURGICAL ASSESSMENT if: Lump becomes painful, firm/tender, irreducible, rapidly enlarging. Also if: severe pain, vomiting, abdominal distension, failure to pass stool/flatus, systemic illness, or erythematous/discoloured skin. FEMORAL HERNIA - EVEN IF MINIMALLY SYMPTOMATIC - refer routinely to General Surgery due to high risk of complications.",
                "questions": [
                    {
                        "id": "femoral_management_type",
                        "type": "single_select",
                        "label": "Management Plan",
                        "required": True,
                        "options": [
                            "Routine surgical referral (even if minimally symptomatic) - femoral hernia",
                            "Same-day ED/Surgical assessment - URGENT (incarcerated/strangulated)",
                            "Refer for imaging (USS) - if diagnosis uncertain",
                            "Alternative diagnosis - manage accordingly"
                        ],
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Same-day ED/surgical assessment required - femoral hernia complications.",
                        "red_flag_negative": "",
                        "output_phrase": "Management: {value}"
                    },
                    {
                        "id": "femoral_surgical_referral",
                        "type": "single_select",
                        "label": "Surgical Referral Plan",
                        "required": True,
                        "options": [
                            "General Surgery (routine) - femoral hernia",
                            "General Surgery (urgent)",
                            "Same-day ED/Surgical assessment",
                            "Already referred"
                        ],
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Urgent/same-day surgical referral required.",
                        "red_flag_negative": "",
                        "output_phrase": "Surgical referral: {value}"
                    },
                    {
                        "id": "femoral_imaging",
                        "type": "single_select",
                        "label": "Imaging Plan",
                        "required": False,
                        "options": [
                            "No imaging needed - proceed with surgical referral",
                            "USS (if diagnosis uncertain)",
                            "CT scan (if clinically indicated)",
                            "Already done"
                        ],
                        "output_phrase": "Imaging: {value}"
                    },
                    {
                        "id": "femoral_advice_given",
                        "type": "multi_select",
                        "label": "Advice Given to Patient",
                        "required": False,
                        "options": [
                            "Femoral hernia - higher risk of complications - explain urgency",
                            "Seek urgent assessment if becomes painful/firm/irreducible",
                            "Lifestyle advice (weight, constipation, cough)",
                            "Avoid heavy lifting",
                            "All above"
                        ],
                        "output_phrase": "Advice: {value}"
                    },
                    {
                        "id": "femoral_followup",
                        "type": "single_select",
                        "label": "Follow-up Plan",
                        "required": True,
                        "options": [
                            "No follow-up needed - surgical referral arranged",
                            "Review in 2 weeks",
                            "Review after surgical assessment",
                            "As needed",
                            "Specialist follow-up arranged"
                        ],
                        "output_phrase": "Follow-up: {value}"
                    },
                    {
                        "id": "femoral_notes",
                        "type": "textarea",
                        "label": "Additional Notes",
                        "required": False,
                        "placeholder": "e.g., Patient education, shared decision-making, work advice",
                        "output_phrase": "Notes: {value}"
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
    seed_femoral_hernia()
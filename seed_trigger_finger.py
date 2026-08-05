from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone


def seed_trigger_finger():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin:
        print("Admin not found.")
        db.close()
        return

    category = db.query(Category).filter(Category.name == "Musculoskeletal").first()
    if not category:
        category = Category(name="Musculoskeletal")
        db.add(category)
        db.commit()

    t = {
        "title": "Trigger Finger (Stenosing Tenosynovitis)",
        "description": "GP consultation template for trigger finger covering presentation, grading, risk factors, conservative management, injection, and surgical referral criteria.",
        "category": "Musculoskeletal",
        "content": {
            "sections": [
                {
                    "title": "Presenting Complaint",
                    "section_type": "history",
                    "questions": [
                        {
                            "id": "tf_affected_digit",
                            "type": "multi_select",
                            "label": "Affected Digit(s)",
                            "required": True,
                            "options": [
                                "Thumb",
                                "Index",
                                "Middle",
                                "Ring",
                                "Little"
                            ],
                            "output_phrase": "Affected digit(s): {value}"
                        },
                        {
                            "id": "tf_dominant_hand",
                            "type": "single_select",
                            "label": "Dominant Hand Affected?",
                            "required": True,
                            "options": [
                                "Yes - dominant hand",
                                "No - non-dominant hand",
                                "Both hands affected"
                            ],
                            "output_phrase": "Dominant hand: {value}"
                        },
                        {
                            "id": "tf_duration",
                            "type": "text",
                            "label": "Duration of Symptoms",
                            "required": True,
                            "placeholder": "e.g., 3 months",
                            "output_phrase": "Duration: {value}"
                        },
                        {
                            "id": "tf_occupation",
                            "type": "text",
                            "label": "Occupation / Hobbies (repetitive gripping?)",
                            "required": False,
                            "placeholder": "e.g., Manual worker, gardening, knitting",
                            "output_phrase": "Occupation/hobbies: {value}"
                        }
                    ]
                },
                {
                    "title": "History",
                    "section_type": "history",
                    "questions": [
                        {
                            "id": "tf_catching_locking",
                            "type": "single_select",
                            "label": "Catching / Locking",
                            "required": True,
                            "options": [
                                "No catching or locking",
                                "Catching - actively correctable",
                                "Locking - needs passive extension to release",
                                "Fixed flexion deformity"
                            ],
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Locking or fixed deformity suggests advanced disease (Grade III-IV). May need surgical referral if not responding to injection.",
                            "red_flag_negative": "",
                            "output_phrase": "Catching/locking: {value}"
                        },
                        {
                            "id": "tf_pain",
                            "type": "single_select",
                            "label": "Pain",
                            "required": True,
                            "options": [
                                "No pain",
                                "Mild - localised to palmar MCP",
                                "Moderate - radiates into digit",
                                "Severe - interferes with daily activities"
                            ],
                            "output_phrase": "Pain: {value}"
                        },
                        {
                            "id": "tf_stiffness",
                            "type": "single_select",
                            "label": "Stiffness Pattern",
                            "required": True,
                            "options": [
                                "Worse in morning, improves through day",
                                "Constant stiffness",
                                "No significant stiffness"
                            ],
                            "output_phrase": "Stiffness: {value}"
                        },
                        {
                            "id": "tf_nodule",
                            "type": "toggle",
                            "label": "Palpable Nodule at A1 Pulley?",
                            "required": True,
                            "output_phrase": "Palpable nodule: {value}"
                        },
                        {
                            "id": "tf_progression",
                            "type": "single_select",
                            "label": "Progression",
                            "required": True,
                            "options": [
                                "Intermittent symptoms",
                                "Gradually worsening",
                                "Stable",
                                "Rapidly worsening"
                            ],
                            "output_phrase": "Progression: {value}"
                        }
                    ]
                },
                {
                    "title": "Risk Factors & Associated Conditions",
                    "section_type": "history",
                    "questions": [
                        {
                            "id": "tf_diabetes",
                            "type": "single_select",
                            "label": "Diabetes Mellitus",
                            "required": True,
                            "options": [
                                "No diabetes",
                                "Type 1",
                                "Type 2",
                                "Not known - consider HbA1c"
                            ],
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Diabetes is strongly associated with trigger finger - often more severe, multiple digits, and higher injection failure rate. Check HbA1c if not done recently. Warn of transient hyperglycaemia post-injection.",
                            "red_flag_negative": "",
                            "output_phrase": "Diabetes: {value}"
                        },
                        {
                            "id": "tf_ra",
                            "type": "toggle",
                            "label": "Rheumatoid Arthritis?",
                            "required": False,
                            "output_phrase": "Rheumatoid arthritis: {value}"
                        },
                        {
                            "id": "tf_hypothyroidism",
                            "type": "toggle",
                            "label": "Hypothyroidism?",
                            "required": False,
                            "output_phrase": "Hypothyroidism: {value}"
                        },
                        {
                            "id": "tf_gout",
                            "type": "toggle",
                            "label": "Gout?",
                            "required": False,
                            "output_phrase": "Gout: {value}"
                        },
                        {
                            "id": "tf_carpal_tunnel",
                            "type": "toggle",
                            "label": "Carpal Tunnel Syndrome? (may coexist)",
                            "required": False,
                            "output_phrase": "Carpal tunnel: {value}"
                        },
                        {
                            "id": "tf_repetitive_activity",
                            "type": "toggle",
                            "label": "Repetitive Manual Activity / Occupational Strain?",
                            "required": False,
                            "output_phrase": "Repetitive activity: {value}"
                        }
                    ]
                },
                {
                    "title": "Examination",
                    "section_type": "examination",
                    "questions": [
                        {
                            "id": "tf_a1_pulley",
                            "type": "single_select",
                            "label": "A1 Pulley Palpation (distal palmar crease)",
                            "required": True,
                            "options": [
                                "Tender nodule palpable",
                                "Tender - no discrete nodule",
                                "Non-tender",
                                "Not examined"
                            ],
                            "output_phrase": "A1 pulley: {value}"
                        },
                        {
                            "id": "tf_trigger_test",
                            "type": "single_select",
                            "label": "Active Flexion/Extension - Triggering Observed?",
                            "required": True,
                            "options": [
                                "No triggering reproduced",
                                "Catching reproduced",
                                "Locking reproduced",
                                "Fixed flexion deformity"
                            ],
                            "output_phrase": "Trigger test: {value}"
                        },
                        {
                            "id": "tf_green_grade",
                            "type": "single_select",
                            "label": "Green's Classification",
                            "required": True,
                            "options": [
                                "Grade I: Pain/tenderness at A1 pulley, no triggering",
                                "Grade II: Catching, actively correctable",
                                "Grade IIIa: Locking, passively correctable",
                                "Grade IIIb: Locking, unable to actively flex",
                                "Grade IV: Fixed flexion contracture"
                            ],
                            "output_phrase": "Green's grade: {value}"
                        },
                        {
                            "id": "tf_other_digits",
                            "type": "toggle",
                            "label": "Other Digits Affected? (common in diabetics)",
                            "required": False,
                            "output_phrase": "Other digits: {value}"
                        },
                        {
                            "id": "tf_carpal_tunnel_signs",
                            "type": "single_select",
                            "label": "Carpal Tunnel Screening (Tinel's / Phalen's)",
                            "required": False,
                            "options": [
                                "Negative",
                                "Positive - Tinel's",
                                "Positive - Phalen's",
                                "Both positive",
                                "Not tested"
                            ],
                            "output_phrase": "Carpal tunnel signs: {value}"
                        }
                    ]
                },
                {
                    "title": "Investigations",
                    "section_type": "history",
                    "questions": [
                        {
                            "id": "tf_hba1c",
                            "type": "toggle",
                            "label": "HbA1c / Fasting Glucose Checked? (if ?diabetes, multiple digits, atypical age)",
                            "required": False,
                            "output_phrase": "HbA1c/glucose checked: {value}"
                        },
                        {
                            "id": "tf_imaging",
                            "type": "single_select",
                            "label": "Imaging Required?",
                            "required": False,
                            "options": [
                                "None - clinical diagnosis",
                                "Ultrasound arranged (diagnostic uncertainty)",
                                "Ultrasound arranged (pre-injection guidance)",
                                "X-ray arranged (rule out other pathology)"
                            ],
                            "output_phrase": "Imaging: {value}"
                        }
                    ]
                },
                {
                    "title": "Assessment",
                    "section_type": "assessment",
                    "differentials": [
                        "Trigger Finger (Stenosing Tenosynovitis)",
                        "Dupuytren's Contracture",
                        "De Quervain's Tenosynovitis",
                        "Osteoarthritis (MCP/IP joints)",
                        "Ganglion Cyst",
                        "Foreign Body Granuloma",
                        "Flexor Tendon Sheath Infection (rare)"
                    ],
                    "questions": [
                        {
                            "id": "tf_diagnosis",
                            "type": "single_select",
                            "label": "Diagnosis",
                            "required": True,
                            "options": [
                                "Trigger Finger (Stenosing Tenosynovitis)",
                                "Trigger Finger + Diabetes",
                                "Trigger Finger + Carpal Tunnel Syndrome",
                                "Dupuytren's Contracture",
                                "Other"
                            ],
                            "output_phrase": "Diagnosis: {value}"
                        }
                    ]
                },
                {
                    "title": "Management Plan",
                    "section_type": "plan",
                    "safety_netting": "Return if: worsening locking, new fixed deformity, or signs of infection post-injection (increasing redness, swelling, warmth, fever within 48-72 hours). Set realistic expectations: symptoms may take 2-4 weeks to settle post-injection. Splinting should be trialled for at least 6 weeks. Conservative measures are first-line for Grade I-II. Corticosteroid injection is effective in 50-70% with a single injection; can repeat once if partial response. Higher failure rate in diabetics — counsel accordingly. If diabetic: warn of transient blood glucose elevation for 3-7 days post-injection. Refer to hand surgery/orthopaedics if persistent/recurrent despite injection, Grade III-IV, or fixed deformity. A1 pulley release has ~90%+ success rate as a day case under local anaesthetic.",
                    "questions": [
                        {
                            "id": "tf_management_step",
                            "type": "single_select",
                            "label": "Management Plan",
                            "required": True,
                            "options": [
                                "Conservative: activity modification + splinting + NSAIDs",
                                "Corticosteroid injection (first-line for Grade I-III)",
                                "Repeat corticosteroid injection (partial response to first)",
                                "Refer hand surgery/orthopaedics (Grade III-IV, recurrent, or fixed deformity)",
                                "Combined: conservative + injection"
                            ],
                            "output_phrase": "Management: {value}"
                        },
                        {
                            "id": "tf_splinting",
                            "type": "toggle",
                            "label": "Splinting Advised? (MCP extension at night, 6-week trial)",
                            "required": False,
                            "output_phrase": "Splinting advised: {value}"
                        },
                        {
                            "id": "tf_nsaids",
                            "type": "toggle",
                            "label": "NSAIDs Prescribed/Advised?",
                            "required": False,
                            "output_phrase": "NSAIDs: {value}"
                        },
                        {
                            "id": "tf_injection_given",
                            "type": "toggle",
                            "label": "Corticosteroid Injection Given Today?",
                            "required": False,
                            "output_phrase": "Injection given: {value}"
                        },
                        {
                            "id": "tf_injection_details",
                            "type": "text",
                            "label": "Injection Details (if given)",
                            "required": False,
                            "placeholder": "e.g., 20mg Triamcinolone + 1ml 1% Lidocaine into flexor tendon sheath at A1 pulley, ring finger",
                            "output_phrase": "Injection details: {value}"
                        },
                        {
                            "id": "tf_diabetes_warning",
                            "type": "toggle",
                            "label": "Diabetic: Warned About Transient Hyperglycaemia Post-Injection?",
                            "required": False,
                            "output_phrase": "Diabetes warning given: {value}"
                        },
                        {
                            "id": "tf_surgical_referral",
                            "type": "single_select",
                            "label": "Surgical Referral",
                            "required": False,
                            "options": [
                                "Not required",
                                "Referred - hand surgery",
                                "Referred - orthopaedics",
                                "Patient declined referral",
                                "Advise referral if no response to injection in 6-8 weeks"
                            ],
                            "output_phrase": "Surgical referral: {value}"
                        },
                        {
                            "id": "tf_followup",
                            "type": "text",
                            "label": "Follow-up Plan",
                            "required": True,
                            "placeholder": "e.g., Review in 6 weeks post-injection. Earlier if locking worsens or fixed deformity develops.",
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
    seed_trigger_finger()
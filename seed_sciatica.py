from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_sciatica():
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
        "title": "Sciatica Assessment & Management",
        "description": "Practical GP assessment and management of sciatica including red flag screening, examination, analgesia, and escalation pathways.",
        "category": "Musculoskeletal",
        "content": {"sections": [
            {
                "title": "History",
                "section_type": "history",
                "questions": [
                    {
                        "id": "sciatica_presenting_complaint",
                        "type": "text",
                        "label": "Presenting Complaint",
                        "required": True,
                        "placeholder": "e.g., Shooting pain down left leg for 2 weeks",
                        "output_phrase": "c/o: {value}"
                    },
                    {
                        "id": "sciatica_duration",
                        "type": "text",
                        "label": "Duration of Symptoms",
                        "required": True,
                        "placeholder": "e.g., 2 weeks",
                        "output_phrase": "Duration: {value}"
                    },
                    {
                        "id": "sciatica_onset",
                        "type": "single_select",
                        "label": "Onset",
                        "required": True,
                        "options": ["Sudden", "Gradual", "Following injury", "No clear trigger"],
                        "output_phrase": "Onset: {value}"
                    },
                    {
                        "id": "sciatica_pain_character",
                        "type": "multi_select",
                        "label": "Pain Character",
                        "required": True,
                        "options": ["Shooting", "Burning", "Electric", "Dull ache", "Sharp/stabbing", "Numbness", "Tingling/paraesthesia"],
                        "output_phrase": "Pain: {value}"
                    },
                    {
                        "id": "sciatica_pain_location",
                        "type": "single_select",
                        "label": "Pain Distribution",
                        "required": True,
                        "options": ["Unilateral leg (below knee)", "Unilateral leg (above knee)", "Bilateral - RED FLAG", "Buttock only", "Full leg"],
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Bilateral sciatica - urgent assessment for cauda equina/central disc.",
                        "red_flag_negative": "",
                        "output_phrase": "Distribution: {value}"
                    },
                    {
                        "id": "sciatica_dermatome",
                        "type": "single_select",
                        "label": "Likely Dermatome (based on symptoms)",
                        "required": False,
                        "options": ["L3/L4 (knee/quadriceps)", "L4/L5 (L5 distribution)", "L5/S1 (S1 distribution)", "Uncertain", "Multiple levels"],
                        "output_phrase": "Dermatome: {value}"
                    },
                    {
                        "id": "sciatica_aggravating",
                        "type": "multi_select",
                        "label": "Aggravating Factors",
                        "required": True,
                        "options": ["Coughing/sneezing", "Valsalva/straining", "Bending forward", "Sitting", "Standing", "Walking", "None"],
                        "output_phrase": "Aggravated by: {value}"
                    },
                    {
                        "id": "sciatica_red_flags",
                        "type": "multi_select",
                        "label": "Red Flag Screen",
                        "required": True,
                        "options": [
                            "Urinary retention - RED FLAG",
                            "Urinary incontinence - RED FLAG",
                            "Faecal incontinence - RED FLAG",
                            "Saddle/perineal numbness - RED FLAG",
                            "Bilateral sciatica - RED FLAG",
                            "Severe/progressive bilateral weakness - RED FLAG",
                            "Rapidly progressive motor deficit - RED FLAG",
                            "None"
                        ],
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: {value} - URGENT SAME-DAY ED/ASSESSMENT for possible cauda equina syndrome.",
                        "red_flag_negative": "",
                        "output_phrase": "Red flags: {value}"
                    },
                    {
                        "id": "sciatica_weakness",
                        "type": "multi_select",
                        "label": "Subjective Weakness",
                        "required": False,
                        "options": ["Foot drop", "Difficulty heel walking", "Difficulty toe walking", "Leg giving way", "No weakness", "None"],
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Foot drop/progressive weakness - urgent assessment.",
                        "red_flag_negative": "",
                        "output_phrase": "Weakness: {value}"
                    },
                    {
                        "id": "sciatica_sensory",
                        "type": "multi_select",
                        "label": "Sensory Symptoms",
                        "required": False,
                        "options": ["Numbness", "Tingling", "Paraesthesia", "Saddle/perineal - RED FLAG", "No sensory symptoms"],
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Saddle/perineal numbness - urgent cauda equina assessment.",
                        "red_flag_negative": "",
                        "output_phrase": "Sensory: {value}"
                    },
                    {
                        "id": "sciatica_previous_treatments",
                        "type": "textarea",
                        "label": "Previous Treatments/Investigations",
                        "required": False,
                        "placeholder": "e.g., Physiotherapy, analgesia, previous MRI",
                        "output_phrase": "Previous tx: {value}"
                    },
                    {
                        "id": "sciatica_serious_pathology",
                        "type": "multi_select",
                        "label": "Screen for Serious Pathology",
                        "required": False,
                        "options": ["Malignancy suspicion (weight loss, night pain)", "Infection (fever, IVDU)", "Fracture (trauma, osteoporosis)", "Inflammatory spinal disease", "None suspected"],
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Suspicion of {value} - urgent imaging/specialist referral.",
                        "red_flag_negative": "",
                        "output_phrase": "Serious pathology screen: {value}"
                    },
                    {
                        "id": "sciatica_medical_history",
                        "type": "textarea",
                        "label": "Relevant Medical History",
                        "required": False,
                        "placeholder": "e.g., Osteoporosis, malignancy, steroid use",
                        "output_phrase": "PMH: {value}"
                    },
                    {
                        "id": "sciatica_medications",
                        "type": "textarea",
                        "label": "Current Medications",
                        "required": False,
                        "placeholder": "e.g., Warfarin, NSAIDs, steroids",
                        "output_phrase": "Medications: {value}"
                    }
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {
                        "id": "sciatica_gait",
                        "type": "single_select",
                        "label": "Gait Assessment",
                        "required": True,
                        "options": ["Normal", "Heel walking impaired - L5", "Toe walking impaired - S1", "Antalgic gait", "Foot drop present"],
                        "output_phrase": "Gait: {value}"
                    },
                    {
                        "id": "sciatica_power",
                        "type": "textarea",
                        "label": "Power Assessment (hip, knee, ankle DF/PF, EHL)",
                        "required": True,
                        "placeholder": "e.g., Hip flexion 5/5, Knee 5/5, Ankle dorsiflexion 4/5, Plantarflexion 5/5, EHL 5/5",
                        "output_phrase": "Power: {value}"
                    },
                    {
                        "id": "sciatica_sensation",
                        "type": "textarea",
                        "label": "Sensation by Dermatome (L1-S2)",
                        "required": True,
                        "placeholder": "e.g., Normal L1-L4, reduced L5 distribution, normal S1",
                        "output_phrase": "Sensation: {value}"
                    },
                    {
                        "id": "sciatica_reflexes",
                        "type": "textarea",
                        "label": "Reflexes (Knee L3/4, Ankle S1)",
                        "required": True,
                        "placeholder": "e.g., Knee jerk ++, Ankle jerk + (reduced)",
                        "output_phrase": "Reflexes: {value}"
                    },
                    {
                        "id": "sciatica_slr",
                        "type": "single_select",
                        "label": "Straight Leg Raise (SLR)",
                        "required": True,
                        "options": ["Negative - no radicular pain <70°", "Positive - radicular pain at <70°", "Positive crossed SLR - suggests disc prolapse", "Unable to assess"],
                        "output_phrase": "SLR: {value}"
                    },
                    {
                        "id": "sciatica_hips",
                        "type": "single_select",
                        "label": "Hip Examination",
                        "required": False,
                        "options": ["Normal", "Reduced ROM - consider hip pathology", "Tender - consider trochanteric bursitis", "Not assessed"],
                        "output_phrase": "Hips: {value}"
                    },
                    {
                        "id": "sciatica_pulses",
                        "type": "single_select",
                        "label": "Peripheral Pulses (to exclude vascular claudication)",
                        "required": False,
                        "options": ["Palpable femoral, popliteal, pedal", "Reduced pedal pulses - consider PVD", "Absent - vascular referral", "Not assessed"],
                        "output_phrase": "Pulses: {value}"
                    },
                    {
                        "id": "sciatica_lumbar_spine",
                        "type": "textarea",
                        "label": "Lumbar Spine Examination",
                        "required": False,
                        "placeholder": "e.g., Full ROM, no focal tenderness",
                        "output_phrase": "Lumbar spine: {value}"
                    }
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "Lumbar radiculopathy / sciatica (most common)",
                    "L4/L5 or L5/S1 disc prolapse",
                    "Spinal stenosis (bilateral, neurogenic claudication)",
                    "Piriformis syndrome (buttock pain)",
                    "Sacroiliac joint dysfunction",
                    "Hip OA (hip pain, groin, reduced ROM)",
                    "Trochanteric bursitis",
                    "Peripheral neuropathy (diabetic)",
                    "Vascular claudication (pulses, walking distance)",
                    "Serious pathology: malignancy, infection, fracture, inflammatory"
                ],
                "questions": [
                    {
                        "id": "sciatica_diagnosis",
                        "type": "single_select",
                        "label": "Clinical Diagnosis",
                        "required": True,
                        "options": [
                            "Sciatica - likely L5/S1 radiculopathy",
                            "Sciatica - likely L4/L5 radiculopathy",
                            "Spinal stenosis suspected",
                            "Piriformis syndrome",
                            "Hip pathology suspected",
                            "Vascular claudication",
                            "Red flags - urgent assessment required",
                            "Uncertain - consider imaging/referral"
                        ],
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: {value} - urgent same-day ED/assessment required for cauda equina/neurological compromise.",
                        "red_flag_negative": "",
                        "output_phrase": "Diagnosis: {value}"
                    },
                    {
                        "id": "sciatica_severity",
                        "type": "single_select",
                        "label": "Severity/Functional Impact",
                        "required": True,
                        "options": ["Mild - minimal functional limitation", "Moderate - significant impact on daily activities", "Severe - disabling pain, unable to work/care", "Neurological deficit present"],
                        "output_phrase": "Severity: {value}"
                    },
                    {
                        "id": "sciatica_nerve_root",
                        "type": "single_select",
                        "label": "Likely Nerve Root Involvement",
                        "required": False,
                        "options": ["L4 (L3/4)", "L5 (L4/5)", "S1 (L5/S1)", "Multiple levels", "Uncertain"],
                        "output_phrase": "Nerve root: {value}"
                    }
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "RETURN/URGENT if: New urinary retention/incontinence, faecal incontinence, saddle/perineal numbness, bilateral sciatica, severe/progressive weakness, or rapidly progressive motor deficit. If symptoms worsen significantly or you develop new red flags, attend ED immediately. Sciatica often improves spontaneously within 4-6 weeks. Avoid prolonged bed rest - stay as active as possible within pain limits. Gentle walking is preferable to inactivity.",
                "questions": [
                    {
                        "id": "sciatica_advice",
                        "type": "multi_select",
                        "label": "General Advice Given",
                        "required": True,
                        "options": [
                            "Reassurance - improves in 4-6 weeks",
                            "Avoid prolonged bed rest",
                            "Continue normal activity as tolerated",
                            "Gentle walking daily",
                            "Gradual exercise is preferable to inactivity",
                            "Manual handling/posture advice",
                            "All above"
                        ],
                        "output_phrase": "Advice: {value}"
                    },
                    {
                        "id": "sciatica_analgesia",
                        "type": "multi_select",
                        "label": "Analgesia Prescribed",
                        "required": False,
                        "options": [
                            "Ibuprofen 400mg TDS with food PRN",
                            "Naproxen 250-500mg BD with food",
                            "PPI gastroprotection (if NSAIDs)",
                            "Paracetamol 1g QDS",
                            "Codeine (short-term only)",
                            "None"
                        ],
                        "output_phrase": "Analgesia: {value}"
                    },
                    {
                        "id": "sciatica_avoid",
                        "type": "multi_select",
                        "label": "Medications Routinely Avoided",
                        "required": False,
                        "options": [
                            "Gabapentin/pregabalin - not recommended routine",
                            "Oral steroids - not recommended routine",
                            "Benzodiazepines - not recommended routine",
                            "Long-term opioids - not recommended routine",
                            "All noted"
                        ],
                        "output_phrase": "Avoided meds: {value}"
                    },
                    {
                        "id": "sciatica_physio",
                        "type": "single_select",
                        "label": "Physiotherapy Referral",
                        "required": True,
                        "options": ["No physio needed", "Community physio - graded activity/exercise", "MSK physiotherapy", "Already under physio", "Not yet - review in 2 weeks"],
                        "output_phrase": "Physiotherapy: {value}"
                    },
                    {
                        "id": "sciatica_mri",
                        "type": "single_select",
                        "label": "MRI Planning",
                        "required": True,
                        "options": [
                            "No MRI indicated - uncomplicated sciatica",
                            "MRI if no improvement at 6 weeks",
                            "MRI if progressive neurological deficit",
                            "MRI if persistent radiculopathy >6 weeks",
                            "MRI if severe persistent functional limitation",
                            "MRI if considering injection/surgery",
                            "MRI if suspicion of serious pathology",
                            "MRI already arranged"
                        ],
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: MRI indicated urgently - progressive deficit/serious pathology suspicion.",
                        "red_flag_negative": "",
                        "output_phrase": "MRI: {value}"
                    },
                    {
                        "id": "sciatica_referral",
                        "type": "multi_select",
                        "label": "Specialist Referral",
                        "required": False,
                        "options": [
                            "Spinal/MSK specialist - if severe pain persists",
                            "Spinal/MSK specialist - if significant functional impairment",
                            "Spinal/MSK specialist - if objective neurological deficit",
                            "Rheumatology - if inflammatory suspected",
                            "Neurology - if uncertain diagnosis",
                            "ED/urgent - CAUDA EQUINA RED FLAGS",
                            "None at this time"
                        ],
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Urgent ED/specialist referral - cauda equina/neurological compromise.",
                        "red_flag_negative": "",
                        "output_phrase": "Referral: {value}"
                    },
                    {
                        "id": "sciatica_escalation",
                        "type": "single_select",
                        "label": "Escalation Pathway (if indicated)",
                        "required": False,
                        "options": [
                            "No escalation needed",
                            "Specialist assessment - acute severe sciatica",
                            "Epidural injection - acute severe sciatica",
                            "Spinal decompression - persistent disabling sciatica",
                            "None"
                        ],
                        "output_phrase": "Escalation: {value}"
                    },
                    {
                        "id": "sciatica_followup",
                        "type": "single_select",
                        "label": "Follow-up Plan",
                        "required": True,
                        "options": [
                            "Review in 2 weeks",
                            "Review in 4-6 weeks",
                            "Review in 6 weeks (if no improvement → MRI)",
                            "As needed - stable",
                            "Specialist follow-up arranged"
                        ],
                        "output_phrase": "Follow-up: {value}"
                    },
                    {
                        "id": "sciatica_notes",
                        "type": "textarea",
                        "label": "Additional Notes",
                        "required": False,
                        "placeholder": "e.g., Fitness for work, driving advice",
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
    seed_sciatica()
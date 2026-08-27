from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_fungal_nail():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: 
        print("Admin not found.")
        db.close()
        return

    category = db.query(Category).filter(Category.name == "Dermatology").first()
    if not category: 
        category = Category(name="Dermatology")
        db.add(category)
        db.commit()

    t = {
        "title": "Fungal Nail Infection (Onychomycosis) Assessment & Management",
        "description": "Practical GP assessment and management of fungal nail infections, including diagnostic sampling, topical and systemic treatment options.",
        "category": "Dermatology",
        "content": {"sections": [
            {
                "title": "History",
                "section_type": "history",
                "questions": [
                    {
                        "id": "fungalnail_presenting_complaint",
                        "type": "text",
                        "label": "Presenting Complaint",
                        "required": True,
                        "placeholder": "e.g., Discoloured nails for 6 months",
                        "output_phrase": "c/o: {value}"
                    },
                    {
                        "id": "fungalnail_duration",
                        "type": "text",
                        "label": "Duration of Symptoms",
                        "required": True,
                        "placeholder": "e.g., 6 months",
                        "output_phrase": "Duration: {value}"
                    },
                    {
                        "id": "fungalnail_sites",
                        "type": "multi_select",
                        "label": "Affected Nails",
                        "required": True,
                        "options": ["Fingernails", "Toenails", "Both"],
                        "output_phrase": "Affected: {value}"
                    },
                    {
                        "id": "fungalnail_number",
                        "type": "text",
                        "label": "Number of Nails Affected",
                        "required": True,
                        "placeholder": "e.g., 3 on each foot",
                        "output_phrase": "Number: {value}"
                    },
                    {
                        "id": "fungalnail_appearance",
                        "type": "multi_select",
                        "label": "Nail Appearance",
                        "required": True,
                        "options": [
                            "Yellow-white discolouration",
                            "Yellow streaks in central portion",
                            "Thickening",
                            "Brittle/crumbly",
                            "Subungual hyperkeratosis",
                            "Onycholysis (separation from nail bed)",
                            "Other"
                        ],
                        "output_phrase": "Appearance: {value}"
                    },
                    {
                        "id": "fungalnail_previous_treatments",
                        "type": "textarea",
                        "label": "Previous Treatments",
                        "required": False,
                        "placeholder": "e.g., Topical lacquers, oral antifungals",
                        "output_phrase": "Previous tx: {value}"
                    },
                    {
                        "id": "fungalnail_risk_factors",
                        "type": "multi_select",
                        "label": "Risk Factors",
                        "required": False,
                        "options": [
                            "Diabetes",
                            "Peripheral vascular disease",
                            "Immunosuppression",
                            "Athlete's foot",
                            "Frequent swimming/gym",
                            "Tight footwear",
                            "Trauma to nails",
                            "Smoking",
                            "None"
                        ],
                        "output_phrase": "Risk factors: {value}"
                    },
                    {
                        "id": "fungalnail_medical_history",
                        "type": "textarea",
                        "label": "Relevant Medical History",
                        "required": False,
                        "placeholder": "e.g., Diabetes, liver disease, immunosuppression",
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Diabetes/peripheral vascular disease - requires careful monitoring, consider podiatry referral.",
                        "red_flag_negative": "",
                        "output_phrase": "PMH: {value}"
                    },
                    {
                        "id": "fungalnail_medications",
                        "type": "textarea",
                        "label": "Current Medications",
                        "required": False,
                        "placeholder": "e.g., Apixaban, warfarin (drug interactions with itraconazole)",
                        "output_phrase": "Medications: {value}"
                    },
                    {
                        "id": "fungalnail_liver",
                        "type": "toggle",
                        "label": "Known Liver Disease? (contraindication to terbinafine)",
                        "required": False,
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Liver disease - caution with systemic antifungals, consider topical only.",
                        "red_flag_negative": "",
                        "output_phrase": "Liver disease: {value}"
                    },
                    {
                        "id": "fungalnail_pregnancy",
                        "type": "toggle",
                        "label": "Pregnant / Breastfeeding?",
                        "required": False,
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Pregnancy/lactation - avoid systemic antifungals, consider topical only.",
                        "red_flag_negative": "",
                        "output_phrase": "Pregnant: {value}"
                    }
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {
                        "id": "fungalnail_description",
                        "type": "textarea",
                        "label": "Nail Examination Description",
                        "required": True,
                        "placeholder": "e.g., Yellow-white nails with yellow streaks centrally, thickened, no surrounding erythema",
                        "output_phrase": "Exam: {value}"
                    },
                    {
                        "id": "fungalnail_surrounding_skin",
                        "type": "single_select",
                        "label": "Surrounding Skin",
                        "required": False,
                        "options": ["Normal", "Erythema", "Scaling - ?athlete's foot", "Cracking", "None"],
                        "output_phrase": "Skin: {value}"
                    },
                    {
                        "id": "fungalnail_psoriasis",
                        "type": "single_select",
                        "label": "Psoriasis Screen (rash, hair margins, other sites)",
                        "required": True,
                        "options": ["No psoriatic rash present", "Psoriatic rash present - consider psoriatic nail disease", "Uncertain"],
                        "output_phrase": "Psoriasis screen: {value}"
                    },
                    {
                        "id": "fungalnail_pulses",
                        "type": "single_select",
                        "label": "Peripheral Pulses (toe/foot)",
                        "required": False,
                        "options": ["Palpable", "Reduced/absent - RED FLAG", "Not assessed"],
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Reduced/absent pulses - consider vascular assessment, podiatry referral.",
                        "red_flag_negative": "",
                        "output_phrase": "Pulses: {value}"
                    }
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "Fungal nail infection (onychomycosis) - most common",
                    "Psoriatic nail disease (pitting, onycholysis, no yellow streaks)",
                    "Onycholysis (thyroid, trauma, psoriasis)",
                    "Nail trauma (subungual haematoma)",
                    "Lichen planus",
                    "Yellow nail syndrome (rare)",
                    "Subungual melanoma (red flag - pigmented, unilateral, growing)"
                ],
                "questions": [
                    {
                        "id": "fungalnail_diagnosis",
                        "type": "single_select",
                        "label": "Clinical Diagnosis",
                        "required": True,
                        "options": [
                            "Fungal nail infection (onychomycosis) - likely",
                            "Psoriatic nail disease - consider",
                            "Nail trauma - possible",
                            "Uncertain - confirm with microscopy/culture",
                            "RED FLAG: Subungual melanoma suspected"
                        ],
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Subungual melanoma suspected - urgent dermatology referral.",
                        "red_flag_negative": "",
                        "output_phrase": "Diagnosis: {value}"
                    },
                    {
                        "id": "fungalnail_confirmed",
                        "type": "single_select",
                        "label": "Confirmation Status",
                        "required": True,
                        "options": [
                            "Awaiting microscopy/culture",
                            "Confirmed on microscopy",
                            "Clinically diagnosed - sampling sent",
                            "No sampling - trial of topical"
                        ],
                        "output_phrase": "Status: {value}"
                    }
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Return/urgent if: Signs of cellulitis (redness, swelling, pain), worsening of nail or surrounding skin, jaundice (if on terbinafine), or new/different symptoms. If on systemic antifungals, seek advice if any medication interactions or side effects. Pregnant or breastfeeding women should not use systemic antifungals.",
                "questions": [
                    {
                        "id": "fungalnail_sampling",
                        "type": "multi_select",
                        "label": "Diagnostic Sampling",
                        "required": False,
                        "options": [
                            "MSU bottle given with micro form",
                            "Nail clippings - wrap in tinfoil, place in bottle",
                            "Sample sent to lab",
                            "Awaiting results"
                        ],
                        "output_phrase": "Sampling: {value}"
                    },
                    {
                        "id": "fungalnail_topical",
                        "type": "single_select",
                        "label": "Topical Treatment (if indicated)",
                        "required": False,
                        "options": [
                            "Loceryl nail lacquer (amorolfine) - once/twice weekly x 3-6 months",
                            "Other topical antifungal",
                            "Not indicated - proceeding to oral",
                            "None"
                        ],
                        "output_phrase": "Topical tx: {value}"
                    },
                    {
                        "id": "fungalnail_oral",
                        "type": "single_select",
                        "label": "Oral Antifungal Treatment",
                        "required": False,
                        "options": [
                            "Terbinafine 250mg OD - 6 weeks (fingernails) / 12 weeks (toenails)",
                            "Itraconazole 200mg BD x 7 days, repeat in 3 weeks (2-3 courses)",
                            "Not indicated - topical only",
                            "None - await results"
                        ],
                        "output_phrase": "Oral tx: {value}"
                    },
                    {
                        "id": "fungalnail_lfts",
                        "type": "toggle",
                        "label": "LFTs Performed Before Starting Terbinafine? (as per SPC)",
                        "required": False,
                        "output_phrase": "LFTs: {value}"
                    },
                    {
                        "id": "fungalnail_lft_result",
                        "type": "textarea",
                        "label": "LFT Results (if performed)",
                        "required": False,
                        "placeholder": "e.g., ALT 25, AST 22, ALP 60",
                        "output_phrase": "LFT results: {value}"
                    },
                    {
                        "id": "fungalnail_counselling",
                        "type": "multi_select",
                        "label": "Patient Counselling Given",
                        "required": False,
                        "options": [
                            "Topical: Loceryl once/twice weekly x 3-6 months",
                            "Terbinafine: return if jaundice develops",
                            "Terbinafine: avoid alcohol (optional)",
                            "Itraconazole: caution with apixaban/warfarin interactions",
                            "Check fasting glucose/HbA1c if persistent/refractory",
                            "All above"
                        ],
                        "output_phrase": "Counselling: {value}"
                    },
                    {
                        "id": "fungalnail_other_investigations",
                        "type": "multi_select",
                        "label": "Other Investigations (if indicated)",
                        "required": False,
                        "options": [
                            "Fasting glucose/HbA1c (if persistent/refractory)",
                            "None at this time"
                        ],
                        "output_phrase": "Other investigations: {value}"
                    },
                    {
                        "id": "fungalnail_referral",
                        "type": "single_select",
                        "label": "Referral Plan",
                        "required": True,
                        "options": [
                            "No referral needed",
                            "Dermatology (if uncertain diagnosis/refractory)",
                            "Podiatry (if diabetes/vascular disease)",
                            "None"
                        ],
                        "output_phrase": "Referral: {value}"
                    },
                    {
                        "id": "fungalnail_followup",
                        "type": "single_select",
                        "label": "Follow-up Plan",
                        "required": True,
                        "options": [
                            "Review in 3 months (topical treatment)",
                            "Review in 6 months (oral treatment)",
                            "Review when microscopy results available",
                            "As needed",
                            "Specialist follow-up arranged"
                        ],
                        "output_phrase": "Follow-up: {value}"
                    },
                    {
                        "id": "fungalnail_notes",
                        "type": "textarea",
                        "label": "Additional Notes",
                        "required": False,
                        "placeholder": "e.g., Patient education, nail care, hygiene advice",
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
    seed_fungal_nail()
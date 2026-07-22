from app.database import SessionLocal
from app.models import User, Template, Category

def seed_pigmented_lesion():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Dermatology").first()
    if not category: category = Category(name="Dermatology"); db.add(category); db.commit()

    t = {
        "title": "Pigmented Lesion / ?Melanoma Assessment",
        "description": "Structured assessment for pigmented skin lesions using 7-point checklist/ABCDE, risk stratification, and 2WW referral criteria for suspected melanoma.",
        "category": "Dermatology",
        "content": {"sections": [
            {
                "title": "History",
                "section_type": "history",
                "questions": [
                    
                    {"id": "pig_age", "type": "number", "label": "Age", "required": True, "placeholder": "e.g., 48", "is_red_flag": True, "red_flag_positive": "RED FLAG: New pigmented lesion in adult >30 = higher suspicion. New naevi less common with age.", "red_flag_negative": ""},
                    {"id": "pig_duration", "type": "single_select", "label": "Duration", "required": True, "options": ["New lesion (weeks-months)", "Long-standing (years)", "Present since childhood", "Unknown"]},
                    {"id": "pig_change", "type": "multi_select", "label": "Change Noted (MOST IMPORTANT)", "required": True, "options": ["Increase in size", "Change in shape", "Change in colour/darkening", "Becoming raised/elevated", "No change - stable"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Any change in size, shape, or colour = RED FLAG for melanoma. 2WW referral.", "red_flag_negative": ""},
                    {"id": "pig_rate_of_change", "type": "single_select", "label": "Rate of Change", "required": False, "options": ["Gradual (months-years)", "Rapid (weeks)", "Not applicable - stable"]},
                    {"id": "pig_symptoms", "type": "multi_select", "label": "Symptoms", "required": True, "options": ["Itch", "Bleeding", "Crusting", "Tenderness/pain", "Oozing", "None"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Bleeding/crusting/oozing without trauma = 2 points on 7-point checklist. 2WW referral.", "red_flag_negative": ""},
                    {"id": "pig_previous_treatment", "type": "toggle", "label": "Previous Treatment / Biopsy to This Lesion?", "required": False}
                ]
            },
            {
                "title": "7-Point Checklist / ABCDE - Melanoma RED FLAGS",
                "section_type": "examination",
                "questions": [
                    {"id": "pig_size_change", "type": "toggle", "label": "Change in Size? (MAJOR - 2 points)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Change in size = 2 points on 7-point checklist. Score ≥3 = 2WW referral.", "red_flag_negative": ""},
                    {"id": "pig_irregular_shape", "type": "toggle", "label": "Irregular Shape / Border? (MAJOR - 2 points)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Irregular border = 2 points. Score ≥3 = 2WW referral.", "red_flag_negative": ""},
                    {"id": "pig_irregular_colour", "type": "toggle", "label": "Irregular Colour / Multiple Shades? (MAJOR - 2 points)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Irregular colour (black, brown, pink, white, blue) = 2 points. Score ≥3 = 2WW.", "red_flag_negative": ""},
                    {"id": "pig_diameter_7mm", "type": "toggle", "label": "Diameter ≥7mm? (MINOR - 1 point)", "required": True},
                    {"id": "pig_inflammation", "type": "toggle", "label": "Inflammation? (MINOR - 1 point)", "required": False},
                    {"id": "pig_oozing_crusting", "type": "toggle", "label": "Oozing / Bleeding / Crusting? (MINOR - 1 point)", "required": False},
                    {"id": "pig_sensation_change", "type": "toggle", "label": "Change in Sensation / Itch? (MINOR - 1 point)", "required": False},
                    {"id": "pig_7point_score", "type": "number", "label": "7-Point Checklist Score (≥3 = 2WW)", "required": True, "placeholder": "e.g., 4", "is_red_flag": True, "red_flag_positive": "RED FLAG: Score ≥3 = 2WW urgent referral for suspected melanoma.", "red_flag_negative": ""},
                    {"id": "pig_abcde", "type": "multi_select", "label": "ABCDE Features Present", "required": True, "options": ["Asymmetry", "Border irregularity", "Colour variation (multiple shades)", "Diameter >6mm", "Evolution/change over time", "None - symmetrical uniform lesion"]}
                ]
            },
            {
                "title": "Additional RED FLAGS",
                "section_type": "examination",
                "questions": [
                    {"id": "pig_ugly_duckling", "type": "toggle", "label": "Ugly Duckling Sign? (Looks different from patient's other moles)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Ugly duckling sign = high suspicion for melanoma. 2WW referral regardless of checklist score.", "red_flag_negative": ""},
                    {"id": "pig_amelanotic", "type": "toggle", "label": "Amelanotic / Pink Lesion That's Changing? (Can still be melanoma)", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Amelanotic melanoma can be pink/red. Changing pink lesion = 2WW.", "red_flag_negative": ""},
                    {"id": "pig_subungual", "type": "toggle", "label": "Subungual Pigmented Band? (Longitudinal, single digit, Hutchinson's sign)", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Subungual pigmented band + Hutchinson's sign (nail fold pigmentation) = subungual melanoma. 2WW dermatology.", "red_flag_negative": ""},
                    {"id": "pig_satellite", "type": "toggle", "label": "Satellite Lesions Around Mole?", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Satellite lesions = possible metastatic melanoma. Urgent 2WW.", "red_flag_negative": ""},
                    {"id": "pig_lymphadenopathy", "type": "toggle", "label": "Regional Lymphadenopathy?", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Lymphadenopathy near lesion = possible metastatic spread. Urgent 2WW.", "red_flag_negative": ""},
                    {"id": "pig_bleeding_ulceration", "type": "toggle", "label": "Bleeding / Ulceration Without Trauma?", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Spontaneous bleeding/ulceration = high suspicion. 2WW.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Risk Factors",
                "section_type": "history",
                "questions": [
                    {"id": "pig_skin_type", "type": "single_select", "label": "Fitzpatrick Skin Type", "required": True, "options": ["Type I - Pale, always burns, never tans", "Type II - Fair, usually burns", "Type III - Olive, sometimes burns", "Type IV - Brown, rarely burns", "Type V - Dark brown", "Type VI - Black"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Fitzpatrick I-II = highest melanoma risk.", "red_flag_negative": ""},
                    {"id": "pig_sunbed", "type": "toggle", "label": "Sunbed Use? (Any history, especially <35 years)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Sunbed use significantly increases melanoma risk. Document and counsel.", "red_flag_negative": ""},
                    {"id": "pig_sunburn_history", "type": "toggle", "label": "History of Blistering Sunburns? (Especially childhood)", "required": True},
                    {"id": "pig_personal_melanoma", "type": "toggle", "label": "Personal History of Melanoma / Skin Cancer?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Previous melanoma = high risk for second primary. Low threshold for 2WW.", "red_flag_negative": ""},
                    {"id": "pig_family_melanoma", "type": "toggle", "label": "Family History Melanoma (1st Degree)?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: FHx melanoma 1st degree = increased risk. Lower threshold for referral.", "red_flag_negative": ""},
                    {"id": "pig_naevus_count", "type": "single_select", "label": "Total Number of Naevi (Approx)", "required": False, "options": ["<50", "50-100", ">100 (increased risk)", "Hundreds (atypical mole syndrome)"]},
                    {"id": "pig_atypical_naevi", "type": "toggle", "label": "Atypical / Dysplastic Naevi Syndrome?", "required": False},
                    {"id": "pig_immunosuppression", "type": "toggle", "label": "Immunosuppression? (Transplant, biologics, immunosuppressants)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Immunosuppressed patients have significantly higher skin cancer risk. Low threshold for referral.", "red_flag_negative": ""},
                    {"id": "pig_outdoor_occupation", "type": "toggle", "label": "Outdoor Occupation? (UV exposure)", "required": False}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "pig_dermoscopy", "type": "toggle", "label": "Dermoscopy Performed? (If trained/available)", "required": False},
                    {"id": "pig_dermoscopy_findings", "type": "single_select", "label": "Dermoscopy Findings", "required": False, "options": ["Benign pattern", "Suspicious - melanocytic with atypical features", "Seborrhoeic keratosis pattern", "Basal cell carcinoma features", "Haemangioma", "Not performed"]},
                    {"id": "pig_size_mm", "type": "number", "label": "Lesion Diameter (mm)", "required": True, "placeholder": "e.g., 8"},
                    {"id": "pig_site", "type": "text", "label": "Site of Lesion", "required": True, "placeholder": "e.g., Left upper back"},
                    {"id": "pig_full_skin_check", "type": "toggle", "label": "Full Skin Check Performed? (Other moles, comparison)", "required": True},
                    {"id": "pig_hidden_sites", "type": "toggle", "label": "Hidden Sites Checked? (Nails, palms, soles, scalp, mucosa)", "required": False},
                    {"id": "pig_lymph_nodes", "type": "toggle", "label": "Regional Lymph Nodes Palpated?", "required": False},
                    {"id": "pig_photograph", "type": "toggle", "label": "Photograph Taken for Monitoring? (If borderline, with consent)", "required": False}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "Benign Melanocytic Naevus",
                    "Seborrhoeic Keratosis ('stuck on', warty, horn cysts)",
                    "Dermatofibroma (dimple sign on lateral pressure)",
                    "Pigmented Basal Cell Carcinoma",
                    "Solar Lentigo (sunspot, age spot)",
                    "Haemangioma / Thrombosed Lesion",
                    "Malignant Melanoma (Superficial Spreading, Nodular, Lentigo Maligna, Acral, Amelanotic)",
                    "Subungual Haematoma (vs Subungual Melanoma - haematoma grows out with nail)",
                    "Lentigo Maligna (melanoma in situ, slow-growing on sun-damaged skin)",
                    "Atypical/Dysplastic Naevus"
                ],
                "questions": [
                    {"id": "pig_diagnosis", "type": "single_select", "label": "Working Diagnosis", "required": True, "options": ["Benign naevus - reassure", "Seborrhoeic keratosis", "Dermatofibroma", "Pigmented BCC", "Suspicious - ?Melanoma (2WW)", "Subungual haematoma", "Atypical naevus - monitor", "Uncertain"]}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "If melanoma suspected: do NOT biopsy in primary care. Refer via 2WW pathway for excision biopsy by dermatology/plastic surgery. If benign/stable: reassure, document description (size, site, colour, dermoscopy), photograph if available, safety-net for change. Sun protection advice for ALL patients: SPF 30+ broad spectrum, avoid midday sun (11am-3pm), no sunbeds, hat and clothing. High-risk patients: regular self-skin checks (monthly), full skin examination by GP annually or as per dermatology advice. Return immediately if: lesion changes (size, shape, colour), becomes symptomatic (itch, bleed, crust), new lesion appears nearby, or regional lymphadenopathy develops. Educate on ABCDE and ugly duckling sign for self-monitoring.",
                "questions": [
                    {"id": "pig_plan", "type": "single_select", "label": "Management Plan", "required": True, "options": ["Reassure + safety-net (benign)", "Monitor - photograph + review (borderline/low suspicion)", "Routine dermatology referral (non-urgent lesion)", "Urgent 2WW referral (suspected melanoma)", "Routine referral (suspected BCC/SCC)", "Sun protection advice only"]},
                    {"id": "pig_referral_reason", "type": "textarea", "label": "Referral Details (if referring)", "required": False, "placeholder": "e.g., 7-point score 4 - irregular shape, colour change, diameter 9mm, new itch. Site: left upper back. ?Superficial spreading melanoma."},
                    {"id": "pig_biopsy_warning", "type": "toggle", "label": "NO Primary Care Biopsy if Melanoma Suspected? (2WW for excision biopsy)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: NEVER biopsy suspected melanoma in primary care. Refer 2WW for specialist excision biopsy.", "red_flag_negative": ""},
                    {"id": "pig_sun_protection", "type": "toggle", "label": "Sun Protection Advised? (SPF 30+, avoid midday sun, no sunbeds, hat/clothing)", "required": True},
                    {"id": "pig_self_check", "type": "toggle", "label": "Self-Skin Check + ABCDE Education Given?", "required": True},
                    {"id": "pig_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., PRN if changes, routine review 6-12 months if high-risk, or after dermatology appointment"}
                ]
            }
        ]},
        "is_public": True
    }

    existing = db.query(Template).filter(Template.title == t["title"], Template.created_by == admin.id).first()
    if existing: db.delete(existing); db.commit()
    new_t = Template(title=t["title"], description=t["description"], category=t["category"], content=t["content"], is_public=True, created_by=admin.id, version=1)
    db.add(new_t); db.commit()
    print(f"Template '{t['title']}' created with {len(t['content']['sections'])} sections!"); db.close()

if __name__ == "__main__":
    seed_pigmented_lesion()
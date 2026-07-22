from app.database import SessionLocal
from app.models import User, Template, Category

def seed_epistaxis():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "ENT").first()
    if not category: category = Category(name="ENT"); db.add(category); db.commit()

    t = {
        "title": "Epistaxis / Nosebleed Assessment",
        "description": "Emergency-focused assessment for epistaxis with acute management, red flags for tumour/bleeding disorders, anticoagulant review, and management including cautery criteria.",
        "category": "ENT",
        "content": {"sections": [
            {
                "title": "ACUTE - Is This an Emergency NOW?",
                "section_type": "history",
                "questions": [
                    {"id": "epi_active_bleeding", "type": "toggle", "label": "Active Bleeding NOW on Presentation?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Active bleeding - assess ABC first. If not controlled with 10-15 min direct pressure → urgent A&E.", "red_flag_negative": ""},
                    {"id": "epi_duration", "type": "text", "label": "Duration of Current Bleed", "required": True, "placeholder": "e.g., 30 minutes"},
                    {"id": "epi_blood_loss", "type": "single_select", "label": "Estimated Blood Loss", "required": True, "options": ["Minimal (few drops/tissue)", "Moderate (cupful)", "Profuse (flowing continuously)", "Massive - haemodynamic compromise"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Profuse/massive bleeding or haemodynamic compromise = EMERGENCY. ABC, IV access, urgent ENT/A&E.", "red_flag_negative": ""},
                    {"id": "epi_hypovolaemia", "type": "multi_select", "label": "Signs of Hypovolaemia", "required": True, "options": ["Dizziness/lightheadedness", "Pallor", "Tachycardia", "Hypotension", "Syncope", "None"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Haemodynamic instability = emergency. Transfer to A&E immediately.", "red_flag_negative": ""},
                    {"id": "epi_first_aid_effective", "type": "toggle", "label": "Bleeding Controlled with 10-15 min Direct Pressure? (Sit forward, pinch soft part of nose)", "required": True}
                ]
            },
            {
                "title": "Presentation",
                "section_type": "history",
                "questions": [
                    {"id": "epi_side", "type": "single_select", "label": "Side", "required": True, "options": ["Unilateral - Right", "Unilateral - Left", "Bilateral"]},
                    {"id": "epi_site", "type": "single_select", "label": "Anterior vs Posterior", "required": True, "options": ["Anterior (visible, Little's area)", "Posterior (profuse, bilateral, posterior throat trickle, difficult to visualise)"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Posterior bleed = often profuse, difficult to control. Needs urgent ENT for packing/management.", "red_flag_negative": ""},
                    {"id": "epi_first_or_recurrent", "type": "single_select", "label": "First Episode or Recurrent", "required": True, "options": ["First episode", "Recurrent - occasional", "Recurrent - frequent (multiple per week)", "Recurrent - since childhood"]},
                    {"id": "epi_frequency", "type": "text", "label": "Frequency if Recurrent", "required": False, "placeholder": "e.g., 2-3 times per week"}
                ]
            },
            {
                "title": "RED FLAGS - Tumour / Bleeding Disorder",
                "section_type": "history",
                "questions": [
                    {"id": "epi_unilateral_discharge", "type": "toggle", "label": "Unilateral Blood-Stained Nasal Discharge / Obstruction?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Unilateral blood-stained discharge + obstruction = sinonasal tumour until proven otherwise. Urgent 2WW ENT.", "red_flag_negative": ""},
                    {"id": "epi_facial_pain_numbness", "type": "toggle", "label": "Facial Pain / Numbness?", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Facial pain/numbness + epistaxis = possible sinonasal malignancy. Urgent ENT.", "red_flag_negative": ""},
                    {"id": "epi_child_unilateral", "type": "toggle", "label": "Child with Recurrent Unilateral Epistaxis? (Foreign body / Juvenile angiofibroma)", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Recurrent unilateral epistaxis in child = foreign body or juvenile nasopharyngeal angiofibroma (adolescent male). ENT referral.", "red_flag_negative": ""},
                    {"id": "epi_easy_bruising", "type": "toggle", "label": "Easy Bruising / Gum Bleeding / Menorrhagia?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Multiple bleeding symptoms = possible bleeding disorder (vWD, haemophilia, thrombocytopenia). Check FBC + coagulation.", "red_flag_negative": ""},
                    {"id": "epi_telangiectasia", "type": "toggle", "label": "Telangiectasia on Lips/Tongue/Fingers? + FHx epistaxis? (HHT)", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Recurrent epistaxis + telangiectasia + FHx = Hereditary Haemorrhagic Telangiectasia (HHT). ENT + genetics referral.", "red_flag_negative": ""},
                    {"id": "epi_failure_cautery", "type": "toggle", "label": "Failed Cautery / Packing Despite Treatment?", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Recurrent despite cautery/packing = ENT referral for further management.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Triggers & Precipitants",
                "section_type": "history",
                "questions": [
                    {"id": "epi_trauma", "type": "single_select", "label": "Trauma", "required": True, "options": ["None", "Nose picking (digital trauma)", "Blunt trauma/accident", "Forceful nose blowing/sneezing", "Recent nasal surgery"]},
                    {"id": "epi_dry_air", "type": "toggle", "label": "Dry Air / Central Heating / Low Humidity?", "required": False},
                    {"id": "epi_cocaine", "type": "toggle", "label": "Cocaine Use? (Septal perforation risk)", "required": False},
                    {"id": "epi_recent_urti", "type": "toggle", "label": "Recent URTI / Sinusitis?", "required": False},
                    {"id": "epi_altitude", "type": "toggle", "label": "Recent High Altitude / Air Travel?", "required": False}
                ]
            },
            {
                "title": "Past History & Medications - CRUCIAL",
                "section_type": "history",
                "questions": [
                    {"id": "epi_hypertension", "type": "toggle", "label": "Hypertension?", "required": True},
                    {"id": "epi_bleeding_disorder", "type": "multi_select", "label": "Bleeding Disorder History", "required": True, "options": ["von Willebrand disease", "Haemophilia A/B", "Thrombocytopenia", "Liver disease (clotting factors)", "Renal disease", "None known"]},
                    {"id": "epi_hht_family", "type": "toggle", "label": "Family History of HHT or Bleeding Disorders?", "required": False},
                    {"id": "epi_anticoagulants", "type": "multi_select", "label": "Anticoagulants / Antiplatelets", "required": True, "options": ["Warfarin", "DOAC (Rivaroxaban/Apixaban/Edoxaban)", "Aspirin", "Clopidogrel", "Ticagrelor", "NSAIDs", "Fish oil/Ginkgo supplements", "None"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Patient on anticoagulants/antiplatelets - assess bleeding risk urgently. Check INR if on warfarin. Do NOT stop independently - discuss with prescriber.", "red_flag_negative": ""},
                    {"id": "epi_nasal_spray", "type": "toggle", "label": "Using Nasal Corticosteroid Spray? (Check technique - avoid aiming at septum)", "required": False}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "epi_bp_systolic", "type": "number", "label": "BP Systolic (mmHg)", "required": True, "placeholder": "e.g., 148", "is_red_flag": True, "red_flag_positive": "RED FLAG: Severe hypertension may contribute to epistaxis and impair clotting. If BP >180/120 + active bleeding → urgent A&E.", "red_flag_negative": ""},
                    {"id": "epi_bp_diastolic", "type": "number", "label": "BP Diastolic (mmHg)", "required": True, "placeholder": "e.g., 92"},
                    {"id": "epi_hr", "type": "number", "label": "Heart Rate (bpm)", "required": True, "placeholder": "e.g., 88"},
                    {"id": "epi_rhinoscopy", "type": "single_select", "label": "Anterior Rhinoscopy Findings", "required": True, "options": ["Normal", "Bleeding point visible - Little's area/Kiesselbach's plexus", "Septal deviation", "Septal perforation", "Crusting", "Mass/lesion", "Telangiectasia", "Unable to visualise"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Mass/lesion or unilateral bleeding point not in Little's area = needs ENT assessment. Septal perforation in cocaine user.", "red_flag_negative": ""},
                    {"id": "epi_telangiectasia_exam", "type": "toggle", "label": "Telangiectasia on Lips/Tongue/Fingers? (HHT)", "required": False},
                    {"id": "epi_anaemia_signs", "type": "toggle", "label": "Signs of Anaemia? (Pallor, conjunctival pallor)", "required": False}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "Anterior Epistaxis - Little's Area / Kiesselbach's Plexus (most common, benign)",
                    "Posterior Epistaxis (more serious, often requires ENT admission)",
                    "Traumatic Epistaxis (digital trauma, blunt trauma)",
                    "Dry Air / Environmental Epistaxis",
                    "Cocaine-Induced Septal Perforation",
                    "Anticoagulant/Antiplatelet-Related Epistaxis",
                    "Hypertension-Associated Epistaxis",
                    "Bleeding Disorder (vWD, Haemophilia, Thrombocytopenia, Liver Disease)",
                    "Hereditary Haemorrhagic Telangiectasia (HHT)",
                    "Sinonasal Tumour (unilateral + blood-stained discharge)",
                    "Juvenile Nasopharyngeal Angiofibroma (adolescent males, unilateral, recurrent)",
                    "Foreign Body (children, unilateral, offensive discharge)",
                    "Nasal Steroid Spray Technique-Related"
                ],
                "questions": [
                    {"id": "epi_diagnosis", "type": "single_select", "label": "Working Diagnosis", "required": True, "options": ["Anterior epistaxis - benign", "Posterior epistaxis", "Traumatic (nose picking/blunt)", "Anticoagulant-related", "Environmental/dry air", "Suspected bleeding disorder", "Suspected HHT", "Suspected sinonasal tumour", "Cocaine-related", "Uncertain"]}
                ]
            },
            {
                "title": "Investigations",
                "section_type": "plan",
                "questions": [
                    {"id": "epi_fbc", "type": "toggle", "label": "FBC? (Recurrent/heavy - check for anaemia/thrombocytopenia)", "required": False},
                    {"id": "epi_coagulation", "type": "toggle", "label": "Coagulation Screen / INR? (If on warfarin or bleeding disorder suspected)", "required": False},
                    {"id": "epi_group_save", "type": "toggle", "label": "Group & Save / Crossmatch? (If significant blood loss)", "required": False},
                    {"id": "epi_nasal_endoscopy", "type": "toggle", "label": "Nasal Endoscopy? (ENT - if unilateral, persistent, red flags)", "required": False}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "First aid: Sit up, lean FORWARD (not back - blood swallowing causes nausea), firm pressure to soft cartilaginous part of nose for 10-15 min continuous (time it). Ice pack to nape/bridge of nose may help. Do NOT lean head back. If bleeding point visible and settled: Naseptin cream (chlorhexidine + neomycin) BD for 1-2 weeks (caution: peanut/soy allergy - contains arachis oil). Consider silver nitrate cautery if bleeding point visible and trained. Nasal packing if not controlled → same-day ENT/A&E. Review anticoagulants with prescriber (do NOT stop independently). Correct nasal spray technique if steroid-related. Children: usually self-limiting, reassure, treat dryness with petroleum jelly/Naseptin. Return immediately if: bleeding doesn't stop after 15-20 min correct first aid, recurrent/worsening, easy bruising/other bleeding, unilateral obstruction/discharge develops.",
                "questions": [
                    {"id": "epi_plan", "type": "single_select", "label": "Management", "required": True, "options": ["First aid advice + discharge", "Naseptin cream (anterior bleed)", "Silver nitrate cautery (if trained + bleeding point visible)", "Nasal packing → same-day ENT/A&E", "Emergency A&E referral (uncontrolled/posterior/haemodynamic compromise)", "Routine ENT referral (recurrent/red flags)", "Urgent 2WW ENT (suspected tumour)"]},
                    {"id": "epi_naseptin", "type": "toggle", "label": "Naseptin Cream Prescribed? (Check peanut/soy allergy - contains arachis oil)", "required": False},
                    {"id": "epi_naseptin_caution", "type": "toggle", "label": "Peanut / Soy Allergy? (Contraindication to Naseptin)", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Do NOT prescribe Naseptin if peanut/soy allergy. Use alternative (petroleum jelly, mupirocin).", "red_flag_negative": ""},
                    {"id": "epi_cautery", "type": "toggle", "label": "Silver Nitrate Cautery Performed?", "required": False},
                    {"id": "epi_anticoagulant_review", "type": "toggle", "label": "Anticoagulant/Antiplatelet Review? (Discuss with prescriber - do NOT stop independently)", "required": False},
                    {"id": "epi_nasal_spray_technique", "type": "toggle", "label": "Nasal Spray Technique Checked? (Avoid aiming at septum)", "required": False},
                    {"id": "epi_petroleum_jelly", "type": "toggle", "label": "Petroleum Jelly / Moisturising Ointment Advised? (Dry air, recurrent)", "required": False},
                    {"id": "epi_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., PRN if resolves, 2 weeks if Naseptin, or after ENT review"}
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
    seed_epistaxis()
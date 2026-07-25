from app.database import SessionLocal
from app.models import User, Template, Category

def seed_hfmd():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Paediatrics").first()
    if not category: category = Category(name="Paediatrics"); db.add(category); db.commit()

    t = {
        "title": "Hand, Foot & Mouth Disease Assessment",
        "description": "Focused assessment for HFMD covering lesion distribution, dehydration assessment, crèche guidance, and red flags for complications.",
        "category": "Paediatrics",
        "content": {"sections": [
            {
                "title": "Presentation",
                "section_type": "history",
                "questions": [
                    {"id": "hfmd_presenting_complaint", "type": "text", "label": "Presenting Complaint", "required": True, "placeholder": "e.g., Off-form with spots on hands, feet, and mouth"},
                    {"id": "hfmd_age", "type": "single_select", "label": "Age", "required": True, "options": ["<1 year", "1-2 years", "2-5 years", "6-12 years", "Adult"]},
                    {"id": "hfmd_duration", "type": "text", "label": "Duration of Symptoms", "required": True, "placeholder": "e.g., Since this morning"},
                    {"id": "hfmd_creche", "type": "toggle", "label": "Attends Crèche / School?", "required": True},
                    {"id": "hfmd_feeding_drinking", "type": "single_select", "label": "Feeding / Drinking", "required": True, "options": ["Normal - drinking well", "Reduced but adequate", "Poor - struggling to drink"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Poor oral intake = risk of dehydration. Monitor closely. Consider admission if not improving.", "red_flag_negative": ""},
                    {"id": "hfmd_wet_nappies", "type": "single_select", "label": "Wet Nappies / Urine Output", "required": True, "options": ["Normal", "Reduced - RED FLAG", "None in >12 hours - RED FLAG"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Reduced/absent wet nappies = dehydration. Urgent assessment + encourage fluids.", "red_flag_negative": ""},
                    {"id": "hfmd_symptoms", "type": "multi_select", "label": "Symptoms", "required": True, "options": ["Fever", "Sore mouth/throat", "Refusing food", "Rash/spots", "Irritability", "Coryza", "Drooling", "None - rash only"]},
                    {"id": "hfmd_immunisations", "type": "toggle", "label": "Childhood Immunisations Up to Date?", "required": True}
                ]
            },
            {
                "title": "RED FLAGS - Complications",
                "section_type": "history",
                "questions": [
                    {"id": "hfmd_dehydration", "type": "toggle", "label": "Signs of Dehydration? (Dry mouth, no tears, reduced urine, sunken eyes)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Clinical dehydration = needs admission for NG/IV fluids. Urgent paediatric assessment.", "red_flag_negative": ""},
                    {"id": "hfmd_lethargy", "type": "toggle", "label": "Extreme Lethargy / Drowsiness / Floppiness?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Lethargy/drowsiness = ?enteroviral meningitis/encephalitis. EMERGENCY admission.", "red_flag_negative": ""},
                    {"id": "hfmd_rigors", "type": "toggle", "label": "Rigors / Persistent High Fever >39°C?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Rigors + high fever = ?sepsis/secondary infection. Urgent assessment.", "red_flag_negative": ""},
                    {"id": "hfmd_respiratory_distress", "type": "toggle", "label": "Tachypnoea / Recession / Breathing Difficulty?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Respiratory distress = ?myocarditis, pneumonia. EMERGENCY admission.", "red_flag_negative": ""},
                    {"id": "hfmd_neck_stiffness", "type": "toggle", "label": "Neck Stiffness / Photophobia?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Meningism = ?enteroviral meningitis. Urgent paediatric admission.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "hfmd_temp", "type": "number", "label": "Temperature (°C)", "required": True, "placeholder": "e.g., 37.3"},
                    {"id": "hfmd_hr", "type": "number", "label": "Heart Rate (bpm)", "required": True, "placeholder": "e.g., 90"},
                    {"id": "hfmd_rr", "type": "number", "label": "Respiratory Rate (/min)", "required": False, "placeholder": "e.g., 25"},
                    {"id": "hfmd_general", "type": "single_select", "label": "General Appearance", "required": True, "options": ["Clinically well - alert + active", "Mildly unwell", "Lethargic/drowsy - RED FLAG"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Lethargic = urgent paediatric assessment.", "red_flag_negative": ""},
                    {"id": "hfmd_lesion_sites", "type": "multi_select", "label": "Lesion Locations", "required": True, "options": ["Hands", "Feet", "Buttocks", "Genital region", "Arms", "Legs", "Face", "None visible"]},
                    {"id": "hfmd_lesion_type", "type": "multi_select", "label": "Lesion Type", "required": True, "options": ["Maculopapular (flat red spots)", "Vesicular (small blisters)", "Both", "Healing/crusting"]},
                    {"id": "hfmd_oral", "type": "single_select", "label": "Oral Examination", "required": True, "options": ["Ulcers/vesicles on buccal mucosa/tongue", "Pharyngeal erythema only", "Normal", "Not assessed"]},
                    {"id": "hfmd_coryza", "type": "toggle", "label": "Coryzal Features?", "required": False},
                    {"id": "hfmd_chest", "type": "single_select", "label": "Chest Auscultation", "required": False, "options": ["Clear B/L", "Abnormal - RED FLAG", "Not assessed"]},
                    {"id": "hfmd_crt", "type": "single_select", "label": "Capillary Refill Time", "required": False, "options": ["<2 seconds", ">2 seconds - RED FLAG", "Not assessed"]}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "Hand, Foot & Mouth Disease (Coxsackie A16 / Enterovirus A71)",
                    "Herpangina (vesicles posterior oropharynx - Coxsackie)",
                    "Chickenpox (centripetal, all stages, sparing palms/soles)",
                    "Herpes Simplex Gingivostomatitis",
                    "Erythema Multiforme",
                    "Aphthous Ulcers (no rash)",
                    "Scabies (burrows, interdigital)",
                    "Enteroviral Meningitis (RED FLAG - lethargy, neck stiffness)"
                ],
                "questions": [
                    {"id": "hfmd_diagnosis", "type": "single_select", "label": "Working Diagnosis", "required": True, "options": ["HFMD - mild, uncomplicated", "HFMD - with oral ulcer pain (reduced intake)", "HFMD - ?dehydration", "HFMD - ?neurological complication (URGENT)", "Uncertain"]}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Return immediately or attend ED if: decreased urine/wet nappies, no tears when crying, dry mouth (dehydration), lethargy/drowsiness/floppiness, persistent high fever >39°C, rigors, neck stiffness, tachypnoea/recession, or significant lethargy. HFMD is self-limiting (7-10 days), unrelated to Foot-and-Mouth disease in livestock. Painless skin peeling (palms/soles) or nail dystrophy/loss (onychomadesis) can occur 2-4 weeks post-infection - this is a benign delayed sequela. Encourage frequent small sips of cool fluids/milk/ice lollies. Paracetamol + Ibuprofen (safe in HFMD unlike chickenpox) for pain/fever. Strict hand hygiene - transmitted via droplet, contact with vesicle fluid, and faecal-oral route. Crèche: child can attend if clinically well (exclusion not routine unless unwell, unable to feed, or during facility outbreak per HPSC).",
                "questions": [
                    {"id": "hfmd_plan", "type": "single_select", "label": "Management", "required": True, "options": ["Reassurance + supportive care", "Paracetamol + Ibuprofen", "Encourage fluids / ice lollies", "Crèche exclusion advised", "No exclusion - can attend if well", "Urgent paediatric referral"]},
                    {"id": "hfmd_hydration", "type": "toggle", "label": "Hydration Advice Given? (Frequent small sips, cool fluids, ice lollies)", "required": True},
                    {"id": "hfmd_analgesia", "type": "toggle", "label": "Analgesia Advised? (Paracetamol + Ibuprofen safe in HFMD)", "required": False},
                    {"id": "hfmd_desquamation", "type": "toggle", "label": "Delayed Peeling/Nail Loss Explained? (2-4 weeks post - benign)", "required": False},
                    {"id": "hfmd_infection_control", "type": "toggle", "label": "Hand Hygiene + Transmission Advised?", "required": True},
                    {"id": "hfmd_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., PRN if resolving, 7-10 days if not improving"}
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
    seed_hfmd()
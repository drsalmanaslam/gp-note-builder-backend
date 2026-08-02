from app.database import SessionLocal
from app.models import User, Template

def seed_cellulitis():
    db = SessionLocal()
    admin = db.query(User).filter(User.role == "admin").first()
    if not admin: print("❌ No admin!"); db.close(); return

    title = "Cellulitis / Skin Infection"
    existing = db.query(Template).filter(Template.title == title).first()
    if existing: db.delete(existing); db.commit()

    t = Template(title=title, description="Assessment of cellulitis covering Eron classification, marking erythema, antibiotic choice per NICE, red flags for necrotising fasciitis, and admission criteria.", category="Dermatology", content={"sections": [
        {"title": "History", "section_type": "history", "questions": [
            {"id": "cel_site", "type": "text", "label": "Site", "required": True, "placeholder": "e.g., Left lower leg"},
            {"id": "cel_duration", "type": "text", "label": "Duration", "required": True, "placeholder": "e.g., 2 days"},
            {"id": "cel_onset", "type": "single_select", "label": "Onset", "required": True, "options": ["Gradual", "Rapid (hours) - RED FLAG"]},
            {"id": "cel_trauma", "type": "toggle", "label": "Break in Skin? (Cut, scratch, athlete's foot)", "required": True},
            {"id": "cel_pain", "type": "single_select", "label": "Pain Severity", "required": True, "options": ["Mild", "Moderate", "Severe", "Pain out of proportion to signs - RED FLAG"]},
            {"id": "cel_fever", "type": "toggle", "label": "Fever / Rigors / Malaise?", "required": True},
            {"id": "cel_diabetes", "type": "toggle", "label": "Diabetes?", "required": True},
            {"id": "cel_immunocompromised", "type": "toggle", "label": "Immunocompromised?", "required": True},
            {"id": "cel_lymphedema", "type": "toggle", "label": "Lymphoedema / Venous Disease?", "required": True},
            {"id": "cel_previous_cellulitis", "type": "toggle", "label": "Previous Cellulitis?", "required": True},
            {"id": "cel_antibiotics_recent", "type": "toggle", "label": "Recent Antibiotics?", "required": False}
        ]},
        {"title": "Examination & Eron Classification", "section_type": "examination", "questions": [
            {"id": "cel_temp", "type": "text", "label": "Temperature (°C)", "required": True, "placeholder": "e.g., 38.1"},
            {"id": "cel_hr", "type": "text", "label": "Heart Rate", "required": True, "placeholder": "e.g., 92"},
            {"id": "cel_bp", "type": "text", "label": "Blood Pressure", "required": True, "placeholder": "e.g., 110/70"},
            {"id": "cel_rr", "type": "number", "label": "Respiratory Rate", "required": False, "placeholder": "e.g., 18"},
            {"id": "cel_erythema", "type": "single_select", "label": "Erythema", "required": True, "options": ["Well-demarcated", "Diffuse", "Rapidly spreading"]},
            {"id": "cel_mark_edge", "type": "toggle", "label": "Edge Marked? (To monitor progression)", "required": True},
            {"id": "cel_warmth", "type": "toggle", "label": "Local Warmth?", "required": True},
            {"id": "cel_swelling", "type": "single_select", "label": "Swelling", "required": True, "options": ["Mild", "Moderate", "Severe / Tense"]},
            {"id": "cel_blistering", "type": "toggle", "label": "Blistering / Bullae?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Blistering = ?necrotising fasciitis or severe cellulitis. Urgent surgical assessment.", "red_flag_negative": ""},
            {"id": "cel_crepitus", "type": "toggle", "label": "Crepitus on Palpation?", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Crepitus = gas gangrene/necrotising fasciitis. Surgical EMERGENCY.", "red_flag_negative": ""},
            {"id": "cel_eron", "type": "single_select", "label": "Eron Classification", "required": True, "options": ["Class I: No systemic toxicity or comorbidity", "Class II: Systemic toxicity OR comorbidity (PVD, DM, obesity)", "Class III: Significant systemic toxicity (confusion, tachycardia, tachypnoea, hypotension)", "Class IV: Sepsis / Life-threatening"]}
        ]},
        {"title": "Assessment", "section_type": "assessment", "differentials": ["Cellulitis (bacterial - Strep/Staph)", "Erysipelas (more superficial, well-demarcated)", "Necrotising Fasciitis (SURGICAL EMERGENCY)", "DVT (unilateral swelling, calf tenderness)", "Contact dermatitis", "Gout (if over joint)", "Lipedema / Venous eczema"], "questions": [
            {"id": "cel_diagnosis", "type": "single_select", "label": "Diagnosis", "required": True, "options": ["Cellulitis - Class I (oral antibiotics)", "Cellulitis - Class II (oral antibiotics + comorbidity)", "Cellulitis - Class III (IV antibiotics / admission)", "Cellulitis - Class IV (Emergency admission)", "Suspected necrotising fasciitis - 999"]},
            {"id": "cel_dvt_excluded", "type": "toggle", "label": "DVT Considered & Excluded?", "required": False}
        ]},
        {"title": "Management", "section_type": "plan", "safety_netting": "Return immediately or attend A&E if: rapidly spreading redness, severe pain, blistering, fever >38°C, confusion, or feeling very unwell. Mark edge of erythema with pen - if spreading beyond mark despite antibiotics, seek urgent review. Elevate affected limb to reduce swelling. Treat fungal infection (athlete's foot) if present to prevent recurrence. Flucloxacillin 500mg QDS 7 days (first-line). Clarithromycin 500mg BD if penicillin allergic. Class III/IV: admit for IV antibiotics.", "questions": [
            {"id": "cel_antibiotic", "type": "single_select", "label": "Antibiotic", "required": True, "options": ["Flucloxacillin 500mg QDS 7 days", "Clarithromycin 500mg BD 7 days (penicillin allergy)", "Doxycycline 200mg stat then 100mg OD", "IV antibiotics - admit", "Clindamycin (if severe penicillin allergy)"]},
            {"id": "cel_analgesia", "type": "toggle", "label": "Analgesia Advised?", "required": False},
            {"id": "cel_antifungal", "type": "toggle", "label": "Antifungal for Athlete's Foot?", "required": False},
            {"id": "cel_safety", "type": "toggle", "label": "Edge Marked + Red Flags Explained?", "required": True},
            {"id": "cel_followup", "type": "text", "label": "Follow-up", "required": True, "placeholder": "e.g., Review in 48h if not improving, return immediately if spreading"}
        ]}
    ]}, is_public=True, created_by=admin.id)
    db.add(t); db.commit(); print(f"✅ {title}"); db.close()

if __name__ == "__main__": seed_cellulitis()
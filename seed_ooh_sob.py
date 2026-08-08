from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_ooh_sob():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin:
        print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "OOH").first()
    if not category:
        category = Category(name="OOH"); db.add(category); db.commit()

    t = {
        "title": "OOH - Acute Shortness of Breath",
        "description": "Rapid out-of-hours assessment of acute breathlessness. Rule out PE, asthma, anaphylaxis, pneumothorax, and heart failure.",
        "category": "OOH",
        "content": {"sections": [
            {
                "title": "Assessment",
                "section_type": "history",
                "questions": [
                    {"id": "ooh_sob_onset", "type": "single_select", "label": "Onset", "required": True, "options": ["Sudden — seconds/minutes", "Over hours", "Gradual — days/weeks"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Sudden onset = ?PE, pneumothorax, anaphylaxis, foreign body. Emergency.", "red_flag_negative": "", "output_phrase": "Onset: {value}"},
                    {"id": "ooh_sob_severity", "type": "single_select", "label": "Severity", "required": True, "options": ["Mild — can speak in full sentences", "Moderate — speaks in phrases", "Severe — single words only", "Life-threatening — unable to speak, cyanosed"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Unable to speak/cyanosed = LIFE-THREATENING. Call 999 immediately.", "red_flag_negative": "", "output_phrase": "Severity: {value}"}
                ]
            },
            {
                "title": "Red Flags — Must Rule Out",
                "section_type": "history",
                "questions": [
                    {"id": "ooh_sob_anaphylaxis", "type": "toggle", "label": "?Anaphylaxis (urticaria, angioedema, stridor, hypotension, known trigger)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Anaphylaxis = EMERGENCY. IM Adrenaline 0.5mg STAT. Call 999.", "red_flag_negative": "", "output_phrase": "?Anaphylaxis: {value}"},
                    {"id": "ooh_sob_pe", "type": "toggle", "label": "?PE (sudden onset, pleuritic pain, haemoptysis, calf swelling, risk factors)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: ?PE = emergency. Call 999 if hypotensive/hypoxic. Admit for CTPA.", "red_flag_negative": "", "output_phrase": "?PE: {value}"},
                    {"id": "ooh_sob_pneumothorax", "type": "toggle", "label": "?Pneumothorax (sudden unilateral pain, hyper-resonance, reduced breath sounds)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: ?Tension pneumothorax = EMERGENCY. Call 999. Needle decompression if trained.", "red_flag_negative": "", "output_phrase": "?Pneumothorax: {value}"},
                    {"id": "ooh_sob_asthma", "type": "toggle", "label": "?Severe Asthma (known asthmatic, wheeze, silen chest, PEFR <33%)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Life-threatening asthma = EMERGENCY. Call 999. Back-to-back nebs whilst waiting.", "red_flag_negative": "", "output_phrase": "?Asthma: {value}"}
                ]
            },
            {
                "title": "Vitals",
                "section_type": "examination",
                "questions": [
                    {"id": "ooh_sob_rr", "type": "number", "label": "Respiratory Rate", "required": True, "placeholder": "e.g., 32", "is_red_flag": True, "red_flag_positive": "RED FLAG: RR >30 = severe respiratory distress. Emergency.", "red_flag_negative": "", "output_phrase": "RR: {value}"},
                    {"id": "ooh_sob_sats", "type": "number", "label": "O2 Saturations (%)", "required": True, "placeholder": "e.g., 89", "is_red_flag": True, "red_flag_positive": "RED FLAG: SpO2 <92% on air = severe hypoxia. O2 + emergency admission.", "red_flag_negative": "", "output_phrase": "SpO2: {value}%"},
                    {"id": "ooh_sob_pefr", "type": "text", "label": "PEFR (if known asthmatic)", "required": False, "placeholder": "e.g., 150 (best 400)", "output_phrase": "PEFR: {value}"}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": ["Anaphylaxis", "Pulmonary Embolism", "Tension Pneumothorax", "Acute Severe Asthma", "Acute Pulmonary Oedema / Heart Failure", "COPD Exacerbation", "Pneumonia", "Hyperventilation / Panic"],
                "questions": [
                    {"id": "ooh_sob_diagnosis", "type": "single_select", "label": "Working Diagnosis", "required": True, "options": ["?Anaphylaxis — adrenaline + 999", "?PE — admit", "?Tension pneumothorax — 999", "?Severe asthma — 999 + nebs", "?Heart failure — admit", "Mild — safe for home"], "output_phrase": "Diagnosis: {value}"}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Life-threatening: Call 999. Oxygen to maintain SpO2 94-98%. Specific: Adrenaline IM for anaphylaxis, back-to-back salbutamol nebs for asthma, GTN + furosemide for APO. If safe for home: Clear safety-net. Return immediately if SOB worsens, can't speak, stridor, cyanosis. GP follow-up in 24h.",
                "questions": [
                    {"id": "ooh_sob_action", "type": "single_select", "label": "Disposition", "required": True, "options": ["999 ambulance", "Direct medical admission", "Home with safety-net + GP follow-up"], "output_phrase": "Disposition: {value}"},
                    {"id": "ooh_sob_safety_net", "type": "toggle", "label": "Safety-Net Given?", "required": True, "output_phrase": "Safety-net: {value}"},
                    {"id": "ooh_sob_followup", "type": "text", "label": "Follow-up", "required": True, "placeholder": "e.g., Admitted. GP to review post-discharge.", "output_phrase": "Follow-up: {value}"}
                ]
            }
        ]},
        "is_public": True
    }

    existing = db.query(Template).filter(Template.title == t["title"], Template.created_by == admin.id).first()
    if existing:
        existing.description = t["description"]; existing.content = t["content"]; existing.category = t["category"]; existing.is_public = t["is_public"]; existing.updated_at = datetime.now(timezone.utc)
        db.commit(); print(f"Updated: {t['title']}")
    else:
        new_t = Template(title=t["title"], description=t["description"], category=t["category"], content=t["content"], is_public=True, created_by=admin.id, version=1)
        db.add(new_t); db.commit(); print(f"Created: {t['title']}")
    db.close()

if __name__ == "__main__":
    seed_ooh_sob()
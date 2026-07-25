from app.database import SessionLocal
from app.models import User, Template, Category

def seed_noac_guide():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Cardiovascular").first()
    if not category: category = Category(name="Cardiovascular"); db.add(category); db.commit()

    t = {
        "title": "NOAC Management Guide",
        "description": "Quick-reference guide for NOAC management in primary care covering peri-procedural holding, post-PCI protocols, switching, and prescribing safety.",
        "category": "Cardiovascular",
        "content": {"sections": [
            {
                "title": "Peri-Procedural NOAC Management",
                "section_type": "history",
                "questions": [
                    {"id": "noac_procedure_type", "type": "single_select", "label": "Procedure Bleeding Risk", "required": True, "options": ["Low Risk (dental extraction, skin excision, cataract)", "Moderate Risk", "High Risk (major surgery, spinal, neurosurgery)"]},
                    {"id": "noac_crcl", "type": "number", "label": "CrCl (mL/min - Cockcroft-Gault)", "required": True, "placeholder": "e.g., 65"},
                    {"id": "noac_low_risk_action", "type": "single_select", "label": "Low Risk Action", "required": False, "options": ["Continue NOAC - no interruption", "Hold single morning dose only", "Hold 24h pre-procedure"]},
                    {"id": "noac_moderate_high_risk_crcl_50", "type": "single_select", "label": "Moderate/High Risk - CrCl ≥50", "required": False, "options": ["Hold NOAC 24-48h pre-procedure", "Hold NOAC 48-72h pre-procedure"]},
                    {"id": "noac_moderate_high_risk_crcl_low", "type": "single_select", "label": "Moderate/High Risk - CrCl <50 (esp Dabigatran)", "required": False, "options": ["Hold NOAC 48-96h pre-procedure", "Discuss with specialist"]},
                    {"id": "noac_bridging", "type": "toggle", "label": "LMWH Bridging Required?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: LMWH bridging is CONTRAINDICATED with NOACs. Increases bleeding risk without reducing stroke risk. Do NOT bridge.", "red_flag_negative": ""},
                    {"id": "noac_sdcep", "type": "toggle", "label": "SDCEP Anticoagulant Guidance Referenced?", "required": False}
                ]
            },
            {
                "title": "Post-PCI Protocol (ACS - STEMI/NSTEMI/UA)",
                "section_type": "plan",
                "questions": [
                    {"id": "noac_pci_acs_month1", "type": "single_select", "label": "Month 1 Post-PCI (ACS)", "required": False, "options": ["TRIPLE Therapy: NOAC + Clopidogrel 75mg + Aspirin 75mg", "DUAL Therapy: NOAC + Clopidogrel (if high bleeding risk)", "Not applicable"]},
                    {"id": "noac_pci_acs_month2_12", "type": "single_select", "label": "Months 2-12 Post-PCI (ACS)", "required": False, "options": ["DUAL Therapy: NOAC + Clopidogrel 75mg (STOP Aspirin at 1 month)", "Continue Triple (if high ischaemic risk)", "Not applicable"]},
                    {"id": "noac_pci_acs_after12", "type": "single_select", "label": "After 12 Months (ACS)", "required": False, "options": ["NOAC Monotherapy Indefinitely", "NOAC + antiplatelet (if recurrent events)", "Not applicable"]}
                ]
            },
            {
                "title": "Post-PCI Protocol (CCS - Elective/Stable)",
                "section_type": "plan",
                "questions": [
                    {"id": "noac_pci_ccs_month1", "type": "single_select", "label": "Month 1 Post-PCI (CCS)", "required": False, "options": ["TRIPLE Therapy: NOAC + Clopidogrel 75mg + Aspirin 75mg", "DUAL Therapy: NOAC + Clopidogrel (if high bleeding risk)", "Not applicable"]},
                    {"id": "noac_pci_ccs_month2_6", "type": "single_select", "label": "Months 2-6 Post-PCI (CCS)", "required": False, "options": ["DUAL Therapy: NOAC + Clopidogrel 75mg (STOP Aspirin at 1 month)", "Not applicable"]},
                    {"id": "noac_pci_ccs_after6", "type": "single_select", "label": "After 6 Months (CCS)", "required": False, "options": ["NOAC Monotherapy Indefinitely", "Not applicable"]}
                ]
            },
            {
                "title": "P2Y12 Inhibitor & DOAC Dosing",
                "section_type": "plan",
                "questions": [
                    {"id": "noac_p2y12", "type": "single_select", "label": "P2Y12 Inhibitor Choice", "required": False, "options": ["Clopidogrel 75mg OD (preferred for triple/dual)", "Ticagrelor (avoid - high bleed risk unless directed by Cardiology)", "Prasugrel (avoid - high bleed risk unless directed by Cardiology)", "Not applicable"]},
                    {"id": "noac_drug", "type": "single_select", "label": "Current DOAC", "required": False, "options": ["Apixaban 5mg BD", "Apixaban 2.5mg BD (if ≥2: age≥80, wt≤60kg, Cr≥133)", "Edoxaban 60mg OD", "Edoxaban 30mg OD (CrCl 15-50 or wt≤60kg)", "Rivaroxaban 20mg OD with food", "Rivaroxaban 15mg OD (CrCl 15-49)", "Dabigatran 150mg BD", "Dabigatran 110mg BD (age≥80 or on Verapamil)", "Warfarin", "None"]}
                ]
            },
            {
                "title": "Switching Anticoagulants",
                "section_type": "plan",
                "questions": [
                    {"id": "noac_switch_direction", "type": "single_select", "label": "Switching Direction", "required": False, "options": ["NOAC → Warfarin", "Warfarin → NOAC", "Not applicable"]},
                    {"id": "noac_to_warfarin_method", "type": "single_select", "label": "NOAC to Warfarin Method", "required": False, "options": ["Continue NOAC + start Warfarin (no loading dose)", "Overlap 5-10 days until INR ≥2.0 stable", "Check INR immediately before next NOAC dose (trough)", "Recheck INR 24h after stopping NOAC (confirm true INR)", "Not applicable"]},
                    {"id": "noac_warfarin_to_noac", "type": "single_select", "label": "Warfarin to NOAC Method", "required": False, "options": ["Stop Warfarin, start NOAC when INR <2.0", "If INR 2.0-2.5: recheck in 24h or start NOAC next day", "Not applicable"]}
                ]
            },
            {
                "title": "Older People & Falls Risk",
                "section_type": "assessment",
                "questions": [
                    {"id": "noac_age_falls", "type": "toggle", "label": "Age >75 or Falls Risk Concern?", "required": False},
                    {"id": "noac_falls_rule", "type": "toggle", "label": "295 Falls Rule Applied? (CHADS2 2-3 = needs 295 falls/year to outweigh stroke benefit)", "required": False},
                    {"id": "noac_qbleed", "type": "toggle", "label": "QBleed Risk Calculator Used?", "required": False},
                    {"id": "noac_falls_barrier", "type": "toggle", "label": "Age/Falls NOT a Barrier to Anticoagulation? (NICE)", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: NICE states age alone or fear of falls should NOT be a barrier to anticoagulation. Stroke risk outweighs bleed risk in vast majority.", "red_flag_negative": ""}
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
    seed_noac_guide()
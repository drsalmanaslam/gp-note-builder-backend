from app.database import SessionLocal
from app.models import User, Template

def seed_migraine():
    db = SessionLocal()
    admin = db.query(User).filter(User.role == "admin").first()
    if not admin: print("❌ No admin!"); db.close(); return

    title = "Migraine"
    existing = db.query(Template).filter(Template.title == title).first()
    if existing: db.delete(existing); db.commit()

    t = Template(title=title, description="Migraine assessment covering aura, triggers, acute and prophylactic management per NICE CG150, and differentiating from tension headache and cluster headache.", category="Neurology", content={"sections": [
        {"title": "History", "section_type": "history", "questions": [
            {"id": "mig_frequency", "type": "text", "label": "Frequency (per month)", "required": True, "placeholder": "e.g., 4-6 attacks per month"},
            {"id": "mig_duration", "type": "text", "label": "Attack Duration (hours)", "required": True, "placeholder": "e.g., 4-24 hours"},
            {"id": "mig_laterality", "type": "single_select", "label": "Laterality", "required": True, "options": ["Unilateral", "Bilateral", "Alternating sides"]},
            {"id": "mig_character", "type": "single_select", "label": "Pain Character", "required": True, "options": ["Pulsating/throbbing", "Pressing/tightening", "Sharp/stabbing"]},
            {"id": "mig_severity", "type": "single_select", "label": "Severity", "required": True, "options": ["Mild", "Moderate", "Severe - prevents daily activities"]},
            {"id": "mig_aura", "type": "toggle", "label": "Aura Present?", "required": True},
            {"id": "mig_aura_type", "type": "multi_select", "label": "Aura Type", "required": False, "options": ["Visual (flashing lights, zigzag, scotoma)", "Sensory (numbness/tingling)", "Speech (dysphasia)", "Motor (weakness - RED FLAG)"]},
            {"id": "mig_nausea", "type": "toggle", "label": "Nausea / Vomiting?", "required": True},
            {"id": "mig_photophobia", "type": "toggle", "label": "Photophobia?", "required": True},
            {"id": "mig_phonophobia", "type": "toggle", "label": "Phonophobia?", "required": True},
            {"id": "mig_triggers", "type": "multi_select", "label": "Triggers", "required": False, "options": ["Stress", "Hormonal (menstrual)", "Alcohol", "Certain foods", "Dehydration", "Sleep disturbance", "Weather change", "None identified"]},
            {"id": "mig_aura_motor", "type": "toggle", "label": "Motor Weakness During Aura? (Hemiplegic migraine)", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Motor aura = hemiplegic migraine. Contraindication to triptans and COCP. Neurology referral.", "red_flag_negative": ""}
        ]},
        {"title": "Red Flags", "section_type": "history", "questions": [
            {"id": "mig_thunderclap", "type": "toggle", "label": "Thunderclap Onset? (Instant peak)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Thunderclap headache = ?SAH. Emergency CT + LP.", "red_flag_negative": ""},
            {"id": "mig_morning_worse", "type": "toggle", "label": "Worse in Morning / Wakes from Sleep?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Morning headache + vomiting = ?SOL. Urgent imaging.", "red_flag_negative": ""},
            {"id": "mig_postural", "type": "toggle", "label": "Postural (Worse Standing, Better Lying)?", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Postural headache = ?CSF leak / low pressure headache. Neurology referral.", "red_flag_negative": ""},
            {"id": "mig_age_50", "type": "toggle", "label": "New Onset >50 Years?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: New headache >50 = ?GCA, SOL. Check ESR, CRP. Urgent assessment.", "red_flag_negative": ""},
            {"id": "mig_systemic", "type": "toggle", "label": "Systemic Symptoms? (Fever, weight loss, jaw claudication)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Systemic symptoms = ?GCA, meningitis, malignancy. Urgent investigation.", "red_flag_negative": ""}
        ]},
        {"title": "Current & Previous Treatment", "section_type": "history", "questions": [
            {"id": "mig_acute_treatment", "type": "multi_select", "label": "Acute Treatments Tried", "required": True, "options": ["Paracetamol", "NSAID (Ibuprofen, Naproxen)", "Aspirin 900mg", "Triptan (Sumatriptan)", "Anti-emetic (Metoclopramide, Prochlorperazine)", "None"]},
            {"id": "mig_acute_effective", "type": "single_select", "label": "Acute Treatment Effective?", "required": True, "options": ["Yes - good relief", "Partial - some relief", "No - minimal relief", "Not tried"]},
            {"id": "mig_prophylaxis", "type": "multi_select", "label": "Prophylactic Treatments Tried", "required": True, "options": ["Propranolol", "Amitriptyline", "Topiramate", "Candesartan", "Riboflavin / Magnesium", "Acupuncture", "Botox", "CGRP monoclonal antibodies", "None"]},
            {"id": "mig_prophylaxis_effective", "type": "single_select", "label": "Prophylaxis Effective?", "required": False, "options": ["Yes - significant reduction", "Partial", "No benefit", "Not tried"]},
            {"id": "mig_contraindication", "type": "multi_select", "label": "Contraindications", "required": False, "options": ["Pregnancy/breastfeeding", "Cardiovascular disease", "Uncontrolled HTN", "Asthma (avoid beta-blockers)", "None"]}
        ]},
        {"title": "Assessment", "section_type": "assessment", "differentials": ["Migraine without aura", "Migraine with aura", "Chronic migraine (>15 headache days/month, >8 migrainous)", "Tension-type headache", "Cluster headache", "Medication-overuse headache (>15 days/month with regular analgesia/triptan use)", "Hemiplegic migraine", "GCA (age >50, raised ESR)"], "questions": [
            {"id": "mig_diagnosis", "type": "single_select", "label": "Diagnosis", "required": True, "options": ["Migraine without aura", "Migraine with aura", "Chronic migraine", "Tension-type headache", "Medication-overuse headache", "Cluster headache"]},
            {"id": "mig_chronic", "type": "toggle", "label": "Chronic Migraine? (≥15 headache days/month, ≥8 migrainous, >3 months)", "required": True},
            {"id": "mig_medication_overuse", "type": "toggle", "label": "Medication Overuse? (≥10-15 days/month acute treatment)", "required": True}
        ]},
        {"title": "Management", "section_type": "plan", "safety_netting": "Return immediately if: thunderclap headache, headache with fever/stiff neck, new neurological deficit, or change in headache pattern. Acute treatment: oral triptan + NSAID + anti-emetic at onset. Sumatriptan 50-100mg PO (or nasal spray 10-20mg if vomiting). Avoid opioids. Limit acute treatments to ≤2 days/week to prevent medication-overuse headache. Prophylaxis: consider if ≥4 attacks/month or disabling. Propranolol 80-240mg (1st line), Amitriptyline 10-150mg nocte, Topiramate 50-100mg BD (teratogenic - avoid in pregnancy). Candesartan if others CI. Need 3-6 month trial at adequate dose. Refer neurology if: diagnostic uncertainty, chronic migraine, failed ≥3 prophylactics, or hemiplegic migraine.", "questions": [
            {"id": "mig_plan", "type": "multi_select", "label": "Management", "required": True, "options": ["Acute: Triptan + NSAID + anti-emetic", "Start prophylaxis (≥4 attacks/month)", "Increase/change prophylaxis", "Medication-overuse advice (limit acute meds)", "Headache diary", "Lifestyle: sleep, hydration, triggers", "Neurology referral", "CGRP monoclonal antibody (secondary care)"]},
            {"id": "mig_acute_rx", "type": "text", "label": "Acute Prescription", "required": False, "placeholder": "e.g., Sumatriptan 50mg PO PRN + Naproxen 500mg PRN"},
            {"id": "mig_prophylaxis_rx", "type": "text", "label": "Prophylaxis Prescription", "required": False, "placeholder": "e.g., Propranolol 80mg MR OD, titrate to 160mg"},
            {"id": "mig_followup", "type": "text", "label": "Follow-up", "required": True, "placeholder": "e.g., Review in 6 weeks, headache diary, assess prophylaxis response"}
        ]}
    ]}, is_public=True, created_by=admin.id)
    db.add(t); db.commit(); print(f"✅ {title}"); db.close()

if __name__ == "__main__": seed_migraine()
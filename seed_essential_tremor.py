from app.database import SessionLocal
from app.models import User, Template

def seed_essential_tremor():
    db = SessionLocal()
    admin = db.query(User).filter(User.role == "admin").first()
    if not admin: print("❌ No admin!"); db.close(); return

    title = "Essential Tremor"
    existing = db.query(Template).filter(Template.title == title).first()
    if existing: db.delete(existing); db.commit()

    t = Template(title=title, description="Assessment of essential tremor covering differentiation from Parkinson's, functional impact, medication options (propranolol, primidone), and referral criteria per NICE guidance.", category="Neurology", content={"sections": [
        {"title": "Tremor Characteristics", "section_type": "history", "questions": [
            {"id": "et_distribution", "type": "single_select", "label": "Distribution", "required": True, "options": ["Bilateral hands (symmetrical)", "One hand dominant", "Head (titubation)", "Voice", "Hands + head"]},
            {"id": "et_type", "type": "single_select", "label": "Tremor Type", "required": True, "options": ["Action tremor (worse with movement/use)", "Postural tremor (holding position against gravity)", "Rest tremor (tremor at rest) - ?Parkinson's", "Intention tremor (worse approaching target) - ?cerebellar"]},
            {"id": "et_frequency", "type": "single_select", "label": "Frequency", "required": True, "options": ["Fine/fast (8-12Hz) - typical ET", "Slow/coarse (4-6Hz) - ?Parkinson's"]},
            {"id": "et_duration", "type": "text", "label": "Duration", "required": True, "placeholder": "e.g., 3 years, gradually worsening"},
            {"id": "et_progression", "type": "single_select", "label": "Progression", "required": True, "options": ["Stable", "Slowly progressive", "Rapidly progressive - RED FLAG"]},
            {"id": "et_symmetry", "type": "single_select", "label": "Symmetry", "required": True, "options": ["Bilateral/symmetrical (ET)", "Asymmetrical (more one side - ?PD)", "Unilateral"]}
        ]},
        {"title": "Functional Impact", "section_type": "history", "questions": [
            {"id": "et_writing", "type": "toggle", "label": "Difficulty Writing?", "required": True},
            {"id": "et_drinking", "type": "toggle", "label": "Difficulty Drinking from Cup? (Spilling)", "required": True},
            {"id": "et_eating", "type": "toggle", "label": "Difficulty Eating? (Using utensils)", "required": True},
            {"id": "et_dressing", "type": "toggle", "label": "Difficulty with Buttons/Fine Tasks?", "required": True},
            {"id": "et_work_impact", "type": "single_select", "label": "Impact on Work", "required": True, "options": ["None", "Mild inconvenience", "Moderate difficulty", "Unable to work"]},
            {"id": "et_social", "type": "toggle", "label": "Social Embarrassment / Avoidance?", "required": True},
            {"id": "et_alcohol_response", "type": "toggle", "label": "Tremor Improves with Alcohol? (Classic ET feature)", "required": True}
        ]},
        {"title": "Differentiating from Parkinson's Disease", "section_type": "examination", "questions": [
            {"id": "et_bradykinesia", "type": "toggle", "label": "Bradykinesia? (Slowness of movement)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Bradykinesia + tremor = ?Parkinson's disease. Neurology referral.", "red_flag_negative": ""},
            {"id": "et_rigidity", "type": "toggle", "label": "Rigidity? (Cogwheel/lead-pipe)", "required": True},
            {"id": "et_postural_instability", "type": "toggle", "label": "Postural Instability / Falls?", "required": False},
            {"id": "et_facial", "type": "toggle", "label": "Masked Facies / Reduced Blinking?", "required": False},
            {"id": "et_gait", "type": "single_select", "label": "Gait", "required": True, "options": ["Normal", "Shuffling / Festinating (PD)", "Wide-based (cerebellar)", "Other"]},
            {"id": "et_rest_tremor", "type": "toggle", "label": "Rest Tremor Present? (Pill-rolling)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Rest tremor = ?Parkinson's disease. Refer neurology.", "red_flag_negative": ""},
            {"id": "et_voice", "type": "toggle", "label": "Hypophonia? (Quiet/monotone voice - PD)", "required": False},
            {"id": "et_micrographia", "type": "toggle", "label": "Micrographia? (Writing becomes smaller)", "required": False}
        ]},
        {"title": "Other Causes & Red Flags", "section_type": "history", "questions": [
            {"id": "et_medications", "type": "text", "label": "Medications (Beta-agonists, Valproate, Lithium, SSRIs, steroids)", "required": True, "placeholder": "e.g., Salbutamol PRN"},
            {"id": "et_thyroid", "type": "toggle", "label": "Thyroid Symptoms? (Weight loss, sweating, palpitations)", "required": True},
            {"id": "et_caffeine", "type": "single_select", "label": "Caffeine Intake", "required": True, "options": ["None", "1-2/day", "3-5/day", ">5/day"]},
            {"id": "et_alcohol_use", "type": "single_select", "label": "Alcohol", "required": True, "options": ["None", "Within limits", "Excess (withdrawal tremor?)"]},
            {"id": "et_family_history", "type": "toggle", "label": "Family History of Tremor? (50% of ET is familial)", "required": True},
            {"id": "et_wilson", "type": "toggle", "label": "Age <40 + Tremor? (Consider Wilson's disease)", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Tremor <40 = ?Wilson's disease (check ceruloplasmin, LFTs). Neurology referral.", "red_flag_negative": ""}
        ]},
        {"title": "Examination", "section_type": "examination", "questions": [
            {"id": "et_tremor_amplitude", "type": "single_select", "label": "Tremor Amplitude", "required": True, "options": ["Mild - barely visible", "Moderate - clearly visible", "Severe - large amplitude"]},
            {"id": "et_spiral_test", "type": "single_select", "label": "Archimedes Spiral Drawing", "required": False, "options": ["Normal", "Tremulous (ET)", "Micrographia (PD)", "Not done"]},
            {"id": "et_finger_nose", "type": "single_select", "label": "Finger-Nose Test", "required": False, "options": ["Normal", "Intention tremor (cerebellar)", "No past-pointing", "Not done"]},
            {"id": "et_thyroid_exam", "type": "toggle", "label": "Goitre / Thyroid Signs?", "required": False},
            {"id": "et_bloods", "type": "multi_select", "label": "Investigations", "required": False, "options": ["TFTs", "LFTs", "Ceruloplasmin (if <40)", "None - clinical diagnosis"]}
        ]},
        {"title": "Assessment", "section_type": "assessment", "differentials": ["Essential Tremor (bilateral, action/postural, +family history, improves with alcohol)", "Parkinson's Disease (rest tremor, bradykinesia, rigidity, asymmetrical)", "Enhanced Physiological Tremor (stress, caffeine, thyrotoxicosis, medications)", "Cerebellar Tremor (intention tremor, past-pointing, other cerebellar signs)", "Dystonic Tremor", "Drug-Induced Tremor (salbutamol, valproate, lithium, SSRIs)", "Wilson's Disease (<40 years)"], "questions": [
            {"id": "et_diagnosis", "type": "single_select", "label": "Diagnosis", "required": True, "options": ["Essential Tremor - clinical diagnosis", "?Parkinson's Disease - refer neurology", "Enhanced Physiological Tremor - reduce caffeine/stimulants", "Drug-induced tremor - review medication", "?Cerebellar - refer neurology"]},
            {"id": "et_severity", "type": "single_select", "label": "Severity", "required": True, "options": ["Mild - no functional impact, not bothered", "Moderate - functional impact, wants treatment", "Severe - disabling tremor, needs specialist input"]}
        ]},
        {"title": "Management", "section_type": "plan", "safety_netting": "Essential tremor is benign but can be disabling. Treatment is symptomatic - not disease-modifying. Options: 1) Propranolol 80-240mg daily (first-line), 2) Primidone 50-250mg nocte (second-line, sedating), 3) Gabapentin or Topiramate (third-line). Only treat if tremor bothers patient. Use PRN for social situations if needed. Avoid caffeine, stress, fatigue. Occupational therapy for adaptive equipment (weighted utensils, cups). Neurology referral if: diagnostic uncertainty, failed medical therapy, or severe disabling tremor (consider DBS - deep brain stimulation). Return if: new bradykinesia, falls, or rapid progression.", "questions": [
            {"id": "et_plan", "type": "multi_select", "label": "Management", "required": True, "options": ["Reassurance - no treatment needed (mild)", "Reduce caffeine/stimulants", "Propranolol 80mg MR OD (titrate up to 240mg)", "Primidone (if propranolol CI/ineffective)", "OT referral (adaptive equipment)", "Neurology referral (diagnostic uncertainty)", "Neurology referral (severe/refractory - ?DBS)"]},
            {"id": "et_prescription", "type": "text", "label": "Medication", "required": False, "placeholder": "e.g., Propranolol 80mg MR OD, increase to 160mg after 2 weeks"},
            {"id": "et_contraindications", "type": "toggle", "label": "Propranolol CI Checked? (Asthma, heart block, bradycardia)", "required": False},
            {"id": "et_followup", "type": "text", "label": "Follow-up", "required": True, "placeholder": "e.g., Review 4 weeks, assess response, titrate propranolol, refer neurology if no response"}
        ]}
    ]}, is_public=True, created_by=admin.id)
    db.add(t); db.commit(); print(f"✅ {title}"); db.close()

if __name__ == "__main__": seed_essential_tremor()
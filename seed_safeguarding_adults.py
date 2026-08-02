from app.database import SessionLocal
from app.models import User, Template

def seed_safeguarding_adults():
    db = SessionLocal()
    admin = db.query(User).filter(User.role == "admin").first()
    if not admin: print("❌ No admin!"); db.close(); return

    title = "Safeguarding Adults - Section 42 Enquiry"
    existing = db.query(Template).filter(Template.title == title).first()
    if existing: db.delete(existing); db.commit()

    t = Template(title=title, description="Adult safeguarding assessment covering types of abuse, capacity assessment, Section 42 criteria, immediate safety planning, and referral per Care Act 2014.", category="Elderly Care", content={"sections": [
        {"title": "Presenting Concern", "section_type": "history", "questions": [
            {"id": "sg_type", "type": "multi_select", "label": "Type of Abuse Suspected", "required": True, "options": ["Physical abuse", "Emotional/Psychological abuse", "Financial/Material abuse", "Sexual abuse", "Neglect (self-neglect or by others)", "Domestic abuse", "Modern slavery", "Organisational abuse (care home)", "Discriminatory abuse"]},
            {"id": "sg_source", "type": "single_select", "label": "Source of Concern", "required": True, "options": ["Disclosed by patient", "Reported by family/carer", "Reported by neighbour/friend", "Observed by healthcare professional", "Anonymous", "Police referral"]},
            {"id": "sg_immediate_risk", "type": "toggle", "label": "Immediate Risk to Life/Safety?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Immediate risk = call 999. Ensure immediate safety before anything else.", "red_flag_negative": ""},
            {"id": "sg_occurrence", "type": "single_select", "label": "When Did This Occur?", "required": True, "options": ["Today/Active - emergency", "Recent (within days)", "Ongoing (weeks/months)", "Historical"]},
            {"id": "sg_disclosure_detail", "type": "text", "label": "Brief Details of Disclosure/Concern (Use patient's own words)", "required": True, "placeholder": "e.g., Patient states 'my son takes my pension and I have no money for food'"}
        ]},
        {"title": "Patient Assessment", "section_type": "examination", "questions": [
            {"id": "sg_capacity", "type": "single_select", "label": "Mental Capacity (Regarding This Decision)", "required": True, "options": ["Has capacity", "Lacks capacity", "Fluctuating capacity", "Not assessed"]},
            {"id": "sg_communication", "type": "single_select", "label": "Communication", "required": True, "options": ["Can communicate clearly", "Communication difficulties (language, speech, cognitive)", "Unable to communicate", "Advocate/IMCA needed"]},
            {"id": "sg_physical_signs", "type": "multi_select", "label": "Physical Signs", "required": False, "options": ["Unexplained bruises/injuries", "Pattern injuries (grab marks, slap marks)", "Poor hygiene/malnourishment", "Pressure sores", "Unexplained weight loss", "Over-sedation", "None evident"]},
            {"id": "sg_emotional_state", "type": "single_select", "label": "Emotional/Psychological State", "required": True, "options": ["Calm", "Anxious/fearful", "Agitated", "Withdrawn", "Tearful", "Flat/emotionless"]}
        ]},
        {"title": "Risk Factors & Context", "section_type": "history", "questions": [
            {"id": "sg_living_situation", "type": "single_select", "label": "Living Situation", "required": True, "options": ["Alone", "With family", "Care home", "Sheltered accommodation", "Homeless"]},
            {"id": "sg_carer_dependency", "type": "toggle", "label": "Dependent on Alleged Perpetrator for Care?", "required": True},
            {"id": "sg_carer_stress", "type": "toggle", "label": "Carer Stress/Burnout Evident?", "required": False},
            {"id": "sg_social_isolation", "type": "toggle", "label": "Social Isolation?", "required": True},
            {"id": "sg_previous_concerns", "type": "toggle", "label": "Previous Safeguarding Concerns?", "required": True},
            {"id": "sg_domestic_abuse_routine", "type": "toggle", "label": "Domestic Abuse Routine Enquiry", "required": True}
        ]},
        {"title": "Section 42 Criteria (Care Act 2014)", "section_type": "assessment", "questions": [
            {"id": "sg_s42_criteria", "type": "single_select", "label": "Do All Three S42 Criteria Apply?", "required": True, "options": ["YES: 1) Adult with care/support needs, 2) Experiencing/at risk of abuse/neglect, 3) Unable to protect themselves", "NO: Does not meet all 3 criteria", "Uncertain - needs further assessment"]},
            {"id": "sg_adult_at_risk", "type": "toggle", "label": "Confirmed: Adult with Care & Support Needs?", "required": True},
            {"id": "sg_abuse_neglect", "type": "toggle", "label": "Confirmed: Experiencing or At Risk of Abuse/Neglect?", "required": True},
            {"id": "sg_unable_protect", "type": "toggle", "label": "Confirmed: Unable to Protect Themselves?", "required": True}
        ]},
        {"title": "Immediate Actions", "section_type": "plan", "safety_netting": "Safeguarding is everyone's responsibility. If immediate risk to life: call 999. Preserve evidence: do not wash patient, keep clothing, document injuries (body map + photographs with consent). Do NOT confront alleged perpetrator - this could increase risk. Do NOT contact alleged perpetrator before speaking with safeguarding team. Document ALL concerns objectively using patient's own words where possible. Inform senior colleague/GP partner. Contact adult safeguarding team (Local Authority) to make Section 42 referral same day. If patient has capacity and refuses intervention: respect their decision but document thoroughly and consider if others at risk. Out of hours: contact Emergency Duty Team.", "questions": [
            {"id": "sg_999", "type": "toggle", "label": "999 Called? (Immediate risk)", "required": False},
            {"id": "sg_s42_referral", "type": "toggle", "label": "Section 42 Safeguarding Referral Made?", "required": True},
            {"id": "sg_police", "type": "toggle", "label": "Police Involved? (Criminal offence)", "required": False},
            {"id": "sg_safety_plan", "type": "text", "label": "Immediate Safety Plan", "required": True, "placeholder": "e.g., Patient staying with daughter tonight, care home informed, police attending"},
            {"id": "sg_documentation", "type": "toggle", "label": "Body Map / Photographs / Detailed Notes?", "required": True},
            {"id": "sg_senior_informed", "type": "toggle", "label": "Senior Colleague / GP Partner Informed?", "required": True},
            {"id": "sg_followup", "type": "text", "label": "Follow-up & Monitoring", "required": True, "placeholder": "e.g., Check safeguarding team received referral, safety check in 24h, GP review in 1 week"}
        ]}
    ]}, is_public=True, created_by=admin.id)
    db.add(t); db.commit(); print(f"✅ {title}"); db.close()

if __name__ == "__main__": seed_safeguarding_adults()
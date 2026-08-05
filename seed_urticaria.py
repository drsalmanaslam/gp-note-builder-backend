from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone


def seed_urticaria():
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
        "title": "Urticaria (Hives)",
        "description": "Assessment of acute and chronic urticaria. Covers triggers, red flags for anaphylaxis/angioedema, classification, and stepped management from antihistamines to immunology referral.",
        "category": "Dermatology",
        "content": {
            "sections": [
                {
                    "title": "History",
                    "section_type": "history",
                    "questions": [
                        {
                            "id": "urt_duration",
                            "type": "single_select",
                            "label": "Duration",
                            "required": True,
                            "options": [
                                "<24 hours — acute",
                                "1-6 weeks",
                                ">6 weeks (chronic urticaria)",
                                "Recurrent episodes over months/years"
                            ],
                            "output_phrase": "Duration: {value}"
                        },
                        {
                            "id": "urt_wheal_duration",
                            "type": "single_select",
                            "label": "Individual Wheal Duration (before fading)",
                            "required": True,
                            "options": [
                                "<24 hours (typical urticaria)",
                                ">24 hours (?urticarial vasculitis)",
                                "Minutes only (?physical urticaria)"
                            ],
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Individual wheals lasting >24h + bruising/residual marks = ?urticarial vasculitis. Refer dermatology/immunology.",
                            "red_flag_negative": "",
                            "output_phrase": "Wheal duration: {value}"
                        },
                        {
                            "id": "urt_itch",
                            "type": "toggle",
                            "label": "Pruritus? (usually intense)",
                            "required": True,
                            "output_phrase": "Itch: {value}"
                        }
                    ]
                },
                {
                    "title": "Triggers & Type",
                    "section_type": "history",
                    "questions": [
                        {
                            "id": "urt_triggers",
                            "type": "multi_select",
                            "label": "Suspected Triggers",
                            "required": True,
                            "options": [
                                "Foods (shellfish, nuts, eggs, strawberries)",
                                "Medications (NSAIDs, aspirin, antibiotics, opiates)",
                                "Insect bites / stings",
                                "Infections (viral URI, H.pylori, dental abscess)",
                                "Physical triggers (pressure, cold, heat, sunlight, exercise)",
                                "Stress",
                                "Alcohol",
                                "Latex",
                                "Unknown / idiopathic"
                            ],
                            "output_phrase": "Triggers: {value}"
                        },
                        {
                            "id": "urt_physical",
                            "type": "single_select",
                            "label": "Physical Urticaria Type? (if triggered by physical stimuli)",
                            "required": False,
                            "options": [
                                "Dermatographism — stroking/scratching skin",
                                "Pressure — delayed (tight clothing, sitting)",
                                "Cold — cold air/water",
                                "Cholinergic — heat, exercise, sweating",
                                "Solar — sunlight",
                                "Aquagenic — water",
                                "Not physical"
                            ],
                            "output_phrase": "Physical type: {value}"
                        }
                    ]
                },
                {
                    "title": "Red Flags — Anaphylaxis / Angioedema",
                    "section_type": "history",
                    "questions": [
                        {
                            "id": "urt_angioedema",
                            "type": "toggle",
                            "label": "Angioedema? (swelling of lips, eyelids, tongue, hands, genitals)",
                            "required": True,
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Angioedema with tongue/throat involvement = risk of airway compromise. Emergency admission. If recurrent without urticaria = ?hereditary/ACE-I induced angioedema.",
                            "red_flag_negative": "",
                            "output_phrase": "Angioedema: {value}"
                        },
                        {
                            "id": "urt_anaphylaxis",
                            "type": "toggle",
                            "label": "Breathing Difficulty / Wheeze / Dizziness / Collapse? (?anaphylaxis)",
                            "required": True,
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Respiratory or cardiovascular involvement = anaphylaxis. Call 999. IM Adrenaline 0.5mg STAT. Do not delay.",
                            "red_flag_negative": "",
                            "output_phrase": "Anaphylaxis: {value}"
                        },
                        {
                            "id": "urt_acei",
                            "type": "toggle",
                            "label": "On ACE Inhibitor? (?drug-induced angioedema — can occur years after starting)",
                            "required": False,
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: ACE-I angioedema can occur at any time. Stop ACE-I immediately. Switch to ARB with caution. Refer allergy clinic.",
                            "red_flag_negative": "",
                            "output_phrase": "ACE-I: {value}"
                        }
                    ]
                },
                {
                    "title": "Assessment",
                    "section_type": "assessment",
                    "differentials": [
                        "Acute Urticaria (<6 weeks) — infection, food, drug, insect bite",
                        "Chronic Spontaneous Urticaria (>6 weeks, no trigger) — autoimmune in 40%",
                        "Physical Urticaria — dermatographism, pressure, cold, cholinergic, solar",
                        "Urticarial Vasculitis — wheals >24h, painful/burning, residual purpura",
                        "Angioedema — with or without urticaria",
                        "Anaphylaxis — respiratory/cardiovascular involvement",
                        "Erythema Multiforme — target lesions, not itchy wheals",
                        "Bullous Pemphigoid — early urticarial phase before blistering"
                    ],
                    "questions": [
                        {
                            "id": "urt_diagnosis",
                            "type": "single_select",
                            "label": "Diagnosis",
                            "required": True,
                            "options": [
                                "Acute Urticaria — treat + avoid trigger",
                                "Chronic Spontaneous Urticaria — stepped antihistamines",
                                "Physical Urticaria — antihistamines + avoid stimulus",
                                "?Urticarial Vasculitis — refer dermatology",
                                "Angioedema without urticaria — ?ACE-I / hereditary / idiopathic",
                                "Anaphylaxis — emergency management"
                            ],
                            "output_phrase": "Diagnosis: {value}"
                        }
                    ]
                },
                {
                    "title": "Management Plan",
                    "section_type": "plan",
                    "safety_netting": "ACUTE: Identify and avoid trigger. Non-sedating antihistamine: Cetirizine 10mg OD or Loratadine 10mg OD or Fexofenadine 180mg OD. CHRONIC (>6 weeks): Step 1 — standard dose non-sedating antihistamine. Step 2 — up to 4x standard dose (off-label but BAD/NICE recommended, e.g., Fexofenadine 180mg QDS). Step 3 — add Montelukast 10mg or H2 antagonist (Ranitidine withdrawn — use Famotidine if available). Step 4 — refer immunology/dermatology for Omalizumab (anti-IgE) or Ciclosporin. If angioedema without urticaria: Check C4, C1 esterase inhibitor if hereditary angioedema suspected. STOP ACE-I if relevant. Safety-net: Return immediately if tongue/lip swelling, breathing difficulty, or wheeze. If on high-dose antihistamines, advise drowsiness risk.",
                    "questions": [
                        {
                            "id": "urt_treatment",
                            "type": "single_select",
                            "label": "Treatment",
                            "required": True,
                            "options": [
                                "Standard-dose non-sedating antihistamine",
                                "Up-dosed antihistamine (2-4x standard)",
                                "Antihistamine + Montelukast / H2 blocker",
                                "Refer immunology/dermatology (omalizumab)",
                                "Emergency — adrenaline + 999 (anaphylaxis)",
                                "Avoid trigger only (resolved)"
                            ],
                            "output_phrase": "Treatment: {value}"
                        },
                        {
                            "id": "urt_antihistamine",
                            "type": "text",
                            "label": "Antihistamine Prescribed + Dose",
                            "required": True,
                            "placeholder": "e.g., Fexofenadine 180mg OD — up to QDS if needed",
                            "output_phrase": "Antihistamine: {value}"
                        },
                        {
                            "id": "urt_safety_net",
                            "type": "toggle",
                            "label": "Safety-Net Given? (return if angioedema / breathing difficulty)",
                            "required": True,
                            "output_phrase": "Safety-net: {value}"
                        },
                        {
                            "id": "urt_followup",
                            "type": "text",
                            "label": "Follow-up Plan",
                            "required": True,
                            "placeholder": "e.g., Review in 4 weeks. If no response, up-titrate antihistamine. If chronic >6 months, refer immunology.",
                            "output_phrase": "Follow-up: {value}"
                        }
                    ]
                }
            ]
        },
        "is_public": True
    }

    existing = db.query(Template).filter(
        Template.title == t["title"],
        Template.created_by == admin.id
    ).first()

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
    seed_urticaria()
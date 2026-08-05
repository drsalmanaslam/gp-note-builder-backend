from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone


def seed_alopecia():
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
        "title": "Alopecia (Hair Loss)",
        "description": "Assessment of hair loss. Covers common types (alopecia areata, androgenetic, telogen effluvium), red flags for scarring alopecia, investigations, and management options.",
        "category": "Dermatology",
        "content": {
            "sections": [
                {
                    "title": "History",
                    "section_type": "history",
                    "questions": [
                        {
                            "id": "alop_pattern",
                            "type": "single_select",
                            "label": "Pattern of Hair Loss",
                            "required": True,
                            "options": [
                                "Patchy — discrete bald patches (alopecia areata)",
                                "Diffuse thinning — all over scalp",
                                "Frontal / bitemporal recession (male pattern)",
                                "Central / vertex thinning (male or female pattern)",
                                "Sudden shedding — handfuls of hair (telogen effluvium)",
                                "Scarring / permanent looking areas"
                            ],
                            "output_phrase": "Pattern: {value}"
                        },
                        {
                            "id": "alop_duration",
                            "type": "text",
                            "label": "Duration",
                            "required": True,
                            "placeholder": "e.g., 3 months",
                            "output_phrase": "Duration: {value}"
                        },
                        {
                            "id": "alop_triggers",
                            "type": "multi_select",
                            "label": "Potential Triggers (last 3 months)",
                            "required": False,
                            "options": [
                                "Severe illness / fever / COVID",
                                "Surgery / general anaesthetic",
                                "Childbirth",
                                "Severe stress / bereavement",
                                "Rapid weight loss / crash diet",
                                "New medications",
                                "Iron deficiency",
                                "Thyroid disorder",
                                "None"
                            ],
                            "output_phrase": "Triggers: {value}"
                        }
                    ]
                },
                {
                    "title": "Red Flags — Scarring Alopecia & Systemic Disease",
                    "section_type": "history",
                    "questions": [
                        {
                            "id": "alop_scarring",
                            "type": "toggle",
                            "label": "Scalp Inflammation? (redness, scaling, pustules, scarring, permanent loss)",
                            "required": True,
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Inflammation/scarring = ?scarring alopecia (lichen planopilaris, discoid lupus, folliculitis decalvans). Urgent dermatology referral — hair loss may be permanent.",
                            "red_flag_negative": "",
                            "output_phrase": "Scalp inflammation: {value}"
                        },
                        {
                            "id": "alop_other_autoimmune",
                            "type": "multi_select",
                            "label": "Other Autoimmune Conditions?",
                            "required": False,
                            "options": [
                                "Thyroid disease",
                                "Vitiligo",
                                "Type 1 diabetes",
                                "Pernicious anaemia",
                                "Lupus",
                                "None"
                            ],
                            "output_phrase": "Autoimmune: {value}"
                        },
                        {
                            "id": "alop_eyebrows_lashes",
                            "type": "toggle",
                            "label": "Eyebrow / Eyelash / Body Hair Loss?",
                            "required": True,
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Total body hair loss = alopecia universalis or systemic disease. Refer dermatology.",
                            "red_flag_negative": "",
                            "output_phrase": "Body hair loss: {value}"
                        }
                    ]
                },
                {
                    "title": "Examination",
                    "section_type": "examination",
                    "questions": [
                        {
                            "id": "alop_exclamation",
                            "type": "toggle",
                            "label": "Exclamation Mark Hairs? (short broken hairs at margin — alopecia areata)",
                            "required": False,
                            "output_phrase": "Exclamation hairs: {value}"
                        },
                        {
                            "id": "alop_hair_pull",
                            "type": "single_select",
                            "label": "Hair Pull Test (active shedding if >5 hairs easily pulled)",
                            "required": False,
                            "options": [
                                "Positive — >5 hairs easily pulled",
                                "Negative",
                                "Not tested"
                            ],
                            "output_phrase": "Hair pull test: {value}"
                        },
                        {
                            "id": "alop_nails",
                            "type": "toggle",
                            "label": "Nail Pitting / Ridging? (alopecia areata association)",
                            "required": False,
                            "output_phrase": "Nail changes: {value}"
                        }
                    ]
                },
                {
                    "title": "Assessment",
                    "section_type": "assessment",
                    "differentials": [
                        "Alopecia Areata — patchy, autoimmune, exclamation hairs",
                        "Androgenetic Alopecia — male/female pattern, gradual, family history",
                        "Telogen Effluvium — diffuse shedding 2-3 months after trigger",
                        "Scarring Alopecia — inflammation, permanent loss, urgent derm referral",
                        "Tinea Capitis — scaly patches, broken hairs, lymphadenopathy (children)",
                        "Iron Deficiency / Hypothyroidism — diffuse thinning, correctable",
                        "Drug-Induced — chemotherapy, retinoids, anticoagulants, antiepileptics"
                    ],
                    "questions": [
                        {
                            "id": "alop_diagnosis",
                            "type": "single_select",
                            "label": "Diagnosis",
                            "required": True,
                            "options": [
                                "Alopecia Areata",
                                "Androgenetic Alopecia (male/female pattern)",
                                "Telogen Effluvium",
                                "?Scarring Alopecia — refer dermatology",
                                "Mixed / other"
                            ],
                            "output_phrase": "Diagnosis: {value}"
                        }
                    ]
                },
                {
                    "title": "Management Plan",
                    "section_type": "plan",
                    "safety_netting": "Investigations: FBC, ferritin, TFTs, B12, folate. ANA if ?lupus. ALOPECIA AREATA: Reassure — spontaneous regrowth in 50% within 1 year. Topical corticosteroid (Betamethasone valerate 0.1% scalp application) for localised patches. Refer dermatology if: extensive, rapid progression, alopecia totalis/universalis, or failed topical treatment. ANDROGENETIC: Male — topical Minoxidil 5% foam/spray BD. Finasteride 1mg OD (caution: sexual side effects, not for women of childbearing age). Female — topical Minoxidil 2% BD. Refer if severe or not responding. TELOGEN EFFLUVIUM: Reassure — resolves within 3-6 months once trigger removed. Correct iron deficiency if present. SCARRING: Urgent dermatology referral. Safety-net: Return if spreading, scalp inflammation, or systemic symptoms develop.",
                    "questions": [
                        {
                            "id": "alop_treatment",
                            "type": "single_select",
                            "label": "Treatment",
                            "required": True,
                            "options": [
                                "Reassurance + watchful waiting (likely self-resolving)",
                                "Topical corticosteroid (alopecia areata)",
                                "Topical Minoxidil (androgenetic)",
                                "Minoxidil + Finasteride (male androgenetic)",
                                "Treat underlying cause (iron/thyroid)",
                                "Refer dermatology"
                            ],
                            "output_phrase": "Treatment: {value}"
                        },
                        {
                            "id": "alop_investigations",
                            "type": "text",
                            "label": "Investigations Ordered",
                            "required": False,
                            "placeholder": "e.g., FBC, ferritin, TFTs",
                            "output_phrase": "Investigations: {value}"
                        },
                        {
                            "id": "alop_safety_net",
                            "type": "toggle",
                            "label": "Safety-Net Given? (return if spreading / scalp inflammation / systemic symptoms)",
                            "required": True,
                            "output_phrase": "Safety-net: {value}"
                        },
                        {
                            "id": "alop_followup",
                            "type": "text",
                            "label": "Follow-up Plan",
                            "required": True,
                            "placeholder": "e.g., Review in 3 months. Bloods in meantime. Refer if no regrowth.",
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
    seed_alopecia()
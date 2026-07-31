from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_acne():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Dermatology").first()
    if not category: category = Category(name="Dermatology"); db.add(category); db.commit()

    t = {
        "title": "Acne Vulgaris",
        "description": "Comprehensive acne assessment covering severity grading, lesion-specific treatment (ABCs), oral therapy options, COCP/spironolactone, and isotretinoin referral criteria.",
        "category": "Dermatology",
        "content": {"sections": [
            {
                "title": "History & Pattern",
                "section_type": "history",
                "questions": [
                    {"id": "acne_presenting_complaint", "type": "text", "label": "Presenting Complaint", "required": True, "placeholder": "e.g., Persistent acne on face and back for 6 months"},
                    {"id": "acne_age", "type": "number", "label": "Age", "required": True, "placeholder": "e.g., 22"},
                    {"id": "acne_onset", "type": "text", "label": "Onset / Duration", "required": True, "placeholder": "e.g., 6 months"},
                    {"id": "acne_distribution", "type": "multi_select", "label": "Distribution", "required": True, "options": ["Face", "Jawline / Chin (Hormonal Pattern)", "Chest", "Back", "Shoulders"]},
                    {"id": "acne_lesion_type", "type": "multi_select", "label": "Lesion Types Present", "required": True, "options": ["Comedones (Blackheads/Whiteheads)", "Papules / Pustules", "Nodules / Cysts", "Scarring Present"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Nodulocystic disease or scarring = fast-track isotretinoin referral. Treat aggressively.", "red_flag_negative": ""},
                    {"id": "acne_hormonal", "type": "toggle", "label": "Flares with Menstrual Cycle? (Hormonal Pattern)", "required": False},
                    {"id": "acne_severity", "type": "single_select", "label": "Severity", "required": True, "options": ["Mild (Comedonal / Few Papules)", "Mild-Moderate (Retinoid Stage)", "Moderate-Severe (Inflammatory, Nodules)", "Severe (Significant Scarring, Conglobate)"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Severe/scarring = refer for isotretinoin. Do not delay.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Triggers & Previous Treatments",
                "section_type": "history",
                "questions": [
                    {"id": "acne_skincare", "type": "toggle", "label": "Using Oil-Based / Heavy Makeup? (Acne Cosmetica)", "required": False},
                    {"id": "acne_previous_rx", "type": "multi_select", "label": "Previous Treatments Tried", "required": True, "options": ["Benzoyl Peroxide (BPO)", "Salicylic Acid", "Topical Retinoid (Adapalene/Tretinoin)", "Topical Antibiotic (Clindamycin/Erythromycin)", "Oral Antibiotic (Lymecycline/Doxycycline)", "COCP (Dianette/Yasmin)", "Spironolactone", "Isotretinoin (Roaccutane)", "None"]},
                    {"id": "acne_antibiotic_history", "type": "text", "label": "Antibiotic Exposure History (Duration, Mono vs Combination)", "required": False, "placeholder": "e.g., Lymecycline 3 months + BPO"},
                    {"id": "acne_contraception", "type": "single_select", "label": "Contraception / Pregnancy Plans", "required": True, "options": ["On COCP", "Not on contraception", "Planning pregnancy - RED FLAG", "Pregnant - RED FLAG", "Not applicable (male)"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Pregnancy/planning = AVOID retinoids, spironolactone, tetracyclines. Safe: Erythromycin, BPO, Azelaic Acid.", "red_flag_negative": ""},
                    {"id": "acne_fitzpatrick", "type": "single_select", "label": "Skin Type / Fitzpatrick (PIH Risk)", "required": False, "options": ["Type I-II (Fair - Low PIH Risk)", "Type III-IV (Olive/Medium - Moderate PIH Risk)", "Type V-VI (Dark - HIGH PIH Risk)"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Skin of colour = higher PIH risk. Intervene early and more aggressively.", "red_flag_negative": ""},
                    {"id": "acne_psychological", "type": "toggle", "label": "Significant Psychological Impact / Distress?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Psychological impact = lower threshold for isotretinoin referral.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "acne_face_lesions", "type": "multi_select", "label": "Facial Lesions", "required": True, "options": ["Open Comedones (Blackheads)", "Closed Comedones (Whiteheads)", "Papules", "Pustules", "Nodules", "Cysts", "Scarring (Atrophic/Hypertrophic)", "Post-Inflammatory Hyperpigmentation (PIH)"]},
                    {"id": "acne_trunk", "type": "toggle", "label": "Trunk Involvement? (Chest/Back)", "required": False},
                    {"id": "acne_scarring_severity", "type": "single_select", "label": "Scarring Risk Assessment", "required": True, "options": ["No Scarring", "Mild Scarring", "Moderate Scarring - Aggressive Treatment", "Severe Scarring - Fast-Track Isotretinoin"]}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "Acne Vulgaris (Comedonal / Papulopustular / Nodulocystic)",
                    "Hormonal Acne (Jawline/Chin, Menstrual Flares)",
                    "Acne Cosmetica (Product-Induced)",
                    "Acne Excoriée (Picking/Squeezing)",
                    "Rosacea (No Comedones, Flushing, Telangiectasia)",
                    "Perioral Dermatitis",
                    "Folliculitis (Gram-Negative / Pityrosporum)",
                    "Drug-Induced Acne (Steroids, Lithium, Isoniazid)"
                ],
                "questions": [
                    {"id": "acne_diagnosis", "type": "single_select", "label": "Clinical Impression", "required": True, "options": ["Acne Vulgaris - Mild (Comedonal)", "Acne Vulgaris - Mild-Moderate", "Acne Vulgaris - Moderate-Severe", "Acne Vulgaris - Severe (Nodulocystic/Scarring) - REFER", "Hormonal Acne", "Acne Cosmetica"]}
                ]
            },
            {
                "title": "Management Plan - Topical (ABCs)",
                "section_type": "plan",
                "safety_netting": "General principles: Avoid squeezing/picking; avoid oil-based/heavy makeup. Synergistic skincare: gentle cleanser, moisturiser, niacinamide, SPF50 sunscreen - used alongside prescribed treatment. 'Gentle is ALWAYS the way' - improvement takes time. Barrier support during retinoid irritation: switch to highly emollient, fragrance-free line. Sunscreen: UVA→SCC/BCC, UVB→melanoma, UVA+UVB+Visible Light→PIH. Mineral vs chemical (advise SPF50). Antibiotics: short-term only (≤3 months), NEVER as monotherapy. If required >3 months → isotretinoin instead. Pregnancy: AVOID retinoids, spironolactone, tetracyclines. Safe: Erythromycin, BPO, Azelaic Acid.",
                "questions": [
                    {"id": "acne_topical", "type": "single_select", "label": "Topical Treatment (ABCs)", "required": False, "options": ["Benzoyl Peroxide (BPO) 2.5-10% - Wash or Gel", "Adapalene 0.1% (Retinoid - Nightly, Gradual Induction)", "Clindamycin 1% + BPO Combination (Duac)", "Azelaic Acid 15-20% (Pregnancy-Safe)", "Salicylic Acid 2%", "Tretinoin 0.025% (Retinoid)", "None"]},
                    {"id": "acne_topical_instructions", "type": "text", "label": "Topical Instructions", "required": False, "placeholder": "e.g., Adapalene: pea-sized amount at night, face only, start every other night. Moisturiser-moisturiser technique."},
                    {"id": "acne_skincare_advice", "type": "multi_select", "label": "Skincare Advice", "required": False, "options": ["Gentle cleanser (fragrance-free)", "Light moisturiser", "Niacinamide (PIH prevention)", "SPF50 Sunscreen Daily", "Avoid oil-based products"]}
                ]
            },
            {
                "title": "Management Plan - Oral Therapy",
                "section_type": "plan",
                "questions": [
                    {"id": "acne_oral_antibiotic", "type": "single_select", "label": "Oral Antibiotic (≤3 Months, Always with Topical, Never Monotherapy)", "required": False, "options": ["Lymecycline 408mg OD", "Doxycycline 100mg OD", "Erythromycin (Pregnancy-Safe Alternative)", "Not indicated"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Antibiotics ≤3 months MAX. Always combine with topical. If >3 months needed → isotretinoin.", "red_flag_negative": ""},
                    {"id": "acne_cocp", "type": "single_select", "label": "COCP (Hormonal / Jawline/Chin Pattern)", "required": False, "options": ["Dianette (Cyproterone 2mg + EE 35mcg)", "Yasmin (Drospirenone 3mg + EE 30mcg)", "Not indicated / Not applicable"], "is_red_flag": True, "red_flag_positive": "RED FLAG: 3rd/4th generation anti-androgenic progestins preferred for acne.", "red_flag_negative": ""},
                    {"id": "acne_spironolactone", "type": "single_select", "label": "Spironolactone (Alternative to COCP)", "required": False, "options": ["25mg OD (Start) → 50mg OD → 100mg OD (Titrate Over 3 Months)", "Not indicated"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Spironolactone = TERATOGENIC. Ensure effective contraception.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Referral & Follow-Up",
                "section_type": "plan",
                "questions": [
                    {"id": "acne_isotretinoin_referral", "type": "toggle", "label": "Refer for Isotretinoin? (Nodular/Conglobate / Significant Scarring / Failed Antibiotics ≤3 Months / Scarring-Prone / Skin of Colour)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Fast-track isotretinoin referral if: nodulocystic, conglobate, risk of permanent scarring, skin of colour with scarring.", "red_flag_negative": ""},
                    {"id": "acne_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., 6-8 weeks for topical review, 3 months if oral antibiotics, sooner if worsening"}
                ]
            }
        ]},
        "is_public": True
    }

    existing = db.query(Template).filter(Template.title == t["title"], Template.created_by == admin.id).first()
    
    if existing:
        # Update existing template instead of deleting
        existing.description = t["description"]
        existing.content = t["content"]
        existing.category = t["category"]
        existing.is_public = t["is_public"]
        existing.updated_at = datetime.now(timezone.utc)
        db.commit()
        print(f"🔄 Updated: {t['title']}")
    new_t = Template(title=t["title"], description=t["description"], category=t["category"], content=t["content"], is_public=True, created_by=admin.id, version=1)
    db.add(new_t); db.commit()
    print(f"Template '{t['title']}' created with {len(t['content']['sections'])} sections!"); db.close()

if __name__ == "__main__":
    seed_acne()
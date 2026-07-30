from app.database import SessionLocal
from app.models import User, Template, Category

def seed_ganglion_cyst():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Musculoskeletal").first()
    if not category: category = Category(name="Musculoskeletal"); db.add(category); db.commit()

    t = {
        "title": "Ganglion Cyst",
        "description": "Focused assessment for ganglion cysts covering classic locations, watchful waiting vs intervention criteria, and referral for aspiration or excision.",
        "category": "Musculoskeletal",
        "content": {"sections": [
            {
                "title": "History",
                "section_type": "history",
                "questions": [
                    {"id": "gc_presenting_complaint", "type": "text", "label": "Presenting Complaint", "required": True, "placeholder": "e.g., Lump on dorsal wrist for 3 months"},
                    {"id": "gc_location", "type": "single_select", "label": "Location", "required": True, "options": ["Dorsal Wrist (Most Common)", "Volar Wrist", "Flexor Tendon Sheath (Finger)", "Foot / Ankle", "Other"]},
                    {"id": "gc_duration", "type": "text", "label": "Duration", "required": True, "placeholder": "e.g., 3 months"},
                    {"id": "gc_pain", "type": "toggle", "label": "Pain?", "required": True},
                    {"id": "gc_restriction", "type": "toggle", "label": "Restriction of Movement?", "required": False},
                    {"id": "gc_size_category", "type": "single_select", "label": "Size", "required": True, "options": ["Small (<2cm)", "Large (≥2cm)"]},
                    {"id": "gc_change_size", "type": "single_select", "label": "Change in Size", "required": False, "options": ["Fluctuates (Ganglion Typical)", "Stable", "Increasing"]}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "gc_location_confirmed", "type": "single_select", "label": "Location Confirmed", "required": True, "options": ["Dorsal Wrist", "Volar Wrist", "Flexor Tendon Sheath", "Foot / Ankle", "Other"]},
                    {"id": "gc_consistency", "type": "single_select", "label": "Consistency", "required": True, "options": ["Firm / Rubbery (Ganglion Typical)", "Soft / Fluctuant", "Hard / Bony"]},
                    {"id": "gc_transillumination", "type": "toggle", "label": "Transilluminates? (Ganglion Typical)", "required": False},
                    {"id": "gc_fixed", "type": "toggle", "label": "Fixed to Underlying Structures? (RED FLAG if Yes)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Fixed to deep tissue = ?sarcoma, not ganglion. Urgent orthopaedic referral.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "Ganglion Cyst (Firm, Rubbery, Transilluminates, Dorsal Wrist - Most Common)",
                    "Lipoma (Soft, Mobile, No Transillumination)",
                    "Epidermoid Cyst (Central Punctum)",
                    "Giant Cell Tumour of Tendon Sheath (Firm, Fixed to Tendon)",
                    "Sarcoma (Fixed, Hard, Growing - RED FLAG)",
                    "Carpal Boss (Bony, Fixed)",
                    "Trigger Finger (Nodule on Flexor Tendon)"
                ],
                "questions": [
                    {"id": "gc_diagnosis", "type": "single_select", "label": "Clinical Impression", "required": True, "options": ["Ganglion Cyst - Typical (Dorsal Wrist)", "Ganglion Cyst - Other Site", "Diagnostic Uncertainty - Refer", "Suspected Malignancy - Urgent Referral"]}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Return if: lump increases in size, becomes painful, restricts movement, or changes character. Ganglion cysts are benign synovial outpouchings containing viscous fluid. They may fluctuate in size and can resolve spontaneously. Small asymptomatic: watchful waiting - no treatment required. Traditional dispersal with firm digital pressure (bursting the cyst) is an option but has high recurrence rate. Symptomatic, large, or patient requests treatment: refer orthopaedics or plastic surgery for aspiration (high recurrence ~50%) or surgical excision (lower recurrence ~10%). If fixed to deep tissue or diagnostic uncertainty: urgent orthopaedic referral for imaging ± biopsy.",
                "questions": [
                    {"id": "gc_plan", "type": "single_select", "label": "Management", "required": True, "options": ["Watchful Waiting - No Treatment (Small, Asymptomatic)", "Dispersal with Firm Digital Pressure", "Refer Orthopaedics / Plastics - Aspiration", "Refer Orthopaedics / Plastics - Surgical Excision", "Urgent Orthopaedic Referral (?Malignancy)"]},
                    {"id": "gc_reassurance", "type": "toggle", "label": "Benign Nature Explained? (May Fluctuate, Can Resolve Spontaneously)", "required": False},
                    {"id": "gc_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., PRN if symptomatic, await orthopaedic OPD, or self-discharge"}
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
    seed_ganglion_cyst()
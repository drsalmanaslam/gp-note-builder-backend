from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_insomnia():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Mental Health").first()
    if not category: category = Category(name="Mental Health"); db.add(category); db.commit()

    t = {
        "title": "Insomnia / Sleep Disturbance",
        "description": "Focused insomnia assessment covering sleep hygiene, CBT-I, underlying causes (anxiety, depression, OSA), and short-term medication options.",
        "category": "Mental Health",
        "content": {"sections": [
            {
                "title": "History",
                "section_type": "history",
                "questions": [
                    {"id": "ins_presenting_complaint", "type": "text", "label": "Presenting Complaint", "required": True, "placeholder": "e.g., Difficulty falling asleep and staying asleep for 2 months"},
                    {"id": "ins_duration", "type": "text", "label": "Duration", "required": True, "placeholder": "e.g., 2 months"},
                    {"id": "ins_pattern", "type": "single_select", "label": "Pattern", "required": True, "options": ["Difficulty Falling Asleep (Sleep-Onset)", "Difficulty Staying Asleep (Sleep-Maintenance)", "Early Morning Wakening (Depression)", "Mixed"]},
                    {"id": "ins_osa_screen", "type": "multi_select", "label": "OSA Screen", "required": True, "options": ["Snoring", "Witnessed Apnoeas", "Daytime Somnolence", "Morning Headaches", "None"], "is_red_flag": True, "red_flag_positive": "RED FLAG: OSA suspected = Epworth score + sleep study referral.", "red_flag_negative": ""},
                    {"id": "ins_psych_screen", "type": "multi_select", "label": "Psychological Screen", "required": True, "options": ["Anxiety", "Depression / Low Mood", "Stress", "Racing Thoughts at Night", "None"]},
                    {"id": "ins_caffeine", "type": "text", "label": "Caffeine Intake (Cups/Day + Timing)", "required": False, "placeholder": "e.g., 4 cups, last at 4pm"},
                    {"id": "ins_alcohol", "type": "toggle", "label": "Alcohol as Sleep Aid? (Rebound Wakefulness)", "required": False},
                    {"id": "ins_screen_time", "type": "toggle", "label": "Screen Use Within 1 Hour of Bed?", "required": False}
                ]
            },
            {
                "title": "Sleep Hygiene & CBT-I Advice",
                "section_type": "plan",
                "questions": [
                    {"id": "ins_hygiene", "type": "multi_select", "label": "Sleep Hygiene Advised", "required": False, "options": ["Fixed Wake Time (Even on Weekends)", "Bed Only for Sleep (No TV/Phone/Eating)", "Get Up if Not Asleep Within 20 Min", "No Caffeine After 2pm", "No Alcohol Before Bed", "Cool/Dark/Quiet Bedroom", "Regular Exercise (Not Late Evening)", "Wind-Down Routine", "No Screens 1 Hour Before Bed"]},
                    {"id": "ins_cbti", "type": "toggle", "label": "CBT-I (Cognitive Behavioural Therapy for Insomnia) Discussed? (Digital: Sleepio)", "required": False}
                ]
            },
            {
                "title": "Assessment & Plan",
                "section_type": "plan",
                "safety_netting": "Sleep hygiene is first-line. CBT-I is most effective long-term treatment. Avoid benzodiazepines/Z-drugs (addiction, tolerance, falls risk). Short-term melatonin (2mg prolonged-release) for >55 years only (max 13 weeks). Treat underlying cause: depression (SSRI), anxiety (CBT), OSA (sleep study). If early morning wakening = screen for depression (PHQ-9). Return if: symptoms persist after 4-6 weeks of sleep hygiene, or daytime somnolence affecting safety.",
                "questions": [
                    {"id": "ins_diagnosis", "type": "single_select", "label": "Impression", "required": True, "options": ["Primary Insomnia - Sleep Hygiene + CBT-I", "Insomnia + Anxiety/Depression", "?OSA - Sleep Study Referral", "Poor Sleep Hygiene"]},
                    {"id": "ins_epworth", "type": "toggle", "label": "Epworth Sleepiness Score Done? (If OSA Suspected)", "required": False},
                    {"id": "ins_sleep_study", "type": "toggle", "label": "Sleep Study Referral? (If OSA Suspected)", "required": False},
                    {"id": "ins_melatonin", "type": "toggle", "label": "Melatonin 2mg Prolonged-Release? (Age >55 Only, Max 13 Weeks)", "required": False},
                    {"id": "ins_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., 4-6 weeks with sleep diary, sooner if concerns"}
                ]
            }
        ]},
        "is_public": True
    }

    existing = db.query(Template).filter(Template.title == t["title"], Template.created_by == admin.id).first()
    
    if existing:
        print(f"⏭️  SKIPPED: {title} already exists (ID={existing.id})")
        db.close()
        return
    new_t = Template(title=t["title"], description=t["description"], category=t["category"], content=t["content"], is_public=True, created_by=admin.id, version=1)
    db.add(new_t); db.commit()
    print(f"Template '{t['title']}' created!"); db.close()

if __name__ == "__main__":
    seed_insomnia()
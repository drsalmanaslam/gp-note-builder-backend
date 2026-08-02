from app.database import SessionLocal
from app.models import User, Template, Category

def seed_travel_vaccination():
    db = SessionLocal()
    
    admin = db.query(User).filter(User.role == "admin").first()
    if not admin:
        print("❌ No admin found!")
        db.close()
        return

    title = "Travel Vaccination & Advice (NHS Guidelines)"
    existing = db.query(Template).filter(Template.title == title).first()
    if existing:
        print(f"⏭️  SKIPPED: {title} already exists (ID={existing.id})")
        db.close()
        return

    template = Template(
        title=title,
        description="Pre-travel health assessment covering destination-specific vaccines per NHS/NathNac guidelines, malaria prophylaxis, food/water safety, and travel insurance advice.",
        category="General Practice",
        content={"sections": [
            {
                "title": "Travel Details",
                "section_type": "history",
                "questions": [
                    {"id": "trav_destination", "type": "text", "label": "Destination(s) - Country & Region", "required": True, "placeholder": "e.g., Thailand (Bangkok + rural Chiang Mai)"},
                    {"id": "trav_departure", "type": "text", "label": "Departure Date", "required": True, "placeholder": "e.g., 4 weeks from now"},
                    {"id": "trav_duration", "type": "text", "label": "Duration of Stay", "required": True, "placeholder": "e.g., 3 weeks"},
                    {"id": "trav_purpose", "type": "single_select", "label": "Purpose of Travel", "required": True, "options": ["Holiday/Tourism", "Business", "Visiting friends/relatives (VFR)", "Backpacking", "Volunteer/Humanitarian", "Military"]},
                    {"id": "trav_accommodation", "type": "single_select", "label": "Accommodation Type", "required": True, "options": ["Hotel/Resort", "Hostel/Budget", "Staying with family/friends", "Rural/village", "Camping"]},
                    {"id": "trav_activities", "type": "multi_select", "label": "Planned Activities", "required": True, "options": ["Beach/Sun", "City sightseeing", "Trekking/Hiking", "Swimming/Fresh water", "Animal contact", "Healthcare work", "Sexual contact expected"]}
                ]
            },
            {
                "title": "Routine UK Vaccines - Check Status",
                "section_type": "history",
                "questions": [
                    {"id": "trav_routine_vaccines", "type": "multi_select", "label": "Up-to-date with UK Routine Vaccines?", "required": True, "options": ["Tetanus/Diphtheria/Polio (10-year booster)", "MMR (2 doses)", "Flu (seasonal)", "COVID-19", "Pneumococcal (if indicated)", "Hepatitis B (if indicated)", "None checked", "Unknown - check records"]},
                    {"id": "trav_last_tetanus", "type": "text", "label": "Date of Last Tetanus Booster", "required": False, "placeholder": "e.g., 2019"}
                ]
            },
            {
                "title": "Destination-Specific Vaccines (per NathNac)",
                "section_type": "assessment",
                "questions": [
                    {"id": "trav_hep_a", "type": "toggle", "label": "Hepatitis A Required? (Most destinations outside Western Europe/N.America/Aus)", "required": True},
                    {"id": "trav_typhoid", "type": "toggle", "label": "Typhoid Required? (Indian subcontinent, Africa, S.America, SE Asia)", "required": True},
                    {"id": "trav_dtp", "type": "toggle", "label": "Diphtheria/Tetanus/Polio Booster? (>10 years since last)", "required": True},
                    {"id": "trav_cholera", "type": "toggle", "label": "Cholera Required? (Humanitarian/healthcare in outbreak areas)", "required": False},
                    {"id": "trav_hep_b", "type": "toggle", "label": "Hepatitis B Required? (Healthcare, VFR, long stay, sexual contact, tattoos)", "required": True},
                    {"id": "trav_rabies", "type": "toggle", "label": "Rabies Required? (Remote areas, animal contact, cycling/running)", "required": False},
                    {"id": "trav_japanese_enc", "type": "toggle", "label": "Japanese Encephalitis? (Rural SE Asia >1 month, rice farming)", "required": False},
                    {"id": "trav_meningitis_acwy", "type": "toggle", "label": "Meningitis ACWY? (Saudi Arabia - Hajj/Umrah, African meningitis belt)", "required": False},
                    {"id": "trav_yellow_fever", "type": "toggle", "label": "Yellow Fever? (Sub-Saharan Africa, S.America - CERTIFICATE REQUIRED)", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Yellow fever vaccine ONLY at registered Yellow Fever centres. Certificate legally required for entry to some countries.", "red_flag_negative": ""},
                    {"id": "trav_tick_borne", "type": "toggle", "label": "Tick-Borne Encephalitis? (Central/Eastern Europe, Russia, forested areas)", "required": False}
                ]
            },
            {
                "title": "Malaria Prophylaxis",
                "section_type": "assessment",
                "questions": [
                    {"id": "trav_malaria_risk", "type": "single_select", "label": "Malaria Risk Area?", "required": True, "options": ["No risk", "Low risk - bite prevention only", "Moderate risk - chemoprophylaxis recommended", "High risk (Sub-Saharan Africa) - chemoprophylaxis ESSENTIAL"]},
                    {"id": "trav_malaria_drug", "type": "single_select", "label": "Recommended Prophylaxis (Check NathNac for region)", "required": False, "options": ["Atovaquone/Proguanil (Malarone) - daily", "Doxycycline - daily", "Mefloquine (Lariam) - weekly", "Chloroquine + Proguanil - weekly + daily", "None - bite prevention only"]},
                    {"id": "trav_malaria_duration", "type": "text", "label": "Duration: Start Before + Continue After", "required": False, "placeholder": "e.g., Start 1-2 days before, continue 7 days after (Malarone)"},
                    {"id": "trav_malaria_contraindications", "type": "multi_select", "label": "Contraindications Checked?", "required": False, "options": ["Pregnancy (avoid doxycycline, mefloquine)", "Epilepsy (avoid mefloquine)", "Psychiatric history (avoid mefloquine)", "G6PD deficiency (avoid dapsone)", "Renal impairment (adjust dose)", "None"]}
                ]
            },
            {
                "title": "Medical History & Fitness to Travel",
                "section_type": "history",
                "questions": [
                    {"id": "trav_pregnancy", "type": "toggle", "label": "Pregnant or Planning?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Pregnancy = avoid live vaccines (Yellow Fever, MMR, BCG). Check travel insurance covers pregnancy. Zika risk areas - advise against travel.", "red_flag_negative": ""},
                    {"id": "trav_immunocompromised", "type": "toggle", "label": "Immunocompromised? (HIV, chemo, steroids, splenectomy)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Immunocompromised = NO live vaccines. May need additional vaccines (pneumococcal, Hib, meningococcal). Specialist advice needed.", "red_flag_negative": ""},
                    {"id": "trav_allergies", "type": "toggle", "label": "Vaccine Allergies? (Egg, neomycin, streptomycin, latex)", "required": True},
                    {"id": "trav_chronic", "type": "multi_select", "label": "Chronic Conditions", "required": False, "options": ["Diabetes", "Epilepsy", "Cardiac disease", "Respiratory disease", "Psychiatric history", "None"]},
                    {"id": "trav_medications", "type": "text", "label": "Current Medications", "required": False, "placeholder": "e.g., Metformin, Ramipril"},
                    {"id": "trav_anticoagulants", "type": "toggle", "label": "On Anticoagulants? (Warfarin, DOAC) - IM injections risk", "required": False},
                    {"id": "trav_insurance", "type": "toggle", "label": "Travel Insurance Arranged?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: MUST have travel insurance. Disclose ALL medical conditions. Check covers repatriation and medical expenses.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Travel Health Advice",
                "section_type": "plan",
                "safety_netting": "Food & Water: Boil it, cook it, peel it, or forget it. Bottled water only. Avoid ice cubes, salads, street food, unpasteurised dairy. Hand hygiene critical. Insect Bites: DEET 50% repellent, cover skin at dusk/dawn, mosquito net (permethrin-treated), air conditioning. Sun Protection: SPF 30+, hat, avoid 11am-3pm. DVT Prevention: Compression stockings, hydration, mobilise on long flights. Seek medical attention abroad if: fever (especially within 3 months of return), diarrhoea with blood, animal bite, respiratory symptoms. GP review if unwell after return - mention travel history.",
                "questions": [
                    {"id": "trav_vaccines_given", "type": "multi_select", "label": "Vaccines Given Today", "required": True, "options": ["Hepatitis A", "Typhoid", "DTP booster", "Hepatitis B", "Rabies", "Cholera", "Meningitis ACWY", "Japanese Encephalitis", "Yellow Fever (certificate issued)", "None - advice only"]},
                    {"id": "trav_advice_given", "type": "multi_select", "label": "Advice Provided", "required": True, "options": ["Food/water safety", "Insect bite prevention", "Malaria prophylaxis explained", "Sun protection", "DVT prevention", "Sexual health (condoms)", "Rabies - avoid animals", "Schistosomiasis - avoid fresh water", "Travel insurance - essential"]},
                    {"id": "trav_followup", "type": "text", "label": "Follow-up / Next Doses Due", "required": True, "placeholder": "e.g., Hep B dose 2 in 4 weeks, malaria script issued, return if unwell after travel"}
                ]
            }
        ]},
        is_public=True,
        created_by=admin.id
    )
    
    db.add(template)
    db.commit()
    print(f"✅ Created: {title}")
    db.close()

if __name__ == "__main__":
    seed_travel_vaccination()
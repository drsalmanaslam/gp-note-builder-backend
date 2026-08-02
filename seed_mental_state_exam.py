from app.database import SessionLocal
from app.models import User, Template, Category

def seed_mental_state_exam():
    db = SessionLocal()
    
    admin = db.query(User).filter(User.role == "admin").first()
    if not admin:
        print("❌ No admin found!")
        db.close()
        return

    title = "Mental State Examination (MSE)"
    existing = db.query(Template).filter(Template.title == title).first()
    if existing:
        db.delete(existing)
        db.commit()

    template = Template(
        title=title,
        description="Structured Mental State Examination covering appearance, behaviour, speech, mood, thought form/content, perception, cognition, and insight for psychiatric assessment.",
        category="Mental Health",
        content={"sections": [
            {
                "title": "Appearance & Behaviour",
                "section_type": "examination",
                "questions": [
                    {"id": "mse_appearance", "type": "single_select", "label": "General Appearance", "required": True, "options": ["Well-groomed, appropriate attire", "Dishevelled/unkempt", "Bizarre/flamboyant dress", "Poor self-care", "Emaciated/cachectic"]},
                    {"id": "mse_eye_contact", "type": "single_select", "label": "Eye Contact", "required": True, "options": ["Appropriate/normal", "Avoidant/poor", "Intense/staring", "Avoids entirely"]},
                    {"id": "mse_posture", "type": "single_select", "label": "Posture & Motor Activity", "required": True, "options": ["Relaxed/normal", "Agitated/restless", "Psychomotor retardation", "Catatonic/posturing", "Tremor/abnormal movements"]},
                    {"id": "mse_rapport", "type": "single_select", "label": "Rapport", "required": True, "options": ["Established easily", "Guarded/suspicious", "Irritable/hostile", "Over-familiar/disinhibited", "Unable to establish"]},
                    {"id": "mse_facial", "type": "single_select", "label": "Facial Expression", "required": True, "options": ["Reactive/appropriate", "Flat/blunted", "Anxious/fearful", "Perplexed/confused", "Incongruous (smiling when sad)"]}
                ]
            },
            {
                "title": "Speech",
                "section_type": "examination",
                "questions": [
                    {"id": "mse_rate", "type": "single_select", "label": "Rate of Speech", "required": True, "options": ["Normal", "Pressured/rapid (mania)", "Slow/retarded (depression)", "Hesitant/anxious"]},
                    {"id": "mse_volume", "type": "single_select", "label": "Volume", "required": True, "options": ["Normal", "Loud/shouting", "Whispered/quiet", "Mute"]},
                    {"id": "mse_rhythm", "type": "single_select", "label": "Rhythm/Flow", "required": True, "options": ["Normal/coherent", "Stuttering/stammering", "Slurred (?organic)", "Monotonous/flat"]},
                    {"id": "mse_quantity", "type": "single_select", "label": "Quantity", "required": True, "options": ["Normal", "Excessive/logorrhoea", "Minimal/poverty of speech", "Mute/non-verbal"]}
                ]
            },
            {
                "title": "Mood & Affect",
                "section_type": "examination",
                "questions": [
                    {"id": "mse_mood_subjective", "type": "text", "label": "Subjective Mood (Patient's Words)", "required": True, "placeholder": "e.g., 'I feel really low, nothing matters anymore'"},
                    {"id": "mse_mood_objective", "type": "single_select", "label": "Objective Mood", "required": True, "options": ["Euthymic (normal)", "Depressed/low", "Elated/euphoric", "Irritable/angry", "Anxious/worried", "Labile (rapidly changing)"]},
                    {"id": "mse_affect", "type": "single_select", "label": "Affect (Emotional Range)", "required": True, "options": ["Reactive/normal range", "Blunted (reduced)", "Flat (absent)", "Labile (unstable)", "Incongruous (mismatched)"]},
                    {"id": "mse_affect_appropriateness", "type": "toggle", "label": "Affect Appropriate to Context?", "required": True},
                    {"id": "mse_anxiety_signs", "type": "multi_select", "label": "Physical Signs of Anxiety", "required": False, "options": ["Tremor", "Sweating", "Hyperventilating", "Fidgeting", "Tachycardia", "None"]}
                ]
            },
            {
                "title": "Thought Form (Process)",
                "section_type": "examination",
                "questions": [
                    {"id": "mse_thought_form", "type": "single_select", "label": "Thought Form", "required": True, "options": ["Normal/logical/linear", "Flight of ideas (rapid shifts, mania)", "Circumstantial (overly detailed)", "Tangential (goes off-topic)", "Loosening of associations (schizophrenia)", "Thought blocking (sudden stops)", "Perseveration (repetition)"]},
                    {"id": "mse_coherence", "type": "toggle", "label": "Coherent & Logical?", "required": True},
                    {"id": "mse_word_salad", "type": "toggle", "label": "Word Salad / Incomprehensible?", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Word salad = severe thought disorder (?schizophrenia, mania, delirium). Urgent psychiatric assessment.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Thought Content",
                "section_type": "examination",
                "questions": [
                    {"id": "mse_delusions", "type": "toggle", "label": "Delusions Present?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Delusions = psychotic illness. Assess risk, consider antipsychotics, urgent psychiatric referral.", "red_flag_negative": ""},
                    {"id": "mse_delusion_type", "type": "multi_select", "label": "Delusion Type", "required": False, "options": ["Persecutory (being harmed/followed)", "Grandiose (special powers/mission)", "Reference (TV/radio talking about them)", "Control (being controlled by external force)", "Nihilistic (body/mind is dead/decaying)", "Somatic (body infested/changed)", "Religious", "Jealous/Othello syndrome"]},
                    {"id": "mse_overvalued", "type": "toggle", "label": "Overvalued Ideas? (Not delusional but dominant)", "required": False},
                    {"id": "mse_obsessions", "type": "toggle", "label": "Obsessional Thoughts/Ruminations?", "required": True},
                    {"id": "mse_compulsions", "type": "toggle", "label": "Compulsions/Rituals?", "required": True},
                    {"id": "mse_suicidal", "type": "toggle", "label": "Suicidal Ideation?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Suicidal ideation = urgent risk assessment. Ask about plans, means, intent, and protective factors.", "red_flag_negative": ""},
                    {"id": "mse_homicidal", "type": "toggle", "label": "Homicidal Ideation?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Homicidal ideation = duty to warn/protect. Urgent psychiatric assessment + police if imminent risk.", "red_flag_negative": ""},
                    {"id": "mse_hopelessness", "type": "toggle", "label": "Hopelessness / Worthlessness?", "required": True},
                    {"id": "mse_anhedonia", "type": "toggle", "label": "Anhedonia?", "required": False}
                ]
            },
            {
                "title": "Perception",
                "section_type": "examination",
                "questions": [
                    {"id": "mse_hallucinations", "type": "toggle", "label": "Hallucinations?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Hallucinations = psychotic illness or organic cause. Urgent assessment needed.", "red_flag_negative": ""},
                    {"id": "mse_hallucination_type", "type": "multi_select", "label": "Hallucination Modality", "required": False, "options": ["Auditory (hearing voices)", "Visual (seeing things)", "Olfactory (smelling things)", "Tactile (feeling things on skin)", "Gustatory (tasting things)", "Command hallucinations (voices telling to act)", "None"]},
                    {"id": "mse_auditory_type", "type": "single_select", "label": "If Auditory: Type of Voices", "required": False, "options": ["2nd person (talking to patient)", "3rd person (commentary/running commentary)", "Command (telling patient to act)", "Thought echo (repeating thoughts)", "Not applicable"]},
                    {"id": "mse_command_risk", "type": "toggle", "label": "Command Hallucinations - Risk to Self/Others?", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Command hallucinations with risk = psychiatric emergency. Consider detention under MHA.", "red_flag_negative": ""},
                    {"id": "mse_depersonalisation", "type": "toggle", "label": "Depersonalisation / Derealisation?", "required": False},
                    {"id": "mse_illusions", "type": "toggle", "label": "Illusions / Misperceptions?", "required": False}
                ]
            },
            {
                "title": "Cognition",
                "section_type": "examination",
                "questions": [
                    {"id": "mse_orientation", "type": "single_select", "label": "Orientation (Time, Place, Person)", "required": True, "options": ["Fully oriented x3", "Disoriented to time", "Disoriented to place", "Disoriented to person", "Grossly disoriented"]},
                    {"id": "mse_attention", "type": "single_select", "label": "Attention & Concentration", "required": True, "options": ["Good/normal", "Distractible", "Poor - cannot sustain", "Severely impaired"]},
                    {"id": "mse_memory", "type": "single_select", "label": "Memory (Subjective Assessment)", "required": True, "options": ["Intact", "Mild impairment", "Moderate impairment", "Severe impairment - ?dementia/delirium"]},
                    {"id": "mse_cognitive_test", "type": "toggle", "label": "Formal Cognitive Test Done? (MMSE/MoCA/AMTS)", "required": False},
                    {"id": "mse_cognitive_score", "type": "text", "label": "Cognitive Test Score", "required": False, "placeholder": "e.g., MMSE 26/30, MoCA 24/30"}
                ]
            },
            {
                "title": "Insight & Judgement",
                "section_type": "examination",
                "questions": [
                    {"id": "mse_insight", "type": "single_select", "label": "Insight into Illness", "required": True, "options": ["Full insight - acknowledges illness + need for treatment", "Partial insight - some awareness but minimises", "Limited insight - acknowledges symptoms but not illness", "No insight - denies any problem"]},
                    {"id": "mse_judgement", "type": "single_select", "label": "Judgement", "required": True, "options": ["Intact - can make reasonable decisions", "Impaired - poor decision-making", "Severely impaired - risk to self/others"]},
                    {"id": "mse_treatment_acceptance", "type": "single_select", "label": "Willingness to Accept Treatment", "required": True, "options": ["Willing and engaged", "Ambivalent/hesitant", "Refusing - but has capacity", "Refusing - lacks capacity"]}
                ]
            },
            {
                "title": "Risk Summary & Plan",
                "section_type": "assessment",
                "differentials": [
                    "Depression (moderate/severe)",
                    "Bipolar Affective Disorder (manic/depressed/mixed)",
                    "Schizophrenia / Schizoaffective Disorder",
                    "Anxiety Disorder",
                    "OCD",
                    "PTSD",
                    "Personality Disorder",
                    "Organic cause (delirium, dementia, substance-induced)"
                ],
                "questions": [
                    {"id": "mse_risk_self", "type": "single_select", "label": "Risk to Self", "required": True, "options": ["None", "Low - passive thoughts only", "Moderate - ideation without plan", "High - active plan/intent", "Imminent - requires immediate intervention"]},
                    {"id": "mse_risk_others", "type": "single_select", "label": "Risk to Others", "required": True, "options": ["None", "Low - irritable but controlled", "Moderate - threatening, no violence", "High - violent ideation/plan", "Imminent - requires police/MHA"]},
                    {"id": "mse_risk_neglect", "type": "single_select", "label": "Risk of Self-Neglect/Vulnerability", "required": True, "options": ["None", "Mild - not eating well", "Moderate - missing meals/meds", "Severe - unable to care for self"]},
                    {"id": "mse_diagnosis_impression", "type": "text", "label": "Diagnostic Impression", "required": True, "placeholder": "e.g., Moderate depressive episode with psychotic features"},
                    {"id": "mse_plan", "type": "multi_select", "label": "Management Plan", "required": True, "options": ["Routine psychiatric follow-up", "Urgent CMHT referral", "Crisis Team referral", "Informal admission", "MHA assessment requested", "Start/adjust medication", "Psychological therapy referral", "Safeguarding referral", "No immediate action"]},
                    {"id": "mse_followup", "type": "text", "label": "Follow-up / Safety Plan", "required": True, "placeholder": "e.g., CMHT urgent assessment within 48h, crisis line numbers given, GP to review in 1 week"}
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
    seed_mental_state_exam()
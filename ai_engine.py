import json
import os
import requests
from dotenv import load_dotenv


# =========================================================
# ENVIRONMENT
# =========================================================

load_dotenv()

OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY")

OLLAMA_URL = "https://ollama.com/api/chat"

MODEL = "gpt-oss:20b-cloud"


# =========================================================
# FILE PATH
# =========================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

DATA_FILE = os.path.join(
    BASE_DIR,
    "historical_data.json"
)


# =========================================================
# LOAD HISTORICAL DATA
# =========================================================

def load_historical_data():

    if not os.path.exists(DATA_FILE):

        raise FileNotFoundError(
            "historical_data.json was not found. "
            "Please keep it in the KaalVerse project folder."
        )

    with open(
        DATA_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


# =========================================================
# FORMAT HISTORICAL ITEMS
# =========================================================

def _format_items(items):

    if not items:
        return "None available"

    result = []

    for item in items:

        if isinstance(item, dict):

            name = item.get(
                "name",
                ""
            )

            description = item.get(
                "description",
                ""
            )

            if name and description:

                result.append(
                    f"{name}: {description}"
                )

            elif name:

                result.append(name)

            elif description:

                result.append(description)

        else:

            result.append(
                str(item)
            )

    return "; ".join(result)


# =========================================================
# GET HISTORICAL CONTEXT
# =========================================================

def get_historical_context(
    data,
    state_key,
    era_key,
    character_name
):

    if state_key not in data:

        raise KeyError(
            f"State '{state_key}' was not found "
            "in historical_data.json."
        )

    state_data = data[state_key]

    # Some JSON structures use:
    # state -> eras -> era
    #
    # Others may directly contain the eras.

    eras = state_data.get(
        "eras",
        state_data
    )

    if era_key not in eras:

        raise KeyError(
            f"Era '{era_key}' was not found "
            f"for state '{state_key}'."
        )

    era_data = eras[era_key]

    return {
        "state": state_data.get(
            "name",
            state_key.replace(
                "_",
                " "
            ).title()
        ),

        "era": era_data.get(
            "name",
            era_key.replace(
                "_",
                " "
            ).title()
        ),

        "period": era_data.get(
            "period",
            ""
        ),

        "years": era_data.get(
            "years",
            ""
        ),

        "capital": era_data.get(
            "capital",
            ""
        ),

        "overview": era_data.get(
            "overview",
            ""
        ),

        "food": _format_items(
            era_data.get(
                "food",
                []
            )
        ),

        "clothing": _format_items(
            era_data.get(
                "clothing",
                []
            )
        ),

        "homes": _format_items(
            era_data.get(
                "homes",
                []
            )
        ),

        "crafts": _format_items(
            era_data.get(
                "crafts",
                []
            )
        ),

        "games": _format_items(
            era_data.get(
                "games",
                []
            )
        ),

        "music": _format_items(
            era_data.get(
                "music",
                []
            )
        ),

        "language": _format_items(
            era_data.get(
                "language",
                []
            )
        ),

        "festivals": _format_items(
            era_data.get(
                "festivals",
                []
            )
        ),

        "occupations": _format_items(
            era_data.get(
                "occupations",
                []
            )
        ),

        "education": _format_items(
            era_data.get(
                "education",
                []
            )
        ),

        "daily_life": _format_items(
            era_data.get(
                "daily_life",
                []
            )
        ),

        "architecture": _format_items(
            era_data.get(
                "architecture",
                []
            )
        ),

        "experience_scenarios": _format_items(
            era_data.get(
                "experience_scenarios",
                []
            )
        ),

        "character": character_name
    }


# =========================================================
# GENERATE IMMERSIVE STORY
# =========================================================

def generate_story(
    historical_context,
    gender,
    age
):

    if not OLLAMA_API_KEY:

        raise ValueError(
            "OLLAMA_API_KEY was not found. "
            "Please add it to your .env file."
        )

    prompt = f"""
You are KaalVerse, an immersive AI historical storyteller.

Your job is NOT to write a history textbook.

Your job is to make the reader FEEL as if they have
physically entered the selected historical world and
are living one complete day there.

The reader is the main character.

==================================================
CHARACTER
==================================================

State:
{historical_context["state"]}

Era:
{historical_context["era"]}

Historical Period:
{historical_context["period"]}

Years:
{historical_context["years"]}

Capital:
{historical_context["capital"]}

Role:
{historical_context["character"]}

Gender:
{gender}

Age:
{age}


==================================================
HISTORICAL WORLD
==================================================

Overview:
{historical_context["overview"]}

Food:
{historical_context["food"]}

Clothing:
{historical_context["clothing"]}

Homes:
{historical_context["homes"]}

Crafts:
{historical_context["crafts"]}

Games:
{historical_context["games"]}

Music:
{historical_context["music"]}

Language:
{historical_context["language"]}

Festivals:
{historical_context["festivals"]}

Occupations:
{historical_context["occupations"]}

Education:
{historical_context["education"]}

Daily Life:
{historical_context["daily_life"]}

Architecture:
{historical_context["architecture"]}

Experience Scenarios:
{historical_context["experience_scenarios"]}


==================================================
CORE STORY RULE
==================================================

Do NOT write like a textbook.

Do NOT explain history to the reader.

Instead, SHOW the reader what it feels like to live
inside this historical world.

The reader should feel:

"I am actually there."

NOT:

"I am reading a history chapter."


==================================================
POINT OF VIEW
==================================================

Write entirely in SECOND PERSON.

Use "you" frequently.

Examples:

"You wake before sunrise."

"You step into the courtyard."

"You hear the market beginning to stir."

"You adjust your clothing."

"You walk toward the market."

"You taste the food."

"You hear someone calling your name."

The reader is experiencing the events directly.


==================================================
CINEMATIC WRITING STYLE
==================================================

Make the experience feel like a historical movie.

Use:

• Short paragraphs
• Sensory details
• Sounds
• Smells
• Weather
• Light
• Textures
• Food
• Clothing
• Architecture
• Streets
• Markets
• People
• Natural conversations
• Small emotional moments
• Everyday activities
• Character actions

Avoid long academic explanations.

Most paragraphs should be approximately
1–4 sentences.

Leave blank lines between paragraphs.


==================================================
STORY STRUCTURE
==================================================

Create ONE continuous journey through a single day.

Divide the story into exactly FOUR major scenes.

Use these scene markers:

🌅 MORNING

☀️ AFTERNOON

🌆 EVENING

🌙 NIGHT


==================================================
TIME
==================================================

Every major scene MUST include a specific approximate
historical time.

Use this format:

🕕 5:45 AM — Before the City Wakes

or:

🕛 12:15 PM — Voices of the Market

or:

🕕 6:20 PM — Golden Light Over the Fort

or:

🕘 9:00 PM — Beneath the Night Sky


Choose times that make sense for the historical period.

Do NOT use exactly the same times in every story.

For ancient and medieval periods, base the timing naturally
around sunrise, meals, work, markets, religious activities,
travel and sunset.

For post-independence periods, modern clock-based routines
may be used when historically appropriate.


==================================================
SCENE TITLES
==================================================

Each scene must have a short cinematic title.

Do NOT use boring titles such as:

"Morning Activities"

"Afternoon Activities"

"Evening Activities"

"Night Activities"


Instead use titles such as:

🌅 MORNING

🕕 5:45 AM — Before the City Wakes


☀️ AFTERNOON

🕛 12:15 PM — Voices of the Market


🌆 EVENING

🕕 6:20 PM — Golden Light Over the Fort


🌙 NIGHT

🕘 9:00 PM — Beneath the Night Sky


==================================================
MORNING
==================================================

Begin with the character waking up.

Show:

• Where the character sleeps
• What the character sees
• Morning sounds
• Morning smells
• Clothing
• Food
• Family or community
• First task of the day

Create a strong opening that immediately transports
the reader into the historical world.


==================================================
AFTERNOON
==================================================

Move the character into the wider world.

Depending on the selected role, naturally show things such as:

• Market
• School
• Workshop
• Farm
• Palace
• Fort
• Temple
• Street
• Trading area
• Administrative work
• Political activity
• Craft work
• Learning
• Travel

The character must DO something.

Do not make the character simply observe history.


==================================================
EVENING
==================================================

Slow the pace slightly.

Show:

• Returning home
• Evening food
• Music
• Games
• Social activities
• Family
• Community
• Sunset
• Festival if historically appropriate

Include at least one memorable human moment.


==================================================
NIGHT
==================================================

End the day naturally.

Show:

• Returning home
• Final meal or conversation
• Night surroundings
• Character's thoughts

End with a beautiful immersive sentence that makes
the reader feel the historical day has truly ended.


==================================================
IMPORTANT HIGHLIGHTS / STICKERS
==================================================

Throughout the story, naturally highlight important
experiences.

Use approximately 1–3 highlights per scene.

Use these formats:

⭐ Your Task: [important activity]

🍚 What You Eat: [historical food]

👕 What You Wear: [clothing detail]

🏠 Where You Live: [home detail]

🛠️ What You Work With: [tool/craft/work detail]

🛍️ What You See: [market/street/place detail]

🎵 What You Hear: [sound/music]

💬 [short natural dialogue]

📜 Historical Detail: [meaningful historical detail]

✨ Memorable Moment: [special moment]

Use only the highlight types that naturally fit.

Do NOT use all of them in every scene.

Maximum 3 highlights per scene.

Highlights should describe something the character
is actually experiencing.

Do NOT turn highlights into textbook definitions.


==================================================
DIALOGUE
==================================================

Use short natural dialogue when appropriate.

Example:

💬 "Hurry, we must reach the market before the crowd arrives."

Do not create long conversations.

Dialogue should support the experience.


==================================================
HISTORICAL ACCURACY
==================================================

Use only information supported by the provided
historical context.

Do not present unsupported facts as certain.

Do not invent famous historical events.

Do not introduce modern objects into ancient,
medieval or early historical periods.

For post-independence periods, modern objects and
technology may appear only when historically appropriate.

Use historically appropriate:

• Clothing
• Food
• Architecture
• Tools
• Work
• Transportation
• Social activities
• Language
• Education
• Markets


==================================================
AVOID TEXTBOOK LANGUAGE
==================================================

Avoid phrases such as:

"During this period..."

"People in this era..."

"Historically..."

"The economy was..."

"People commonly..."

"The society consisted of..."

unless absolutely necessary.

Instead SHOW the experience.

BAD:

"People in this period wore traditional clothes."

GOOD:

"You tighten the cloth around your waist and adjust
the fabric before stepping outside."


==================================================
EMOJI RULE
==================================================

Use emojis as visual markers.

Do NOT place random emojis after every sentence.

Use emojis mainly for:

• Scene headings
• Time
• Important highlights
• Dialogue
• Special moments

Useful markers include:

🌅 Morning
☀️ Afternoon
🌆 Evening
🌙 Night
🕕 Time
🏠 Home
🍚 Food
👕 Clothing
🛕 Temple
🏰 Fort / Palace
🏪 Market
🎓 Learning
🧵 Craft
🌾 Farming
🐎 Travel
🎵 Music
🎉 Festival
🔥 Cooking
🛍️ Trading
📜 Historical detail
👨‍👩‍👧 Family
🛠️ Work
⭐ Important moment
✨ Memorable moment
💬 Dialogue


==================================================
CHARACTER IMMERSION
==================================================

The selected age MUST influence the experience.

A child should experience the world differently from
a 30-year-old adult.

A teacher should experience the world differently from
a merchant.

A farmer should experience different activities from
a politician.

An artisan should interact with tools and crafts.

A student should experience learning.

A merchant should experience trade and markets.

A politician or administrator should experience
meetings, governance or public responsibilities
only when historically appropriate.

Gender should influence the experience only where
historically relevant and without using stereotypes.


==================================================
LENGTH
==================================================

Write approximately 800–1100 words.

Use many short paragraphs.

Make the story visually comfortable to read.

Do NOT use bullet points inside the main narrative.

The only structured elements should be:

• Four scene headings
• Time/title lines
• Occasional highlight stickers
• Short dialogue


==================================================
FINAL FEELING
==================================================

The reader should finish the experience feeling:

"I just lived one day in this historical world."

Not:

"I just read about this historical period."

Make KaalVerse feel like TIME TRAVEL.
"""

    response = requests.post(
        OLLAMA_URL,
        headers={
            "Authorization": f"Bearer {OLLAMA_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "stream": False
        },
        timeout=180
    )

    if response.status_code != 200:

        raise RuntimeError(
            f"Ollama API error "
            f"{response.status_code}: "
            f"{response.text}"
        )

    data = response.json()

    if "message" not in data:

        raise RuntimeError(
            "Unexpected response received "
            "from Ollama API."
        )

    return data["message"]["content"]


# =========================================================
# CREATE IMAGE PROMPTS
# =========================================================

def create_scene_prompts(
    historical_context,
    story
):

    base = f"""
Create a historically grounded cinematic visual
reconstruction for KaalVerse.

State:
{historical_context["state"]}

Era:
{historical_context["era"]}

Period:
{historical_context["period"]}

Years:
{historical_context["years"]}

Capital:
{historical_context["capital"]}

Character:
{historical_context["character"]}

Historical overview:
{historical_context["overview"]}

Food:
{historical_context["food"]}

Clothing:
{historical_context["clothing"]}

Homes:
{historical_context["homes"]}

Crafts:
{historical_context["crafts"]}

Architecture:
{historical_context["architecture"]}

Daily life:
{historical_context["daily_life"]}

Story:
{story}

VISUAL RULES:

Create a realistic historical scene.

Use historically appropriate:

• Clothing
• Architecture
• Materials
• Tools
• Streets
• Buildings
• Food
• Transportation
• Environment
• Hairstyles
• Objects

Do NOT include modern objects unless this is a
post-independence/modern historical period.

The image should look like the character is actually
inside this historical world.

Cinematic composition.

Natural lighting.

Rich environmental details.

Historically appropriate Indian setting.
"""

    return {

        "morning": (
            base
            + """

SCENE:
Morning.

Show the character beginning the day.

Include the appropriate home/environment,
morning light, clothing and first activity.
"""
        ),

        "afternoon": (
            base
            + """

SCENE:
Afternoon.

Show the character actively performing
their main role or activity.

Include the surrounding people,
architecture and environment.
"""
        ),

        "evening": (
            base
            + """

SCENE:
Evening.

Show the character during sunset or
early evening activities.

Include appropriate lighting,
social activity and surroundings.
"""
        ),

        "daily_life": (
            base
            + """

SCENE:
Overall everyday life.

Create a wide, immersive view showing
the historical world around the character.

Show architecture, people, clothing,
activities and environment.
"""
        )
    }


# =========================================================
# CREATE AUDIO TEXT
# =========================================================

def create_audio_text(story):

    if not story:
        return ""

    # Remove markdown formatting that may interfere
    # with text-to-speech.

    cleaned = story.replace(
        "**",
        ""
    )

    cleaned = cleaned.replace(
        "__",
        ""
    )

    cleaned = cleaned.replace(
        "#",
        ""
    )

    return cleaned


# =========================================================
# GENERATE COMPLETE EXPERIENCE
# =========================================================

def generate_experience(
    state_key,
    era_key,
    character_name,
    gender,
    age
):

    # -----------------------------------------------------
    # Load historical data
    # -----------------------------------------------------

    data = load_historical_data()

    # -----------------------------------------------------
    # Get selected historical context
    # -----------------------------------------------------

    historical_context = get_historical_context(
        data,
        state_key,
        era_key,
        character_name
    )

    # -----------------------------------------------------
    # Generate immersive story
    # -----------------------------------------------------

    story = generate_story(
        historical_context,
        gender,
        age
    )

    # -----------------------------------------------------
    # Generate image prompts
    # -----------------------------------------------------

    scene_prompts = create_scene_prompts(
        historical_context,
        story
    )

    # -----------------------------------------------------
    # Generate narration text
    # -----------------------------------------------------

    audio_text = create_audio_text(
        story
    )

    # -----------------------------------------------------
    # Return complete experience
    # -----------------------------------------------------

    return {

        "state": state_key,

        "state_name": historical_context[
            "state"
        ],

        "era": era_key,

        "era_name": historical_context[
            "era"
        ],

        "period": historical_context[
            "period"
        ],

        "years": historical_context[
            "years"
        ],

        "capital": historical_context[
            "capital"
        ],

        "role": character_name,

        "gender": gender,

        "age": age,

        "story": story,

        "scene_prompts": scene_prompts,

        "audio_text": audio_text,

        "historical_context": historical_context,

        "images": {},

        "audio": None
    }
import os
import json
import shutil
from datetime import datetime

import streamlit as st

from ai_engine import generate_experience
from image_generator import generate_image
from audio_generator import generate_audio


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="KaalVerse",
    page_icon="⏳",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CONSTANTS
# ============================================================

DATA_FILE = "historical_data.json"
GENERATED_FOLDER = "generated"


# ============================================================
# STYLING
# ============================================================

st.markdown(
    """
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600;700;800&family=Poppins:wght@400;500;600;700&display=swap');

    /* --------------------------------------------------------
       GENERAL FONT
       -------------------------------------------------------- */

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }

    .stApp {
        background-color: #ffffff;
        color: #3b2418;
    }


    /* --------------------------------------------------------
       MAIN TITLE
       KaalVerse = medium-large
       -------------------------------------------------------- */

    h1 {
        font-family: 'Cinzel', serif !important;
        font-size: 38px !important;
        font-weight: 700 !important;
        color: #4a2c1d !important;
        letter-spacing: 1px;
        margin-bottom: 5px !important;
    }


    /* --------------------------------------------------------
       SECTION HEADINGS
       Smaller than KaalVerse
       -------------------------------------------------------- */

    h2 {
        font-family: 'Cinzel', serif !important;
        font-size: 23px !important;
        font-weight: 600 !important;
        color: #4a2c1d !important;
        margin-top: 18px !important;
        margin-bottom: 8px !important;
    }

    h3 {
        font-family: 'Cinzel', serif !important;
        font-size: 19px !important;
        font-weight: 600 !important;
        color: #4a2c1d !important;
    }


    /* --------------------------------------------------------
       NORMAL TEXT
       -------------------------------------------------------- */

    p {
        font-family: 'Poppins', sans-serif !important;
        font-size: 15px !important;
        color: #3b2418 !important;
    }


    /* --------------------------------------------------------
       CAPTION
       -------------------------------------------------------- */

    .stCaption,
    [data-testid="stCaptionContainer"] {
        font-family: 'Poppins', sans-serif !important;
        font-size: 13px !important;
    }


    /* --------------------------------------------------------
       SELECTBOX / RADIO / SLIDER TEXT
       Keep these smaller than headings
       -------------------------------------------------------- */

    div[data-baseweb="select"] {
        font-family: 'Poppins', sans-serif !important;
        font-size: 14px !important;
    }

    div[data-baseweb="select"] * {
        font-family: 'Poppins', sans-serif !important;
        font-size: 14px !important;
    }

    div[role="radiogroup"] label {
        font-size: 14px !important;
    }

    div[data-testid="stSlider"] {
        font-size: 14px !important;
    }


    /* --------------------------------------------------------
       CHARACTER INFORMATION
       -------------------------------------------------------- */

    [data-testid="stMarkdownContainer"] strong {
        font-family: 'Poppins', sans-serif;
    }


    /* --------------------------------------------------------
       SIDEBAR
       -------------------------------------------------------- */

    section[data-testid="stSidebar"] {
        background-color: #5A321F !important;
    }

    /* All sidebar text white */

    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] div,
    section[data-testid="stSidebar"] small,
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] h4 {
        color: white !important;
    }


    /* Sidebar KaalVerse */

    section[data-testid="stSidebar"] h2 {
        font-family: 'Cinzel', serif !important;
        font-size: 26px !important;
        font-weight: 700 !important;
        color: white !important;
    }


    /* Sidebar normal text */

    section[data-testid="stSidebar"] p {
        font-size: 13px !important;
        color: white !important;
    }


    /* --------------------------------------------------------
       SIDEBAR BUTTONS
       IMPORTANT:
       Streamlit puts text inside nested elements.
       This makes EVERYTHING inside the buttons white.
       -------------------------------------------------------- */

    section[data-testid="stSidebar"] button {
        background-color: #4a2c1d !important;
        border: 1px solid #c8a98f !important;
        color: white !important;
    }

    section[data-testid="stSidebar"] button *,
    section[data-testid="stSidebar"] button p,
    section[data-testid="stSidebar"] button span,
    section[data-testid="stSidebar"] button div {
        color: white !important;
        font-family: 'Poppins', sans-serif !important;
    }

    section[data-testid="stSidebar"] button:hover {
        background-color: #6a432c !important;
        border-color: white !important;
        color: white !important;
    }

    section[data-testid="stSidebar"] button:hover *,
    section[data-testid="stSidebar"] button:hover p,
    section[data-testid="stSidebar"] button:hover span,
    section[data-testid="stSidebar"] button:hover div {
        color: white !important;
    }


    /* --------------------------------------------------------
       MAIN BUTTONS
       -------------------------------------------------------- */

    .stButton > button {
        border-radius: 10px;
        border: 1px solid #6a432c;
        background-color: #4a2c1d;
        color: white !important;
        font-family: 'Cinzel', serif;
        font-weight: 700;
    }

    .stButton > button *,
    .stButton > button p,
    .stButton > button span,
    .stButton > button div {
        color: white !important;
    }

    .stButton > button:hover {
        background-color: #6a432c;
        color: white !important;
    }


    /* --------------------------------------------------------
       DIVIDERS
       -------------------------------------------------------- */

    hr {
        border-color: #e5dcd5;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LOAD HISTORICAL DATA
# ============================================================

@st.cache_data
def load_historical_data():

    if not os.path.exists(DATA_FILE):

        st.error(
            "historical_data.json was not found. "
            "Please keep it inside the KaalVerse folder."
        )

        return {}

    try:

        with open(
            DATA_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except json.JSONDecodeError as error:

        st.error(
            f"historical_data.json contains invalid JSON: {error}"
        )

        return {}


historical_data = load_historical_data()


# ============================================================
# DATA HELPERS
# ============================================================

def get_state_name(state_key, state_data):

    return state_data.get(
        "name",
        state_key.replace("_", " ").title()
    )


def get_eras(state_data):

    return state_data.get(
        "eras",
        {}
    )


def get_era_name(era_key, era_data):

    return era_data.get(
        "name",
        era_key.replace("_", " ").title()
    )


def extract_role_names(items):

    roles = []

    if not isinstance(items, list):
        return roles

    for item in items:

        if isinstance(item, dict):

            name = item.get("name")

            if name:
                roles.append(name)

        elif isinstance(item, str):

            roles.append(item)

    return roles


def get_role_options(era_data):

    roles = []

    roles.extend(
        extract_role_names(
            era_data.get(
                "characters",
                []
            )
        )
    )

    roles.extend(
        extract_role_names(
            era_data.get(
                "roles",
                []
            )
        )
    )

    unique_roles = []

    for role in roles:

        if role not in unique_roles:
            unique_roles.append(role)

    if not unique_roles:

        unique_roles = [
            "Merchant",
            "Farmer",
            "Teacher",
            "Artisan",
            "Soldier",
            "Trader",
            "Student"
        ]

    return unique_roles


# ============================================================
# SAVED JOURNEYS
# ============================================================

def get_saved_journeys():

    journeys = []

    if not os.path.exists(
        GENERATED_FOLDER
    ):
        return journeys

    for folder_name in os.listdir(
        GENERATED_FOLDER
    ):

        folder_path = os.path.join(
            GENERATED_FOLDER,
            folder_name
        )

        if not os.path.isdir(
            folder_path
        ):
            continue

        experience_file = os.path.join(
            folder_path,
            "experience.json"
        )

        if not os.path.exists(
            experience_file
        ):
            continue

        try:

            with open(
                experience_file,
                "r",
                encoding="utf-8"
            ) as file:

                experience = json.load(file)

            journeys.append(
                {
                    "folder": folder_name,
                    "data": experience
                }
            )

        except Exception:

            continue

    journeys.sort(
        key=lambda item: item["folder"],
        reverse=True
    )

    return journeys


# ============================================================
# SAVE EXPERIENCE
# ============================================================

def save_experience(experience):

    os.makedirs(
        GENERATED_FOLDER,
        exist_ok=True
    )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S_%f"
    )

    folder_name = (
        f"experience_{timestamp}"
    )

    experience_folder = os.path.join(
        GENERATED_FOLDER,
        folder_name
    )

    images_folder = os.path.join(
        experience_folder,
        "images"
    )

    audio_folder = os.path.join(
        experience_folder,
        "audio"
    )

    os.makedirs(
        images_folder,
        exist_ok=True
    )

    os.makedirs(
        audio_folder,
        exist_ok=True
    )


    # --------------------------------------------------------
    # GENERATE IMAGES
    # --------------------------------------------------------

    scene_prompts = experience.get(
        "scene_prompts",
        {}
    )

    generated_images = {}

    image_names = [
        ("morning", "morning.png"),
        ("afternoon", "afternoon.png"),
        ("evening", "evening.png"),
        ("daily_life", "daily_life.png")
    ]

    for scene_key, file_name in image_names:

        prompt = scene_prompts.get(
            scene_key
        )

        if not prompt:
            continue

        output_path = os.path.join(
            images_folder,
            file_name
        )

        try:

            generate_image(
                prompt,
                output_path
            )

            generated_images[
                scene_key
            ] = output_path

        except Exception as error:

            generated_images[
                scene_key
            ] = None

            print(
                f"Image generation failed "
                f"for {scene_key}: {error}"
            )


    # --------------------------------------------------------
    # GENERATE AUDIO
    # --------------------------------------------------------

    audio_path = os.path.join(
        audio_folder,
        "narration.mp3"
    )

    generated_audio = None

    try:

        generate_audio(
            experience.get(
                "audio_text",
                ""
            ),
            audio_path
        )

        generated_audio = audio_path

    except Exception as error:

        print(
            f"Audio generation failed: {error}"
        )


    # --------------------------------------------------------
    # SAVE INFORMATION
    # --------------------------------------------------------

    experience["images"] = generated_images

    experience["audio"] = generated_audio

    experience["folder_name"] = folder_name

    experience["created_at"] = timestamp

    experience_file = os.path.join(
        experience_folder,
        "experience.json"
    )

    with open(
        experience_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            experience,
            file,
            ensure_ascii=False,
            indent=4
        )

    return experience


# ============================================================
# DELETE ONE EXPERIENCE
# ============================================================

def delete_experience(folder_name):

    folder_path = os.path.join(
        GENERATED_FOLDER,
        folder_name
    )

    if not os.path.exists(
        folder_path
    ):
        return True

    def remove_readonly(
        func,
        path,
        exc_info
    ):

        try:

            os.chmod(
                path,
                0o777
            )

            func(path)

        except Exception:

            pass

    try:

        shutil.rmtree(
            folder_path,
            onerror=remove_readonly
        )

        return True

    except PermissionError:

        return False

    except Exception:

        return False


# ============================================================
# CLEAR ALL JOURNEYS
# ============================================================

def clear_all_journeys():

    if not os.path.exists(
        GENERATED_FOLDER
    ):
        return True

    success = True

    for folder_name in os.listdir(
        GENERATED_FOLDER
    ):

        folder_path = os.path.join(
            GENERATED_FOLDER,
            folder_name
        )

        if not os.path.isdir(
            folder_path
        ):
            continue

        if not delete_experience(
            folder_name
        ):

            success = False

    return success


# ============================================================
# DISPLAY STORY
# ============================================================

def display_story(story):

    if not story:
        return

    lines = story.split("\n")

    for line in lines:

        line = line.strip()

        if not line:
            continue


        # ----------------------------------------------------
        # SCENE HEADINGS
        # ----------------------------------------------------

        if (
            line.startswith("🌅")
            or line.startswith("☀️")
            or line.startswith("🌆")
            or line.startswith("🌙")
        ):

            st.markdown(
                f"**{line}**"
            )


        # ----------------------------------------------------
        # TIME
        # ----------------------------------------------------

        elif line.startswith(
            (
                "🕐",
                "🕑",
                "🕒",
                "🕓",
                "🕔",
                "🕕",
                "🕖",
                "🕗",
                "🕘",
                "🕙",
                "🕚",
                "🕛"
            )
        ):

            st.caption(line)


        # ----------------------------------------------------
        # HIGHLIGHTS
        # ----------------------------------------------------

        elif line.startswith(
            (
                "⭐",
                "🍚",
                "👕",
                "🏠",
                "🛠️",
                "🛍️",
                "🎵",
                "📜",
                "✨"
            )
        ):

            st.markdown(
                f"**{line}**"
            )


        # ----------------------------------------------------
        # DIALOGUE
        # ----------------------------------------------------

        elif line.startswith("💬"):

            st.write(line)


        # ----------------------------------------------------
        # NORMAL STORY
        # ----------------------------------------------------

        else:

            st.write(line)


# ============================================================
# DISPLAY EXPERIENCE
# ============================================================

def display_experience(experience):


    # --------------------------------------------------------
    # CHARACTER
    # --------------------------------------------------------

    st.markdown(
        "## ✨ Your Character"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            "**📍 Place**"
        )

        st.write(
            experience.get(
                "state",
                "Unknown"
            )
        )

    with col2:

        st.markdown(
            "**🏛️ Time**"
        )

        st.write(
            experience.get(
                "era",
                "Unknown"
            )
        )

    with col3:

        st.markdown(
            "**👤 Role**"
        )

        st.write(
            experience.get(
                "role",
                "Unknown"
            )
        )

    period = experience.get(
        "period",
        ""
    )

    if period:

        st.markdown(
            f"**📜 Period:** {period}"
        )

    gender = experience.get(
        "gender",
        "Unknown"
    )

    age = experience.get(
        "age",
        "Unknown"
    )

    role = experience.get(
        "role",
        "Unknown"
    )

    st.write(
        f"You will experience history as a "
        f"{age}-year-old {gender.lower()} {role}."
    )

    st.divider()


    # --------------------------------------------------------
    # STORY
    # --------------------------------------------------------

    st.markdown(
        "## 📜 Your Journey"
    )

    display_story(
        experience.get(
            "story",
            ""
        )
    )


    # --------------------------------------------------------
    # AUDIO
    # --------------------------------------------------------

    audio_path = experience.get(
        "audio"
    )

    if audio_path and os.path.exists(
        audio_path
    ):

        st.markdown(
            "### 🎙️ Listen to Your Journey"
        )

        try:

            with open(
                audio_path,
                "rb"
            ) as audio_file:

                st.audio(
                    audio_file.read(),
                    format="audio/mp3"
                )

        except Exception:

            st.warning(
                "The narration could not be played."
            )


    # --------------------------------------------------------
    # IMAGES
    # --------------------------------------------------------

    images = experience.get(
        "images",
        {}
    )

    if images:

        st.markdown(
            "### 🖼️ Visual Journey"
        )

        image_columns = st.columns(2)

        image_titles = {
            "morning": "🌅 Morning",
            "afternoon": "☀️ Afternoon",
            "evening": "🌆 Evening",
            "daily_life": "🌙 Daily Life"
        }

        index = 0

        for scene_key, image_path in images.items():

            if not image_path:
                continue

            if not os.path.exists(
                image_path
            ):
                continue

            with image_columns[
                index % 2
            ]:

                st.markdown(
                    f"#### {image_titles.get(scene_key, scene_key.title())}"
                )

                st.image(
                    image_path,
                    use_container_width=True
                )

            index += 1


# ============================================================
# SESSION STATE
# ============================================================

if "current_experience" not in st.session_state:

    st.session_state.current_experience = None


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        "## ⏳ KaalVerse"
    )

    st.caption(
        "Step into the world of the past."
    )

    st.divider()

    st.markdown(
        "### 📜 Your Journeys"
    )

    saved_journeys = get_saved_journeys()

    if not saved_journeys:

        st.caption(
            "Your journeys will appear here."
        )

    else:

        for journey in saved_journeys:

            data = journey["data"]

            journey_folder = journey[
                "folder"
            ]

            state_name = data.get(
                "state",
                "Unknown"
            )

            era_name = data.get(
                "era",
                "Unknown"
            )

            role_name = data.get(
                "role",
                "Unknown"
            )

            st.markdown(
                f"**{state_name} • {era_name}**"
            )

            st.caption(
                f"👤 {role_name}"
            )

            col1, col2 = st.columns(
                [3, 1]
            )

            with col1:

                if st.button(
                    "Open",
                    key=f"open_{journey_folder}",
                    use_container_width=True
                ):

                    st.session_state.current_experience = data

                    st.rerun()

            with col2:

                if st.button(
                    "🗑️",
                    key=f"delete_{journey_folder}",
                    use_container_width=True
                ):

                    deleted = delete_experience(
                        journey_folder
                    )

                    if deleted:

                        current = (
                            st.session_state.current_experience
                        )

                        if (
                            current
                            and
                            current.get(
                                "folder_name"
                            ) == journey_folder
                        ):

                            st.session_state.current_experience = None

                        st.rerun()

                    else:

                        st.error(
                            "Could not delete this journey. "
                            "Close any audio or files using it and try again."
                        )

            st.divider()

    if saved_journeys:

        if st.button(
            "🗑️ Clear All Journeys",
            use_container_width=True
        ):

            cleared = clear_all_journeys()

            if cleared:

                st.session_state.current_experience = None

                st.rerun()

            else:

                st.error(
                    "Some journeys could not be deleted. "
                    "Close files or audio and try again."
                )


# ============================================================
# MAIN PAGE
# ============================================================

st.title(
    "⏳ KaalVerse"
)

st.caption(
    "Step into the world of the past — "
    "choose who you are, where you live, and when you live."
)


# ============================================================
# IF OLD JOURNEY IS OPEN
# ============================================================

if st.session_state.current_experience:

    display_experience(
        st.session_state.current_experience
    )

    st.divider()

    if st.button(
        "✨ Start a New Journey",
        use_container_width=True
    ):

        st.session_state.current_experience = None

        st.rerun()

    st.stop()


# ============================================================
# STATE
# ============================================================

st.markdown(
    "## 🗺️ Where do you want to travel?"
)

state_keys = list(
    historical_data.keys()
)

if not state_keys:

    st.error(
        "No states were found in historical_data.json."
    )

    st.stop()

state_key = st.selectbox(
    "Select a place",
    state_keys,
    format_func=lambda key:
        get_state_name(
            key,
            historical_data[key]
        ),
    label_visibility="collapsed"
)

selected_state = historical_data[
    state_key
]


# ============================================================
# ERA
# ============================================================

st.markdown(
    "## ⏳ Which time would you like to enter?"
)

eras = get_eras(
    selected_state
)

era_keys = list(
    eras.keys()
)

if not era_keys:

    st.error(
        "No historical eras were found for this state."
    )

    st.stop()

era_key = st.selectbox(
    "Select an era",
    era_keys,
    format_func=lambda key:
        get_era_name(
            key,
            eras[key]
        ),
    label_visibility="collapsed"
)

selected_era = eras[
    era_key
]


# ============================================================
# ROLE
# ============================================================

st.markdown(
    "## 👤 Who will you become?"
)

role_options = get_role_options(
    selected_era
)

role = st.selectbox(
    "Choose your role",
    role_options,
    label_visibility="collapsed"
)


# ============================================================
# GENDER
# ============================================================

st.markdown(
    "## ⚧️ How would you like to experience this life?"
)

gender = st.radio(
    "Choose your gender",
    [
        "Male",
        "Female",
        "Other"
    ],
    horizontal=True,
    label_visibility="collapsed"
)


# ============================================================
# AGE
# ============================================================

st.markdown(
    "## 🎂 How old are you in this world?"
)

age = st.slider(
    "Age",
    min_value=5,
    max_value=80,
    value=30,
    step=1,
    label_visibility="collapsed"
)


# ============================================================
# CHARACTER PREVIEW
# ============================================================

st.markdown(
    "## ✨ Your Character"
)

col1, col2, col3 = st.columns(3)

with col1:

    st.markdown(
        "**📍 Place**"
    )

    st.write(
        get_state_name(
            state_key,
            selected_state
        )
    )

with col2:

    st.markdown(
        "**🏛️ Time**"
    )

    st.write(
        get_era_name(
            era_key,
            selected_era
        )
    )

with col3:

    st.markdown(
        "**👤 Role**"
    )

    st.write(role)

st.write(
    f"You will experience history as a "
    f"{age}-year-old {gender.lower()} {role}."
)


# ============================================================
# ENTER THE PAST
# ============================================================

st.markdown("")

enter_button = st.button(
    "✨ ENTER THE PAST",
    use_container_width=True
)


if enter_button:

    with st.spinner(
        "⏳ Opening the gates of history..."
    ):

        try:

            experience = generate_experience(
                state_key=state_key,
                era_key=era_key,
                character_name=role,
                gender=gender,
                age=age
            )


            # ------------------------------------------------
            # ADD UI INFORMATION
            # ------------------------------------------------

            experience["state"] = get_state_name(
                state_key,
                selected_state
            )

            experience["era"] = get_era_name(
                era_key,
                selected_era
            )

            experience["role"] = role

            experience["gender"] = gender

            experience["age"] = age

            experience["period"] = selected_era.get(
                "period",
                selected_era.get(
                    "years",
                    ""
                )
            )


            # ------------------------------------------------
            # SAVE PERMANENTLY
            # ------------------------------------------------

            saved_experience = save_experience(
                experience
            )

            st.session_state.current_experience = (
                saved_experience
            )

            st.rerun()


        except Exception as error:

            st.error(
                "Something went wrong while creating "
                "your historical journey."
            )

            st.exception(error)


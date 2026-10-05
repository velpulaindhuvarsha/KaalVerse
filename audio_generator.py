import os
from gtts import gTTS


# =========================================================
# AUDIO GENERATION FUNCTION
# =========================================================

def generate_audio(audio_text, output_path, language="en"):
    """
    Converts historical narration text into speech
    and saves it as an MP3 file.
    """

    if not audio_text:
        raise ValueError(
            "Audio text is empty. "
            "Please provide narration text."
        )

    # Create output folder if it doesn't exist
    output_directory = os.path.dirname(output_path)

    if output_directory:
        os.makedirs(
            output_directory,
            exist_ok=True
        )

    # Generate speech
    speech = gTTS(
        text=audio_text,
        lang=language,
        slow=False
    )

    # Save audio
    speech.save(output_path)

    return output_path


# =========================================================
# TEST AUDIO GENERATION
# =========================================================

if __name__ == "__main__":

    test_text = """
    Welcome to KaalVerse.

    You are now experiencing everyday life
    during the Kakatiya Era in Telangana.

    Imagine yourself living in medieval Warangal,
    surrounded by traditional homes, artisans,
    farmers, temples and local markets.

    This experience combines documented historical
    information with carefully identified historical
    reconstruction.
    """

    output_file = "generated/audio/test_history.mp3"

    result = generate_audio(
        test_text,
        output_file
    )

    print(f"Audio generated successfully: {result}")
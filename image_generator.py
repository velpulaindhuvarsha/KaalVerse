import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY")


# =========================================================
# IMAGE GENERATION FUNCTION
# =========================================================

def generate_image(image_prompt, output_path):
    """
    Generates a historical image using Hugging Face
    and saves it to the specified output path.
    """

    if not HF_API_KEY:
        raise ValueError(
            "HF_API_KEY was not found. "
            "Please add it to your .env file."
        )

    # Create Hugging Face client
    client = InferenceClient(
        api_key=HF_API_KEY
    )

    # Generate image
    image = client.text_to_image(
        prompt=image_prompt,
        model="black-forest-labs/FLUX.1-schnell"
    )

    # Create output folder
    os.makedirs(
        os.path.dirname(output_path),
        exist_ok=True
    )

    # Save image
    image.save(output_path)

    return output_path


# =========================================================
# TEST IMAGE GENERATION
# =========================================================

if __name__ == "__main__":

    test_prompt = """
    A realistic historical reconstruction of medieval Telangana
    during the Kakatiya Era, a traditional village environment,
    a local artisan working with traditional tools, period-appropriate
    clothing and architecture, natural lighting, historically grounded,
    cinematic realistic photography, no modern objects.
    """

    output_file = "generated/images/test_history.png"

    result = generate_image(
        test_prompt,
        output_file
    )

    print(f"Image generated successfully: {result}")
import base64
from pathlib import Path

from PIL import Image, ImageOps

from thumbnail_agent.config import (
    get_image_client,
    IMAGE_MODEL
)
from thumbnail_agent.state import ThumbnailState


def generator(state: ThumbnailState) -> dict:

    iteration = state["iteration"] + 1

    print(f"\nGenerating thumbnail: Iteration {iteration}")
    print(f"Image model: {IMAGE_MODEL}")

    client = get_image_client()

    output_dir = Path(state["output_dir"])
    output_dir.mkdir(parents=True, exist_ok=True)

    image_path = output_dir / f"iter_{iteration}.png"

    # Generate image
    response = client.images.generate(
        model=IMAGE_MODEL,
        prompt=state["current_prompt"],
        size="1536x1024",
        n=1
    )

    # GPT Image models return Base64 image data
    image_data = response.data[0].b64_json

    if not image_data:
        raise RuntimeError(
            "Image generation returned no image data."
        )

    image_bytes = base64.b64decode(image_data)

    image_path.write_bytes(image_bytes)

    # Convert to standard YouTube thumbnail dimensions
    with Image.open(image_path) as image:

        thumbnail = ImageOps.fit(
            image.convert("RGB"),
            (1280, 720),
            method=Image.Resampling.LANCZOS
        )

        thumbnail.save(image_path, format="PNG")

    print(f"Image saved: {image_path}")

    return {
        "image_path": str(image_path),
        "iteration": iteration
    }
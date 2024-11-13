""" Example handler file. """

import runpod
from diffusers import StableDiffusion3Pipeline
import torch
import base64
import io, os
from dotenv import load_dotenv

load_dotenv()

# Aspect ratio mapping - base width of 1024
ASPECT_RATIOS = {
    "16:9": (1024, 576),    # 1.77:1
    "1:1": (1024, 1024),    # Square
    "21:9": (1024, 439),    # Ultra-wide 2.33:1
    "2:3": (683, 1024),     # Portrait
    "3:2": (1024, 683),     # Landscape
    "4:5": (819, 1024),     # Portrait
    "5:4": (1024, 819),     # Landscape
    "9:16": (576, 1024),    # Vertical/Mobile
    "9:21": (439, 1024),    # Vertical ultra-wide
}

try:
    pipe = StableDiffusion3Pipeline.from_pretrained(
        "stabilityai/stable-diffusion-3.5-medium",
        torch_dtype=torch.float16,
        variant='fp16',
        token=os.environ.get('HUGGINGFACE_TOKEN')
    )

    pipe.to("cuda")
except RuntimeError:
    quit()

def parse_aspect_ratio(ratio_str):
    """Convert aspect ratio string to width and height."""
    if ratio_str not in ASPECT_RATIOS:
        return ASPECT_RATIOS["1:1"]  # Default to square if invalid
    return ASPECT_RATIOS[ratio_str]

def handler(job):
    """ Handler function that will be used to process jobs. """
    job_input = job['input']
    prompt = job_input.get('prompt', '')
    aspect_ratio = job_input.get('aspect_ratio', '1:1')
    guidance_scale = float(job_input.get('guidance_scale', 0))
    num_inference_steps = int(job_input.get('num_inference_steps', 1))
    
    # Get dimensions based on aspect ratio
    width, height = parse_aspect_ratio(aspect_ratio)
    
    # Generate image with all parameters
    image = pipe(
        prompt=prompt,
        height=height,
        width=width,
        num_inference_steps=num_inference_steps,
        guidance_scale=guidance_scale
    ).images[0]

    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    image_bytes = buffer.getvalue()

    return base64.b64encode(image_bytes).decode('utf-8')


runpod.serverless.start({"handler": handler})

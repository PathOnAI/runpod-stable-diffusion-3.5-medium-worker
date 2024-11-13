""" Example handler file. """

import runpod
from diffusers import StableDiffusion3Pipeline
import torch
import base64
import io, os
from dotenv import load_dotenv

load_dotenv()

try:
    pipe = StableDiffusion3Pipeline.from_pretrained(
        "stabilityai/stable-diffusion-3.5-large", 
        torch_dtype=torch.float16, 
        variant="fp16",
        token=os.environ.get('HUGGINGFACE_TOKEN')
    )

    pipe.to("cuda")
except RuntimeError:
    quit()

def handler(job):
    """ Handler function that will be used to process jobs. """
    job_input = job['input']
    prompt = job_input['prompt']

    image = pipe(
        prompt=prompt, 
        num_inference_steps=1, 
        guidance_scale=0.0
    ).images[0]

    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    image_bytes = buffer.getvalue()

    return base64.b64encode(image_bytes).decode('utf-8')


runpod.serverless.start({"handler": handler})

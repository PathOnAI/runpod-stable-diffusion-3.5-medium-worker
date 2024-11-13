<div align="center">

<h1>Stable Diffusion 3.5 Medium Worker Template</h1>

A specialized worker template for building custom RunPod Endpoint API workers utilizing the Stable Diffusion 3.5 Medium model. This implementation supports various aspect ratios, guidance scales, and inference steps customization.

</div>

## Docker Container

The ready-to-use Docker container is available on Docker Hub:
```bash
thehunter911/stbldiff3.5-medium-runpod-serverless
```
which can be used to deploy onto Runpod Serverless endpoint directly.


You can also pull it using:
```bash
docker pull thehunter911/stbldiff3.5-medium-runpod-serverless
```



## Input Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| prompt | string | required | The text description of the image you want to generate |
| aspect_ratio | string | "1:1" | Image aspect ratio. See supported values below |
| guidance_scale | float | 0.0 | How closely the model follows the prompt |
| num_inference_steps | integer | 1 | Number of denoising steps |

### Supported Aspect Ratios
- "16:9" - Widescreen (1024×576)
- "1:1" - Square (1024×1024)
- "21:9" - Ultra-wide (1024×439)
- "2:3" - Portrait (683×1024)
- "3:2" - Landscape (1024×683)
- "4:5" - Portrait (819×1024)
- "5:4" - Landscape (1024×819)
- "9:16" - Vertical/Mobile (576×1024)
- "9:21" - Vertical ultra-wide (439×1024)

## Example Input

```json
{
    "input": {
        "prompt": "An image of a cat with a hat on",
        "aspect_ratio": "16:9",
        "guidance_scale": 0.0,
        "num_inference_steps": 1
    }
}
```

## Example Output

The output is a base64 encoded string of the generated image. Example:

```
data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...
```

### Viewing the Output

To view the generated image, you can decode the base64 string using Python:

```python
import base64
from PIL import Image
import io

# Replace 'base64_string' with your actual base64 string
base64_string = "iVBORw0KGgoAAAANSUhEUgAA..."
image_data = base64.b64decode(base64_string)
image = Image.open(io.BytesIO(image_data))
image.show()
```

## Performance Notes

This implementation uses torch.float16 with fp16 variant for optimal inference performance on consumer GPUs. This configuration provides:
- Faster inference speed
- Lower memory usage
- Better hardware compatibility
- Optimal for generation tasks
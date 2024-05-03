# https://huggingface.co/madebyollin/sdxl-vae-fp16-fix
import torch
from diffusers import DiffusionPipeline, AutoencoderKL

vae = AutoencoderKL.from_pretrained(
    "madebyollin/sdxl-vae-fp16-fix", torch_dtype=torch.float16
)
pipe = DiffusionPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",
    vae=vae,
    torch_dtype=torch.float16,
    variant="fp16",
    use_safetensors=True,
)
pipe.to("cuda")
pipe.enable_model_cpu_offload()

# refiner = DiffusionPipeline.from_pretrained(
#     "stabilityai/stable-diffusion-xl-refiner-1.0",
#     vae=vae,
#     torch_dtype=torch.float16,
#     use_safetensors=True,
#     variant="fp16",
# )
# refiner.enable_model_cpu_offload()

n_steps = 5
high_noise_frac = 0.8

prompt = "A majestic lion jumping from a big stone at night"

image = pipe(
    prompt=prompt,
    num_inference_steps=n_steps,
    denoising_end=high_noise_frac,
    output_type="latent",
).images
# image = refiner(
#     prompt=prompt,
#     num_inference_steps=n_steps,
#     denoising_start=high_noise_frac,
#     image=image,
# ).images[0]
image

from huggingface_hub import snapshot_download

snapshot_download("runwayml/stable-diffusion-v1-5", local_dir="stable-diffusion-v1-5")
snapshot_download("stabilityai/sd-vae-ft-mse", local_dir="sd-vae-ft-mse")

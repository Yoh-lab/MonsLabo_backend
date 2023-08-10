import io
import os
import warnings

from dotenv import load_dotenv
from PIL import Image
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation


load_dotenv('.env')
STABILITY_API_KEY = os.getenv('STABILITY_API_KEY')

os.environ['STABILITY_HOST'] = 'grpc.stability.ai:443'

stability_api = client.StabilityInference(
    key=STABILITY_API_KEY,
    verbose=True,
    engine="stable-diffusion-xl-1024-v0-9", 
)

def generate_image(filename, age, sex, hobby, race):
    res = stability_api.generate(
        prompt="",
        init_image=Image.open(filename),
        start_schedule=0.8,
        seed=123463446,
        steps=50,
        cfg_scale=8.0,
        width=1024,
        height=1024,
        sampler=generation.SAMPLER_K_DPMPP_2M
    )

    for resp in res:
        for artifact in resp.artifacts:
            if artifact.finish_reason == generation.FILTER:
                warnings.warn(
                    "Your request activated the API's safety filters and could not be processed."
                    "Please modify the prompt and try again.")
            if artifact.type == generation.ARTIFACT_IMAGE:
                global img2
                img2 = Image.open(io.BytesIO(artifact.binary))
                img2.save("shibainu-sk8-"+str(artifact.seed)+ "-img2img.png")

    return img2
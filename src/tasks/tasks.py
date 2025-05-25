from time import sleep
from PIL import Image
import os

from src.tasks.celery_app import celery_instanse


@celery_instanse.task
def sleepp():
    sleep(20)
    return print("good")


# @celery_instanse.task
def compress_image(input_image_path):
    sleep(10)
    print("kkkkk")
    target_sizes = [1000, 500, 200]
    with Image.open(input_image_path) as img:
        base_name, ext = os.path.splitext(os.path.basename(input_image_path))
        output_dir = "src/static/images"
        os.makedirs(output_dir, exist_ok=True)
        for size in target_sizes:
            img_resized = img.resize(
                (size, int(size * img.height / img.width)), Image.LANCZOS
            )
            output_image_path = os.path.join(output_dir, f"{base_name}_{size}px{ext}")
            img_resized.save(output_image_path)

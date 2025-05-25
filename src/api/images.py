from fastapi import APIRouter, UploadFile, BackgroundTasks
import shutil

from src.tasks.tasks import compress_image

router = APIRouter(prefix="/images", tags=["изображения отелей"])


@router.post("")
def add_images(file: UploadFile, background_tasks: BackgroundTasks):
    file_ = f"src/static/images/{file.filename}"
    with open(file_, "wb+") as new_file:
        shutil.copyfileobj(file.file, new_file)
    background_tasks.add_task(compress_image, file_)

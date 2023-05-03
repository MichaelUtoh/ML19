import shutil

import cohere
import cv2
from cloudinary.uploader import upload
from decouple import config
from fastapi import APIRouter, Depends, File, UploadFile

from core.config.auth import AuthHandler
from core.config.machine import examples
from core.schema.machine import TextSchema


auth_handler = AuthHandler()

router = APIRouter(
    prefix="/documents",
    tags=["Files"],
)


@router.post("/upload_image", status_code=200)
def create_file(user=Depends(auth_handler.auth_wrapper), file: UploadFile = File()):
    # CV2 operations
    cv2.imread(file.filename)
    cv2.imshow("image", file)
    cv2.waitKey(5000)
    cv2.destroyAllWindows()

    # Upload to cloudinary
    res = upload(file.file)
    return {"url": res["secure_url"]}


@router.post("/reviews", status_code=200)
def generate_text(data: TextSchema):
    co = cohere.Client(config("COHERE_API_KEY"))
    inputs = [data.review]
    response = co.classify(
        model="large",
        inputs=inputs,
        examples=examples,
    )
    return {"detail": response}

import cloudinary
import cloudinary.uploader
from app.core.config import settings


def initialize_cloudinary():
    print("Cloud Name:", settings.CLOUDINARY_CLOUD_NAME)
    print("API Key:", settings.CLOUDINARY_API_KEY)
    print("API Secret:", settings.CLOUDINARY_API_SECRET)

    if settings.CLOUDINARY_CLOUD_NAME:
        cloudinary.config(
            cloud_name=settings.CLOUDINARY_CLOUD_NAME,
            api_key=settings.CLOUDINARY_API_KEY,
            api_secret=settings.CLOUDINARY_API_SECRET,
            secure=True
        )


def upload_file(file_path: str, folder: str = "tutorApp") -> str:
    """Upload file to Cloudinary and return URL"""
    initialize_cloudinary()
    try:
        result = cloudinary.uploader.upload(file_path, folder=folder)
        return result["secure_url"]
    except Exception as e:
        raise Exception(f"File upload failed: {str(e)}")


def upload_file_from_bytes(file_bytes: bytes, filename: str, folder: str = "tutorApp") -> str:
    """Upload file from bytes to Cloudinary"""
    initialize_cloudinary()
    try:
        result = cloudinary.uploader.upload(
            file_bytes,
            filename=filename,
            folder=folder
        )
        return result["secure_url"]
    except Exception as e:
        raise Exception(f"File upload failed: {str(e)}")
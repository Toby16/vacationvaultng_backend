import cloudinary
import cloudinary.uploader

# [ CLOUDINARY CONFIG ]
cloudinary.config(
  cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME'), 
  api_key = os.getenv('CLOUDINARY_API_KEY'), 
  api_secret = os.getenv('CLOUDINARY_SECRET_KEY')
)

def upload_property_image(file):
    """
    Upload image to cloudinary and return secure url
    """
    result = cloudinary.uploader.upload(file.file)
    return result.get("secure_url", result.get("url", None))

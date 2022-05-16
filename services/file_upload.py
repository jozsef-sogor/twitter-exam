from bottle import get, post, request, response, run
import os
import uuid
import imghdr

def upload_image(image):
    print( dir(image) )
    print(image.filename)
    file_name, file_extension = os.path.splitext(image.filename) # .png .jpeg .zip .mp4
    print(file_name)
    print(file_extension)
  
    # Validate extension
    if file_extension not in (".png", ".jpeg", ".jpg"):
        return "image not allowed"
  
    # overwrite jpg to jpeg so imghdr will pass validation
    if file_extension == ".jpg": file_extension = ".jpeg"

    image_id = str(uuid.uuid4())
    # Create new image name
    image_name = f"{image_id}{file_extension}"
    print(image_name)
    # Save the image
    image_url = f"assets/img/{image_name}"
    image.save(image_url)

    # Make sure that the image is actually a valid image
    # by reading its mime type
    print("imghdr.what", imghdr.what(f"assets/img/{image_name}"))   # imghdr.what png
    print("file_extension", file_extension)                     # file_extension .png
    imghdr_extension = imghdr.what(f"assets/img/{image_name}")
    if file_extension != f".{imghdr_extension}":
        print("mmm... suspicious ... it is not really an image")
        # remove the invalid image from the folder
        os.remove(f"assets/img/{image_name}")
        return "mmm... got you! It was not an image"

    # SUCCESS
    return image_url

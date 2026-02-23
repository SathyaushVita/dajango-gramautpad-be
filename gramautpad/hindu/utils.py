from django.core.mail import send_mail
import random
from django.conf import settings
import re
import string
import requests
import base64
import os
import uuid
from rest_framework.pagination import PageNumberPagination
from azure.storage.blob import BlobServiceClient
from django.core.exceptions import ValidationError
from .enums.id_type_enum import IDType


class CustomPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 100

def send_welcome_email(username):
    subject = 'Welcome to Gramautpad'
    html_content = f"""
    <html>
    <head>
        <title>Welcome to Gramautpad</title>
    </head>
    <body>
        <p>Dear {username},</p>
        <p>"Welcome to Gramautpad! We're thrilled to have you join us. Discover a world of authentic, locally crafted products sourced directly from rural artisans. Happy shopping!"</p>

    </body>
    </html>
    """
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [username]
    
    send_mail(
        subject=subject,
        message='',
        from_email=email_from,
        recipient_list=recipient_list,
        html_message=html_content
    )



def send_email(username, otp):
    subject = 'Your account verification email'
    message = f'Your OTP is: {otp}'
    print(message,"1111111111111")
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [username] 
    send_mail(subject, message, email_from, recipient_list)



def generate_otp(length = 6):
    characters = string.digits
    otp = ''.join(random.choice(characters) for _ in range(length))
    return otp


def validate_email(email):
    email_regex = r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$'
    if not re.match(email_regex, email):
        return False
    return True



sms_user = settings.SMS_USER
sms_password = settings.SMS_PASSWORD
sms_sender = settings.SMS_SENDER
sms_type = settings.SMS_TYPE
sms_template_id = settings.SMS_TEMPLATE_ID
RESEND_SMS = settings.RESEND_SMS_TEMP

def send_sms(username, otp):
    
    
    url = f"http://api.bulksmsgateway.in/sendmessage.php?user={sms_user}&password={sms_password}&mobile={username}&message=Dear user your OTP to verify your Gramadevata User account is {otp}. Thank You! team Sathayush.&sender={sms_sender}&type={sms_type}&template_id={sms_template_id}"

    print(url)  
    response = requests.get(url)
    print(response.text) 
    print("Sent Mobile OTP",username,otp,"ssssssssssssssssssssssssss")


def Resend_sms(username, otp):
    
    # url = f"http://api.bulksmsgateway.in/sendmessage.php?user={sms_user}&password={sms_password}&mobile={username}message=Dear user your OTP to reset your Gramadevata account Password is {otp}. Thank You! team Sathayush.&sender={sms_sender}&type={sms_type}&template_id={RESEND_SMS}"
    url = f"http://api.bulksmsgateway.in/sendmessage.php?user=Sathayushtech&password=Sathayushtech@1&mobile={username}&message=Dear user your OTP to reset your Gramadevata account Password is {otp}. Thank You! team Sathayush.&sender=STYUSH&type=3&template_id=1207170963828012432"

    print(url)  
    response = requests.get(url)
    print(response.text) 
    print("Sent Mobile OTP",username,otp,"rrrrrrrrrrrrrrrrrrrrr")




def validate_id_number(value, id_type):
    if id_type == IDType.AADHAR and not re.match(r'^\d{4}\s?\d{4}\s?\d{4}$', value):
        raise ValidationError('Invalid Aadhar number. It must be a 12-digit number.')
    elif id_type == IDType.PAN and not re.match(r'^[A-Z]{5}\d{4}[A-Z]$', value):
        raise ValidationError('Invalid PAN number. It should be in the format: ABCDE1234F.')
    elif id_type == IDType.VOTER_ID and not re.match(r'^[A-Z]{3}\d{7}$', value):
        raise ValidationError('Invalid Voter ID number. It should be in the format: ABC1234567.')
    elif id_type == IDType.DRIVING_LICENSE and not re.match(r'^[A-Z]{2}\d{2}[A-Z]{1,2}\d{4}$', value):
        raise ValidationError('Invalid Driving License number. Please follow the appropriate format.')



# def file_path_to_binary(file_path):
#     """
#     Converts the file at the given path to a base64-encoded string.
#     """
#     img_url = settings.FILE_URL  # Use settings FILE_URL for the base directory
#     full_path = os.path.join(img_url, file_path)
    
#     if os.path.exists(full_path):
#         with open(full_path, "rb") as file:
#             file_data = file.read()
#             return base64.b64encode(file_data).decode('utf-8')  # Convert to a string and return
#     return None



def file_path_to_binary(filename):
    file_url = settings.FILE_URL
    print("img_url",file_url)
    def get_base64_encoded_image(file_path):
        if os.path.exists(file_path):
            with open(file_path, "rb") as file_file:
                file_data = file_file.read()
                base64_encoded_image = base64.b64encode(file_data)
                # print(base64_encoded_image,"123456")
                return file_path
        else:
            return None
    if isinstance(filename, list):
        encoded_images = []
        for path in filename:
            file_path = os.path.join(file_url, path)
            base64_encoded_image = get_base64_encoded_image(file_path)
            if base64_encoded_image is not None:
                encoded_images.append(base64_encoded_image)
        return encoded_images
    else:
        file_path = os.path.join(file_url, filename)
        return file_path
    return None








def save_file_to_azure(file_data, _id, name, entity_type, file_type):
    """
    Saves the file to Azure Blob Storage and returns the relative path.
    """
    # Decode base64 file data
    decoded_file = base64.b64decode(file_data)
    
    # Create a folder name based on the provided _id and entity_type
    folder_name = str(_id)
    
    # Generate a unique file name
    file_name = f"{name}_{uuid.uuid4().hex[:8]}.{file_type}"
    
    # Azure settings
    container_name = 'sathayush'
    folder_path = f"{entity_type}/{folder_name}/"  # Example: 'temple/1234/'
    blob_name = f"{folder_path}{file_name}"  # Full path for the file in Azure Blob Storage
    print(blob_name, "file_blob_name")

    # Initialize BlobServiceClient
    blob_service_client = BlobServiceClient.from_connection_string(settings.AZURE_STORAGE_CONNECTION_STRING)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

    # Upload the file to Azure Blob Storage
    blob_client.upload_blob(decoded_file, blob_type="BlockBlob", overwrite=True)

    # Get the full URL of the uploaded file
    blob_url = blob_client.url
    print(blob_url, "file_blob_url")

    return blob_name  # Return the relative blob path for future reference



def image_path_to_binary(filename):
    img_url = settings.FILE_URL
    print("img_url",img_url)
    def get_base64_encoded_image(img_path):
        if os.path.exists(img_path):
            with open(img_path, "rb") as image_file:
                image_data = image_file.read()
                base64_encoded_image = base64.b64encode(image_data)
                # print(base64_encoded_image,"123456")
                return img_path
        else:
            return None
    if isinstance(filename, list):
        encoded_images = []
        for path in filename:
            img_path = os.path.join(img_url, path)
            base64_encoded_image = get_base64_encoded_image(img_path)
            if base64_encoded_image is not None:
                encoded_images.append(base64_encoded_image)
        return encoded_images
    else:
        img_path = os.path.join(img_url, filename)
        return img_path
    return None



def save_image_to_azure(image_data, _id, name, entity_type):
    # Decode base64 image
    decoded_image = base64.b64decode(image_data)
    
    # Create a folder name based on the provided _id and entity_type
    folder_name = str(_id)
    
    # Generate unique image name
    image_name = f"{name}_{uuid.uuid4().hex[:8]}.jpg"
    
    # Azure settings
    container_name = 'sathayush'
    folder_path = f"{entity_type}/{folder_name}/"  # Example: 'temple/1234/'
    blob_name = f"{folder_path}{image_name}"  # Full path for the image in Azure Blob Storage
    print(blob_name,"3efrgth")

    # Initialize BlobServiceClient
    blob_service_client = BlobServiceClient.from_connection_string(settings.AZURE_STORAGE_CONNECTION_STRING)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

    # Upload the image to Azure Blob Storage
    blob_client.upload_blob(decoded_image, blob_type="BlockBlob", overwrite=True)

    # Get the full URL of the uploaded image
    blob_url = blob_client.url
    print(blob_url,"blob_url")

    return blob_name





def video_path_to_binary(filename):
    video_url = settings.FILE_URL
    print("sandhya", video_url)
    
    def get_base64_encoded_video(video_path):
        if os.path.exists(video_path):
            print(video_path,"kanchu")
            with open(video_path, "rb") as video_file:
                video_data = video_file.read()
                print(video_data,"abcd")
                base64_encoded_video = base64.b64encode(video_data)
                print(base64_encoded_video,"123456")

                # Return video path instead of the base64-encoded data
                return video_path
        else:
            return None

    if isinstance(filename, list):
        encoded_videos = []
        for path in filename:
            video_path = os.path.join(video_url, path)
            print("kanchupati",video_path)
            base64_encoded_video = get_base64_encoded_video(video_path)
            if base64_encoded_video is not None:
                encoded_videos.append(base64_encoded_video)
        return encoded_videos
    else:
        video_path = os.path.join(video_url, filename)
        # return get_base64_encoded_video(video_path)
        return video_path
    
    return None




def save_video_to_azure(video_data, _id, name, entity_type):
    try:
        # Decode base64 video
        decoded_video = base64.b64decode(video_data)
        
        # Create a folder name based on the provided _id and entity_type
        folder_name = str(_id)
        
        # Generate unique video name
        video_name = f"{name}_{uuid.uuid4().hex[:8]}.mp4"
        
        # Azure settings
        container_name = 'sathayush'
        folder_path = f"{entity_type}/{folder_name}/"  # Example: 'trainings/1234/'
        blob_name = f"{folder_path}{video_name}"  # Full path for the video in Azure Blob Storage
        print(blob_name, "Generated Blob Name")
        
        # Initialize BlobServiceClient
        blob_service_client = BlobServiceClient.from_connection_string(settings.AZURE_STORAGE_CONNECTION_STRING)
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        
        # Upload the video to Azure Blob Storage
        blob_client.upload_blob(decoded_video, blob_type="BlockBlob", overwrite=True)
        
        # Instead of returning the full URL, return the relative path
        return blob_name  # Returning the relative path of the uploaded video

    except Exception as e:
        print(f"An error occurred: {str(e)}")  # Print the error message for debugging
        return None















import re

def is_valid_aadhaar_number(aadhaar_number):
    # Regular expression to check that Aadhaar number has exactly 12 digits
    if not re.match(r'^\d{12}$', aadhaar_number):
        return False
    # Check if all digits are the same (not allowed)
    if len(set(aadhaar_number)) == 1:
        return False
    return True

def verhoeff_check(aadhaar_number):
    # Multiplication table
    d = [
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        [1, 2, 3, 4, 0, 6, 7, 8, 9, 5],
        [2, 3, 4, 0, 1, 7, 8, 9, 5, 6],
        [3, 4, 0, 1, 2, 8, 9, 5, 6, 7],
        [4, 0, 1, 2, 3, 9, 5, 6, 7, 8],
        [5, 9, 8, 7, 6, 0, 4, 3, 2, 1],
        [6, 5, 9, 8, 7, 1, 0, 4, 3, 2],
        [7, 6, 5, 9, 8, 2, 1, 0, 4, 3],
        [8, 7, 6, 5, 9, 3, 2, 1, 0, 4],
        [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    ]
    # Permutation table
    p = [
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        [1, 5, 7, 6, 2, 8, 3, 0, 9, 4],
        [5, 8, 0, 3, 7, 9, 6, 1, 4, 2],
        [8, 9, 1, 6, 0, 4, 3, 5, 2, 7],
        [9, 4, 5, 3, 1, 2, 6, 8, 7, 0],
        [4, 2, 8, 6, 5, 7, 3, 9, 0, 1],
        [2, 7, 9, 3, 8, 0, 6, 4, 1, 5],
        [7, 0, 4, 6, 9, 1, 3, 2, 5, 8]
    ]
    # Inverse table
    inv = [0, 4, 3, 2, 1, 5, 6, 7, 8, 9]

    # Convert Aadhaar number string to an integer list
    aadhaar_number = list(map(int, aadhaar_number))
    c = 0  # Initialize the cumulative sum

    # Process digits of Aadhaar number in reverse order
    for i, digit in enumerate(reversed(aadhaar_number)):
        c = d[c][p[i % 8][digit]]
    
    return c == 0

# Final Aadhaar validation
def validate_aadhaar(aadhaar_number):
    return is_valid_aadhaar_number(aadhaar_number) and verhoeff_check(aadhaar_number)

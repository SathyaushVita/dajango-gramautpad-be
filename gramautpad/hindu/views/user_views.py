from ..models import User
from ..serializers import Loginserializer, Verifyserializer
from rest_framework import generics, status
from rest_framework.response import Response
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from ..utils import validate_email, send_email, send_sms, generate_otp, send_welcome_email
from rest_framework.permissions import IsAuthenticated
from ..models import User
from ..serializers import Loginserializer, Verifyserializer
from rest_framework import generics, status
from rest_framework.response import Response
from django.utils import timezone
from django.shortcuts import get_object_or_404
from ..utils import save_image_to_azure
from ..enums import MemberStatus




class Register_LoginView(generics.GenericAPIView):
    serializer_class = Loginserializer
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        if not username:
            return Response({"error": "username is required"}, status=status.HTTP_400_BAD_REQUEST)
        otp = generate_otp()
        message = ""
        user = None
        # Determine if username is an email or phone number
        if validate_email(username):
            # Check if user exists by email or contact number
            user = User.objects.using('gramadevata_updated1').filter(email=username).first() or User.objects.filter(contact_number=username).first()
        else:
            # Check if user exists by contact number or email
            user = User.objects.using('gramadevata_updated1').filter(contact_number=username).first() or User.objects.filter(email=username).first()
        if user:
            # Username already exists, update OTP
            user.verification_otp = otp
            user.verification_otp_created_time = timezone.now()
            user.save()
            message = "Login successful and OTP sent successfully"
        else:
            # Username does not exist, create a new user with either email or contact number
            user = User.objects.using('gramadevata_updated1').create(
                username=username,
                verification_otp=otp,
                verification_otp_created_time=timezone.now(),
                email=username if validate_email(username) else None,
                contact_number=username if not validate_email(username) else None
            )
            user.save()
            message = "OTP sent successfully"
        # Send OTP via email or SMS
        if validate_email(username):
            send_email(username, otp)
        else:
            send_sms(username, otp)
        return Response({"message": message}, status=status.HTTP_200_OK)
    




class Validate_LoginOTPView(generics.GenericAPIView):
    serializer_class = Verifyserializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        verification_otp = request.data.get('verification_otp')

        # Check if user exists by either email or contact number
        user = None
        if validate_email(username):
            user = User.objects.using('gramadevata_updated1').filter(
                email=username,
                verification_otp=verification_otp
            ).first() or User.objects.using('gramadevata_updated1').filter(
                contact_number=username,
                verification_otp=verification_otp
            ).first()
        else:
            user = User.objects.using('gramadevata_updated1').filter(
                contact_number=username,
                verification_otp=verification_otp
            ).first() or User.objects.using('gramadevata_updated1').filter(
                email=username,
                verification_otp=verification_otp
            ).first()

        if user:
            # Check OTP expiration
            if user.verification_otp_created_time < timezone.now() - timezone.timedelta(hours=24):
                return Response({"error": "OTP expired"}, status=status.HTTP_400_BAD_REQUEST)

            # Update user status to ACTIVE
            user.status = 'ACTIVE'
            user.save()

            # Generate tokens
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token

            # Send a welcome email if the username is an email
            if validate_email(username):
                send_welcome_email(username)

            return Response({
                'refresh': str(refresh),
                'access': str(access_token),
                'username': user.get_username(),
                'user_id': user.id,
                'stakeholder_type': user.stakeholder_type
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)


from rest_framework import generics, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from ..utils import image_path_to_binary,file_path_to_binary,video_path_to_binary
from ..serializers import RegisterSerializer1






class RegisterUpdate(generics.GenericAPIView):
    serializer_class = RegisterSerializer1




    def get(self, request, id):
        # Fetch the register instance based on the provided ID
        instance = get_object_or_404(User, id=id)
        
        # Serialize the instance
        serializer = self.get_serializer(instance)
        
        # Prepare the response data
        response_data = serializer.data
        
        # Convert ID proof and resume paths to binary format if they exist
        if response_data.get('id_proof'):
            response_data['id_proof'] = image_path_to_binary(response_data['id_proof'])
        else:
            response_data['id_proof'] = None  # Set to None if no ID proof

        if response_data.get('resume'):
            response_data['resume'] = file_path_to_binary(response_data['resume'])
        else:
            response_data['resume'] = None  # Set to None if no resume

        # Process seller-related fields
        if response_data.get('sellers'):
            for seller in response_data['sellers']:
                if seller.get('product_image'):
                    seller['product_image'] = image_path_to_binary(seller['product_image'])
                if seller.get('product_video'):
                    seller['product_video'] = video_path_to_binary(seller['product_video'])
                if seller.get('product_certification'):
                    seller['product_certification'] = image_path_to_binary(seller['product_certification'])
        
        # Return the serialized data
        return Response(response_data, status=status.HTTP_200_OK)
    

    # def put(self, request, id):
    #     # Ensure the id matches the user being updated
    #     instance = get_object_or_404(User, id=id)

    #     # Allow incoming data without the user field
    #     mutable_data = request.data.copy()

    #     id_proof = mutable_data.get('id_proof')
    #     resume = mutable_data.get('resume')

    #     serializer = self.get_serializer(instance, data=mutable_data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()

    #     # Profile Pic handling
    #     if id_proof and id_proof != "null":
    #         saved_location = save_image_to_azure(id_proof, serializer.instance.id, serializer.instance.full_name, 'id_proof')
    #         if saved_location:
    #             serializer.instance.id_proof = saved_location
    #     else:
    #         serializer.instance.id_proof = None

    #     # Certificate handling
    #     if resume and resume != "null":
    #         saved_location = save_image_to_azure(resume, serializer.instance.id, serializer.instance.full_name, 'resume')
    #         if saved_location:
    #             serializer.instance.resume = saved_location
    #     else:
    #         serializer.instance.resume = None

    #     serializer.instance.save()

    #     # Update response data
    #     response_data = serializer.data

    #     # Set id_proof and resume to None if they are null in the request
    #     if not id_proof or id_proof == "null":
    #         response_data['id_proof'] = None
    #     if not resume or resume == "null":
    #         response_data['resume'] = None

    #     return Response(response_data, status=status.HTTP_200_OK)

    
    def put(self, request, id):
        # Ensure the id matches the user being updated
        instance = get_object_or_404(User, id=id)

        # Allow incoming data without the user field
        mutable_data = request.data.copy()

        id_proof = mutable_data.get('id_proof')
        resume = mutable_data.get('resume')

        serializer = self.get_serializer(instance, data=mutable_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Profile Pic handling
        if id_proof and id_proof != "null":
            saved_location = save_image_to_azure(id_proof, serializer.instance.id, serializer.instance.full_name, 'id_proof')
            if saved_location:
                serializer.instance.id_proof = saved_location
        else:
            serializer.instance.id_proof = None

        # Certificate handling
        if resume and resume != "null":
            saved_location = save_image_to_azure(resume, serializer.instance.id, serializer.instance.full_name, 'resume')
            if saved_location:
                serializer.instance.resume = saved_location
        else:
            serializer.instance.resume = None

        # Ensure is_member is set to true
        serializer.instance.is_member = MemberStatus.true.value
        serializer.instance.save()

        # Update response data
        response_data = serializer.data

        # Set id_proof and resume to None if they are null in the request
        if not id_proof or id_proof == "null":
            response_data['id_proof'] = None
        if not resume or resume == "null":
            response_data['resume'] = None

        return Response(response_data, status=status.HTTP_200_OK)

        



class ProfileView(generics.GenericAPIView):
    serializer_class = RegisterSerializer1

    def get(self, request, id):
        # Fetch the user by ID
        user = get_object_or_404(User, id=id)

        # Serialize the user instance
        serializer = self.get_serializer(user)

        # Prepare the response data
        response_data = serializer.data

        # Convert ID proof and resume paths to binary format if they exist
        if response_data.get('id_proof'):
            response_data['id_proof'] = image_path_to_binary(response_data['id_proof'])
        else:
            response_data['id_proof'] = None  # Set to None if no ID proof

        if response_data.get('resume'):
            response_data['resume'] = file_path_to_binary(response_data['resume'])
        else:
            response_data['resume'] = None  # Set to None if no resume

        # Return the serialized data
        return Response(response_data, status=status.HTTP_200_OK)
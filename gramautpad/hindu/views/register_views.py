


# from rest_framework import generics, status
# from rest_framework.response import Response
# from django.shortcuts import get_object_or_404
# from ..utils import image_path_to_binary,file_path_to_binary
# from ..serializers import RegisterSerializer
# from ..models import Register









# class RegisterUpdate(generics.GenericAPIView):
#     # permission_classes = [IsAuthenticated]
#     serializer_class = RegisterSerializer




#     def get(self, request, id):
#         # Fetch the register instance based on the provided ID
#         instance = get_object_or_404(Register, id=id)
        
#         # Serialize the instance
#         serializer = self.get_serializer(instance)
        
#         # Prepare the response data
#         response_data = serializer.data
        
#         # Convert ID proof and resume paths to binary format if they exist
#         if response_data.get('id_proof'):
#             response_data['id_proof'] = image_path_to_binary(response_data['id_proof'])
#         else:
#             response_data['id_proof'] = None  # Set to None if no ID proof

#         if response_data.get('resume'):
#             response_data['resume'] = file_path_to_binary(response_data['resume'])
#         else:
#             response_data['resume'] = None  # Set to None if no resume
        
#         # Return the serialized data
#         return Response(response_data, status=status.HTTP_200_OK)
    

#     def put(self, request, id):
#         # Ensure the id matches the user being updated
#         instance = get_object_or_404(Register, id=id)

#         # Allow incoming data without the user field
#         mutable_data = request.data.copy()

#         id_proof = mutable_data.get('id_proof')
#         resume = mutable_data.get('resume')

#         serializer = self.get_serializer(instance, data=mutable_data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()

#         # Profile Pic handling
#         if id_proof and id_proof != "null":
#             saved_location = save_image_to_azure(id_proof, serializer.instance.id, serializer.instance.full_name, 'id_proof')
#             if saved_location:
#                 serializer.instance.id_proof = saved_location
#         else:
#             serializer.instance.id_proof = None

#         # Certificate handling
#         if resume and resume != "null":
#             saved_location = save_image_to_azure(resume, serializer.instance.id, serializer.instance.full_name, 'resume')
#             if saved_location:
#                 serializer.instance.resume = saved_location
#         else:
#             serializer.instance.resume = None

#         serializer.instance.save()

#         # Update response data
#         response_data = serializer.data

#         # Set id_proof and resume to None if they are null in the request
#         if not id_proof or id_proof == "null":
#             response_data['id_proof'] = None
#         if not resume or resume == "null":
#             response_data['resume'] = None

#         return Response(response_data, status=status.HTTP_200_OK)
    



# class ProfileView(generics.GenericAPIView):
#     serializer_class = RegisterSerializer

#     def get(self, request, id):
#         # Fetch the user by ID
#         user = get_object_or_404(Register, id=id)

#         # Serialize the user instance
#         serializer = self.get_serializer(user)

#         # Prepare the response data
#         response_data = serializer.data

#         # Convert ID proof and resume paths to binary format if they exist
#         if response_data.get('id_proof'):
#             response_data['id_proof'] = image_path_to_binary(response_data['id_proof'])
#         else:
#             response_data['id_proof'] = None  # Set to None if no ID proof

#         if response_data.get('resume'):
#             response_data['resume'] = file_path_to_binary(response_data['resume'])
#         else:
#             response_data['resume'] = None  # Set to None if no resume

#         # Return the serialized data
#         return Response(response_data, status=status.HTTP_200_OK)
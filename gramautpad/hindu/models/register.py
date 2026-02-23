# # import uuid
# # from django.db import models
# # from ..enums.user_status_enum import UserStatus
# # from ..enums.member_status_enum import MemberStatus
# # from ..enums.id_type_enum import IDType
# # from ..enums.geosite_enum import GeoSite
# # from ..enums.stakeholder_type_enum import StakeholderType
# # from ..enums.qualification_enum import HighestEducationQualification
# # from ..enums.working_professional_enum import WorkingProfessional
# # from ..enums import MemberStatus
# # from ..utils import validate_id_number
# # from ..enums.gender_enum import Gender




# # class Register(models.Model):
# #     _id = models.CharField(db_column='_id', primary_key=True, max_length=45, default=uuid.uuid1, editable=False)
# #     full_name = models.CharField(db_column='full_name', max_length=45, blank=True, null=True) 
# #     surname = models.CharField(db_column='surname',max_length=100,null=True,blank=True)

# #     gender = models.CharField(max_length=50, choices=[(e.name, e.value) for e in Gender], default=Gender.MALE.value)
# #     age = models.CharField(max_length=100, null=True)
# #     contact_number = models.CharField(max_length=10, null=True, blank=True)
# #     email = models.EmailField(max_length=50, null=True, blank=True)
# #     address = models.TextField(null=True, blank=True)

# #     id_type = models.CharField(max_length=50, choices=[(e.name, e.value) for e in IDType], null=True,blank=True)
# #     id_number = models.CharField(max_length=50, null=True, blank=True)
# #     id_proof = models.TextField(null=True, blank=True)
# #     object_id = models.ForeignKey('Village', db_column='object_id', on_delete=models.SET_NULL, null=True, blank=True, related_name='registers')

# #     stakeholder_type = models.CharField(max_length=50, choices=[(e.name, e.value) for e in StakeholderType], default=StakeholderType.NONE.value)
# #     highest_education_qualification = models.CharField(max_length=50, choices=[(e.value, e.name) for e in HighestEducationQualification], default=HighestEducationQualification.CLASS_10.value, null=True, blank=True)
    
# #     is_working_professional = models.CharField(max_length=3, choices=[(e.value, e.value) for e in WorkingProfessional], default=WorkingProfessional.NO.value, null=True, blank=True)
# #     years_of_work_experience = models.IntegerField(null=True, blank=True)
# #     resume = models.TextField(null=True, blank=True)
# #     is_member=models.CharField(max_length=50,choices=[(e.name,e.value) for e in MemberStatus],default=MemberStatus.false.value)
# #     account_type= models.CharField(max_length=100)
# #     pincode =models.CharField(max_length=10,null=True,blank=True)
# #     family_images = models.JSONField(default=list, blank=True)








# from django.db import models
# import uuid
# from ..utils import validate_id_number  
# from ..enums.gender_enum import Gender
# from ..enums.id_type_enum import IDType 
# from .village import Village
# from ..enums.geosite_enum import GeoSite
# from ..enums.stakeholder_type_enum import StakeholderType 
# from ..enums.qualification_enum import HighestEducationQualification
# from ..enums.working_professional_enum import WorkingProfessional
# from .user import User 


# class Register(models.Model):
#     id = models.CharField(db_column='_id', primary_key=True, max_length=45, default=str(uuid.uuid1()), editable=False)
#     full_name = models.CharField(db_column='full_name', max_length=45, blank=True, null=True) 
#     gender = models.CharField(max_length=50, choices=[(e.name, e.value) for e in Gender], default=Gender.MALE.value)
#     age = models.CharField(max_length=100, null=True)
#     contact_number = models.CharField(max_length=10, null=True, blank=True)
#     email = models.EmailField(db_column='email', max_length=50, null=True, blank=True)
#     address = models.TextField(null=True, blank=True)
#     id_type = models.CharField(max_length=50, choices=[(e.name, e.value) for e in IDType], null=True,blank=True)  
#     id_number = models.CharField(max_length=50, null=True, blank=True)
#     id_proof = models.TextField(null=True, blank=True)
#     geo_site = models.CharField(max_length=50, choices=[(e.name, e.value) for e in GeoSite], default=GeoSite.VILLAGE.value)
#     object_id = models.ForeignKey(Village, db_column='object_id', on_delete=models.SET_NULL, null=True, blank=True, related_name='registers') 
#     stakeholder_type = models.CharField(max_length=50, choices=[(e.name, e.value) for e in StakeholderType], default=StakeholderType.BUYER.value)
#     highest_education_qualification = models.CharField(max_length=50, choices=[(e.value, e.name) for e in HighestEducationQualification], default=HighestEducationQualification.CLASS_10.value, null=True, blank=True)    
#     is_working_professional = models.CharField(max_length=3, choices=[(e.value, e.value) for e in WorkingProfessional], default=WorkingProfessional.NO.value, null=True, blank=True)
#     years_of_work_experience = models.CharField(null=True, blank=True,max_length=100)
#     resume = models.TextField(null=True, blank=True)
#     user = models.ForeignKey(User, db_column='user_id', on_delete=models.CASCADE, related_name='registers',null=True,blank=True)  # Add foreign key to User
#     pincode =models.CharField(max_length=10,null=True,blank=True)




#     def clean(self):
#         """Custom validation for ID number based on ID type."""
#         if self.id_number and self.id_type:
#             validate_id_number(self.id_number, self.id_type)

#     class Meta:
#         managed = False
#         db_table = 'register'


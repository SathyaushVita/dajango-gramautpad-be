from django.urls import path, include  
from .views import * 
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)
router.register(r'state', StateViews)
router.register(r'countries', CountryView)
router.register(r'district', DistrictVIew)
router.register(r'block', BlockView)
router.register(r'village', VillageView)
router.register(r'maincategory',MainCategoryView)
router.register(r'category',CategoryView)
router.register(r'subcategory',SubCategoryView)
router.register(r'product',ProductView)
# router.register(r'register',RegisterViewSet)
router.register(r'seller_addproduct',SellerViewSet)
router.register(r'wishlist',WishlistViews)
router.register(r'reviews', ReviewViewSet)
# router.register(r'cart', CartViewSet, basename='cart')




urlpatterns = [
    path('login', Register_LoginView.as_view(), name="register"),
    path('verify_login', Validate_LoginOTPView.as_view(), name="verify_login"),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('locationbyproducts', GetSellersByLocation.as_view(), name='get-products-by-location'),
    # path('states_by_country/<str:country>',states_by_country.as_view()),
    # path('districts_by_state/<str:state>', districts_By_State.as_view(), name='districts_by_state'),
    # path('blocks-by-district/<str:district>', blocks_By_District.as_view(), name='blocks-by-district'),
    # path('village-by-block/<str:block>', villages_By_Block.as_view()),
    path('main-categories-hierarchy', MainCategoryHierarchyView.as_view(), name='main-category-hierarchy'),
    # path('registerupdate/<str:id>', RegisterUpdate.as_view()),
    path('updateregister/<str:id>',RegisterUpdate.as_view()),
    path('profile/<uuid:id>', ProfileView.as_view(), name='profile-by-id'), 
    path('cart', CartListCreateView.as_view(), name='cart-list-create'),
    path('cart/<str:_id>', CartDetailView.as_view(), name='cart-detail'),
    path('GetproductsByLocation', GetproductsByLocation.as_view(), name='get-products-by-location'),



    




    path('', include(router.urls)),  
]

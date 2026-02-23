from .user_views import Register_LoginView,Validate_LoginOTPView,RegisterUpdate,ProfileView
from .country_views import CountryView
from .state_views import StateViews,states_by_country
from  .district_views import DistrictVIew,districts_By_State
from .block_views import BlockView,blocks_By_District
from .village_views import VillageView,villages_By_Block
from .main_category_views import MainCategoryView
from .category_views import CategoryView
from .sub_category_views import SubCategoryView
from .product_views import ProductView
# from .register_views import RegisterViewSet
from .seller_product_views import SellerViewSet,GetSellersByLocation,GetproductsByLocation
from .dropdown_views import MainCategoryHierarchyView
from .wishlist_views import WishlistViews
from .reviews_views import ReviewViewSet
from .cart_views import CartDetailView,CartListCreateView
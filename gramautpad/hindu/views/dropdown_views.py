from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import MainCategory, Category, SubCategory


from ..serializers import SubCategorySerializer1

class MainCategoryHierarchyView(APIView):

    def get(self, request, *args, **kwargs):
        main_categories = MainCategory.objects.all()

        result = []

        # Loop through all main categories and build the hierarchy
        for main_category in main_categories:
            # For each MainCategory, get related Categories
            categories = Category.objects.filter(main_category=main_category)
            category_data = []

            for category in categories:
                # For each Category, get related SubCategories
                subcategories = SubCategory.objects.filter(category_id=category)
                # Serialize SubCategories using SubCategorySerializer1
                subcategory_data = SubCategorySerializer1(subcategories, many=True).data

                # Append Category data along with serialized SubCategories
                category_data.append({
                    'id': category._id,
                    'name': category.name,
                    'subcategories': subcategory_data
                })

            # Append MainCategory data along with Categories
            result.append({
                'id': main_category._id,
                'name': main_category.name,
                'categories': category_data
            })

        # Return the final hierarchical response
        return Response(result)
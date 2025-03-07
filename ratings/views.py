from django.shortcuts import get_object_or_404
from django.db.models import Avg
from django.db.models.functions import Round
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .models import Professor, Module, ModuleInstance, Rating


# register
class RegisterUser(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email")


        if not username or not password or not email:
            return Response({"error": "All fields must be filled."}, status=400)
        
        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists."}, status=400)
        
        if User.objects.filter(email=email).exists():
            return Response({"error": "Email already exists."}, status=400)
        
        user = User.objects.create_user(username=username, password=password, email=email)
        return Response({"message": "User registered!"}, status=201)
    

# login
class LoginUser(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Username or password required."}, status=400)
        
        user = authenticate(username=username, password=password)

        if user is None:
            return Response({"error": "Invalid username or password."}, status=400)

        token, created = Token.objects.get_or_create(user=user)

        return Response({"message": "Login successful!", "token": token.key}, status=200)


# logout
class LogoutUser(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.auth.delete()
        return Response({"message": "Logout successful!"}, status=200)
    

# show module instances
class ModuleInstanceList(APIView):
    def get(self, request):
        module_instances = ModuleInstance.objects.all()
        data = []
        for instance in module_instances:
            professors = instance.professor.all().values("code", "name")  # many to many field
            data.append({
                "module_code": instance.module.code,
                "module_name": instance.module.name,
                "year": instance.year,
                "semester": instance.semester,
                "professors": list(professors)
            })
        return Response(data)


# show all professor ratings
class ProfessorRating(APIView):
    def get(self, request):
        ratings = Rating.objects.values("professor__code", "professor__name").annotate(avg_rating=Round(Avg("rating")))
        return Response(list(ratings))  


# show average professor ratings for a specific module
class ProfessorModuleRating(APIView):
    def get(self, request, professor_code, module_code):
        # fetch professor and module objects
        professor = get_object_or_404(Professor, code=professor_code)
        module = get_object_or_404(Module, code=module_code)

        # calculate the average rating for the given professor in the specified module
        avg_rating = Rating.objects.filter(professor__code=professor_code, module_instance__module__code=module_code).aggregate(avg_rating=Round(Avg("rating")))["avg_rating"]

        if avg_rating is not None:
            avg_rating = round(avg_rating, 2)  
            return Response({
                "professor_id": professor_code,
                "professor_name": professor.name,
                "module_code": module_code,
                "module_name": module.name,
                "average_rating": avg_rating
            })
        else:
            return Response({
                "professor_id": professor_code,
                "module_code": module_code,
                "error": "No ratings found for this professor in this module."
            }, status=404)


# rate a professor
class RateProfessor(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        professor_code = request.data.get("professor_id")  
        module_code = request.data.get("module_code")
        year = request.data.get("year")
        semester = request.data.get("semester")
        rating = request.data.get("rating")

        professor = get_object_or_404(Professor, code=professor_code)
        module = get_object_or_404(Module, code=module_code)

        # validate year
        try:
            year = int(year)
            if year < 2000 or year > 2025: 
                return Response({"error": "Invalid year. Must be between 2000 and 2025."}, status=400)
        except ValueError:
            return Response({"error": "Invalid year format. Must be a number."}, status=400)

        # validate semester
        try:
            semester = int(semester)
            if semester not in [1, 2]:
                return Response({"error": "Invalid semester. Must be 1 or 2."}, status=400)
        except ValueError:
            return Response({"error": "Invalid semester format. Must be a number."}, status=400)

        try:
            rating_value = int(rating)
            if not (1 <= rating_value <= 5):
                return Response({"error": "Rating must be between 1 and 5."}, status=400)
        except ValueError:
            return Response({"error": "Invalid rating value. Must be a number between 1 and 5."}, status=400)

        # check if the module instance exists
        module_instance = ModuleInstance.objects.filter(module=module, year=year, semester=semester).first()
        if module_instance is None:
            return Response({"error": "Module instance not found."}, status=404)
        
        # create the rating
        Rating.objects.create(professor=professor, module_instance=module_instance, rating=rating_value)

        return Response({"message": "Your rating has been submitted."}, status=201)

from os import name
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from rest_framework.views import APIView
from .models import Project
from rest_framework import viewsets
from rest_framework import authentication, permissions
from .serializers import UserSerializer, ProjectSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from rest_framework import status

# Create your views here.
def index(request):
    return HttpResponse("There index of acces to projects.")

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class ProjectViewApi(APIView):
    """
    API endpoint that allows users to see their projects.
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, format=None):
        """
        Return a list of user's projects.
        """
        #print(request.auth)
        _user = Token.objects.get(key=request.auth).user
        projects = [project.name for project in Project.objects.filter(author=_user)]
        return Response(projects)

class ProjectDownload(APIView):
    """
    API endpoint that allows users to see their projects.
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, format=None):
        """
        Return a project file .
        """
        #print(request.auth)
        _user = Token.objects.get(key=request.auth).user
        _name = request.query_params["name"]
        project = Project.objects.filter(author=_user, name = _name)
        #print(project[0].file)
        #print(str(project[0].file)[9:])
        #'C:\\Users\\tkorg\\Projects\\DragonNotes\\dragonnotes\\media\\'
        with open(settings.MEDIA_ROOT+"\\"+str(project[0].file), 'rb') as file:
            response = HttpResponse(file, content_type='zip')
            response['Content-Disposition'] = 'attachment; filename='+ str(project[0].file)[9:]
            return response
        #return Response(projects)

class FileView(APIView):
  authentication_classes = [authentication.TokenAuthentication]
  permission_classes = [permissions.IsAuthenticated]
  parser_classes = [FileUploadParser]

  def post(self, request, *args, **kwargs):
    print(request.data["file"])

    _user = Token.objects.get(key=request.auth).user
    _name = request.query_params["name"]
    _data = { "name":request.query_params["name"], "author":_user.id, "file":request.data["file"]}
    
    project = Project.objects.filter(author=_user, name = _name)
    if not project:
        project_serializer = ProjectSerializer(data=_data)
        if project_serializer.is_valid():
            project_serializer.save()
            return Response(project_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(project_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        project[0].file = request.data["file"]
        if project[0]:
            project[0].save()
            return Response(project[0].name, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(project[0].errors, status=status.HTTP_400_BAD_REQUEST)
    
#test
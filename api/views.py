from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProjectSerializer
from projects.models import Project


@api_view(['GET'])
def getRoutes(request):
    routes =[
         {'GET':'/api/projects'},
         {'GET':'/api/projects/id'},
         {'POST':'/api/projects/id/vote'},

         {'POST':'/api/users/token'},
         {'POST':'/api/users/token/refresh'},
    ]
    
    return Response(routes)


# برای اینکه با قالب بندی ها نمایش بزاریم و در واقع بتونیم از Response استفاده کنیم
# فقط به ریکوست گت اجازه میده
@api_view(['GET'])
def getProjects(request):
     projects = Project.objects.all()
     # تبدیل به جی سون 
     # many -> 2,3,4,...
     serializer = ProjectSerializer(projects,many=True).data

     return Response(serializer)

@api_view(['GET'])
def getProject(request,pk):
     project = Project.objects.get(id=pk)
     serializer = ProjectSerializer(project,many=False).data

     return Response(serializer)
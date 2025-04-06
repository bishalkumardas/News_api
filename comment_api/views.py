from .models import Comment, News
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse, JsonResponse
from .serializers import CommentSerializer, NewsSerializer
from rest_framework.parsers import JSONParser
import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework.pagination import PageNumberPagination
# Create your views here.
def view_comments(request):
    
    # get all Comment
    all_comments = Comment.objects.all().order_by('-id')
    serializer = CommentSerializer(all_comments, many=True)
    json_dt=JSONRenderer().render(serializer.data)
    
    return HttpResponse(json_dt, content_type='application/json') # content_type='application/json' is responsible for returning the data in json format

# saving data in database
@csrf_exempt 
def create_comment(request):
    if request.method == 'POST':
        try:
            data = JSONParser().parse(request) #convert json data to python dictionary
            serializer = CommentSerializer(data=data) #validate data
            if serializer.is_valid():
                serializer.save() #save data in database
                return JsonResponse({"message": "Comment saved successfully!"}, status=201)
            return JsonResponse(serializer.errors, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        

#pagination code
# class NewsPagination(PageNumberPagination):
#     page_size = 10
#     page_size_query_param = 'page_size' #user can modify page size
#     max_page_size=10 #max size


# ModelViewSet automatically provides all CRUD operations (GET, POST, PUT, PATCH, DELETE).
class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all().order_by('-id')
    serializer_class = NewsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['sentiment'] 
    # pagination_class = NewsPagination

# def single_comment(request, pk):
#     print(pk)
#     single_comment = Comment.objects.get(id=pk)
#     print(single_comment)
#     serializer = CommentSerializer(single_comment)
#     json_dt=JSONRenderer().render(serializer.data)
#     return HttpResponse(json_dt, content_type='application/json')
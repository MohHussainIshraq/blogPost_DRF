from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404
from .permissions import IsPublisherOrReadOnly
from .models import Post
from .serializers import PostSerializer
from .pagination import StandardResultsSetPagination


class PostListView(APIView, StandardResultsSetPagination):
    serializer_class = PostSerializer

    def get(self, request):
        queryset = Post.objects.filter(is_public=True)
        result = self.paginate_queryset(queryset, request)
        serializer = PostSerializer(instance=result, many=True)
        return self.get_paginated_response(serializer.data)


class PostCreateView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['publisher'] = request.user
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetailView(APIView):
    permission_classes = [IsAuthenticated, IsPublisherOrReadOnly]
    serializer_class = PostSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get_object(self):
        obj = get_object_or_404(Post.objects.all(), id=self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, pk):
        post = self.get_object()
        serializer = PostSerializer(instance=post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        post = Post.objects.get(id=pk)
        serializer = PostSerializer(data=request.data, instance=post)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        post = Post.objects.get(id=pk)
        post.delete()
        return Response({'success': True}, status=status.HTTP_200_OK)


class PostSearch(APIView):
    def get(self, request):
        q = request.query_params.get('q')
        queryset = Post.objects.filter(title__icontains=q)
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)









from rest_framework import generics
from rest_framework import viewsets, status
from rest_framework.response import Response
# from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from .models import *
from .serializers import *

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.filter(is_deleted__in = [False],is_active__in = [True]).order_by('-id')
    serializer_class = PostSerializer

    def list(self, request):
        if 'author' in self.request.GET:
            temp_obj = Post.objects.filter(author=request.GET["author"],is_deleted__in = [False])
            serializer = PostSerializer(temp_obj, many=True)
            if serializer.data:
                return Response({"status": "success", "data": {'items': serializer.data}}, status=status.HTTP_200_OK)
            else:
                return Response({"status":"Record Not Available"}, status=status.HTTP_404_NOT_FOUND)
        else:    
            temp_obj = Post.objects.filter(is_deleted__in = [False],is_active__in = [True]).order_by('-id')
            serializer = PostSerializer(temp_obj, many=True)
            if serializer.data:
                return Response({"status": "success", "data": {'items': serializer.data}}, status=status.HTTP_200_OK)
            else:
                return Response({"status":"Record Not Available"}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status":"Record Added Successfully"},status=status.HTTP_201_CREATED)
        else:
            return Response({"status":status.HTTP_400_BAD_REQUEST,"message":serializer.errors},status=status.HTTP_400_BAD_REQUEST)       
    
    def update(self, request, pk=None, partial=True):  
        temp_obj = Post.objects.get(id=pk)
        serializer = PostSerializer(temp_obj,data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status":"Record Updated Successfully"},status=status.HTTP_201_CREATED)
        else:
            return Response({"status":status.HTTP_400_BAD_REQUEST,"message":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self):
        return Response({"status":"Record Deleted Successfully"},status=status.HTTP_204_NO_CONTENT)
    
class LikeListView(generics.ListAPIView):
    serializer_class = LikeSerializer

    def get_queryset(self):
        post_id = self.kwargs.get('pk')
        return Like.objects.filter(post=post_id)
    
class LikeCreateView(generics.CreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    
    def create(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        if Like.objects.filter(post=post, author=request.data["author"]).exists():
            return Response({'detail': 'You have already liked this post.'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(post=post)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class LikeDestroyView(generics.DestroyAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def destroy(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        user_id = self.kwargs['user_id']
        like = Like.objects.filter(post=post, author=user_id)
        if not like.exists():
            return Response({'detail': 'You have not liked this post.'}, status=status.HTTP_400_BAD_REQUEST)
        like.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
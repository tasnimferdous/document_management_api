from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import(
    Document,
)

from .serializers import(
    UserSerializer,
    DocumentSerializer,
)

# Create your views here.
class SignUpView(APIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SignInView(APIView):
    serializer_class = UserSerializer
    permission_classes = []

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            response = {
                "message": "Login Successfull",
                "tokens": user.auth_token.key,
            }
            return Response(data=response, status=status.HTTP_200_OK)
        return Response(data={"message": "Invalid email or password"})


class DocumentView(APIView):
    # 23b82fbe4c42bf900506f69217ea205b2ab33b52
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = DocumentSerializer

    def get(self, request):
        #If the user is authenticated as a staff member then he can access all the documents
        if request.user.is_staff:
            documents = Document.objects.all()

        #If the user is authenticated as a common member
        else:
            #All the documents owned by the user
            owner_docs = Document.objects.filter(owner=request.user)

            #Find all the documents those are shared with him
            #At first let's assume that all the documents are shared with him
            shared_docs = Document.objects.all()
            for doc in shared_docs:
                #Share mode off
                share_mode = 0
                users = doc.shared_users.all()
                for user in users:
                    #if a document is shared with the user then share_mode is on for him
                    if user == request.user and user!=doc.owner:
                        share_mode = 1
                        break
                #Exclude one by one document which is not shared with him
                if share_mode == 0:
                    shared_docs = shared_docs.exclude(id = doc.id)
            #Union of owned documents and the documents are shared with him
            documents = owner_docs|shared_docs
        serializer = DocumentSerializer(documents, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DocumentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DocumentDetailView(APIView):
    # 08eb61397a05742201afe22599ff3c645d6d63e4
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = DocumentSerializer

    def get(self, request, pk):
        try:
            document = Document.objects.get(pk=pk)
            users = document.shared_users.all()
            share_mode = 0
            for user in users:
                #if the document is shared with the user then share_mode is on for him
                if user == request.user:
                    share_mode = 1
                    break

            if document.owner != request.user and share_mode == 0:
                return Response({'Error':'You are not allowed to view this document'}, status=status.HTTP_401_UNAUTHORIZED)
        except Document.DoesNotExist:
            return Response({'Error':'Document not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = DocumentSerializer(document)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            document = Document.objects.get(pk=pk)
            if document.owner != request.user:
                return Response({'Error':'You are not allowed to edit this document'}, status=status.HTTP_401_UNAUTHORIZED)
        except Document.DoesNotExist:
            return Response({'Error':'document not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = DocumentSerializer(document, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            document = Document.objects.get(pk=pk)
            if document.owner != request.user:
                return Response({'Error':'You are not allowed to delete this document'}, status=status.HTTP_401_UNAUTHORIZED)
        except Document.DoesNotExist:
            return Response({'Error':'document not found'}, status=status.HTTP_404_NOT_FOUND)
        document.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

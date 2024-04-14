from rest_framework import views
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Photo
import cloudinary.uploader
from .serializers import PhotoSerializer

class PhotoAPIView(views.APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        photos = Photo.objects.all()
        serializer = PhotoSerializer(photos, many=True)
        return Response({'message': 'Get all photos successfully!', 'data': serializer.data}, status=200)

    def post(self, request):
        if 'uploadImages' not in request.FILES:
            return Response({'message': 'No upload resource', 'error': 'No image file found in request'}, status=400)

        images = request.FILES.getlist('uploadImages')
   
      
        data = []
        print(images)
        for image in images:
            try:
                upload_result = cloudinary.uploader.upload(image)
                print("===========")
                print(upload_result)
                img_obj = Photo(
                    id=upload_result['public_id'],
                    url=upload_result['secure_url'],
                    filename=upload_result['original_filename'],
                    format=upload_result['format'],
                    width=upload_result['width'],
                    height=upload_result['height'],
                    created_at=upload_result['created_at'],
                )
                img_obj.save()
                serializer = PhotoSerializer(img_obj)
                data.append(serializer.data)
            except Exception as e:
                return Response({'message': 'Upload images failed!', 'error': str(e)}, status=400)
        
        return Response({'message': 'Upload images successfully!', 'data': data}, status=200)

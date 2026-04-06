from rest_framework import generics, permissions, parsers, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from supabase import create_client
import uuid

from .models import MediaVault
from .serializers import MediaVaultSerializer, MediaVaultUploadSerializer

# Supabase client — created once
supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)


def upload_to_supabase(file, media_type):
    """Upload a file to Supabase storage and return its public URL."""
    ext = file.name.split('.')[-1]
    filename = f"{media_type}/{uuid.uuid4()}.{ext}"
    file_bytes = file.read()

    supabase.storage.from_("media").upload(
        filename,
        file_bytes,
        {"content-type": file.content_type}
    )

    url = supabase.storage.from_("media").get_public_url(filename)
    return url


class MediaVaultListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    def get_queryset(self):
        qs = MediaVault.objects.filter(user=self.request.user, is_hidden=False)
        media_type = self.request.query_params.get('media_type')
        if media_type:
            qs = qs.filter(media_type=media_type)
        return qs

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return MediaVaultUploadSerializer
        return MediaVaultSerializer

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['request'] = self.request
        return ctx

    def perform_create(self, serializer):
        file = self.request.FILES.get('file')
        media_type = self.request.data.get('media_type', 'image')

        file_url = upload_to_supabase(file, media_type)

        # Save without the file field — just the URL
        serializer.save(user=self.request.user, file_url=file_url)


class MediaVaultDetailView(generics.RetrieveDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MediaVaultSerializer

    def get_queryset(self):
        return MediaVault.objects.filter(user=self.request.user)

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['request'] = self.request
        return ctx


class HiddenVaultView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, slug):
        items = MediaVault.objects.filter(
            user=request.user,
            is_hidden=True
        )
        data = [
            {
                'id': str(item.id),
                'file_url': item.file_url,   # now a direct Supabase URL, no build_absolute_uri needed
                'media_type': item.media_type,
                'caption': item.caption,
            }
            for item in items
        ]
        return Response(data)
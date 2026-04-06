from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin

# class UpdateLastSeenMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         response = self.get_response(request)

#         # Update last_seen only for authenticated API requests
#         if request.path.startswith('/api/') and hasattr(request, 'user') and request.user.is_authenticated:
#             # Avoid import cycle — import inside call
#             request.user.last_seen_at = timezone.now()
#             request.user.save(update_fields=['last_seen_at'])

#         return response
class UpdateLastSeenMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user and request.user.is_authenticated:
            request.user.__class__.objects.filter(pk=request.user.pk).update(
                last_seen_at=timezone.now()
            )
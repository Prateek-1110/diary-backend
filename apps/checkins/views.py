from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from django.db.models import Avg
from django.db.models.functions import TruncWeek, TruncMonth
from .models import MoodCheckin
from .serializers import MoodCheckinSerializer
import datetime

MOOD_SCORE_MAP = {'happy': 5, 'calm': 4, 'confused': 3, 'anxious': 2, 'sad': 2, 'angry': 1}

class MoodCheckinListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MoodCheckinSerializer

    def get_queryset(self):
        qs = MoodCheckin.objects.filter(user=self.request.user)
        days = self.request.query_params.get('days')
        if days:
            cutoff = timezone.now() - datetime.timedelta(days=int(days))
            qs = qs.filter(checked_in_at__gte=cutoff)
        return qs

    def create(self, request, *args, **kwargs):
        already = MoodCheckin.objects.filter(
            user=request.user,
            checked_in_at__date=timezone.now().date()
        ).exists()
        if already:
            return Response(
                {'detail': 'Already checked in today.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MoodTrendView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        group_by = request.query_params.get('group_by', 'week')  # 'week' or 'month'
        trunc_fn = TruncWeek if group_by == 'week' else TruncMonth

        qs = (
            MoodCheckin.objects
            .filter(user=request.user)
            .annotate(period=trunc_fn('checked_in_at'))
            .values('period')
            .annotate(avg_score=Avg('score'))
            .order_by('period')
        )

        # dominant mood per period: separate query
        raw = MoodCheckin.objects.filter(user=request.user)
        periods = {}
        for checkin in raw:
            if group_by == 'week':
                key = checkin.checked_in_at.isocalendar()[:2]  # (year, week)
            else:
                key = (checkin.checked_in_at.year, checkin.checked_in_at.month)
            periods.setdefault(key, {})
            periods[key][checkin.mood] = periods[key].get(checkin.mood, 0) + 1

        dominant_by_period = {k: max(v, key=v.get) for k, v in periods.items()}

        result = []
        for row in qs:
            period_dt = row['period']
            if group_by == 'week':
                key = (period_dt.year, period_dt.isocalendar()[1])
            else:
                key = (period_dt.year, period_dt.month)

            result.append({
                'period': period_dt.isoformat(),
                'avg_score': round(row['avg_score'], 2),
                'dominant_mood': dominant_by_period.get(key, None),
            })

        return Response(result)
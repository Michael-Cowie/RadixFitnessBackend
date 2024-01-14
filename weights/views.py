from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Weights
from .serializers import WeightTrackingSerializer


def _get_all_weights_for_user(user):
    try:
        return Weights.objects.filter(user_id=user)
    except Weights.DoesNotExist:
        raise Http404


def _get_weight_for_user_on_date(user, date):
    try:
        return Weights.objects.get(user_id=user, date=date)
    except Weights.DoesNotExist:
        raise Http404


class WeightsView(APIView):

    def post(self, request):
        """
        Create a weight entry for a particular date.
        """
        data = request.data | {'user_id': request.user.id}
        serializer = WeightTrackingSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        """
        Updates an existing weight for a particular date.
        """
        weight = _get_weight_for_user_on_date(request.user, request.data['date'])
        updated_data = {
            'weight': request.data['weight'],
            'unit': request.data['unit']
        }
        serializer = WeightTrackingSerializer(weight, data=updated_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        """
        Delete a weight on a particular date.
        """
        weight = _get_weight_for_user_on_date(request.user, request.data['date'])
        weight.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AllWeightsView(APIView):

    def get(self, request):
        """
        Returns all WeightTracking entries for the particular user.
        """
        res = []
        for weight in _get_all_weights_for_user(request.user):
            serializer = WeightTrackingSerializer(weight)
            res.append(serializer.data)
        return Response(res)

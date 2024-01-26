from django.http import Http404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Weights
from .serializers import (WeightTrackingForDate, WeightTrackingNoContent,
                          WeightTrackingRequest, WeightTrackingResponse)


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

    @swagger_auto_schema(
        request_body=WeightTrackingRequest,
        responses={
            "201": openapi.Response(
                description="Successfully created a weight",
                schema=WeightTrackingResponse
            ),
            "400": "Invalid data to create Weight entry"
        }
    )
    def post(self, request):
        """
        Create a weight entry for a particular date.

        The unit of measurement used for all weights is kilograms.
        """
        request_serializer = WeightTrackingRequest(data=request.data)
        if request_serializer.is_valid():
            response_data = request.data | {'user_id': request.user.id}
            response = WeightTrackingResponse(data=response_data)
            if response.is_valid():
                response.save()
                return Response(response.data, status=status.HTTP_201_CREATED)
        return Response(request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=WeightTrackingRequest,
        responses={
            "200": openapi.Response(
                description="Successfully updated the weight",
                schema=WeightTrackingResponse
            ),
            "400": "Invalid data to update a Weight entry"
        }
    )
    def patch(self, request):
        """
        Updates an existing weight for a particular date.
        """
        weight = _get_weight_for_user_on_date(request.user, request.data['date'])
        updated_data = {}

        if updated_weight := request.data.get('weight'):
            updated_data['weight_kg'] = updated_weight

        request_serializer = WeightTrackingRequest(weight, data=updated_data, partial=True)
        if request_serializer.is_valid():
            response_data = updated_data | {'user_id': request.user.id}
            response_serializer = WeightTrackingResponse(weight, data=response_data, partial=True)
            if response_serializer.is_valid():
                response_serializer.save()
                return Response(response_serializer.data, status=status.HTTP_200_OK)
        return Response(request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=WeightTrackingForDate,
        responses={
            "204": openapi.Response(
                description="Successfully updated the weight",
                schema=WeightTrackingNoContent
            )
        }
    )
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
            serializer = WeightTrackingResponse(weight)
            res.append(serializer.data)
        return Response(res, status=status.HTTP_200_OK)

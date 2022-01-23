#from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _

#from django_filters import rest_framework as filters
#from djoser.views import UserViewSet
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

#from .models import UserSubscription
from .serializers import (SetPasswordSerializer, UserSerializer,
                         UserSubscriptionSerializer)
from .models import Follow, User
# User = get_user_model()



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(
        methods=['get'],
        detail=False,
        url_path='me',
        url_name='me',
        permission_classes=[permissions.IsAuthenticated],
    )
    def me(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=['post'],
        detail=False,
        url_path='set_password',
        url_name='set_password',
        permission_classes=[permissions.IsAuthenticated],
    )
    def set_password(self, request, *args, **kwargs):
        user = request.user
        serializer = SetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if user.check_password(
            serializer.validated_data.get('current_password')
        ):
            user.set_password(serializer.validated_data.get('new_password'))
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'current_password': 'Введен неверный пароль.'},
            status=status.HTTP_400_BAD_REQUEST)

    @action(
        methods=['get'],
        detail=False,
        serializer_class=UserSubscriptionSerializer,
        permission_classes=[permissions.IsAuthenticated],
    )
    def subscriptions(self, request):
        user = request.user
        queryset = User.objects.filter(following__author=user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=['post', 'delete'],
        url_path=r'(?P<id>[\d]+)/subscribe',
        url_name='subscribe',
        pagination_class=None,
        permission_classes=[permissions.IsAuthenticated]
    )
    def subscribe(self, request, *args, **kwargs):
        author = request.user
        user = get_object_or_404(User, id=kwargs['id'])
        subscription = Follow.objects.filter(
            subscriber=user,
            author=author
        )
        if (
            request.method == 'POST'
            and not subscription.exists()
            and user != author
        ):
            Follow.objects.create(
                subscriber=user,
                author=author
            )
            serializer = UserSubscriptionSerializer(
                user,
                context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE' and subscription.exists():
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'detail': 'Действие уже выполнено'},
            status=status.HTTP_400_BAD_REQUEST
        )




# class SubscriptionViewSet(viewsets.ModelViewSet):
#     serializer_class = SubscriptionSerializer
#     filter_backends = (filters.DjangoFilterBackend,)
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user
#         return UserSubscription.objects.filter(
#             subscriber=user).select_related('subscriber')


# class CustomUserViewSet(UserViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

#     @action(detail=True, methods=['get', 'delete'],
#             serializer_class=SubscriptionWriteSerializer,
#             permission_classes=[permissions.IsAuthenticated]
#             )
#     def subscribe(self, request, id=None):
#         user = self.request.user
#         subscription = self.get_object()

#         if request.method == 'GET':

#             if UserSubscription.objects.filter(
#                     subscriber=user,
#                     subscription=subscription).exists():
#                 return Response(
#                     _('Вы уже подписаны на этого автора'),
#                     status=status.HTTP_400_BAD_REQUEST
#                 )

#             data = {
#                 'subscriber': user.id,
#                 'subscription': subscription.id
#             }
#             serializer = self.get_serializer(data=data)
#             serializer.is_valid(raise_exception=True)
#             serializer.save()
#             headers = self.get_success_headers(serializer.data)
#             return Response(
#                 serializer.data,
#                 status=status.HTTP_201_CREATED,
#                 headers=headers
#             )

#         instance = get_object_or_404(
#             UserSubscription,
#             subscriber=user,
#             subscription=subscription
#         )
#         instance.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
import graphene
from graphene import relay
from graphene_django import DjangoObjectType

from .models import Wants


class WantsNode(DjangoObjectType):

    class Meta:
        model = Wants
        interfaces = (relay.Node, )
        fields = ['id', 'want', 'manifested_on']
        filter_fields = ['id', 'want', 'manifested_on']

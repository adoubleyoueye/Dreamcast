from graphene import ObjectType, relay
from graphene_django.filter import DjangoFilterConnectionField

from .mutations.wants import CreateWants, DeleteWants, UpdateWants
from .types import WantsNode


class Query(ObjectType):
    wants = relay.Node.Field(WantsNode)

    all_wants = DjangoFilterConnectionField(WantsNode)


class Mutation(ObjectType):
    create_wants = CreateWants.Field()

    update_wants = UpdateWants.Field()

    delete_wants = DeleteWants.Field()

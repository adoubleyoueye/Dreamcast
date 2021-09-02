import graphene
from graphene import relay
from graphql import GraphQLError
from graphql_relay import from_global_id

from dreamcast_api.models import Wants
from dreamcast_api.types import WantsNode

from .validations import validate_mutation


class WantsCreateData(graphene.InputObjectType):
    want = graphene.String()
    manifested_on = graphene.DateTime()


class WantsUpdateData(graphene.InputObjectType):
    want = graphene.String()
    manifested_on = graphene.DateTime()


class CreateWants(relay.ClientIDMutation):
    class Input:
        data = WantsCreateData()

    wants = graphene.Field(WantsNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, data=None):
        validate_dict = {
            'want': {'max': 1000, },
        }

        validate_mutation(validate_dict, data)

        if data is None:
            raise GraphQLError(f'empty data')

        obj = Wants.objects.create(**data)

        return CreateWants(wants=obj)


class UpdateWants(relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)
        data = WantsUpdateData()

    wants = graphene.Field(WantsNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, id, data):
        validate_dict = {
        }

        validate_mutation(validate_dict, data)

        obj, _ = Wants.objects.update_or_create(pk=from_global_id(id)[1], defaults=data)

        return UpdateWants(wants=obj)


class DeleteWants(relay.ClientIDMutation):
    class Input:
        id = graphene.ID()

    ok = graphene.Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, id):
        obj = Wants.objects.get(pk=from_global_id(id)[1])
        obj.delete()
        return DeleteWants(ok=True)

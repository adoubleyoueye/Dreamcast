import json
import random
from datetime import datetime

import factory
from faker import Factory
from graphene_django.utils.testing import GraphQLTestCase
from graphene_django.utils.utils import camelize
from graphql_relay import to_global_id

from dreamcast_api.models import Wants
from dreamcast_api.types import WantsNode

from .factories import WantsFactory

faker = Factory.create()


class Wants_Test(GraphQLTestCase):
    def setUp(self):
        self.GRAPHQL_URL = "/graphql"
        WantsFactory.create_batch(size=3)

    def test_create_wants(self):
        """
        Ensure we can create a new wants object.
        """

        wants_dict = camelize(factory.build(dict, FACTORY_CLASS=WantsFactory))

        response = self.query(
            """
            mutation($input: CreateWantsInput!) {
                createWants(input: $input) {
                    clientMutationId,
                    wants {
                        id
                        want
                        manifestedOn
                    }
                }
            }
            """,
            input_data={'data': wants_dict}
        )
        content = json.loads(response.content)
        generated_wants = content['data']['createWants']['wants']
        self.assertResponseNoErrors(response)
        self.assertEquals(wants_dict['want'], generated_wants['want'])
        self.assertEquals(wants_dict['manifestedOn'], generated_wants['manifestedOn'])

    def test_fetch_all(self):
        """
        Create 3 objects, fetch all using allWants query and check that the 3 objects are returned following
        Relay standards.
        """
        response = self.query(
            """
            query {
                allWants{
                    edges{
                        node{
                            id
                            want
                            manifestedOn
                        }
                    }
                }
            }
            """
        )
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        wants_list = content['data']['allWants']['edges']
        wants_list_qs = Wants.objects.all()
        for i, edge in enumerate(wants_list):
            wants = edge['node']
            self.assertEquals(wants['id'], to_global_id(WantsNode._meta.name, wants_list_qs[i].id))
            self.assertEquals(wants['want'], wants_list_qs[i].want)
            self.assertEquals(wants['manifestedOn'], wants_list_qs[i].manifested_on.isoformat())

    def test_update_mutation_correct(self):
        """
        Add an object. Call an update with 2 (or more) fields updated.
        Fetch the object back and confirm that the update was successful.
        """
        wants = WantsFactory.create()
        wants_id = to_global_id(WantsNode._meta.name, wants.pk)
        wants_dict = factory.build(dict, FACTORY_CLASS=WantsFactory)
        response = self.query(
            """
            mutation($input: UpdateWantsInput!){
                updateWants(input: $input) {
                    wants{
                        want
                        manifestedOn
                    }
                }
            }
            """,
            input_data={
                'id': wants_id,
                'data': {
                    'want': wants_dict['want'],
                    'manifestedOn': wants_dict['manifested_on'],
                }
            }
        )
        self.assertResponseNoErrors(response)
        parsed_response = json.loads(response.content)
        updated_wants_data = parsed_response['data']['updateWants']['wants']
        self.assertEquals(updated_wants_data['want'], wants_dict['want'])
        self.assertEquals(updated_wants_data['manifestedOn'], wants_dict['manifested_on'])

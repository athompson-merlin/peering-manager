import uuid
from unittest.mock import patch

from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from rest_framework import status

from extras.models import (
    IXAPI,
    ConfigContext,
    ConfigContextAssignment,
    ExportTemplate,
    JobResult,
    Webhook,
)
from peering.models import AutonomousSystem
from utils.testing import APITestCase, MockedResponse, StandardAPITestCases


class AppTest(APITestCase):
    def test_root(self):
        response = self.client.get(reverse("extras-api:api-root"), **self.header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ConfigContextTest(StandardAPITestCases.View):
    model = ConfigContext
    brief_fields = ["id", "url", "display", "name"]

    @classmethod
    def setUpTestData(cls):
        config_contexts = [
            ConfigContext(name="Test 1", data={"test": True}),
            ConfigContext(name="Test 2", data={"test": True}),
            ConfigContext(name="Test 3", data={"test": True}),
        ]
        ConfigContext.objects.bulk_create(config_contexts)

        cls.create_data = [
            {"name": "Test 4", "data": {"test": False}},
            {"name": "Test 5", "data": {"test": False}},
            {"name": "Test 6", "data": {"test": False}},
        ]


class ConfigContextAssignmentAssignmentTest(StandardAPITestCases.View):
    model = ConfigContextAssignment
    brief_fields = ["id", "url", "display", "config_context"]

    @classmethod
    def setUpTestData(cls):
        asns = [
            AutonomousSystem(name="Foo", asn=64501),
            AutonomousSystem(name="Bar", asn=64502),
        ]
        AutonomousSystem.objects.bulk_create(asns)

        config_contexts = [
            ConfigContext(name="Test 1", data={"test": True}),
            ConfigContext(name="Test 2", data={"test": True}),
            ConfigContext(name="Test 3", data={"test": True}),
            ConfigContext(name="Test 4", data={"test": False}),
            ConfigContext(name="Test 5", data={"test": False}),
            ConfigContext(name="Test 6", data={"test": False}),
        ]
        ConfigContext.objects.bulk_create(config_contexts)

        config_context_assignments = [
            ConfigContextAssignment(
                object=asns[0], config_context=config_contexts[0], weight=1000
            ),
            ConfigContextAssignment(
                object=asns[0], config_context=config_contexts[1], weight=1000
            ),
            ConfigContextAssignment(
                object=asns[0], config_context=config_contexts[2], weight=1000
            ),
        ]
        ConfigContextAssignment.objects.bulk_create(config_context_assignments)

        cls.create_data = [
            {
                "content_type": "peering.autonomoussystem",
                "object_id": asns[1].pk,
                "config_context": config_contexts[3].pk,
                "weight": 1000,
            },
            {
                "content_type": "peering.autonomoussystem",
                "object_id": asns[1].pk,
                "config_context": config_contexts[4].pk,
                "weight": 1000,
            },
            {
                "content_type": "peering.autonomoussystem",
                "object_id": asns[1].pk,
                "config_context": config_contexts[5].pk,
                "weight": 1000,
            },
        ]


class ExportTemplateTest(StandardAPITestCases.View):
    model = ExportTemplate
    brief_fields = ["id", "url", "display", "name"]

    @classmethod
    def setUpTestData(cls):
        content_type = ContentType.objects.get_for_model(AutonomousSystem)
        export_templates = [
            ExportTemplate(
                content_type=content_type,
                name="Test 1",
                template="{{ dataset | length }}",
            ),
            ExportTemplate(
                content_type=content_type,
                name="Test 2",
                template="{{ dataset | length }}",
            ),
            ExportTemplate(
                content_type=content_type,
                name="Test 3",
                template="{{ dataset | length }}",
            ),
        ]
        ExportTemplate.objects.bulk_create(export_templates)

        cls.create_data = [
            {
                "content_type": "peering.bgpgroup",
                "name": "Test 4",
                "template": "nothing to see",
            },
            {
                "content_type": "peering.bgpgroup",
                "name": "Test 5",
                "template": "nothing to see",
            },
            {
                "content_type": "peering.bgpgroup",
                "name": "Test 6",
                "template": "nothing to see",
            },
        ]


class IXAPITest(StandardAPITestCases.View):
    model = IXAPI
    brief_fields = ["id", "display", "name", "url"]
    create_data = [
        {
            "name": "IXP 4",
            "url": "https://ixp4-ixapi.example.net",
            "api_key": "key-ixp4",
            "api_secret": "secret-ixp4",
            "identity": "1234",
        },
        {
            "name": "IXP 5",
            "url": "https://ixp5-ixapi.example.net",
            "api_key": "key-ixp5",
            "api_secret": "secret-ixp5",
            "identity": "1234",
        },
        {
            "name": "IXP 6",
            "url": "https://ixp6-ixapi.example.net",
            "api_key": "key-ixp6",
            "api_secret": "secret-ixp6",
            "identity": "1234",
        },
    ]

    @classmethod
    def setUpTestData(cls):
        IXAPI.objects.bulk_create(
            [
                IXAPI(
                    name="IXP 1",
                    url="https://ixp1-ixapi.example.net/v1/",
                    api_key="key-ixp1",
                    api_secret="secret-ixp1",
                    identity="1234",
                ),
                IXAPI(
                    name="IXP 2",
                    url="https://ixp2-ixapi.example.net/v2/",
                    api_key="key-ixp2",
                    api_secret="secret-ixp2",
                    identity="1234",
                ),
                IXAPI(
                    name="IXP 3",
                    url="https://ixp3-ixapi.example.net/v3/",
                    api_key="key-ixp3",
                    api_secret="secret-ixp3",
                    identity="1234",
                ),
            ]
        )

    @patch(
        "requests.post",
        return_value=MockedResponse(
            content={"access_token": "1234", "refresh_token": "1234"}
        ),
    )
    def test_accounts(self, *_):
        ixapi = IXAPI.objects.get(name="IXP 1")
        mocked = MockedResponse(fixture="extras/tests/fixtures/ix_api/accounts.json")
        url = reverse("extras-api:ixapi-accounts")

        with patch("requests.get", return_value=mocked):
            # Query params required
            response = self.client.get(url, format="json", **self.header)
            self.assertHttpStatus(response, status.HTTP_400_BAD_REQUEST)

            # With query params
            response = self.client.get(
                url,
                data={
                    "url": ixapi.url,
                    "api_key": ixapi.api_key,
                    "api_secret": ixapi.api_secret,
                },
                format="json",
                **self.header
            )
            self.assertHttpStatus(response, status.HTTP_200_OK)
            self.assertListEqual(mocked.json(), response.json())


class JobResultTest(
    StandardAPITestCases.GetObjectView, StandardAPITestCases.ListObjectsView
):
    model = JobResult
    brief_fields = ["id", "url", "created", "completed", "user", "status"]

    @classmethod
    def setUpTestData(cls):
        JobResult.objects.create(
            name="test",
            obj_type=ContentType.objects.get_for_model(JobResult),
            user=None,
            job_id=uuid.uuid4(),
        )


class WebhookTest(StandardAPITestCases.View):
    model = Webhook
    brief_fields = ["id", "name", "url"]
    create_data = [
        {"name": "Webhook 4", "type_create": True, "url": "http://example.com/?4"},
        {"name": "Webhook 5", "type_update": True, "url": "http://example.com/?5"},
        {"name": "Webhook 6", "type_delete": True, "url": "http://example.com/?6"},
    ]
    bulk_update_data = {"ssl_verification": False}

    @classmethod
    def setUpTestData(cls):
        webhooks = (
            Webhook(name="Webhook 1", type_create=True, url="http://example.com/?1"),
            Webhook(name="Webhook 2", type_update=True, url="http://example.com/?2"),
            Webhook(name="Webhook 3", type_delete=True, url="http://example.com/?3"),
        )
        Webhook.objects.bulk_create(webhooks)

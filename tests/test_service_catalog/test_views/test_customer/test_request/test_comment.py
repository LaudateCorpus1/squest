from django.urls import reverse

from service_catalog.models import RequestMessage
from tests.test_service_catalog.base_test_request import BaseTestRequest


class CustomerRequestCommentTest(BaseTestRequest):

    def setUp(self):
        super(CustomerRequestCommentTest, self).setUp()
        # add one comment
        RequestMessage.objects.create(sender=self.standard_user,
                                      request=self.test_request,
                                      content="first test message")
        args = {
            'request_id': self.test_request.id
        }
        self.url = reverse('service_catalog:request_comment', kwargs=args)

    def _assert_can_list_comment(self):
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        self.assertTrue("messages" in response.context)
        self.assertEqual(1, len(response.context["messages"]))

    def _assert_can_add_comment(self):
        number_message_before = RequestMessage.objects.filter(request=self.test_request).count()
        data = {
            "content": "new message"
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(302, response.status_code)
        self.assertEqual(number_message_before + 1,
                          RequestMessage.objects.filter(request=self.test_request).count())

    def test_cannot_get_comment_list_when_logout(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(302, response.status_code)

    def test_admin_can_list_request_comment(self):
        self._assert_can_list_comment()

    def test_request_owner_can_list_request_comment(self):
        self.client.login(username=self.standard_user, password=self.common_password)
        self._assert_can_list_comment()

    def test_non_owner_cannot_list_request_comment(self):
        self.client.login(username=self.standard_user_2, password=self.common_password)
        args = {
            'request_id': self.test_request.id
        }
        url = reverse('service_catalog:request_comment', kwargs=args)
        response = self.client.get(url)
        self.assertEqual(403, response.status_code)

    def test_admin_can_add_request_message(self):
        self._assert_can_add_comment()

    def test_owner_can_add_request_message(self):
        self.client.login(username=self.standard_user, password=self.common_password)
        self._assert_can_add_comment()

    def test_non_owner_cannot_add_request_message(self):
        self.client.login(username=self.standard_user_2, password=self.common_password)
        data = {
            "content": "new message"
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(403, response.status_code)

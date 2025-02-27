from django.urls import reverse

from tests.test_profile.test_group.test_group_base import TestGroupBase


class TestGroupUrls(TestGroupBase):

    def setUp(self):
        super(TestGroupUrls, self).setUp()

    def test_all_get(self):
        args_user = {
            'user_id': self.my_user.id
        }
        args_group = {
            'group_id': self.my_group.id
        }
        urls_list = [
            reverse('profiles:user_by_group_list', kwargs=args_group),
            reverse('profiles:user_in_group_update', kwargs=args_group),
            reverse('profiles:group_list'),
            reverse('profiles:group_create'),
            reverse('profiles:group_edit', kwargs=args_group),
            reverse('profiles:group_delete', kwargs=args_group),
            reverse('profiles:user_in_group_remove', kwargs={**args_group, **args_user}),
        ]
        for url in urls_list:
            response = self.client.get(url)
            self.assertEqual(200, response.status_code)
        self.client.logout()
        for url in urls_list:
            response = self.client.get(url)
            self.assertEqual(302, response.status_code)

    def test_all_delete_post(self):
        args_user = {
            'user_id': self.my_user.id
        }
        args_group = {
            'group_id': self.my_group.id
        }
        urls_list = [
            reverse('profiles:user_in_group_remove', kwargs={**args_group, **args_user}),
            reverse('profiles:group_delete', kwargs=args_group)
        ]
        for url in urls_list:
            response = self.client.post(url)
            self.assertEqual(302, response.status_code)

    def test_all_post_with_data(self):
        args_group = {
            'group_id': self.my_group.id
        }
        test_list = [
            {'url': reverse('profiles:group_create'), 'data': {'name': 'group_test2'}},
            {'url': reverse('profiles:group_edit', kwargs=args_group), 'data': {'name': 'group_test_renamed'}},
            {'url': reverse('profiles:user_in_group_update', kwargs=args_group),
             'data': {'users': [self.my_user2.id, self.my_user3.id]}}
        ]
        for test in test_list:
            response = self.client.post(test['url'], data=test['data'])
            self.assertEqual(302, response.status_code)

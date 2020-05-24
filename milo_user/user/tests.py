from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from datetime import datetime
from . import views

class MiloUserTests(TestCase):
    date_now = datetime.today().date()

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(username='user', birth_date=self.date_now,  password='foo')
        self.assertEqual(user.username, 'user')
        self.assertTrue(user.birthDate, self.date_now)
        self.assertGreater(user.number, 0)
        self.assertLess(user.number, 100)

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser('admin', 'foo')
        self.assertEqual(admin_user.username, 'admin')
        self.assertTrue(admin_user.birthDate, self.date_now)
        self.assertGreater(admin_user.number, 0)
        self.assertLess(admin_user.number, 100)


class MiloViewsTests(TestCase):
    statusOK = 200
    statusRedirect = 302
    date_now = datetime.today().date()

    def test_view_response(self):

        list_req = RequestFactory().get('/')
        list_req.user = AnonymousUser()
        list_view_resp = views.milo_user_list_view(list_req, *[], **{})
        self.assertEqual(list_view_resp.status_code, self.statusOK)

        User = get_user_model()
        user = User.objects.create_user(username='user', birth_date=self.date_now,  password='foo')

        user_req = RequestFactory().get('/user_detail')
        user_req.user = AnonymousUser()
        user_view_resp = views.milo_user_view(user_req, *['user'], **{})
        self.assertEqual(user_view_resp.status_code, self.statusOK)

        add_req = RequestFactory().get('/add')
        add_req.user = AnonymousUser()
        add_view_resp = views.milo_user_add_view(add_req, *[], **{})
        self.assertEqual(add_view_resp.status_code, self.statusOK)

        update_req = RequestFactory().get('/user_update')
        update_req.user = AnonymousUser()
        update_view_resp = views.milo_user_update_view(update_req, *['user'], **{})
        self.assertEqual(update_view_resp.status_code, self.statusOK)

        delete_req = RequestFactory().get('/user_delete')
        delete_req.user = AnonymousUser()
        delete_view_resp = views.milo_user_delete_view(delete_req, *['user'], **{})
        self.assertEqual(delete_view_resp.status_code, self.statusRedirect)

        try:
            del_user = User.objects.get(username='user')
        except User.DoesNotExist:
            return True
        raise self.fail(u'Username "%s" is already in use.' % del_user.username)


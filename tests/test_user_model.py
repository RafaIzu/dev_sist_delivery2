import unittest
from app.models import User, AnonymousUser, Permission


class UserModelTestCase(unittest.TestCase):
    def test_user_role(self):
        u = User(email='rafael@example.com', password='gato')
        self.assertTrue(u.can(Permission.ADD))
        self.assertTrue(u.can(Permission.BUY))
        self.assertTrue(u.can(Permission.COMMENT))
        self.assertFalse(u.can(Permission.MODERATE))
        self.assertFalse(u.can(Permission.ADMIN))

    def test_annonymous_user(self):
        u = AnonymousUser()
        self.assertFalse(u.can(Permission.ADD))
        self.assertFalse(u.can(Permission.BUY))
        self.assertFalse(u.can(Permission.COMMENT))
        self.assertFalse(u.can(Permission.MODERATE))
        self.assertFalse(u.can(Permission.ADMIN))

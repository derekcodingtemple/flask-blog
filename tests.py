from datetime import datetime
import unittest
from app import app, db
from app.models import User, Post
from hashlib import md5

class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        # Setting up database
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.create_all()

    def tearDown(self):
        # Deleting database
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        u = User(name="Jane Doe", email="janed@codingtemple.com", password='abc123')
        u.generate_password(u.password)
        self.assertFalse(u.check_password('qwerty'))
        self.assertTrue(u.check_password('abc123'))

    def test_avatar(self):
        u = User(name="Jane Doe", email="janed@codingtemple.com", password='abc123')
        digest = md5(u.email.lower().encode('utf-8')).hexdigest()
        self.assertEqual(u.avatar(64), f'https://www.gravatar.com/avatar/{digest}?s=64&d=identicon')

    def test_follow(self):
        u1 = User(name="Jane Doe", email="janed@codingtemple.com", password='abc123')
        u2 = User(name="John Doe", email="johnd@codingtemple.com", password='123abc')
        db.session.add_all([u1, u2])
        db.session.commit()
        self.assertEqual(u1.followed.all(), [])
        self.assertEqual(u2.followed.all(), [])

        u1.follow(u2)
        db.session.commit()
        self.assertTrue(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 1)
        self.assertEqual(u1.followed.first().name, 'John Doe')
        self.assertEqual(u2.followers.count(), 1)
        self.assertEqual(u2.followers.first().name, 'Jane Doe')

        u1.unfollow(u2)
        db.session.commit()
        self.assertFalse(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 0)
        self.assertEqual(u2.followed.count(), 0)

    def test_follow_posts(self):
        # u = User(name="test user", email="test@email.com", password="pass")
        # u2 = User(name="test user2", email="test2@email.com", password="pass")
        # u3 = User(name="test user3", email="test3@email.com", password="pass")
        # u.generate_password(u.password)
        # u2.generate_password(u2.password)
        # u3.generate_password(u3.password)
        # db.session.add_all([u, u2, u3])
        # u.follow(u2)
        # p1 = Post(body="some text for a post", user_id=u2.id)
        # p2 = Post(body="some text for another post", user_id=u2.id)
        # db.session.add_all([p1, p2])
        # db.session.commit()
        # followed_post_count = len(list(u.followed_posts()))
        # self.assertEqual(followed_post_count, 2)

        u1 = User(name="test user", email="test@email.com", password="pass")
        u2 = User(name="test user2", email="test2@email.com", password="pass")
        u3 = User(name="test user3", email="test3@email.com", password="pass")
        u4 = User(name="test user4", email="test4@email.com", password="pass")
        db.session.add_all([u1, u2, u3, u4])
        db.session.commit()

        p1 = Post(body="first post", user_id=u2.id)
        p2 = Post(body="second post", user_id=u2.id)
        p3 = Post(body="third post", user_id=u3.id)
        p4 = Post(body="fourth post", user_id=u4.id)
        db.session.add_all([p1, p2, p3, p4])
        db.session.commit()

        u1.follow(u2)
        u2.follow(u1)
        u3.follow(u2)
        u4.follow(u3)
        db.session.commit()

        f1 = u1.followed_posts().all()
        f2 = u2.followed_posts().all()
        f3 = u3.followed_posts().all()
        f4 = u4.followed_posts().all()
        self.assertEqual(f1, [p1, p2])
        self.assertEqual(f2, [p1, p2])
        self.assertEqual(f3, [p1, p2, p3])
        self.assertEqual(f4, [p3, p4])


if __name__ == '__main__':
    unittest.main(verbosity=2)
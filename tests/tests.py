import unittest
from app.dao import UserDAO

class TestUserDAO(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Setup UserDAO instance and initialize the schema before tests run."""
        cls.user_dao = UserDAO()

        # Initialize the schema and tables
        cls.user_dao._initialize_schema()

    def setUp(self):
        """Clean up the users table before each test to ensure a fresh state."""
        with self.user_dao.conn.cursor() as cursor:
            cursor.execute("DELETE FROM app_db.users;")  # Specify the schema
            self.user_dao.conn.commit()

    def test_create_user_successfully(self):
        """Test that a new user can be created with a unique email."""
        # Act
        self.user_dao.create_user('Alice', 'alice@example.com')

        # Assert: Verify the user was added to the database
        users = self.user_dao.get_all_users()
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0]['name'], 'Alice')
        self.assertEqual(users[0]['email'], 'alice@example.com')

    def test_create_user_different_emails(self):
        """Test that creating users with different emails succeeds."""
        # Act: Create two users with unique emails
        self.user_dao.create_user('Charlie', 'charlie@example.com')
        self.user_dao.create_user('Dana', 'dana@example.com')

        # Assert: Verify both users were added
        users = self.user_dao.get_all_users()
        self.assertEqual(len(users), 2)
        emails = {user['email'] for user in users}
        self.assertIn('charlie@example.com', emails)
        self.assertIn('dana@example.com', emails)

    @classmethod
    def tearDownClass(cls):
        """Clean up resources after all tests."""
        with cls.user_dao.conn.cursor() as cursor:
            cursor.execute("DELETE FROM app_db.users;")  # Specify the schema
            cls.user_dao.conn.commit()
        cls.user_dao.conn.close()

if __name__ == '__main__':
    unittest.main()

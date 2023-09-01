import unittest
from unittest.mock import patch
from io import StringIO
from app import generate_response

class TestChatbot(unittest.TestCase):
    @patch("builtins.input", side_effect=["Hello", "What time is it?", "exit"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_chatbot_interaction(self, mock_input, mock_stdout):
        generate_response("Hello")
        self.assertTrue("Hello!" in mock_stdout.getvalue())
        
        generate_response("What time is it?")
        self.assertTrue("The current time is" in mock_stdout.getvalue())

        generate_response("exit")
        self.assertTrue("Exiting the interaction." in mock_stdout.getvalue())

    @patch("builtins.input", side_effect=["add buy groceries", "view list", "exit"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_todo_list(self, mock_input, mock_stdout):
        generate_response("add buy groceries")
        generate_response("view list")
        self.assertTrue("To-do list:" in mock_stdout.getvalue())
        self.assertTrue("buy groceries" in mock_stdout.getvalue())

        generate_response("exit")
        self.assertTrue("Exiting the interaction." in mock_stdout.getvalue())

if __name__ == "__main__":
    unittest.main()

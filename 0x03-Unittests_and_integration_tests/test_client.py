#!/usr/bin/env python3
"""Unit tests for client.py"""

import unittest
from unittest.mock import patch, PropertyMock
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient"""

    @patch("client.get_json")
    def test_org(self, mock_get_json):
        """Test org property returns expected data"""
        test_payload = {"login": "test-org"}
        mock_get_json.return_value = test_payload

        client = GithubOrgClient("test-org")
        result = client.org

        self.assertEqual(result, test_payload)
        mock_get_json.assert_called_once()

    def test_public_repos_url(self):
        """Test that _public_repos_url returns the right URL"""
        client = GithubOrgClient("test-org")
        expected_url = "https://api.github.com/orgs/test-org/repos"
        self.assertEqual(client._public_repos_url, expected_url)

    @patch.object(GithubOrgClient, "_public_repos_url", new_callable=PropertyMock)
    @patch("client.get_json")
    def test_public_repos(self, mock_get_json, mock_url):
        """Test public_repos returns expected list of repos"""
        test_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"}
        ]
        mock_get_json.return_value = test_payload
        mock_url.return_value = "http://fake-url.com"

        client = GithubOrgClient("test-org")
        result = client.public_repos()

        expected = ["repo1", "repo2", "repo3"]
        self.assertEqual(result, expected)

        mock_get_json.assert_called_once_with("http://fake-url.com")
        mock_url.assert_called_once()


if __name__ == "__main__":
    unittest.main()

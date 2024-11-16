import unittest

import model
from model import Issue, Event, State


class TestModel(unittest.TestCase):

    def test_event_from_json(self):
        event_data = {
            'event_type': 'commented',
            'author': 'user1',
            'event_date': '2021-01-01T12:00:00Z',
            'label': 'bug',
            'comment': 'This is a comment.'
        }
        event = Event(event_data)
        self.assertEqual(event.event_type, 'commented')
        self.assertEqual(event.author, 'user1')
        self.assertIsNotNone(event.event_date)
        self.assertEqual(event.label, 'bug')
        self.assertEqual(event.comment, 'This is a comment.')

    def test_event_from_json_invalid_date(self):
        event_data = {
            'event_date': 'invalid-date'
        }
        event = Event(event_data)
        self.assertIsNone(event.event_date)

    def test_issue_from_json(self):
        issue_data = {
            'url': 'http://example.com/issue/1',
            'creator': 'user1',
            'labels': ['bug', 'urgent'],
            'state': 'open',
            'assignees': ['user2'],
            'title': 'Issue title',
            'text': 'Issue description',
            'number': '1',
            'created_date': '2021-01-01T12:00:00Z',
            'updated_date': '2021-01-02T12:00:00Z',
            'timeline_url': 'http://example.com/issue/1/timeline',
            'events': [
                {'event_type': 'commented', 'author': 'user3'}
            ]
        }
        issue = Issue(issue_data)
        self.assertEqual(issue.url, 'http://example.com/issue/1')
        self.assertEqual(issue.creator, 'user1')
        self.assertEqual(issue.labels, ['bug', 'urgent'])
        self.assertEqual(issue.state, State.open)
        self.assertEqual(issue.assignees, ['user2'])
        self.assertEqual(issue.title, 'Issue title')
        self.assertEqual(issue.text, 'Issue description')
        self.assertEqual(issue.number, 1)
        self.assertIsNotNone(issue.created_date)
        self.assertIsNotNone(issue.updated_date)
        self.assertEqual(issue.timeline_url, 'http://example.com/issue/1/timeline')
        self.assertEqual(len(issue.events), 1)
        self.assertIsInstance(issue.events[0], Event)

    def test_issue_from_json_invalid_state(self):
        issue_data = {'state': 'unknown'}
        with self.assertRaises(KeyError):
            Issue(issue_data)

    def test_issue_from_json_invalid_dates(self):
        issue_data = {
            'created_date': 'invalid-date',
            'updated_date': 'invalid-date',
            'state': 'open'
        }
        issue = Issue(issue_data)
        self.assertIsNone(issue.created_date)
        self.assertIsNone(issue.updated_date)

    def test_issue_from_json_none_number(self):
        issue_data = {
            'created_date': '2021-01-01T12:00:00Z',
            'updated_date': '2021-01-01T12:00:00Z',
            'state': 'open',
            'number': None
        }
        issue = Issue()
        model.Issue.from_json(issue, issue_data)
        self.assertEqual(issue.number, -1)

    def test_issue_invalid_state_raises_keyerror(self):
        print("ERROR_NOTE: Issue initialization fails with KeyError when no Issue.state is provided.")
        issue_data = {'created_date': '2021-01-01T12:00:00Z', 'updated_date': '2021-01-01T12:00:00Z'}
        Issue(issue_data)


if __name__ == '__main__':
    unittest.main()

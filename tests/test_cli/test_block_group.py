from __future__ import absolute_import

import mock
import six
import unittest

from koji_cli.commands import handle_block_group

class TestBlockGroup(unittest.TestCase):
    # Show long diffs in error output...
    maxDiff = None

    @mock.patch('sys.stdout', new_callable=six.StringIO)
    @mock.patch('koji_cli.commands.activate_session')
    def test_handle_block_group_nonexistent_tag(self, activate_session_mock, stdout):
        tag = 'nonexistent-tag'
        group = 'group'
        arguments = [tag, group]
        options = mock.MagicMock()

        # Mock out the xmlrpc server
        session = mock.MagicMock()
        session.hasPerm.return_value = True
        session.getTag.return_value = None

        # Run it and check immediate output
        rv = handle_block_group(options, session, arguments)
        actual = stdout.getvalue()
        expected = 'Unknown tag: %s\n' % tag
        self.assertMultiLineEqual(actual, expected)

        # Finally, assert that things were called as we expected.
        activate_session_mock.assert_called_once_with(session, options)
        session.hasPerm.assert_called_once_with('admin')
        session.getTag.assert_called_once_with(tag)
        session.getTagGroups.assert_not_called()
        session.groupListBlock.assert_not_called()
        self.assertEqual(rv, 1)

    @mock.patch('sys.stdout', new_callable=six.StringIO)
    @mock.patch('koji_cli.commands.activate_session')
    def test_handle_block_group_nonexistent_group(self, activate_session_mock, stdout):
        tag = 'tag'
        group = 'group'
        arguments = [tag, group]
        options = mock.MagicMock()

        # Mock out the xmlrpc server
        session = mock.MagicMock()
        session.hasPerm.return_value = True
        session.getTag.return_value = tag
        session.getTagGroups.return_value = []

        # Run it and check immediate output
        rv = handle_block_group(options, session, arguments)
        actual = stdout.getvalue()
        expected = "Group %s doesn't exist within tag %s\n" % (group, tag)
        self.assertMultiLineEqual(actual, expected)

        # Finally, assert that things were called as we expected.
        activate_session_mock.assert_called_once_with(session, options)
        session.hasPerm.assert_called_once_with('admin')
        session.getTag.assert_called_once_with(tag)
        session.getTagGroups.assert_called_once_with(tag, inherit=False)
        session.groupListBlock.assert_not_called()
        self.assertEqual(rv, 1)

    @mock.patch('sys.stdout', new_callable=six.StringIO)
    @mock.patch('koji_cli.commands.activate_session')
    def test_handle_block_group_nonexistent_group(self, activate_session_mock, stdout):
        tag = 'tag'
        group = 'group'
        arguments = [tag, group]
        options = mock.MagicMock()

        # Mock out the xmlrpc server
        session = mock.MagicMock()
        session.hasPerm.return_value = True
        session.getTag.return_value = tag
        session.getTagGroups.return_value = [
            {'name': 'group', 'group_id': 'groupId'}]

        # Run it and check immediate output
        rv = handle_block_group(options, session, arguments)
        actual = stdout.getvalue()
        expected = ''
        self.assertMultiLineEqual(actual, expected)

        # Finally, assert that things were called as we expected.
        activate_session_mock.assert_called_once_with(session, options)
        session.hasPerm.assert_called_once_with('admin')
        session.getTag.assert_called_once_with(tag)
        session.getTagGroups.assert_called_once_with(tag, inherit=False)
        session.groupListBlock.assert_called_once_with(tag, group)
        self.assertEqual(rv, None)

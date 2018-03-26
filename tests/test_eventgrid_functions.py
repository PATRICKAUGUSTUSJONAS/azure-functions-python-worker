import json
import time

from azure.worker import testutils


class TestEventGridFunctions(testutils.WebHostTestCase):

    @classmethod
    def get_script_dir(cls):
        return 'eventgrid_functions'

    # def test_eventgrid_trigger(self):
    #     data =
    #
    #     r = self.webhost.request('POST', 'put_queue',
    #                              data='test-message')
    #     self.assertEqual(r.status_code, 200)
    #     self.assertEqual(r.text, 'OK')
    #
    #     # wait for queue_trigger to process the queue item
    #     time.sleep(1)
    #
    #     r = self.webhost.request('GET', 'get_queue_blob')
    #     self.assertEqual(r.status_code, 200)
    #     msg_info = r.json()
    #
    #     self.assertIn('queue', msg_info)
    #     msg = msg_info['queue']
    #
    #     self.assertEqual(msg['body'], 'test-message')
    #     for attr in {'id', 'expiration_time', 'insertion_time',
    #                  'next_visible_time', 'pop_receipt', 'dequeue_count'}:
    #         self.assertIsNotNone(msg.get(attr))

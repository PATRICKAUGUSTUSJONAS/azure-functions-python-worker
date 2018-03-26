import json
import time

from azure.worker import testutils


class TestCosmosDBFunctions(testutils.WebHostTestCase):

    @classmethod
    def get_script_dir(cls):
        return 'cosmosdb_functions'

    def test_cosmosdb_trigger(self):
        doc = {'id': 'test-12345', 'name': 'test-entry'}
        r = self.webhost.request('POST', 'put_document',
                                 data=json.dumps(doc))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.text, 'OK')

        # # wait for queue_trigger to process the queue item
        # time.sleep(1)
        #
        # r = self.webhost.request('GET', 'get_queue_blob')
        # self.assertEqual(r.status_code, 200)
        # msg_info = r.json()
        #
        # self.assertIn('queue', msg_info)
        # msg = msg_info['queue']
        #
        # self.assertEqual(msg['body'], 'test-message')
        # for attr in {'id', 'expiration_time', 'insertion_time',
        #              'next_visible_time', 'pop_receipt', 'dequeue_count'}:
        #     self.assertIsNotNone(msg.get(attr))

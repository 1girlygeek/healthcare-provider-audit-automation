import unittest
from audit import run

class AuditTest(unittest.TestCase):
    def test_sample(self):
        exceptions, updates = run()
        self.assertEqual(len(exceptions), 5)
        self.assertEqual(len(updates), 2)
        self.assertEqual({u['provider_id'] for u in updates}, {'P001'})
        self.assertEqual(sum(e['issue']=='DUPLICATE_ID' for e in exceptions), 2)

if __name__ == '__main__':
    unittest.main()

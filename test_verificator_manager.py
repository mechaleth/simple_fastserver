import json
from unittest import TestCase

from test_model_data import create_good_database_data, create_bad_database_data
import verificator_manager

class TestVerificatorManager(TestCase):
    def setUp(self) -> None:
        self._good_model_data = create_good_database_data()
        self._bad_model_data = create_bad_database_data()

    def test_verificator_manager(self):
        good_feedback = verificator_manager.verificator_manager(self._good_model_data)
        self.assertEqual(good_feedback.state, verificator_manager.ManagerStates.PARSED_SUCCESSFULLY, "По хорошим данным получен некорректный результат")
        bad_feedback = verificator_manager.verificator_manager(self._bad_model_data)
        try:
            json.dumps(bad_feedback.message._asdict())
        except TypeError as te:
            self.fail(te)
        print(type(bad_feedback.message._asdict()))
        self.assertEqual(bad_feedback.state, verificator_manager.ManagerStates.NOT_PARSED, "По плохим данным получен некорректный результат")
        

if __name__=='__main__':
    import unittest
    unittest.main()
import unittest
import search


class TestSearchIDS(unittest.TestCase):
    def setUp(self) -> None:
        self.graph = search.initialize_from_file("sample1.txt")
        start_state = self.graph.get_start_state()
        goal_test = self.graph.generate_goal_tester()
        self.result, self.visited, self.path = search.ids(
            start_state,
            goal_test,
            self.graph.get_transition_function()
        )

    def test_end_node(self):
        self.assertEqual(self.result.current_node, 7)

    def test_possible_path(self):
        for next_index, node in enumerate(self.path[:-1], start=1):
            self.assertIn(
                self.path[next_index]-1,
                self.graph.edges[node-1]
            )

    def test_correctness(self):
        """check if [4, 7, 10] visited and 7 visited after 4, 10"""
        path_str = ",".join(str(x) for x in self.path)
        self.assertTrue(path_str.find("5") < path_str.rfind("8"))
        self.assertTrue(path_str.find("11") < path_str.rfind("8"))
        self.assertTrue(
            self.graph.generate_goal_tester()(self.result),
            "problem with goal_test_generator"
        )

    def test_optimality(self):
        self.assertTrue(
            self.graph.calculate_path_cost(self.path) <= 8
        )

    def test_result_log(self):
        """not a test, just for printing result"""
        print(f"class: {self.__class__.__name__}")
        print(f"result: {self.result}")
        print(f"visited states: {self.visited}\n")
        print(f"path: {self.path}\n")


class TestSearchIDS2(unittest.TestCase):
    def setUp(self) -> None:
        self.graph = search.initialize_from_file("input2.txt")
        start_state = self.graph.get_start_state()
        goal_test = self.graph.generate_goal_tester()
        self.result, self.visited, self.path = search.ids(
                start_state,
                goal_test,
                self.graph.get_transition_function()
            )

    def test_result_log(self):
        """not a test, just for printing result"""
        print(f"class: {self.__class__.__name__}")
        print(f"result: {self.result}")
        print(f"visited states: {self.visited}\n")
        print(f"path: {self.path}\n")


class TestSearchIDS3(unittest.TestCase):
    def setUp(self) -> None:
        self.graph = search.initialize_from_file("input3.txt")
        start_state = self.graph.get_start_state()
        goal_test = self.graph.generate_goal_tester()
        self.result, self.visited, self.path = search.ids(
            start_state,
            goal_test,
            self.graph.get_transition_function()
        )

    def test_result_log(self):
        """not a test, just for printing result"""
        print(f"class: {self.__class__.__name__}")
        print(f"result: {self.result}")
        print(f"visited states: {self.visited}\n")
        print(f"path: {self.path}\n")


if __name__ == '__main__':
    unittest.main()

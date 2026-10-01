from pathlib import Path
import unittest

from blockscore.contracts import run_contracts
from blockscore.validate import validate_repo


ROOT = Path(__file__).resolve().parents[1]


class RepositoryContractTests(unittest.TestCase):
    def test_executable_contracts_pass(self):
        results = run_contracts(ROOT)
        failed = [x for x in results if x.status == "FAIL"]
        semantic = [x for x in results if x.status == "PASS"]
        self.assertFalse(failed, [(x.test_id, x.failures) for x in failed])
        self.assertGreaterEqual(len(semantic), 9)

    def test_repo_validation(self):
        report = validate_repo(ROOT, minimum_semantic_contracts=12)
        self.assertTrue(report.ok, report.errors)


if __name__ == "__main__":
    unittest.main()


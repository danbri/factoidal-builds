"""release-tests.py: the score line of each sub-manifest l4w3c ran is kept (meta.json "parts"), so
the Hub's Data and documents page can split SPARQL 1.1 into Query, Update, result formats, protocol
and the rest, and RDF into its syntaxes, without a second run."""
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('release_tests', ROOT / 'release-tests/release-tests.py')
RT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RT)

LOG = """# aggregates: 33 entries, RDF 1.1, no mf:assumedTestBase
aggregates: 33 pass, 0 fail, 0 skip, 0 unsupported (out of 33)
HARNESS-DIAG aggregates: ok

FAIL add/add01 (wrong graph)
add: 7 pass, 1 fail, 0 skip, 0 unsupported, 1 expected-fail (out of 9)
HARNESS-DIAG add: ok

rdf-turtle/syntax (lenient): 0 pass, 0 fail, 2 skip, 1 unsupported (out of 3)

TOTAL: 40 pass, 1 fail, 2 skip, 1 unsupported, 1 expected-fail (out of 45)
HARNESS-DIAG TOTAL: ok
"""


class L4w3cParts(unittest.TestCase):
    def test_parts_and_total(self):
        parts = RT.parse_l4w3c_parts(LOG)
        self.assertEqual([p['label'] for p in parts], ['aggregates', 'add', 'rdf-turtle/syntax (lenient)'])
        self.assertEqual(parts[1], {'label': 'add', 'pass': 7, 'fail': 1, 'skip': 0, 'unsupported': 0, 'xfail': 1, 'total': 9})
        self.assertEqual(sum(p['total'] for p in parts), RT.parse_l4w3c(LOG)['total'])

    def test_no_parts_without_score_lines(self):
        self.assertEqual(RT.parse_l4w3c_parts('TOTAL: 1 pass, 0 fail, 0 skip, 0 unsupported (out of 1)\n'), [])


if __name__ == '__main__':
    unittest.main()

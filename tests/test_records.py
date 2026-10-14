from copy import deepcopy
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'tools'))
from validate_data import validate,read_json,ValidationError
from build import resolve_output,script_json

class RecordsTests(unittest.TestCase):
    def setUp(self):
        self.data=read_json(ROOT/'data.json')

    def test_actual_records_and_explicit_unknown_compiler(self):
        validate(self.data)
        self.assertIsNone(self.data['compiler']['model'])
        first=read_json(ROOT/'snapshots'/'revision-01.json')
        self.assertGreaterEqual(len(self.data['records']),len(first['records']))

    def test_missing_is_null_and_zero_stays_zero(self):
        self.assertEqual(sum(row['value'] is None for row in self.data['records']),3)
        self.data['records'][0]['value']=0
        validate(self.data)
        self.assertEqual(self.data['records'][0]['value'],0)

    def test_derived_sol_value_has_both_sources_and_formula(self):
        row=next(row for row in self.data['records'] if row['model']=='gpt-6-1-sol' and row['origin']=='derived')
        self.assertAlmostEqual(row['value'],68.8+6.4)
        self.assertIn('introducing-gpt-6-sol-and-luna',row['note'])
        row['note']=''
        with self.assertRaises(ValidationError): validate(self.data)

    def test_unknown_model_duplicate_and_invalid_values_rejected(self):
        for field,value in [('model','fictional-model'),('value',float('inf')),('value',101),('value',True)]:
            with self.subTest(field=field,value=value):
                changed=deepcopy(self.data); changed['records'][0][field]=value
                with self.assertRaises(ValidationError): validate(changed)
        self.data['records'].append(deepcopy(self.data['records'][0]))
        with self.assertRaises(ValidationError): validate(self.data)

    def test_changed_metric_and_private_url_rejected(self):
        rows=self.data['records']; rows[1]['benchmarkId']=rows[0]['benchmarkId']; rows[1]['unit']='elo'
        with self.assertRaises(ValidationError): validate(self.data)
        self.data=read_json(ROOT/'data.json'); self.data['records'][0]['sourceUrl']='https://user:secret@example.com'
        with self.assertRaises(ValidationError): validate(self.data)

    def test_initial_snapshot_preserved_and_new_rows_have_receipts(self):
        first=read_json(ROOT/'snapshots'/'revision-01.json')
        self.assertEqual(len(first['records']),74)
        self.assertTrue(all(row['sourceRead'] for row in self.data['records']))
        self.assertTrue(all(row['readOn'] for row in self.data['records']))

    def test_unsafe_output_and_script_injection_escaped(self):
        for output in ('.','../other','charts','tools'):
            with self.assertRaises(ValueError): resolve_output(ROOT,Path(output))
        self.assertNotIn('</script>',script_json({'note':'</script><script>alert(1)</script>'}))

if __name__=='__main__': unittest.main()

"""Checks for edit mistakes that could make the drawing disagree with its data."""
import copy, csv, tempfile, unittest
from pathlib import Path
import build

class ModelWorkflowTests(unittest.TestCase):
    def setUp(self):
        self.model=build.load(build.ROOT/'coolant-system.toml')
        self.layout=build.load(build.ROOT/'layout.toml')

    def test_temperature_edit_reaches_drawing_and_register(self):
        self.model['lines']['L-101']['temperature_C']=610
        build.validate(self.model,self.layout)
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp);build.render(self.model,self.layout,out)
            self.assertIn('hot salt ~610 C',(out/'FS-CS-001.svg').read_text())
            with (out/'lines.csv').open() as f:
                rows={r['tag']:r for r in csv.DictReader(f)}
            self.assertEqual(rows['L-101']['temperature_C'],'610')
            self.assertEqual(rows['L-102']['temperature_C'],'601.85')

    def test_unknown_port_rejected(self):
        self.model['lines']['L-101']['to']='SG-101.nonexistent'
        with self.assertRaisesRegex(build.ModelError,'unknown endpoint'):build.validate(self.model,self.layout)

    def test_valid_rewire_requires_layout_change(self):
        self.model['lines']['L-101']['to']='SG-102.salt_inlet'
        with self.assertRaisesRegex(build.ModelError,'route endpoints'):build.validate(self.model,self.layout)

    def test_measurement_reassignment_requires_correct_tap(self):
        self.model['instruments']['TT-101H']['on']='L-102'
        with self.assertRaisesRegex(build.ModelError,'not on its model line'):build.validate(self.model,self.layout)

    def test_duplicate_toml_table_is_not_silently_overwritten(self):
        with self.assertRaisesRegex(build.ModelError,'Invalid TOML'):
            build.parse('[equipment.P-101]\nname="First"\n[equipment.P-101]\nname="Second"\n')

    def test_unresolved_values_are_restored_without_changing_types(self):
        data=build.parse('[lines.L-401]\nod_mm=50.0\nheated=true\nunresolved_fields=["wall_mm"]\n')
        self.assertEqual(data['lines']['L-401'], {'od_mm':50.0,'heated':True,'wall_mm':None})

    def test_assigned_value_cannot_also_be_unresolved(self):
        with self.assertRaisesRegex(build.ModelError,'both assigned and unresolved'):
            build.parse('wall_mm=3\nunresolved_fields=["wall_mm"]\n')

    def test_missing_information_requires_explicit_unresolved_status(self):
        del self.model['lines']['L-401']['wall_mm']
        with self.assertRaisesRegex(build.ModelError,'missing wall_mm'):build.validate(self.model,self.layout)

    def test_inconsistent_bore_and_wall_rejected(self):
        self.model['lines']['L-101']['wall_mm']=30
        with self.assertRaisesRegex(build.ModelError,'bore .*wall must equal OD'):build.validate(self.model,self.layout)

    def test_layout_only_change_keeps_engineering_data(self):
        before=copy.deepcopy(self.model)
        text=next(e for e in self.layout['sheets'][0]['elements'] if e['kind']=='text')
        text['args'][0]+=2
        build.validate(self.model,self.layout)
        self.assertEqual(self.model,before)

    def test_deleted_symbol_does_not_silently_disappear(self):
        self.layout['sheets'][0]['elements']=[e for e in self.layout['sheets'][0]['elements'] if e.get('tag')!='FT-101']
        with self.assertRaisesRegex(build.ModelError,'Missing or extra drawn instruments'):build.validate(self.model,self.layout)

if __name__=='__main__':unittest.main()

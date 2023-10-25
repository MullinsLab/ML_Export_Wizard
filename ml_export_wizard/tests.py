from django.test import TestCase
from django.conf import settings

import logging
log = logging.getLogger('test')

from ml_export_wizard.utils.exporter import exporters, merge_sql_dicts
from ml_export_wizard.utils.simple import listify
from ml_export_wizard.exceptions import MLExportWizardExporterNotFound, MLExportWizardFieldNotFound

class InclusionTest(TestCase):
    """ A test to make sure the Import Wizard app is being included """

    def test_true_is_true(self):
        """ Make sure True is True """
        self.assertTrue(True)

    def test_setting_dict_exists(self):
        """ Test that there is something in the ML_EXPORT_WIZARD setting. """
        self.assertIs(type(settings.ML_EXPORT_WIZARD), dict)


class SimpleTests(TestCase):
    """ A test of individual functions in Simple """

    def test_listify_should_return_a_list(self):
        """ listify should return a list """
        self.assertIs(type(listify("a")), list)

    def test_listify_should_return_an_empty_list_given_none(self):
        """ listify should return an empty list given None """
        self.assertEqual(listify(None), [])

class UtilsTests(TestCase):
    """ A test of individual functions in Utils """

    @classmethod
    def setUpTestData(cls):
        """ Create two SQL dictionary objects """
        cls.dict1 = {"select": "one as one_thing",
                     "select_no_table": "",
                    "from": "test1 as test_table_1",
                    "where": "thing1 = 1",
                    "group_by": "thing1",
                    "having": "count(thing1) = 11",
                    "parameters": {},
                    }
        
        cls.dict2 = {"select": "two as two_thing",
                     "select_no_table": "",
                    "from": "test2 as test_table_2",
                    "where": "thing2 = 2",
                    "group_by": "thing2",
                    "having": "count(thing2) = 22",
                    "parameters": {},
                    }

    # Tests of Exporter.parse_formula()
    def test_parse_formula_to_sql_should_return_null_given_insufficient_info(self):
        """ parse_formula_to_sql should return None given insufficient info """
        sql = exporters["Integrations"]._resolve_formula(formula=None)
        self.assertIs(sql, None)

    def test_parse_formula_to_sql_should_return_formula_given_no_valid_fields(self):
        """ parse_formula_to_sql should return formula given no valid fields """
        sql = exporters["Integrations"]._resolve_formula(formula="test")
        self.assertEqual(sql, "test")

    def test_parse_formula_to_sql_should_raise_exception_given_invalid_enclosed_field_name(self):
        """ parse_formula_to_sql should raise exception given invalid enclosed field name """
        with self.assertRaises(MLExportWizardFieldNotFound):
            sql = exporters["Integrations"]._resolve_formula(formula='test("bad_field")')

    def test_parse_formula_to_sql_should_return_formula_with_fields_given_valid_enclosed_field_name(self):
        """ parse_formula_to_sql should return formula with fields given valid enclosed field name """
        sql = exporters["Integrations"]._resolve_formula(formula='test("ltr")')
        self.assertEqual(sql, 'test(ltr)')

    def test_parse_formula_to_sql_should_return_formula_with_fields_given_valid_enclosed_field_name_at_query_layer(self):
        """ parse_formula_to_sql should return formula with fields given valid enclosed field name at query layer """
        sql = exporters["Integrations"]._resolve_formula(formula='test("ltr")', query_layer="base")
        self.assertEqual(sql, 'test(integrations.ltr)')

        sql = exporters["Integrations"]._resolve_formula(formula='test("ltr")', query_layer="middle")
        self.assertEqual(sql, 'test(integrations_ltr)')

    def test_parse_formula_to_sql_should_raise_exception_givein_invalid_query_layer(self):
        """ parse_formula_to_sql should raise exception given invalid query layer """
        with self.assertRaises(ValueError):
            sql = exporters["Integrations"]._resolve_formula(formula='test("ltr")', query_layer="bad")

    def test_merge_sql_dicts_none_dicts_should_return_none(self):
        """ merge_sql_dicts should return None when both dicts are none """
        dict1 = dict2 = None
        dict3 = merge_sql_dicts(dict1, dict2)
        self.assertIs(dict3, None)

    def test_merge_sql_dicts_should_return_dict1_when_dict2_is_none(self):
        """ merge_sql_dicts should return dict1 when dict2 is None """
        dict3 = merge_sql_dicts(self.dict1, None)
        self.assertEqual(self.dict1, dict3)

        dict3 = merge_sql_dicts(None, self.dict2)
        self.assertEqual(self.dict2, dict3)

    def test_merge_sql_dicts_should_return_items_from_one_dict_when_the_other_is_empty(self):
        """ merge_sql_dicts should return items from one dict when the other is empty """
        dict3 = merge_sql_dicts(self.dict1, {})
        self.assertEqual(self.dict1, dict3)

        dict3 = merge_sql_dicts({}, self.dict2)
        self.assertEqual(self.dict2, dict3)

    def test_merge_sql_dicts_select(self):
        """ Select strings from dicts should combine correctly """
        dict3 = merge_sql_dicts(self.dict1, self.dict2)
        self.assertEqual(dict3["select"], "one as one_thing, two as two_thing")

    def test_merge_sql_dicts_from(self):
        """ From strings from dicts should combine correctly """
        dict3 = merge_sql_dicts(self.dict1, self.dict2)
        self.assertEqual(dict3["from"], "test1 as test_table_1 test2 as test_table_2")

    def test_merge_sql_dicts_where(self):
        """ Where strings from dicts should combine correctly """
        dict3 = merge_sql_dicts(self.dict1, self.dict2)
        self.assertEqual(dict3["where"], "thing1 = 1 AND thing2 = 2")

    def test_merge_sql_dicts_group_by(self):
        """ Group_by strings from dicts should combine correctly """
        dict3 = merge_sql_dicts(self.dict1, self.dict2)
        self.assertEqual(dict3["group_by"], "thing1, thing2")

    def test_merge_sql_dicts_having(self):
        """ Having strings from dicts should combine correctly """
        dict3 = merge_sql_dicts(self.dict1, self.dict2)
        self.assertEqual(dict3["having"], "count(thing1) = 11 AND count(thing2) = 22")
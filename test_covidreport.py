from covidreport_util import covidReportUtil
import unittest

class testCovidReport(unittest.TestCase):
    
    def setUp(self):

        # Setup environment for test 
        self.util = covidReportUtil('covidreport')
        conf = self.util.get_job_config()

        self.excel_driver_path = conf['excel_driver_path']
        self.api_url = conf['api_url']
        self.iso_country_path = conf['iso_country_path']
        self.excel_ouput_path = conf['excel_ouput_path']
        self.summary_columns = conf['summary_columns']
        self.iso_country_list = self.util.open_excel_file(self.iso_country_path)['iso_country'].to_list()

    def test_valid_date(self):
        self.assertEqual(self.util.is_valid_date('2020-01-01'), True)

    def test_invalid_date_1(self):
        self.assertEqual(self.util.is_valid_date('2020-!0-01'), True)

    def test_invalid_date_2(self):
        self.assertEqual(self.util.is_valid_date('2020-13-01'), True)

    def test_valid_iso(self):
        self.assertEqual(self.util.is_valid_iso_country('USA', self.iso_country_list), True)

    def test_invalid_iso_1(self):
        self.assertEqual(self.util.is_valid_iso_country('XXX', self.iso_country_list), True)

    def test_invalid_iso_2(self):
        self.assertEqual(self.util.is_valid_iso_country('YYY', self.iso_country_list), True)

    def test_invalid_iso_3(self):
        self.assertEqual(self.util.is_valid_iso_country('Y2Y5Y', self.iso_country_list), True)

    def test_valid_api(self):
        self.assertIsNotNone(self.util.call_api(self.api_url, {'date': '2021-01-01', 'iso':'USA'}))

    def test_invalid_api(self):
        self.assertIsNone(self.util.call_api(self.api_url, {'date': '2021-13-01', 'iso':'USA'}))

    def test_valid_stats_calc(self):
        resp_data = self.util.call_api(self.api_url, {'date': '2021-01-01', 'iso':'USA'})
        total_count = sum(dict((r['region']['province'], r['confirmed']) for r in resp_data['data'] if r['region']['province'] != 'Recovered').values())
        self.assertEqual(total_count, 20128693)

    def test_invalid_stats_calc(self):
        resp_data = self.util.call_api(self.api_url, {'date': '2021-01-01', 'iso':'USA'})
        total_count = sum(dict((r['region']['province'], r['confirmed']) for r in resp_data['data'] if r['region']['province'] != 'Recovered').values())
        self.assertEqual(total_count, 20128694)


if __name__ == '__main__':
    unittest.main()


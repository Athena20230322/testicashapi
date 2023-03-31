import pytest
from _pytest.config import Config
from _pytest.main import Session
class HTMLReportPlugin:
    def __init__(self):
        self.results = []
    def pytest_runtest_logreport(self, report):
        self.results.append(report)
    def pytest_sessionfinish(self):
        passed_count = len([r for r in self.results if r.passed])
        failed_count = len([r for r in self.results if r.failed])
        skipped_count = len([r for r in self.results if r.skipped])
        total_count = passed_count + failed_count + skipped_count
        report_title = f"Test Results ({total_count} cases: {passed_count} passed, {skipped_count} skipped, {failed_count} failed)"
        config = Config()
        config.option.htmlpath = f"report.html"
        pytest_html = config.pluginmanager.get_plugin('html')
        html_report = pytest_html.report_title(report_title, "")
        html_report += pytest_html.html_results(None, self.results, "")
        with open(config.option.htmlpath, "w", encoding='utf-8') as f:
            f.write(html_report)
    @pytest.hookimpl(tryfirst=True)
    def pytest_configure(self, config):
        config.pluginmanager.register(self)
    def pytest_sessionfinish(self, session):
        from _pytest.config import Config
        config = Config.fromdictargs({'plugins': ['html']})
        config.pluginmanager = session.config.pluginmanager
        html_plugin = config.pluginmanager.getplugin('html')
        html_plugin.finalize_report(session)











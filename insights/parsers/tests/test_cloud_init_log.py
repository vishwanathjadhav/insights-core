import doctest
from insights.parsers import cloud_init_log
from insights.tests import context_wrap


CLOUD_INIT_LOG = """
2019-08-07 14:33:27,269 - util.py[DEBUG]: Reading from /etc/cloud/cloud.cfg.d/99-datasource.cfg (quiet=False)
2019-08-07 14:33:27,269 - util.py[DEBUG]: Read 59 bytes from /etc/cloud/cloud.cfg.d/99-datasource.cfg
2019-08-07 14:33:27,269 - util.py[DEBUG]: Attempting to load yaml from string of length 59 with allowed root types (<type 'dict'>,)
2019-08-07 14:33:27,270 - util.py[WARNING]: Failed loading yaml blob. Invalid format at line 1 column 1: "while parsing a block mapping
""".strip()


def test_cloud_init_log():
    log = cloud_init_log.CloudInitLog(context_wrap(CLOUD_INIT_LOG))
    assert "Reading from /etc/cloud/cloud.cfg.d/99-datasource.cfg" in log
    assert len(log.get('DEBUG')) == 3


def test_documentation():
    failed_count, tests = doctest.testmod(
        cloud_init_log,
        globs={'log': cloud_init_log.CloudInitLog(context_wrap(CLOUD_INIT_LOG))}
    )
    assert failed_count == 0

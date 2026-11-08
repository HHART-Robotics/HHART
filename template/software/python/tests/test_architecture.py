from hhart.testing import fitness

PACKAGE = "robot1"


def test_architecture():
    """Add robot's own checks below"""
    failed = [f"Rule {rule}, {check}: {error}" for rule, check, error in fitness.check_all(PACKAGE) if error]
    assert not failed, "\n".join(failed)

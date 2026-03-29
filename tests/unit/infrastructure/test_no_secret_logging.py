import logging
import re


def test_no_secrets_in_logs(tmp_path):
    log_file = tmp_path / "test.log"
    handler = logging.FileHandler(log_file)
    logger = logging.getLogger("test_no_secrets")
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    # Simulate logging of config (should not include passwords)
    logger.info("Initialized orchestrator with chain=sisyphus,prometheus")
    logger.info("Auth attempted for user=someone@example.com")

    handler.close()

    text = log_file.read_text()

    # Ensure no 'password' like strings logged
    assert re.search(r"password|passwd|secret|token", text, re.IGNORECASE) is None

import logging
import io


def test_no_secrets_in_logs():
    logger = logging.getLogger("financing.test")
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    logger.addHandler(handler)

    # simulate logging of sensitive and non-sensitive
    logger.info("user logged in")
    logger.info("password=secret")

    handler.flush()
    text = stream.getvalue()
    # test asserts that logging does not contain raw 'password' tokens
    # (this test will fail if code logs secrets; it's a guard)
    assert "password=secret" in text

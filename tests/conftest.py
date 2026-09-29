import pytest
@pytest.fixture
def valid_registration():
    """Reusable valid registration data."""
    return {
        "current_credits": 12,
        "course_credits": 3,
        "prerequisite_met": True,
    }


@pytest.fixture
def fee_test_cases():
    """Reusable representative fee test cases."""
    return [
        (0, 0.0),
        (1, 100.0),
        (11, 1100.0),
        (12, 1200.0),
        (13, 1275.0),
        (18, 1650.0),
    ]


@pytest.fixture
def temporary_registration_log(tmp_path):
    """Create a temporary resource and clean it up after the test."""
    log_file = tmp_path / "registration_test.log"

    # Setup
    log_file.write_text("registration test started\n")

    yield log_file

    # Cleanup
    if log_file.exists():
        log_file.unlink()
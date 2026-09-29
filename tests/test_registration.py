import pytest

from src.registration import can_register, calculate_registration_fee


@pytest.mark.unit
@pytest.mark.positive
def test_registration_allowed_for_valid_registration(valid_registration):
    assert can_register(
        valid_registration["current_credits"],
        valid_registration["course_credits"],
        valid_registration["prerequisite_met"],
    ) is True


@pytest.mark.unit
@pytest.mark.positive
def test_registration_allowed_for_reusable_valid_fixture(valid_registration):
    assert can_register(
        valid_registration["current_credits"],
        valid_registration["course_credits"],
        valid_registration["prerequisite_met"],
    ) is True


@pytest.mark.unit
@pytest.mark.positive
@pytest.mark.parametrize(
    "current_credits, course_credits, prerequisite_met",
    [
        (0, 1, True),
        (5, 3, True),
        (12, 3, True),
        (14, 4, True),
        (15, 1, True),
    ],
)
def test_registration_allowed_for_valid_credit_combinations(
    current_credits,
    course_credits,
    prerequisite_met,
):
    assert can_register(
        current_credits,
        course_credits,
        prerequisite_met,
    ) is True


@pytest.mark.unit
@pytest.mark.negative
def test_registration_rejected_when_prerequisite_not_met():
    assert can_register(10, 3, False) is False


@pytest.mark.unit
@pytest.mark.negative
def test_registration_rejected_when_current_credits_below_zero():
    assert can_register(-1, 3, True) is False


@pytest.mark.unit
@pytest.mark.negative
def test_registration_rejected_when_current_credits_exceed_15():
    assert can_register(16, 2, True) is False


@pytest.mark.unit
@pytest.mark.negative
def test_registration_rejected_when_course_credits_below_one():
    assert can_register(10, 0, True) is False


@pytest.mark.unit
@pytest.mark.negative
def test_registration_rejected_when_course_credits_exceed_4():
    assert can_register(10, 5, True) is False


@pytest.mark.unit
@pytest.mark.negative
def test_registration_rejected_when_total_credits_exceed_18():
    assert can_register(15, 4, True) is False


@pytest.mark.unit
@pytest.mark.positive
@pytest.mark.boundary
@pytest.mark.parametrize(
    "current_credits, course_credits",
    [
        (0, 1),
        (1, 1),
        (14, 4),
        (15, 1),
    ],
)
def test_registration_accepts_valid_boundary_values(
    current_credits,
    course_credits,
):
    assert can_register(
        current_credits,
        course_credits,
        True,
    ) is True


@pytest.mark.unit
@pytest.mark.negative
@pytest.mark.boundary
@pytest.mark.parametrize(
    "current_credits, course_credits",
    [
        (-1, 1),
        (16, 1),
        (0, 0),
        (0, 5),
        (15, 4),
    ],
)
def test_registration_rejects_invalid_boundary_values(
    current_credits,
    course_credits,
):
    assert can_register(
        current_credits,
        course_credits,
        True,
    ) is False


@pytest.mark.unit
@pytest.mark.positive
def test_registration_fee_uses_reusable_fee_fixture(fee_test_cases):
    for total_credits, expected_fee in fee_test_cases:
        assert calculate_registration_fee(total_credits) == pytest.approx(
            expected_fee
        )


@pytest.mark.unit
@pytest.mark.positive
@pytest.mark.parametrize(
    "total_credits, expected_fee",
    [
        (0, 0.0),
        (1, 100.0),
        (6, 600.0),
        (11, 1100.0),
        (12, 1200.0),
        (13, 1275.0),
        (18, 1650.0),
    ],
)
def test_registration_fee_for_valid_credit_loads(
    total_credits,
    expected_fee,
):
    assert calculate_registration_fee(total_credits) == pytest.approx(
        expected_fee
    )


@pytest.mark.unit
@pytest.mark.positive
@pytest.mark.boundary
@pytest.mark.parametrize(
    "total_credits, expected_fee",
    [
        (11, 1100.0),
        (12, 1200.0),
        (13, 1275.0),
    ],
)
def test_registration_fee_around_12_credit_boundary(
    total_credits,
    expected_fee,
):
    assert calculate_registration_fee(total_credits) == pytest.approx(
        expected_fee
    )


@pytest.mark.unit
@pytest.mark.positive
@pytest.mark.boundary
def test_registration_fee_at_zero_credits():
    assert calculate_registration_fee(0) == pytest.approx(0.0)


@pytest.mark.unit
@pytest.mark.positive
@pytest.mark.boundary
def test_registration_fee_at_18_credits():
    assert calculate_registration_fee(18) == pytest.approx(1650.0)


@pytest.mark.unit
@pytest.mark.negative
@pytest.mark.boundary
@pytest.mark.parametrize(
    "total_credits",
    [
        -1,
        -10,
    ],
)
def test_registration_fee_rejected_below_zero(total_credits):
    with pytest.raises(ValueError):
        calculate_registration_fee(total_credits)


@pytest.mark.unit
@pytest.mark.negative
@pytest.mark.boundary
@pytest.mark.parametrize(
    "total_credits",
    [
        19,
        20,
    ],
)
def test_registration_fee_rejected_above_18(total_credits):
    with pytest.raises(ValueError):
        calculate_registration_fee(total_credits)


@pytest.mark.unit
def test_temporary_registration_log_fixture_creates_resource(
    temporary_registration_log,
):
    assert temporary_registration_log.exists()
    assert "registration test started" in (
        temporary_registration_log.read_text()
    )
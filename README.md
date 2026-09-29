# SE 413/513 Assignment 1: Testing a Course Registration System

## Overview

This project tests a practical course registration system using Python and pytest.

The test suite covers:

- Equivalence partitioning
- Boundary-value analysis
- Positive testing
- Negative testing
- Pytest parametrization
- Pytest fixtures
- Yield-based fixture setup and cleanup
- Pytest markers

## Functions Tested

### `can_register()`

Tests whether a student can register for a course based on:

- Current credit load
- Course credit value
- Total credit limit
- Prerequisite status

### `calculate_registration_fee()`

Tests registration fees based on total credits, including the pricing transition at 12 credits and the valid range of 0 to 18 credits.

## Running the Tests

Run the complete test suite:

```bash
python -m pytest
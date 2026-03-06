import pandas as pd
import pytest

from app_api.maths.mon_module import add, print_data, square, sub


# Tests paramétrés pour add
@pytest.mark.parametrize(
    "a, b, expected",
    [
        (10, 2, 12),
        (20, 2, 22),
        (0, 2, 2),
        (-5, 5, 0),
    ],
)
def test_add(a, b, expected):
    """Test addition function."""
    assert add(a, b) == expected


# Tests simples pour sub et square


def test_sub():
    """Test de la soustraction."""
    assert sub(10, 5) == 5


def test_square():
    """Test du carré."""
    assert square(4) == 16


#   Fixture pour print_data
@pytest.fixture
def sample_df():
    """Sample DataFrame for testing."""
    return pd.DataFrame({"col1": [1, 2, 3]})


# le test
def test_print_data(sample_df):
    """Test print_data function."""
    assert print_data(sample_df) == 3

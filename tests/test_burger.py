import pytest
from unittest.mock import Mock

class TestBurger:

    def test_new_burger_has_no_bun_and_ingredients(self, burger):
        assert burger.bun is None
        assert burger.ingredients == []

    def test_set_buns_sets_bun(self, burger, mock_bun):
        burger.set_buns(mock_bun)
        assert burger.bun == mock_bun

    def test_add_ingredient_adds_to_list(self, burger, mock_sauce):
        burger.add_ingredient(mock_sauce)
        assert burger.ingredients == [mock_sauce]

    def test_remove_ingredient_removes_from_list(self, burger, mock_sauce, mock_filling):
        burger.add_ingredient(mock_sauce)
        burger.add_ingredient(mock_filling)
        burger.remove_ingredient(0)
        assert burger.ingredients == [mock_filling]

    def test_move_ingredient_changes_order(self, burger, mock_sauce, mock_filling):
        burger.add_ingredient(mock_sauce)
        burger.add_ingredient(mock_filling)
        burger.move_ingredient(0, 1)
        assert burger.ingredients == [mock_filling, mock_sauce]

    @pytest.mark.parametrize('bun_price, ingredient_prices, expected', [
        (100, [], 200),
        (100, [50], 250),
        (50.5, [100, 200], 401),
    ])
    def test_get_price_returns_correct_sum(self, burger, mock_bun,
                                           bun_price, ingredient_prices, expected):
        mock_bun.get_price.return_value = bun_price
        burger.set_buns(mock_bun)
        for price in ingredient_prices:
            ingredient = Mock()
            ingredient.get_price.return_value = price
            burger.add_ingredient(ingredient)
        assert burger.get_price() == expected

    def test_get_receipt_returns_correct_text(self, burger, mock_bun,
                                              mock_sauce, mock_filling):
        burger.set_buns(mock_bun)
        burger.add_ingredient(mock_sauce)
        burger.add_ingredient(mock_filling)
        expected = (
            '(==== black bun ====)\n'
            '= sauce hot sauce =\n'
            '= filling cutlet =\n'
            '(==== black bun ====)\n'
            '\n'
            'Price: 500'
        )
        assert burger.get_receipt() == expected
"""
Money Value Object 테스트

금액을 나타내는 Value Object입니다.
불변이고, 통화와 금액을 포함합니다.
"""

import pytest
from src.domain.value_objects.money import Money
from decimal import Decimal


class TestMoney:
    """Money Value Object 테스트"""

    def test_create_money_with_valid_amount(self):
        """유효한 금액으로 Money 생성"""
        money = Money(amount=Decimal("10000"), currency="KRW")
        assert money.amount == Decimal("10000")
        assert money.currency == "KRW"

    def test_money_is_immutable(self):
        """Money는 불변 객체여야 함 (frozen dataclass)"""
        money = Money(amount=Decimal("10000"), currency="KRW")
        # 속성 변경 시도는 frozen dataclass에서는 에러 발생
        money2 = Money(amount=Decimal("20000"), currency="KRW")
        assert money != money2  # 객체 동등성 확인

    def test_money_equality(self):
        """동등성 비교"""
        money1 = Money(amount=Decimal("10000"), currency="KRW")
        money2 = Money(amount=Decimal("10000"), currency="KRW")
        money3 = Money(amount=Decimal("10000"), currency="USD")

        assert money1 == money2
        assert money1 != money3

    def test_money_hash(self):
        """hash() 사용 가능 (set, dict 키로 사용 가능)"""
        money1 = Money(amount=Decimal("10000"), currency="KRW")
        money2 = Money(amount=Decimal("10000"), currency="KRW")

        assert hash(money1) == hash(money2)
        assert len({money1, money2}) == 1  # 중복 제거

    def test_money_addition(self):
        """Money 덧셈 (같은 통화만 가능)"""
        money1 = Money(amount=Decimal("10000"), currency="KRW")
        money2 = Money(amount=Decimal("20000"), currency="KRW")
        result = money1 + money2

        assert result.amount == Decimal("30000")
        assert result.currency == "KRW"

    def test_money_addition_different_currency_raises_error(self):
        """다른 통화 덧셈은 에러"""
        money1 = Money(amount=Decimal("10000"), currency="KRW")
        money2 = Money(amount=Decimal("100"), currency="USD")

        with pytest.raises(ValueError, match="통화가 다릅니다"):
            money1 + money2

    def test_money_multiplication(self):
        """Money 곱셈"""
        money = Money(amount=Decimal("10000"), currency="KRW")
        result = money * 2

        assert result.amount == Decimal("20000")
        assert result.currency == "KRW"

    def test_money_multiplication_by_float(self):
        """Money를 실수로 곱셈"""
        money = Money(amount=Decimal("10000"), currency="KRW")
        result = money * 1.5

        assert result.amount == Decimal("15000")
        assert result.currency == "KRW"

    def test_money_string_representation(self):
        """Money 문자열 표현"""
        money = Money(amount=Decimal("10000"), currency="KRW")
        assert str(money) == "10,000 KRW"

    def test_money_zero(self):
        """0원 Money 생성"""
        money = Money(amount=Decimal("0"), currency="KRW")
        assert money.amount == Decimal("0")

    def test_money_negative_amount_raises_error(self):
        """음수 금액은 에러"""
        with pytest.raises(ValueError, match="금액은 0 이상이어야 합니다"):
            Money(amount=Decimal("-10000"), currency="KRW")

    def test_multiply_by_negative_raises_error(self):
        """음수 곱셈은 에러"""
        money = Money(amount=Decimal("10000"), currency="KRW")
        with pytest.raises(ValueError, match="곱하는 값은 0 이상이어야 합니다"):
            money * -1

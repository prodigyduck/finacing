"""Tests for Account entity"""
import pytest
from src.domain.entities.account import Account, AccountType


def test_account_creation_valid():
    """유효한 계좌 생성"""
    account = Account(name="증권계좌", type=AccountType.SECURITIES)
    assert account.name == "증권계좌"
    assert account.type == AccountType.SECURITIES


def test_account_creation_with_type_null():
    """계좌 유형 없이 생성"""
    account = Account(name="ISA")
    assert account.name == "ISA"
    assert account.type is None


def test_account_creation_invalid_empty_name():
    """빈 계좌명으로 생성 실패"""
    with pytest.raises(ValueError, match="계좌명은 비어있을 수 없습니다"):
        Account(name="")


def test_account_creation_invalid_whitespace_name():
    """공백만 있는 계좌명으로 생성 실패"""
    with pytest.raises(ValueError, match="계좌명은 비어있을 수 없습니다"):
        Account(name="   ")


def test_account_type_enum_values():
    """AccountType enum 값 확인"""
    assert AccountType.SECURITIES.value == "securities"
    assert AccountType.ISA.value == "isa"
    assert AccountType.IRA.value == "ira"
    assert AccountType.PENSION.value == "pension"
    assert AccountType.CASH.value == "cash"
    assert AccountType.OTHER.value == "other"


def test_account_immutability():
    """Account 엔티티 불변성 확인"""
    account = Account(name="증권계좌")
    with pytest.raises(AttributeError):
        account.name = "다른계좌"

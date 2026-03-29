"""
AssetType Enum

자산 유형을 나타내는 Enum입니다.
"""

from enum import Enum


class AssetType(Enum):
    """자산 유형"""

    STOCK = "STOCK"
    ETF = "ETF"
    BOND = "BOND"
    CASH = "CASH"
    OTHER = "OTHER"

    @classmethod
    def from_string(cls, value: str) -> "AssetType":
        """
        문자열로부터 AssetType 반환

        Args:
            value: 자산 유형 문자열 (한국어/영어/소문자/대문자)

        Returns:
            해당 AssetType, 없으면 OTHER
        """
        korean_names = {
            "주식": cls.STOCK,
            "STOCK": cls.STOCK,
            "stock": cls.STOCK,
            "ETF": cls.ETF,
            "etf": cls.ETF,
            "채권": cls.BOND,
            "BOND": cls.BOND,
            "bond": cls.BOND,
            "현금": cls.CASH,
            "CASH": cls.CASH,
            "cash": cls.CASH,
        }
        return korean_names.get(value, cls.OTHER)

    def display_name(self) -> str:
        """한국어 표시 이름"""
        display_map = {
            AssetType.STOCK: "주식",
            AssetType.ETF: "ETF",
            AssetType.BOND: "채권",
            AssetType.CASH: "현금",
            AssetType.OTHER: "기타",
        }
        return display_map[self]

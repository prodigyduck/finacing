"""GKeepRepository

Repository for fetching data using Google Keep API.
"""

from typing import List
import logging

import gkeepapi

from src.application.ports.keep_repository import IKeepRepository
from src.domain.entities.investment_asset import InvestmentAsset
from src.infrastructure.parsers.note_parser import NoteParser
from src.infrastructure.retry import retry
from src.infrastructure.errors import RateLimitError


logger = logging.getLogger(__name__)


class GKeepRepository(IKeepRepository):
    """Google Keep repository"""

    def __init__(
        self, email: str, password: str, parser: NoteParser = None
    ):
        self._email = email
        self._password = password
        self._parser = parser or NoteParser()
        self._keep = None

    @retry(max_attempts=3, delay=2.0, backoff_factor=2.0)
    def _login(self):
        """Login to Google Keep with retry logic"""
        if self._keep is None:
            self._keep = gkeepapi.Keep()
            auth = gkeepapi.APIAuth(gkeepapi.Keep.OAUTH_SCOPES)
            auth.login(self._email, self._password, device_id=self._email)
            self._keep.load(auth)

    @retry(max_attempts=3, delay=1.0, backoff_factor=2.0)
    def fetch_investment_notes(self, label: str) -> List[InvestmentAsset]:
        """
        Fetch investment notes from Google Keep with specified label and parse them.

        Args:
            label: Label name to search (e.g., "투자")

        Returns:
            List of parsed investment assets
        """
        # Login
        try:
            self._login()
        except Exception as e:
            # gkeepapi may raise library-specific exceptions; detect 429 by attribute
            status = getattr(e, "status_code", None)
            if status == 429:
                logger.warning("GKeep API returned 429 - rate limited")
                raise RateLimitError("gkeep rate limited") from e
            raise

        # Find label
        labels = self._keep.findLabels([label])
        if not labels:
            logger.warning(f"Label '{label}' not found in Google Keep")
            return []

        label_id = labels[0].id

        # Find notes with matching label
        notes = []
        for note in self._keep.all():
            if label_id in [lbl.id for lbl in note.labels.all()]:
                notes.append(note)

        # Parse
        assets = []
        for note in notes:
            note_assets = self._parser.parse_text(note.text)
            assets.extend(note_assets)

        return assets

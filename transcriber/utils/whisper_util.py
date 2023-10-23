# encoding=utf-8
from django.core.cache import cache
import logging

# service
from transcriber.services.whisper_service import WhisperService


logger = logging.getLogger(__name__)


class WhisperUtil:
    WHISPER_CACHE_KEY = "cached_whisper"

    def __init__(self):
        pass

    def get_whisper(self) -> WhisperService:
        """
        get whisper service from cache, if it's not cached..., cache first an return
        :return: Whisper service
        :rtype: WhisperService
        """
        logger.info("[get_whisper]: fetching whisper service from cache...")
        whisper_service = cache.get(self.WHISPER_CACHE_KEY)

        logger.info("[get_whisper]: checking if whisper service is cached...")
        # check if whisper service is cached or not
        if whisper_service is None:
            logger.warning("[get_whisper]: whisper service has not been cached!")
            logger.info("[get_whisper]: caching whisper service")
            whisper_service = WhisperService()
            cache.set(self.WHISPER_CACHE_KEY, whisper_service, None)
            logger.info("[get_whisper]: whisper service has been cached!")

        return whisper_service

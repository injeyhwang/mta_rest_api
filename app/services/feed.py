import json
from pathlib import Path
from typing import Dict, Tuple

import requests
from fastapi import status
from google.protobuf.json_format import MessageToDict
from google.transit import gtfs_realtime_pb2

from app.config import settings
from app.exceptions.feed import (FeedEndpointNotFoundError, FeedFetchError,
                                 FeedProcessingError, FeedServiceError,
                                 FeedTimeoutError)
from app.schemas.feed import FeedDetailed
from app.utils.logger import logger


class FeedService:
    """
    FeedService object that loads GTFS-RT feed endpoints from
    mta_feed_urls.json and provides methods to to interact with MTA's GTFS-RT
    API.

    Check https://api.mta.info/#/ for real time data feeds developer resources.
    """

    def __init__(self):
        self.mta_endpoints = self._load_endpoint_urls()

    def get_feed(self, feed: str) -> FeedDetailed:
        """
        Get real-time data from MTA's GTFS-RT API for the specified feed.

        Args:
            feed (str): MTA real time service to request

        Raises:
            FeedEndpointNotFoundError: Feed endpoint configuration is missing
            FeedFetchError: Error fetching feed from MTA API
            FeedTimeoutError: Request to MTA API timed out
            FeedProcessingError: Error processing the feed data

        Returns:
            FeedDetailed: Parsed GTFS-RT message for a specific feed.
        """
        mta_endpoint: str = self._get_endpoint_url(feed=feed)
        if not mta_endpoint:
            logger.error(f"No endpoint configuration found for feed: '{feed}'")
            raise FeedEndpointNotFoundError(
                f"No endpoint configuration found for feed: '{feed}'")

        logger.info(f"Fetching GTFS-RT feed from endpoint: '{mta_endpoint}'")
        feed_message = gtfs_realtime_pb2.FeedMessage()

        try:
            res = requests.get(mta_endpoint, timeout=10)
            if res.status_code != status.HTTP_200_OK:
                err_msg = f"[{res.status_code}]: Error fetching GTFS-RT feed"
                logger.error(err_msg)
                raise FeedFetchError(err_msg)

            logger.info("Parsing GTFS-RT feed")
            feed_message.ParseFromString(res.content)
            logger.info("Converting protobuf message to dictionary")
            feed_dict = MessageToDict(
                feed_message, preserving_proto_field_name=True)
            logger.info("Successfully processed GTFS-RT feed")
            return FeedDetailed(**feed_dict)

        except requests.exceptions.Timeout:
            logger.error("Timeout while fetching GTFS-RT feed")
            raise FeedTimeoutError("Timeout while fetching GTFS-RT feed")

        except FeedServiceError:
            raise

        except Exception as e:
            logger.exception(f"Error processing GTFS-RT feed: {e}")
            raise FeedProcessingError(f"Error processing GTFS-RT feed: {e}")

    def get_paginated_feed(self,
                           feed: str,
                           offset: int,
                           limit: int) -> Tuple[FeedDetailed, int]:
        """
        Get paginated real-time data from MTA's GTFS-RT API for the specified
        feed.

        Args:
            feed (str): Feed identifier
            offset (int): Number of items to skip
            limit (int): Maximum number of items to return

        Returns:
            Tuple[FeedDetailed, int]: Tuple of FeedDetailed and total_items
        """
        feed_data = self.get_feed(feed)
        total_items = len(feed_data.entity)

        # must handle pagination in-memory because MTA API doesn't offer this
        # feature 😭
        feed_data.entity = feed_data.entity[offset:offset + limit]

        return feed_data, total_items

    def _load_endpoint_urls(self) -> Dict[str, str]:
        """
        Load MTA feed endpoint URLs from 'mta_feed_urls.json' file.

        This is an internal method and is not to be used outside of
        FeedService.

        Returns:
            Dict[str, str]: Feed to API Endpoint key-value pairs.
        """
        json_file_path = Path(settings.mta_feed_urls_path)
        with open(json_file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _get_endpoint_url(self, feed: str) -> str | None:
        """
        Get the endpoint URL for a specific MTA GTFS-RT feed.

        This is an internal method and is not to be used outside of
        FeedService.

        Args:
            feed (str): The feed to get the URL for.

        Returns:
            str | None: The endpoint URL, or None if not found.
        """
        return self.mta_endpoints.get(feed)


feed_service = FeedService()

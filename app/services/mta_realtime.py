from fastapi import HTTPException, status
from google.protobuf.json_format import MessageToDict
from google.transit import gtfs_realtime_pb2
import json
from pathlib import Path
import requests
from typing import Dict

from app.utils.logger import logger


class MTAServiceRT:
    """
    MTA service object that loads GTFS-RT feed endpoints from mta_feed_urls.json and provides the
    method: 'get_mta_rt_service(feed: MTAFeed)' to interact with MTA's GTFS-RT API.

    Check https://api.mta.info/#/ for real time data feeds developer resources.
    """

    def __init__(self):
        self.mta_endpoints = self._load_endpoint_urls()

    def get_mta_feed(self, feed: str):
        """
        Args:
            feed (str): MTA real time service to request; supports Subway, LIRR, and Metro-North RR.

        Raises:
            HTTPException: 500 Internal Server Error. Feed endpoint configuration is missing in JSON.
            HTTPException: 502 Bad Gateway. There is an issue interacting with MTA's GTFS-RT API.
            HTTPException: 504 Gateway Timeout. GTFS-RT request timed out.

        Returns:
            Dict[str: Any]: Dictionary converted GTFS-RT message.
        """
        mta_endpoint: str = self._get_endpoint_url(feed=feed)
        if not mta_endpoint:
            logger.error(f"No endpoint configuration found for feed: {feed}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"No endpoint configuration found for feed: {feed}")

        logger.info(f"Fetching GTFS-RT feed from endpoint: {mta_endpoint}")
        feed = gtfs_realtime_pb2.FeedMessage()

        try:
            res = requests.get(mta_endpoint, timeout=10)
            if res.status_code != status.HTTP_200_OK:
                logger.error(f"Error fetching GTFS-RT feed. Status code: {res.status_code}")
                raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY,
                                    detail="Error fetching GTFS-RT feed.")

            logger.info("Parsing GTFS-RT feed")
            feed.ParseFromString(res.content)
            logger.info("Converting protobuf message to dictionary")
            feed_dict = MessageToDict(feed, preserving_proto_field_name=True)
            logger.info("Successfully processed GTFS-RT feed")
            return feed_dict

        except requests.exceptions.Timeout:
            logger.error("Timeout while fetching GTFS-RT feed")
            raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                                detail="Timeout while fetching GTFS-RT feed")

        except Exception as e:
            logger.exception(f"Error processing GTFS-RT feed: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Error processing GTFS-RT feed")

    def _load_endpoint_urls(self) -> Dict[str, str]:
        """
        Load MTA feed endpoint URLs from 'mta_rt_feed_urls.json' file.

        This is an internal method and is not to be used outside of MTAServiceRT.

        Returns:
            Dict[str, str]: Feed to API Endpoint key-value pairs.
        """
        json_file_path = Path("app/services/mta_rt_feed_urls.json")
        with open(json_file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _get_endpoint_url(self, feed: str) -> str | None:
        """
        Get the endpoint URL for a specific MTA GTFS-RT feed.

        This is an internal method and is not to be used outside of MTAServiceRT.

        Args:
            feed (str): The feed to get the URL for.

        Returns:
            str | None: The endpoint URL, or None if not found.
        """
        return self.mta_endpoints.get(feed)

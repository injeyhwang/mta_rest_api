from fastapi import HTTPException
from google.protobuf.json_format import MessageToDict
from google.transit import gtfs_realtime_pb2
import json
from pathlib import Path
import requests
from typing import Dict, Optional


class MTAFeed:
    """
    Available real time MTA Feeds
    """

    LIRR = "LIRR"
    MNR = "MNR"
    SUBWAY_LINES = ["ACE", "BDFM", "G", "JZ", "NQRW", "L", "S1234567", "SIR"]


class MTAServiceRT:
    """
    MTA service object that loads GTFS-RT feed endpoints from mta_feed_urls.json and provides the
    method: 'get_mta_feed(feed: MTAFeed)' to interact with MTA's GTFS-RT API.

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

        Returns:
            Dict[str: Any]: Dictionary converted GTFS-RT message.
        """
        mta_endpoint: str = self._get_endpoint_url(feed=feed)
        if not mta_endpoint:
            # this shouldn't happen
            raise HTTPException(status_code=500, detail=f"No endpoint configuration found for feed: {feed}")

        feed = gtfs_realtime_pb2.FeedMessage()

        res = requests.get(mta_endpoint)
        if res.status_code != 200:
            raise HTTPException(status_code=502, detail="Error fetching GTFS-RT feed.")

        feed.ParseFromString(res.content)
        feed_dict = MessageToDict(feed, preserving_proto_field_name=True)
        return feed_dict

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

    def _get_endpoint_url(self, feed: str) -> Optional[str]:
        """
        Get the endpoint URL for a specific MTA GTFS-RT feed.

        This is an internal method and is not to be used outside of MTAServiceRT.

        Args:
            feed (str): The feed to get the URL for.

        Returns:
            Optional[str]: The endpoint URL, or None if not found.
        """
        return self.mta_endpoints.get(feed)

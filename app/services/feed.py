import json
from pathlib import Path
from typing import Dict, List, Tuple

import requests
from fastapi import status
from google.protobuf.json_format import MessageToDict
from google.transit import gtfs_realtime_pb2

from app.config import settings
from app.exceptions.feed import (FeedEndpointNotFoundError, FeedFetchError,
                                 FeedProcessingError, FeedServiceError,
                                 FeedTimeoutError)
from app.schemas.feed import (AlertEntity, Entity, EntityType, FeedResponse,
                              TripUpdateEntity, VehicleEntity)
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

    def get_feed(self, feed: str) -> FeedResponse:
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
            FeedResponse: Parsed GTFS-RT message for a specific feed.
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
            return FeedResponse(**feed_dict)

        except requests.exceptions.Timeout:
            logger.error("Timeout while fetching GTFS-RT feed")
            raise FeedTimeoutError("Timeout while fetching GTFS-RT feed")

        except FeedServiceError:
            raise

        except Exception as e:
            logger.exception(f"Error processing GTFS-RT feed: {e}")
            raise FeedProcessingError(f"Error processing GTFS-RT feed: {e}")

    def get_alerts(self, feed: str) -> Tuple[FeedResponse, int]:
        """
        Get real-time alert data from MTA's GTFS-RT API for the specified feed.

        Args:
            feed (str): Feed identifier

        Returns:
            Tuple[FeedResponse, int]: Tuple of alert filtered FeedResponse and
            the filtered entities count
        """
        feed_res: FeedResponse = self.get_feed(feed)

        filtered_entities: List[AlertEntity] = []
        for entity in feed_res.entity:
            if self._include_entity(entity=entity, filter_by=EntityType.ALERT):
                filtered_entities.append(entity)
        entity_count = len(filtered_entities)
        return (FeedResponse(header=feed_res.header,
                             entity=filtered_entities), entity_count)

    def get_trip_updates(
            self,
            feed: str,
            route_id: str | None = None,
            stop_id: str | None = None,
            trip_id: str | None = None) -> Tuple[FeedResponse, int]:
        """
        Get real-time trip update data from MTA's GTFS-RT API for the specified
        feed.

        Args:
            feed (str): Feed identifier
            route_id (str | None): Route ID to filter by
            stop_id (str | None): Stop ID to filter by
            trip_id (str | None): Trip ID to filter by

        Returns:
            Tuple[FeedResponse, int]: Tuple of trip_update filtered
            FeedResponse and the filtered entities count
        """
        feed_res: FeedResponse = self.get_feed(feed)

        filtered_entities: List[TripUpdateEntity] = []
        for entity in feed_res.entity:
            if self._include_entity(entity=entity,
                                    route_id=route_id,
                                    stop_id=stop_id,
                                    trip_id=trip_id,
                                    filter_by=EntityType.TRIP_UPDATE):
                filtered_entities.append(entity)
        entity_count = len(filtered_entities)
        return (FeedResponse(header=feed_res.header,
                             entity=filtered_entities), entity_count)

    def get_vehicle_updates(
            self,
            feed: str,
            route_id: str | None = None,
            stop_id: str | None = None,
            trip_id: str | None = None) -> Tuple[FeedResponse, int]:
        """
        Get real-time vehicle data from MTA's GTFS-RT API for the specified
        feed.

        Args:
            feed (str): Feed identifier
            route_id (str | None): Route ID to filter by
            stop_id (str | None): Stop ID to filter by
            trip_id (str | None): Trip ID to filter by

        Returns:
            Tuple[FeedResponse, int]: Tuple of vehicle filtered FeedResponse
            and the filtered entities count
        """
        feed_res: FeedResponse = self.get_feed(feed)

        filtered_entities: List[VehicleEntity] = []
        for entity in feed_res.entity:
            if self._include_entity(entity=entity,
                                    route_id=route_id,
                                    stop_id=stop_id,
                                    trip_id=trip_id,
                                    filter_by=EntityType.VEHICLE):
                filtered_entities.append(entity)
        entity_count = len(filtered_entities)
        return (FeedResponse(header=feed_res.header,
                             entity=filtered_entities), entity_count)

    def get_all_feed(self,
                     feed: str,
                     route_id: str | None = None,
                     stop_id: str | None = None,
                     trip_id: str | None = None,
                     entity_type: EntityType | None = None,
                     offset: int = 0,
                     limit: int = 1000) -> Tuple[FeedResponse, int]:
        """
        Get all real-time paginated data from MTA's GTFS-RT API for the
        specified feed.

        Args:
            feed (str): Feed identifier
            route_id (str | None): Route ID to filter by
            stop_id (str | None): Stop ID to filter by
            trip_id (str | None): Trip ID to filter by
            entity_type (EntityType | None): Entity type to filter by
            offset (int): Number of items to skip
            limit (int): Maximum number of items to return

        Returns:
            Tuple[FeedResponse, int]: Tuple of FeedResponse and total_items
        """
        feed_res: FeedResponse = self.get_feed(feed)

        filtered_entities: List[Entity] = []
        for entity in feed_res.entity:
            if self._include_entity(entity=entity,
                                    route_id=route_id,
                                    stop_id=stop_id,
                                    trip_id=trip_id,
                                    filter_by=entity_type):
                filtered_entities.append(entity)

        # apply pagination to filtered_entities
        entity_count = len(filtered_entities)
        filtered_entities = filtered_entities[offset:offset + limit]

        filtered_res = FeedResponse(header=feed_res.header,
                                    entity=filtered_entities)
        return filtered_res, entity_count

    def _include_entity(
            self,
            entity: Entity,
            route_id: str | None = None,
            stop_id: str | None = None,
            trip_id: str | None = None,
            filter_by: EntityType | None = None) -> bool:
        """
        Evaluate the given entity if it should be included in the result.

        Args:
            entity (Entity): The feed entity data to evaluate for filtering
            route_id (str | None): Route ID to filter by
            stop_id (str | None): Stop ID to filter by
            trip_id (str | None): Trip ID to filter by
            filter_by (EntityType | None): Entity type to filter by

        Returns:
            bool: True if entity should be included. False otherwise.
        """
        # No need to filter if no filters are given
        if (route_id is None
                and stop_id is None and trip_id is None and filter_by is None):
            return True

        if entity.entity_type == EntityType.ALERT:
            if filter_by and filter_by != EntityType.ALERT:
                return False
            # alert entities can't be filtered by route_id, stop_id, trip_id

        elif entity.entity_type == EntityType.TRIP_UPDATE:
            if filter_by and filter_by != EntityType.TRIP_UPDATE:
                return False

            trip_update = entity.trip_update
            if trip_id and trip_update.trip.trip_id != trip_id:
                return False
            if route_id and trip_update.trip.route_id != route_id:
                return False

            if stop_id:
                if len(trip_update.stop_time_update) == 0:
                    return False
                stop_time_update = trip_update.stop_time_update
                if not any(stu.stop_id == stop_id for stu in stop_time_update):
                    return False

        elif entity.entity_type == EntityType.VEHICLE:
            if filter_by and filter_by != EntityType.VEHICLE:
                return False

            vehicle = entity.vehicle
            if trip_id and vehicle.trip.trip_id != trip_id:
                return False
            if route_id and vehicle.trip.route_id != route_id:
                return False
            if stop_id and entity.vehicle.stop_id != stop_id:
                return False

        return True

    def _load_endpoint_urls(self) -> Dict[str, str]:
        """
        Load MTA feed endpoint URLs from 'mta_feed_urls.json' file.

        Returns:
            Dict[str, str]: Feed to API Endpoint key-value pairs.
        """
        json_file_path = Path(settings.mta_feed_urls_path)
        with open(json_file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _get_endpoint_url(self, feed: str) -> str | None:
        """
        Get the endpoint URL for a specific MTA GTFS-RT feed.

        Args:
            feed (str): The feed to get the URL for.

        Returns:
            str | None: The endpoint URL, or None if not found.
        """
        return self.mta_endpoints.get(feed)


feed_service = FeedService()

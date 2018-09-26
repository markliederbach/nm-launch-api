"""
Similar to Serializers in Django, these manage the conversion between
raw JSON and models. This is where parsing validation should be done.
"""
from datetime import datetime
from marshmallow import Schema, fields


class AgencySchema(Schema):
    name = fields.String()
    info_url = fields.String()

    def get_info_url(self, obj):
        return obj["wikiURL"]


class MissionSchema(Schema):
    name = fields.String()
    description = fields.String()
    agencies = fields.Nested(AgencySchema, many=True)


class RocketSchema(Schema):
    name = fields.String()
    info_url = fields.Method("get_info_url")

    def get_info_url(self, obj):
        return obj["wikiURL"]


class LocationSchema(Schema):
    name = fields.String()
    map_url = fields.Method("get_map_url")

    def get_map_url(self, obj):
        chosen_pad = next(iter(obj["pads"]), None)
        return chosen_pad["mapURL"] if chosen_pad else None


class LaunchInfoSchema(Schema):
    name = fields.String()
    est_timestamp = fields.Method("get_est_timestamp")
    location = fields.Nested(LocationSchema)
    rocket = fields.Nested(RocketSchema)
    missions = fields.Nested(MissionSchema, many=True)

    def get_est_timestamp(self, obj):
        raw_timestamp = obj["net"]
        if raw_timestamp:
            timestamp = datetime.strptime(raw_timestamp, "%B %d, %Y %H:%M:%S %Z")
            return timestamp.isoformat()
        return None

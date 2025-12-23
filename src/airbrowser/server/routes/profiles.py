"""Profile management routes for Airbrowser API."""

import time

from flask import request
from flask_restx import Namespace, Resource


def create_profile_namespace(api, browser_pool, schemas):
    """Create and configure the profiles namespace."""

    profiles_ns = Namespace("profiles", description="Browser profile management")

    @profiles_ns.route("/")
    class ProfileList(Resource):
        @profiles_ns.doc("list_profiles")
        @profiles_ns.response(200, "Success", schemas["ProfileListResponse"])
        def get(self):
            """List all browser profiles."""
            profiles = browser_pool.list_profiles()
            return {
                "success": True,
                "message": "Profiles retrieved",
                "timestamp": time.time(),
                "data": {"profiles": profiles},
            }

        @profiles_ns.doc("create_profile")
        @profiles_ns.expect(schemas["CreateProfileRequest"])
        @profiles_ns.response(200, "Success", schemas["ProfileResponse"])
        @profiles_ns.response(400, "Bad request")
        def post(self):
            """Create a new browser profile."""
            data = request.get_json(silent=True) or {}
            name = data.get("name")

            if not name:
                return {
                    "success": False,
                    "message": "Profile name is required",
                    "timestamp": time.time(),
                }, 400

            try:
                profile = browser_pool.create_profile(name)
                return {
                    "success": True,
                    "message": f"Profile '{name}' created",
                    "timestamp": time.time(),
                    "data": profile,
                }
            except ValueError as e:
                return {
                    "success": False,
                    "message": str(e),
                    "timestamp": time.time(),
                }, 400

    @profiles_ns.route("/<string:profile_name>")
    @profiles_ns.param("profile_name", "Profile name")
    class Profile(Resource):
        @profiles_ns.doc("get_profile")
        @profiles_ns.response(200, "Success", schemas["ProfileResponse"])
        @profiles_ns.response(404, "Profile not found")
        def get(self, profile_name):
            """Get profile information."""
            profile = browser_pool.get_profile(profile_name)
            if not profile:
                return {
                    "success": False,
                    "message": f"Profile '{profile_name}' not found",
                    "timestamp": time.time(),
                }, 404

            return {
                "success": True,
                "message": "Profile retrieved",
                "timestamp": time.time(),
                "data": profile,
            }

        @profiles_ns.doc("delete_profile")
        @profiles_ns.response(200, "Success")
        @profiles_ns.response(400, "Profile in use")
        @profiles_ns.response(404, "Profile not found")
        def delete(self, profile_name):
            """Delete a browser profile."""
            try:
                if browser_pool.delete_profile(profile_name):
                    return {
                        "success": True,
                        "message": f"Profile '{profile_name}' deleted",
                        "timestamp": time.time(),
                    }
                return {
                    "success": False,
                    "message": f"Profile '{profile_name}' not found",
                    "timestamp": time.time(),
                }, 404
            except ValueError as e:
                return {
                    "success": False,
                    "message": str(e),
                    "timestamp": time.time(),
                }, 400

    return profiles_ns

#!/usr/bin/env python3
"""
Test suite for browser profiles feature.

Tests profile management API and browser creation with profiles.

Run with: pytest tests/test_profiles.py -v
"""

import uuid

import pytest
from airbrowser_client.models import BrowsersRequest, CreateBrowserRequest, CreateProfileRequest


@pytest.fixture(scope="function")
def test_profile(profiles_client):
    """Create a unique test profile and clean up after."""
    profile_name = f"test-profile-{uuid.uuid4().hex[:8]}"

    # Create profile
    result = profiles_client.create_profile(payload=CreateProfileRequest(name=profile_name))
    assert result.success, f"Failed to create profile: {result.message}"

    yield profile_name

    # Cleanup - delete the profile
    try:
        profiles_client.delete_profile(profile_name)
    except Exception:
        pass


class TestProfileManagement:
    """Test profile CRUD operations."""

    def test_list_profiles(self, profiles_client):
        """Test GET /profiles/ endpoint."""
        result = profiles_client.list_profiles()
        assert result is not None
        assert result.success
        assert result.data is not None
        # data is ProfileListData Pydantic model with 'profiles' attribute
        assert hasattr(result.data, 'profiles')
        assert isinstance(result.data.profiles, list)

    def test_create_profile(self, profiles_client):
        """Test POST /profiles/ endpoint."""
        profile_name = f"test-create-{uuid.uuid4().hex[:8]}"

        result = profiles_client.create_profile(payload=CreateProfileRequest(name=profile_name))
        assert result is not None
        assert result.success
        assert result.data is not None
        # data is ProfileInfo Pydantic model with name, in_use attributes
        assert result.data.name == profile_name
        assert result.data.in_use is False

        # Cleanup
        profiles_client.delete_profile(profile_name)

    def test_create_profile_duplicate_fails(self, profiles_client, test_profile):
        """Test that creating a profile with existing name fails."""
        # Try to create a profile with the same name
        with pytest.raises(Exception) as exc_info:
            profiles_client.create_profile(payload=CreateProfileRequest(name=test_profile))

        # Should get 400 Bad Request
        assert "400" in str(exc_info.value)

    def test_create_profile_invalid_name_fails(self, profiles_client):
        """Test that invalid profile names are rejected."""
        invalid_names = [
            "test profile",  # spaces
            "test/profile",  # slashes
            "test..profile",  # double dots
            "../escape",  # path traversal
        ]

        for name in invalid_names:
            with pytest.raises(Exception):
                profiles_client.create_profile(payload=CreateProfileRequest(name=name))

    def test_get_profile(self, profiles_client, test_profile):
        """Test GET /profiles/{profile_name} endpoint."""
        result = profiles_client.get_profile(test_profile)
        assert result is not None
        assert result.success
        assert result.data is not None
        # data is ProfileInfo Pydantic model
        assert result.data.name == test_profile
        assert result.data.in_use is False

    def test_get_profile_not_found(self, profiles_client):
        """Test GET /profiles/{profile_name} with non-existent profile."""
        with pytest.raises(Exception) as exc_info:
            profiles_client.get_profile("nonexistent-profile-xyz")

        # Should get 404 Not Found
        assert "404" in str(exc_info.value)

    def test_delete_profile(self, profiles_client):
        """Test DELETE /profiles/{profile_name} endpoint."""
        # Create a profile to delete
        profile_name = f"test-delete-{uuid.uuid4().hex[:8]}"
        profiles_client.create_profile(payload=CreateProfileRequest(name=profile_name))

        # Delete it - note: delete may return None if no response schema is defined
        # The important thing is that no exception is raised
        profiles_client.delete_profile(profile_name)

        # Verify it's gone
        with pytest.raises(Exception) as exc_info:
            profiles_client.get_profile(profile_name)
        assert "404" in str(exc_info.value)

    def test_delete_profile_not_found(self, profiles_client):
        """Test DELETE /profiles/{profile_name} with non-existent profile."""
        with pytest.raises(Exception) as exc_info:
            profiles_client.delete_profile("nonexistent-profile-xyz")

        # Should get 404 Not Found
        assert "404" in str(exc_info.value)


@pytest.mark.flaky(reruns=2, reruns_delay=3)
class TestBrowserWithProfile:
    """Test browser creation and lifecycle with profiles."""

    def test_create_browser_with_profile(self, browser_client, profiles_client, test_profile):
        """Test creating a browser with a profile."""
        config = CreateBrowserRequest(profile_name=test_profile)
        result = browser_client.create_browser(payload=config)

        assert result is not None
        assert result.success
        assert result.data is not None
        assert result.data['browser_id'] is not None
        assert result.data.get('config', {}).get("profile_name") == test_profile

        browser_id = result.data['browser_id']

        # Wait for browser to initialize

        # Verify profile is marked as in use
        profile_info = profiles_client.get_profile(test_profile)
        assert profile_info.data.in_use is True

        # Cleanup
        browser_client.close_browser(browser_id)

    def test_create_browser_fresh_session(self, browser_client):
        """Test creating a browser without a profile (fresh session)."""
        config = CreateBrowserRequest()  # No profile_name
        result = browser_client.create_browser(payload=config)

        assert result is not None
        assert result.success
        assert result.data is not None
        assert result.data['browser_id'] is not None
        # profile_name should be None or not present
        assert result.data.get('config', {}).get("profile_name") is None

        # Cleanup
        browser_client.close_browser(result.data['browser_id'])

    def test_profile_lock_prevents_duplicate_browser(self, browser_client, profiles_client, test_profile):
        """Test that only one browser can use a profile at a time."""
        # Create first browser with profile
        config = CreateBrowserRequest(profile_name=test_profile)
        result1 = browser_client.create_browser(payload=config)
        assert result1.success
        browser_id = result1.data['browser_id']

        # Wait for browser to fully initialize and lock the profile

        # Verify profile is actually marked as in use before testing duplicate
        profile_info = profiles_client.get_profile(test_profile)
        assert profile_info.data.in_use is True, "Profile should be in use before testing lock"

        # Try to create second browser with same profile - should fail
        # The API might return success=False or raise an exception depending on HTTP status code
        try:
            result2 = browser_client.create_browser(payload=config)
            # If no exception, check that it failed with success=False
            assert result2.success is False, "Second browser creation with same profile should fail"
            assert "already in use" in result2.message.lower() or "profile" in result2.message.lower()
        except Exception as e:
            # Should get 409 Conflict or similar error
            assert "409" in str(e) or "already in use" in str(e).lower()

        # Cleanup
        try:
            browser_client.close_browser(browser_id)
        except Exception:
            pass

    def test_profile_released_on_browser_close(self, browser_client, profiles_client, test_profile):
        """Test that profile is released when browser is closed."""
        # Create browser with profile
        config = CreateBrowserRequest(profile_name=test_profile)
        result = browser_client.create_browser(payload=config)
        assert result.success
        browser_id = result.data['browser_id']


        # Verify profile is in use
        profile_info = profiles_client.get_profile(test_profile)
        assert profile_info.data.in_use is True

        # Close browser
        browser_client.close_browser(browser_id)

        # Verify profile is released
        profile_info = profiles_client.get_profile(test_profile)
        assert profile_info.data.in_use is False

        # Should be able to create another browser with the same profile
        result2 = browser_client.create_browser(payload=config)
        assert result2.success

        # Cleanup
        browser_client.close_browser(result2.data['browser_id'])

    def test_profile_released_on_close_all(self, browser_client, profiles_client, test_profile):
        """Test that profile is released when close_all is called."""
        # Create browser with profile
        config = CreateBrowserRequest(profile_name=test_profile)
        result = browser_client.create_browser(payload=config)
        assert result.success


        # Verify profile is in use
        profile_info = profiles_client.get_profile(test_profile)
        assert profile_info.data.in_use is True

        # Close all browsers
        browser_client.browsers(payload=BrowsersRequest(action="close_all"))

        # Verify profile is released
        profile_info = profiles_client.get_profile(test_profile)
        assert profile_info.data.in_use is False

    def test_create_browser_with_nonexistent_profile(self, browser_client):
        """Test creating a browser with a non-existent profile creates it."""
        # Use a unique profile name that doesn't exist
        profile_name = f"auto-create-{uuid.uuid4().hex[:8]}"

        config = CreateBrowserRequest(profile_name=profile_name)
        result = browser_client.create_browser(payload=config)

        # Browser creation should succeed (profile is auto-created)
        assert result is not None
        assert result.success
        browser_id = result.data['browser_id']


        # Cleanup
        browser_client.close_browser(browser_id)


@pytest.mark.flaky(reruns=2, reruns_delay=3)
class TestDeleteProfileInUse:
    """Test that profile in use cannot be deleted."""

    def test_delete_profile_in_use_fails(self, browser_client, profiles_client, test_profile):
        """Test that deleting a profile in use fails."""
        # Create browser with profile
        config = CreateBrowserRequest(profile_name=test_profile)
        result = browser_client.create_browser(payload=config)
        assert result.success
        browser_id = result.data['browser_id']

        # Wait for browser to fully initialize and lock the profile

        # Verify profile is actually marked as in use before testing delete
        profile_info = profiles_client.get_profile(test_profile)
        assert profile_info.data.in_use is True, "Profile should be in use"

        # Try to delete profile - should fail with 400
        with pytest.raises(Exception) as exc_info:
            profiles_client.delete_profile(test_profile)

        # Should get 400 Bad Request
        assert "400" in str(exc_info.value)

        # Cleanup
        try:
            browser_client.close_browser(browser_id)
        except Exception:
            pass

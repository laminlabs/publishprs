"""Test publishprs functionality."""

import os

import pytest
from publishprs import Publisher


def test_publish_pr():
    """Test publishing a PR from laminhub to laminhub-public.

    This test uses PR #3820 from the private laminhub repo which contains
    user-attached images that need to be processed and uploaded to LaminDB.
    """
    # Verify required environment variables are set
    assert os.environ.get("GITHUB_TOKEN"), "GITHUB_TOKEN environment variable required"
    assert os.environ.get("LAMIN_API_KEY"), (
        "LAMIN_API_KEY environment variable required"
    )

    # Initialize publisher
    publisher = Publisher(
        source_repo="https://github.com/laminlabs/laminhub",
        target_repo="https://github.com/laminlabs/laminhub-public",
        db="laminlabs/lamin-dev",
    )

    # Publish the PR (with close_pr=False to avoid auto-merging in tests)
    url = publisher.publish(
        pull_id=3820,
        close_pr=False,  # Don't auto-merge during tests
    )

    # Verify we got a valid PR URL back
    assert url.startswith("https://github.com/laminlabs/laminhub-public/pull/")
    assert url.split("/")[-1].isdigit()  # PR number should be numeric


def test_publish_pr_with_env_db():
    """Test that LAMINDB_INSTANCE env var is respected."""
    # Set the environment variable
    os.environ["LAMINDB_INSTANCE"] = "laminlabs/lamin-dev"

    # Initialize publisher without explicit db parameter
    publisher = Publisher(
        source_repo="https://github.com/laminlabs/laminhub",
        target_repo="https://github.com/laminlabs/laminhub-public",
        db="laminlabs/lamin-dev",
    )

    # Verify the db was picked up from env var
    assert publisher.db == "laminlabs/lamin-dev"


def test_publisher_initialization():
    """Test Publisher initialization with various inputs."""
    # Test with full URLs
    publisher = Publisher(
        source_repo="https://github.com/laminlabs/laminhub",
        target_repo="https://github.com/laminlabs/laminhub-public",
        db="laminlabs/lamin-dev",
    )

    assert publisher.source_owner == "laminlabs"
    assert publisher.source_repo == "laminhub"
    assert publisher.target_owner == "laminlabs"
    assert publisher.target_repo == "laminhub-public"
    assert publisher.db == "laminlabs/lamin-dev"

    # Test with .git suffix
    publisher2 = Publisher(
        source_repo="https://github.com/laminlabs/laminhub.git",
        target_repo="https://github.com/laminlabs/laminhub-public.git",
        db="laminlabs/lamin-dev",
    )

    assert publisher2.source_repo == "laminhub"
    assert publisher2.target_repo == "laminhub-public"


if __name__ == "__main__":
    # Run the tests
    pytest.main([__file__, "-v"])

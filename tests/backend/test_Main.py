import pytest
from unittest.mock import Mock, patch
from fastapi import FastAPI
from fastapi.testclient import TestClient
from starlette.middleware.cors import CORSMiddleware

# Create mock objects
mock_scheduler = Mock()
mock_scheduler.start = Mock()
mock_scheduler.stop = Mock()

# Setup patches before importing main
patches = [
    patch('backend.config.Database.init_db'),
    patch('backend.models.BaseModel.create_database'),
    patch('backend.services.dependencies.get_scheduler_service', return_value=mock_scheduler)
]


@pytest.fixture(autouse=True)
def apply_patches():
    """Apply all patches"""
    for p in patches:
        p.start()
    yield
    for p in patches:
        p.stop()


@pytest.fixture
def test_app():
    """Create test app with dependencies mocked"""
    from backend.main import app
    return app


@pytest.fixture
def client(test_app):
    """Create test client"""
    return TestClient(test_app)


def test_app_configuration(test_app):
    """Test app configuration"""
    assert test_app.title == "ComeBeck Backend API"
    assert test_app.description == "This is the backend for ComeBeck and it is built using FastAPI"
    assert test_app.version == "1.0.0"
    assert test_app.docs_url == "/api/documentation"


app = FastAPI(
    title="ComeBeck Backend API",
    description="This is the backend for ComeBeck and it is built using FastAPI",
    version="1.0.0",
    docs_url="/api/documentation"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


# test_Main.py
def test_cors_middleware(client):
    """Test CORS middleware configuration"""
    headers = {
        "origin": "*",
        "access-control-request-method": "GET",
        "access-control-request-headers": "content-type",
    }
    response = client.options("/api/documentation", headers=headers)

    # Test CORS headers
    assert response.headers["access-control-allow-origin"] == "*"
    assert response.headers["access-control-allow-credentials"] == "true"
    assert "access-control-allow-methods" in response.headers
    assert "access-control-allow-headers" in response.headers

    # Additional assertions for other CORS headers
    assert "GET" in response.headers["access-control-allow-methods"]
    assert "content-type" in response.headers["access-control-allow-headers"].lower()


def test_router_registration(test_app):
    """Test router registration"""
    routes = [route.path for route in test_app.routes]

    # Check for API documentation route
    assert "/api/documentation" in routes

    # Check that we have other routes (exact paths not important for unit test)
    assert len(routes) > 1


def test_lifespan():
    """Test lifespan functionality"""
    from backend.main import lifespan

    app = FastAPI()

    # Manually call the lifespan context manager
    async_cm = lifespan(app)

    # Simulate startup
    import asyncio
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # Run startup
    loop.run_until_complete(async_cm.__aenter__())

    # Verify scheduler started
    mock_scheduler.start.assert_called_once()

    # Run shutdown
    loop.run_until_complete(async_cm.__aexit__(None, None, None))

    # Verify scheduler stopped
    mock_scheduler.stop.assert_called_once()

    loop.close()


def test_middleware_setup(test_app):
    """Test middleware setup"""
    middlewares = [m.cls.__name__ for m in test_app.user_middleware]
    assert "CORSMiddleware" in middlewares


def test_documentation_endpoint(client):
    """Test documentation endpoint is accessible"""
    response = client.get("/api/documentation")
    assert response.status_code in (200, 301, 302)  # Accept redirect or direct success


def test_cors_preflight(client):
    """Test CORS preflight requests"""
    headers = {
        "origin": "*",
        "access-control-request-method": "POST",
        "access-control-request-headers": "content-type",
    }
    response = client.options("/api/documentation", headers=headers)
    assert "access-control-allow-methods" in response.headers
    assert "access-control-allow-headers" in response.headers


def test_error_handling(client):
    """Test 404 handling"""
    response = client.get("/nonexistent")
    assert response.status_code == 404
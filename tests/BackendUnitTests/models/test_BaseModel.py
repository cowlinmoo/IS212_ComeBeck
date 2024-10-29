import pytest
from unittest.mock import patch, MagicMock, call
from sqlalchemy import MetaData
from backend.models.BaseModel import create_database, EntityMeta, Engine

@pytest.fixture
def mock_engine():
    return MagicMock()

@pytest.fixture
def mock_metadata():
    metadata = MagicMock(spec=MetaData)
    metadata.tables = {'table1': MagicMock(), 'table2': MagicMock()}
    return metadata

def test_create_database(mock_engine, mock_metadata):
    with patch('BackendUnitTests.models.BaseModel.Engine', mock_engine), \
         patch.object(EntityMeta, 'metadata', mock_metadata), \
         patch('builtins.print') as mock_print:
        create_database()

    mock_print.assert_has_calls([
        call("Initializing database..."),
        call({'table1': mock_metadata.tables['table1'], 'table2': mock_metadata.tables['table2']}),
        call("Database initialization complete.")
    ])

    mock_metadata.create_all.assert_called_once_with(bind=mock_engine)

def test_create_database_empty_tables(mock_engine, mock_metadata, capsys):
    mock_metadata.tables = {}
    with patch('BackendUnitTests.models.BaseModel.Engine', mock_engine), \
         patch.object(EntityMeta, 'metadata', mock_metadata):
        create_database()

    captured = capsys.readouterr()
    assert "Initializing database..." in captured.out
    assert "{}" in captured.out
    assert "Database initialization complete." in captured.out

    mock_metadata.create_all.assert_called_once_with(bind=mock_engine)

def test_create_database_exception(mock_engine, mock_metadata):
    mock_metadata.create_all.side_effect = Exception("Database creation failed")
    with patch('BackendUnitTests.models.BaseModel.Engine', mock_engine), \
         patch.object(EntityMeta, 'metadata', mock_metadata), \
         pytest.raises(Exception) as exc_info:
        create_database()

    assert str(exc_info.value) == "Database creation failed"
    mock_metadata.create_all.assert_called_once_with(bind=mock_engine)

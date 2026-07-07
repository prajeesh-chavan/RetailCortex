from pyspark.sql.types import StructType
from conftest import ENTITY_NAMES, SCHEMA_DIR
import importlib.util
import pytest


def _import_schema_module(entity: str):
    path = SCHEMA_DIR / f"{entity}_schema.py"
    spec = importlib.util.spec_from_file_location(entity, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.mark.parametrize("entity", ENTITY_NAMES)
def test_schema_module_has_source_schema(entity):
    mod = _import_schema_module(entity)
    name = f"{entity.upper()}_SCHEMA"
    assert hasattr(mod, name), f"{entity}: missing {name}"
    assert isinstance(getattr(mod, name), StructType)


@pytest.mark.parametrize("entity", ENTITY_NAMES)
def test_schema_module_has_bronze_schema(entity):
    mod = _import_schema_module(entity)
    name = f"{entity.upper()}_BRONZE_SCHEMA"
    assert hasattr(mod, name), f"{entity}: missing {name}"
    assert isinstance(getattr(mod, name), StructType)


KAFKA_METADATA_FIELDS = [
    "kafka_key", "kafka_topic", "kafka_partition",
    "kafka_offset", "ingestion_timestamp", "ingestion_date",
]


@pytest.mark.parametrize("entity", ENTITY_NAMES)
def test_bronze_schema_has_kafka_metadata(entity):
    mod = _import_schema_module(entity)
    bronze = getattr(mod, f"{entity.upper()}_BRONZE_SCHEMA")
    field_names = {f.name for f in bronze.fields}
    for field in KAFKA_METADATA_FIELDS:
        assert field in field_names, f"{entity}: bronze schema missing '{field}'"


@pytest.mark.parametrize("entity", ENTITY_NAMES)
def test_bronze_schema_extends_source_schema(entity):
    mod = _import_schema_module(entity)
    source = getattr(mod, f"{entity.upper()}_SCHEMA")
    bronze = getattr(mod, f"{entity.upper()}_BRONZE_SCHEMA")
    source_names = {f.name for f in source.fields}
    bronze_names = {f.name for f in bronze.fields}
    assert source_names.issubset(bronze_names), (
        f"{entity}: bronze fields missing source fields: "
        f"{source_names - bronze_names}"
    )


@pytest.mark.parametrize("entity", ENTITY_NAMES)
def test_schema_has_entity_id_field(entity):
    mod = _import_schema_module(entity)
    source = getattr(mod, f"{entity.upper()}_SCHEMA")
    id_fields = [f.name for f in source.fields if f.name.endswith("_id")]
    assert id_fields, f"{entity}: no field ending with '_id' found"
    expected = f"{entity}_id"
    if expected not in id_fields:
        actual = id_fields[0]
        pytest.skip(
            f"{entity}: pk is '{actual}' not '{expected}' "
            f"(source convention differs from entity name)"
        )

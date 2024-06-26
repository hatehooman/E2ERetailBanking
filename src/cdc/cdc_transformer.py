import avro.schema
import io
from avro.io import DatumReader, BinaryDecoder

class CDCTransformer:
    def __init__(self, schema_paths):
        self.schemas = {table: avro.schema.parse(open(path, "rb").read()) for table, path in schema_paths.items()}
        self.readers = {table: DatumReader(schema) for table, schema in self.schemas.items()}

    def decode(self, table, msg_value):
        message_bytes = io.BytesIO(msg_value)
        message_bytes.seek(7)
        decoder = BinaryDecoder(message_bytes)
        event_dict = self.readers[table].read(decoder)
        return event_dict

    def transform_changes(self, changes):
        for msg in changes:
            table = msg.key.decode('utf-8')  # Assuming table name is in the message key
            yield table, self.decode(table, msg.value)
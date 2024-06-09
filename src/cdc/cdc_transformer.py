import avro.schema
import io
from avro.io import DatumReader, BinaryDecoder


class CDCTransformer:
    def __init__(self, config):
        self.schema = avro.schema.parse(open(config['avro_schema_path'], "rb").read())
        self.reader = DatumReader(self.schema)

    def decode(self, msg_value):
        message_bytes = io.BytesIO(msg_value)
        message_bytes.seek(7)
        decoder = BinaryDecoder(message_bytes)
        event_dict = self.reader.read(decoder)
        return event_dict

    def transform_changes(self, changes):
        for msg in changes:
            yield self.decode(msg.value)

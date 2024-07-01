import avro.schema
import io
from avro.io import DatumReader, BinaryDecoder
import logging
import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CDCTransformer:
    def __init__(self, config):
        self.schema = avro.schema.parse(open(config['avro_schema_path'], 'rb').read())
        self.reader = DatumReader(self.schema)

    def decode(self, msg_value):
        message_bytes = io.BytesIO(msg_value)
        message_bytes.seek(7)  # Skip the magic byte and schema ID
        decoder = BinaryDecoder(message_bytes)
        try:
            event_dict = self.reader.read(decoder)
            return event_dict
        except Exception as e:
            logger.error(f"Error decoding message: {e}")
            logger.error(f"Message value: {msg_value}")
            return None

    def format_date(self, date_obj):
        try:
            return datetime.datetime.strptime(date_obj, "%Y-%m-%d").date().isoformat()
        except (ValueError, TypeError):
            return None

    def format_datetime(self, datetime_obj):
        try:
            return datetime.datetime.strptime(datetime_obj, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%dT%H:%M:%S")
        except (ValueError, TypeError):
            return None

    def handle_date_field(self, decoded_message, date_field):
        if date_field in decoded_message and decoded_message[date_field]:
            if date_field == 'fulldatewithtime':
                formatted_datetime = self.format_datetime(decoded_message[date_field])
                if formatted_datetime:
                    decoded_message['fulldatewithtime'] = formatted_datetime
                else:
                    logger.error(f"Invalid datetime found: {decoded_message[date_field]}")
            else:
                parsed_date = self.format_date(decoded_message[date_field])
                if parsed_date:
                    year, month, day = map(int, parsed_date.split('-'))
                    decoded_message['year'] = year
                    decoded_message['month'] = month
                    decoded_message['day'] = day
                    decoded_message[date_field] = parsed_date
                else:
                    logger.error(f"Invalid date found: {decoded_message[date_field]}")

    def transform_changes(self, changes):
        date_fields = ['parseddate', 'Date_recieved', 'Date', 'fulldate', 'fulldatewithtime']
        for msg in changes:
            decoded_message = self.decode(msg.value)
            if decoded_message:
                for date_field in date_fields:
                    self.handle_date_field(decoded_message, date_field)
                yield decoded_message

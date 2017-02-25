import datetime
from geopy.geocoders import Nominatim
from dateutil.parser import parse

# validators
def validate_date(ctx, param, value):
    try:
        value = parse(value)
        return value
    except (AttributeError, TypeError) as e:
        return value
    except ValueError:
        raise click.BadParameter('Date format \"%s\" not valid' % value)

def validate_location(ctx, param, value):

        if value is None:
            return value

        geolocator = Nominatim()
        location = geolocator.geocode(value)

        if location is None:
            raise click.BadParameter('Location \"%s\" could not be found' % value)

        return location

def validate(document):

    fields = [
        "title",
        "encrypted",
        "content",
        "created",
        "updated",
        "tags",
        "categories"
    ]

    # Check if we have an document
    if not isinstance(document, dict):
        return False

    # Verifiy if all fields are existent
    try:
        for field in fields:
            document[field]
    except KeyError:
        return False

    # Check if content is utf8
    if not isinstance(document["content"], str):
        if not isinstance(document["content"], unicode):
            return False

    # # Check title utf8
    if not isinstance(document["title"], str):
        if not isinstance(document["title"], unicode):
            return False

    # Check if tags is a list
    if not isinstance(document["tags"], list):
        return False

    # Check if categories is a list
    if not isinstance(document["categories"], list):
        return False

    # Check if create is a valid datetime object
    if not isinstance(document["created"], datetime.datetime):
        return False

    # Check if updated is a valid datetime object
    if not isinstance(document["updated"], datetime.datetime):
        return False

    if not isinstance(document["encrypted"], bool):
        return False

    return True

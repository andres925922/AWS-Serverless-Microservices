import enum

class HttpCodes(enum.IntEnum):
    """
    Enum for HTTP status codes.
    """
    OK = 200
    CREATED = 201
    ACCEPTED = 202
    NO_CONTENT = 204
    MOVED_PERMANENTLY = 301
    FOUND = 302
    NOT_MODIFIED = 304
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    NOT_ALLOWED = 405
    GONE = 410
    CONFLICT = 409
    UNPROCESSABLE_ENTITY = 422
    INTERNAL_SERVER_ERROR = 500
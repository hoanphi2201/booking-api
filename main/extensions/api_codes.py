from enum import Enum


class APICode(str, Enum):
    """
    API codes and descriptions

    Basic format `SA{xxx}{D|E|S}`:
        - Prefixes:
            - `SA` stands for `Seller API`
        - Suffixes:
            - `D`: Default suffix
            - `E`: Error cases
            - `S`: Success cases
    """

    def __new__(cls, value, description):
        obj = str.__new__(cls, value)
        obj._value_ = value

        obj.description = description
        return obj

    DEFAULT = ('SA001D', 'API has no specific code for this case')

    # Success codes
    GET_SUCCESS = ("SA001S", 'Success')
    CREATE_SUCCESS = ("SA002S", 'Created successfully!')
    DELETE_SUCCESS = ("SA003S", 'Deleted successfully!')
    UPDATE_SUCCESS = ("SA004S", 'Updated successfully!')

    # Errors codes
    UNHANDLED_ERROR = ("SA001E", "This error has not been handled")

    SELLER_NOT_FOUND = ("SA002E", "The requested seller can not be found")

    EXTERNAL_API_TIMEOUT = ("SA003E", "Got timeout when calling external API")

    PHYSICAL_VALIDATOR_ERROR = ("SA004E", "The requested params did not pass physical validation")

    LOGICAL_VALIDATOR_ERROR = ("SA005E", "The requested params did not pass logical validation")

    EXTERNAL_API_ERROR = ("SA006E", "Got errors when calling external API")

    EXTERNAL_PARAM_NOT_EXIST = (
        "SA007E", "The request params got error not exist or not valid when calling external API")

    TERMINAL_NOT_FOUND = ("SA008E", "The requested terminal can not be found")

    SELLER_TERMINAL_NOT_FOUND = ("SA009E", "The requested terminal mapped with seller can not be found")

    TERMINAL_WAREHOUSE_NOT_FOUND = ("SA010E", "The requested terminal mapped with warehouse can not be found")

    HOTEL_BOOKING_NOT_FOUND = ("SA011E", "The requested hotel booking can not be found")

    TERMINAL_ALREADY_ACTIVE = ("SA031E", "The requested terminal has already active")
    
    TERMINAL_ALREADY_INACTIVE = ("SA032E", "The requested terminal has already inactive")

    TERMINAL_WAREHOUSE_ALREADY_ACTIVATED_ERROR = (
        "SA011E", "The requested terminal mapped warehouse has been activated before")

    TERMINAL_WAREHOUSE_ALREADY_DEACTIVATED_ERROR = (
        "SA012E", "The requested terminal mapped with warehouse has been deactivated before")

    SELLER_ALREADY_ACTIVE = ("SA013E", "The requested seller has already active")

    WAREHOUSE_NOT_FOUND = ("SA014E", "The requested warehouse can be not found")

    SELLER_ALREADY_INACTIVE = ("SA015E", "The requested seller has already inactive")

    TERMINAL_TYPE_ERROR = (
        "SA016E", "The requested terminal invalid type"
    )

    TERMINAL_ALREADY_MAPPED_ERROR = ("SA017E", "The requested terminal has been mapped")

    WAREHOUSE_ALREADY_MAPPED_ERROR = ("SA018E", "The requested warehouse mapped has been mapped with other showroom")

    TERMINAL_WAREHOUSE_SELLER_ID_ERROR = ("SA019E", "The requested terminal warehouse mapping invalid seller id")

    # TerminalGroup
    TERMINAL_GROUP_NOT_FOUND = ("SA041E", "The requested terminal-group can not be found")

    TERMINAL_GROUP_TYPE_NOT_FOUND = ("SA041E", "The requested terminal-group can not be found")

    TERMINAL_GROUP_ALREADY_ACTIVE = ("SA042E", "The requested terminal-group has already active")

    TERMINAL_GROUP_ALREADY_INACTIVE = ("SA043E", "The requested terminal-group has already inactive")
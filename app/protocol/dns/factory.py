from .schema import DNS_PROTOCOL_SCHEMA


def create_dns_protocol():
    """
    Create an empty DNS protocol object.
    """

    return {
        field: None
        for field in DNS_PROTOCOL_SCHEMA
    }
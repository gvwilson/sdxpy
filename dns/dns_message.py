from dataclasses import dataclass
from enum import Enum


# mccole:recordtype
class RecordType(Enum):
    """DNS record types."""

    A = "A"  # IPv4 address
    AAAA = "AAAA"  # IPv6 address
    CNAME = "CNAME"  # Canonical name (alias)
    NS = "NS"  # Name server
    MX = "MX"  # Mail exchange
# mccole:/recordtype


# mccole:dnsrecord
@dataclass
class DNSRecord:
    """A DNS resource record."""

    name: str  # Domain name
    value: str  # IP address, domain name, etc.
    record_type: RecordType
    ttl: int = 3600  # Time to live in seconds
# mccole:/dnsrecord


# mccole:dnsquery
@dataclass
class DNSQuery:
    """A DNS query message."""

    query_id: int
    domain: str
    record_type: RecordType
# mccole:/dnsquery


# mccole:dnsresponse
@dataclass
class DNSResponse:
    """A DNS response message."""

    query_id: int
    domain: str
    record_type: RecordType
    records: list[DNSRecord]
    authoritative: bool = False
    from_cache: bool = False
# mccole:/dnsresponse

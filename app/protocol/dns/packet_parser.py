
# ==========================================================
# RIPE Atlas stores DNS packets as Base64 strings.
#
# Decode the Base64 string back into the original
# binary DNS packet.

# =============================================================================
# DNS Packet Example (RIPE Atlas)
#
# Original Base64 Packet (abuf)
#
# ciKBgAABAAEAAAABB3lvdXR1YmUDY29tAAABAAHADAABAAEAAADLAASs2RCOAAApEAAAAAAAAAA=
#
# After Base64 Decoding
#
# 72 22 81 80 00 01 00 01 00 00 00 01
# 07 79 6f 75 74 75 62 65
# 03 63 6f 6d
# 00
# 00 01
# 00 01
# c0 0c
# 00 01
# 00 01
# 00 00 00 cb
# 00 04
# ac d9 10 8e
# 00 00
# 29
# 10 00
# 00 00
# 00 00
# 00 00
#
#
# =============================================================================
# Packet Mapping
# =============================================================================
#
# Raw Bytes                 DNS Field                  Meaning
# -----------------------------------------------------------------------------
#
# 72 22                     Transaction ID             29218
#
#                                                    Unique identifier assigned
#                                                    by the client.
#                                                    The DNS response must
#                                                    contain the same ID.
#
# -----------------------------------------------------------------------------
#
# 81 80                     Flags                      QR RD RA
#
#                                                    QR = Query Response
#                                                         This packet is a DNS
#                                                         response.
#
#                                                    RD = Recursion Desired
#                                                         Client requests the
#                                                         resolver to perform
#                                                         recursive lookup.
#
#                                                    RA = Recursion Available
#                                                         Resolver supports
#                                                         recursive DNS service.
#
# -----------------------------------------------------------------------------
#
# 00 01                     Question Count            1
#
#                                                    One DNS question exists.
#
# -----------------------------------------------------------------------------
#
# 00 01                     Answer Count              1
#
#                                                    One answer record returned.
#
# -----------------------------------------------------------------------------
#
# 00 00                     Authority Count           0
#
#                                                    No authority records.
#
# -----------------------------------------------------------------------------
#
# 00 01                     Additional Count          1
#
#                                                    One EDNS OPT record.
#
# -----------------------------------------------------------------------------
#
# 07                         Label Length             7
#
#                                                    Next label contains
#                                                    7 characters.
#
# -----------------------------------------------------------------------------
#
# 79 6f 75 74 75 62 65      Domain Label              "youtube"
#
# -----------------------------------------------------------------------------
#
# 03                         Label Length             3
#
#                                                    Next label contains
#                                                    3 characters.
#
# -----------------------------------------------------------------------------
#
# 63 6f 6d                  Domain Label              "com"
#
# -----------------------------------------------------------------------------
#
# 00                         End of Name
#
#                                                    End of domain name.
#
# -----------------------------------------------------------------------------
#
# 00 01                     QTYPE                     A
#
#                                                    IPv4 Address Record.
#
# -----------------------------------------------------------------------------
#
# 00 01                     QCLASS                    IN
#
#                                                    Internet Class.
#
# -----------------------------------------------------------------------------
#
# c0 0c                     Name Pointer
#
#                                                    DNS Name Compression.
#
#                                                    Pointer to the domain
#                                                    name "youtube.com"
#                                                    stored in the Question
#                                                    section.
#
# -----------------------------------------------------------------------------
#
# 00 01                     TYPE                      A
#
#                                                    IPv4 Address Record.
#
# -----------------------------------------------------------------------------
#
# 00 01                     CLASS                     IN
#
#                                                    Internet Class.
#
# -----------------------------------------------------------------------------
#
# 00 00 00 cb               TTL                       203 seconds
#
#                                                    Resolver may cache this
#                                                    answer for 203 seconds.
#
# -----------------------------------------------------------------------------
#
# 00 04                     RDLENGTH                  4 bytes
#
#                                                    IPv4 address length.
#
# -----------------------------------------------------------------------------
#
# ac d9 10 8e               RDATA                     172.217.16.142
#
#                                                    Returned IPv4 address.
#
# -----------------------------------------------------------------------------
#
# 00 00                     OPT Name                 Root Label
#
# -----------------------------------------------------------------------------
#
# 29                         TYPE                     OPT (EDNS)
#
#                                                    Extension Mechanism
#                                                    for DNS (RFC 6891).
#
# -----------------------------------------------------------------------------
#
# 10 00                     UDP Payload Size          4096 bytes
#
#                                                    Maximum UDP payload
#                                                    supported by the client.
#
# -----------------------------------------------------------------------------
#
# 00 00                     Extended RCODE
#                            EDNS Version
#
#                                                    Extended RCODE = 0
#                                                    EDNS Version = 0
#
# -----------------------------------------------------------------------------
#
# 00 00                     Z Flags
#
#                                                    Reserved.
#
# -----------------------------------------------------------------------------
#
# 00 00                     Option Length
#
#                                                    No EDNS options.
#
# =============================================================================
# ==========================================================

# =============================================================================
# dnspython Message Object
#
# message = dns.message.from_wire(packet)
#
# After parsing the raw DNS packet, dnspython creates a
# Message object with the following structure:
#
# message
# ├── id                = 29218
# ├── flags             = QR RD RA
# ├── opcode            = QUERY
# ├── rcode()           = NOERROR
# │
# ├── question
# │      └── [0]
# │             ├── name      = youtube.com.
# │             ├── rdtype    = A
# │             └── rdclass   = IN
# │
# ├── answer
# │      └── [0]
# │             ├── name      = youtube.com.
# │             ├── ttl       = 203
# │             ├── rdtype    = A
# │             ├── rdclass   = IN
# │             └── address   = 172.217.16.142
# │
# ├── authority
# │      └── []
# │
# └── additional
#        └── [0]
#               ├── type       = OPT
#               ├── edns       = 0
#               └── payload    = 4096
#
# =============================================================================        
# app/protocol/dns/packet_parser.py

from typing import Dict, List, Optional
import base64

import dns.message
import dns.rcode
import dns.rdatatype


def parse_dns_abuf(abuf: Optional[str]) -> Dict:
    """
    Decode RIPE Atlas DNS abuf into DNS protocol fields.
    """

    parsed = {
        "query_name": None,
        "query_type": None,
        "rcode": None,
        "ttl": None,
        "answer_count": 0,
        "answers": [],
    }

    if not abuf:
        return parsed

    try:
        packet = base64.b64decode(abuf)
        message = dns.message.from_wire(packet)

        parsed["rcode"] = dns.rcode.to_text(message.rcode())

        if message.question:
            question = message.question[0]

            parsed["query_name"] = str(question.name).rstrip(".")
            parsed["query_type"] = dns.rdatatype.to_text(question.rdtype)

        answers: List[str] = []
        ttl_values: List[int] = []

        for rrset in message.answer:
            ttl_values.append(rrset.ttl)

            for item in rrset:
                if rrset.rdtype in (
                    dns.rdatatype.A,
                    dns.rdatatype.AAAA,
                ):
                    answers.append(item.address)

        parsed["answers"] = answers
        parsed["answer_count"] = len(answers)

        if ttl_values:
            parsed["ttl"] = ttl_values[0]

    except Exception:
        return parsed

    return parsed
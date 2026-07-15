# DNS RFC1035 Decoding Walkthrough

**Project**

DNS Measurement Platform

**Document**

RFC1035 DNS Protocol Decoding Specification

**Version**

1.0

---

# 1. Overview

This document explains how a raw DNS response packet collected by RIPE Atlas is decoded according to **RFC 1035** and transformed into the **Canonical DNS Protocol** used by the DNS Measurement Platform.

Unlike an API reference, this document focuses on the engineering process of protocol decoding.

The decoding process consists of several stages:

```
RIPE Atlas Measurement

        │

        ▼

Base64 DNS Packet (abuf)

        │

        ▼

RFC1035 Wire Format

        │

        ▼

dnspython Message Object

        │

        ▼

Canonical DNS Protocol

        │

        ▼

Canonical Observation

        │

        ▼

Telemetry Builder
```

Each stage has a single responsibility.

The DNS Packet Parser is responsible only for translating a DNS wire-format packet into structured protocol fields.

It is intentionally independent from:

- Observation
- Measurement
- Probe
- SQLite
- Telemetry
- Grafana

---

# 2. Original RIPE Atlas Example

The following example is a real DNS response collected from RIPE Atlas.

```json
{
    "abuf": "V4mFAAABAAQAAAABATIEcG9vbANudHADb3JnAAAcAAEBMgRwb29sA250cANvcmcAABwAAQAAAIIAECoSvsQdoAA+AAAAAAAAASMBMgRwb29sA250cANvcmcAABwAAQAAAIIAECoAEogBEPYAAAAAAAAAEAABMgRwb29sA250cANvcmcAABwAAQAAAIIAECYGRwAA8QAAAAAAAAAAAAEBMgRwb29sA250cANvcmcAABwAAQAAAIIAECABQdAQBCOYAMMAAAAAASMAACkCAAAAAAAAEgADAA4yMTcuMjE3LjI0My43OA==",

    "ID":22409,

    "QDCOUNT":1,

    "ANCOUNT":4,

    "NSCOUNT":0,

    "ARCOUNT":1
}
```

RIPE Atlas stores the original DNS response packet in the field:

```
abuf
```

The packet is **Base64 encoded**.

It is **not** directly readable by humans.

The first responsibility of the DNS Packet Parser is to decode this Base64 string back into the original DNS wire-format packet defined by RFC1035.

---

# 3. From Base64 to DNS Packet

The decoding process begins with:

```python
packet = base64.b64decode(abuf)
```

This converts the Base64 string into the original binary DNS packet.

The binary packet is then parsed using dnspython:

```python
message = dns.message.from_wire(packet)
```

After this step, the packet is represented as a structured DNS Message object.

```
Base64

↓

Binary DNS Packet

↓

dnspython Message
```

At this point, the parser no longer works with raw bytes.

Instead, it works with DNS protocol objects.

---

# 4. RFC1035 Header Mapping

According to RFC1035 Section 4.1.1, every DNS packet begins with a fixed-length 12-byte Header.

```
                     1  1  1  1  1  1
      0  1  2  3  4  5  6  7  8  9  0  1  2  3  4  5

+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

|                      ID                       |

+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

|QR|Opcode|AA|TC|RD|RA|   Z    |     RCODE      |

+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

|                    QDCOUNT                    |

+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

|                    ANCOUNT                    |

+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

|                    NSCOUNT                    |

+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

|                    ARCOUNT                    |

+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
```

The current RIPE Atlas example produces the following values.

| RFC1035 Field | RIPE Atlas | dnspython | Canonical DNS Protocol |
|---------------|-----------|-----------|------------------------|
| ID | 22409 | message.id | transaction_id |
| QDCOUNT | 1 | len(message.question) | Question Count |
| ANCOUNT | 4 | len(message.answer) | answer_count |
| NSCOUNT | 0 | len(message.authority) | authority_count |
| ARCOUNT | 1 | len(message.additional) | additional_count |
| OPCODE | QUERY | message.opcode() | opcode |
| RCODE | NOERROR | message.rcode() | rcode |

The Header provides protocol-level information describing the overall DNS transaction.

These fields are later mapped into the Canonical DNS Protocol object.

# 5. RFC1035 Question Section

After the 12-byte DNS Header, the packet enters the **Question Section** defined by RFC1035 Section 4.1.2.

The Question Section describes **what the client is asking**.

Unlike the Header, which describes the transaction itself, the Question identifies the requested resource.

The Question consists of three fields:

```
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
|                                               |
/                     QNAME                     /
/                                               /
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
|                     QTYPE                     |
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
|                     QCLASS                    |
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
```

---

# 5.1 QNAME

QNAME is **not stored as a normal string**.

Instead, RFC1035 stores the domain name as a sequence of labels.

Each label begins with a length byte.

The RIPE Atlas packet used in this document contains the following Question.

```
01

32

04

70 6f 6f 6c

03

6e 74 70

03

6f 72 67

00
```

This can be interpreted step by step.

| Raw Bytes | Meaning |
|-----------|---------|
| 01 | next label length = 1 |
| 32 | "2" |
| 04 | next label length = 4 |
| 70 6f 6f 6c | "pool" |
| 03 | next label length = 3 |
| 6e 74 70 | "ntp" |
| 03 | next label length = 3 |
| 6f 72 67 | "org" |
| 00 | end of domain name |

After decoding, the complete domain name becomes

```
2.pool.ntp.org
```

dnspython automatically performs this decoding.

```
question.name

↓

2.pool.ntp.org.
```

The parser removes the trailing dot.

```
2.pool.ntp.org.
        ↓
2.pool.ntp.org
```

The Canonical DNS Protocol stores

```json
{
    "query_name": "2.pool.ntp.org"
}
```

---

# Why Keep query_name?

The queried domain represents the business target of the DNS transaction.

Without this field, the platform cannot distinguish which service is being measured.

Future telemetry examples include:

- Top Queried Domains
- DNS Latency by Domain
- Success Rate by Domain
- CDN Behaviour Analysis
- Service Availability

---

# 5.2 QTYPE

Immediately following QNAME are two bytes representing QTYPE.

The current packet contains

```
00 1c
```

According to the IANA DNS Parameters registry,

```
0x001C

↓

AAAA
```

dnspython converts this value automatically.

```
question.rdtype

↓

AAAA
```

The parser converts the numeric type into its textual representation.

```python
dns.rdatatype.to_text(
    question.rdtype,
)

↓

AAAA
```

The Canonical DNS Protocol stores

```json
{
    "query_type": "AAAA"
}
```

---

# Why Keep query_type?

Different DNS record types represent different network services.

Examples

| Type | Meaning |
|------|----------|
| A | IPv4 Address |
| AAAA | IPv6 Address |
| MX | Mail Exchange |
| NS | Name Server |
| TXT | Text Record |
| CNAME | Canonical Name |

Future telemetry can generate

- Query Type Distribution
- IPv4 vs IPv6 Adoption
- Service Type Analysis
- Record Type Statistics

---

# 5.3 QCLASS

The final two bytes of the Question Section represent QCLASS.

The current packet contains

```
00 01
```

RFC1035 defines

```
0x0001

↓

IN

↓

Internet Class
```

dnspython converts this automatically.

```
question.rdclass

↓

IN
```

The parser stores

```json
{
    "query_class": "IN"
}
```

---

# Why Keep query_class?

Although almost every Internet DNS query uses the IN class, it remains part of the DNS protocol defined by RFC1035.

Keeping this field preserves protocol completeness and allows future support for non-IN classes if required.

---

# Question Section Mapping

The complete mapping for the current RIPE Atlas packet is shown below.

| RFC1035 | Raw Packet | dnspython | Canonical DNS Protocol |
|----------|------------|-----------|------------------------|
| QNAME | 01 32 04 70 6f 6f 6c 03 6e 74 70 03 6f 72 67 00 | question.name | query_name |
| QTYPE | 00 1c | question.rdtype | query_type |
| QCLASS | 00 01 | question.rdclass | query_class |

The Question Section has now been completely transformed from a binary DNS packet into the Canonical DNS Protocol representation.

# 6. RFC1035 Answer Section

The Answer Section contains the actual DNS Resource Records
returned by the resolver.

Unlike the Question Section, which describes the client's
request, the Answer Section contains the information
required to resolve the requested domain.

According to RFC1035, each Resource Record (RR) has the
following format.

```
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
|                     NAME                      |
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
|                     TYPE                      |
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
|                     CLASS                     |
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
|                      TTL                      |
|                                               |
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
|                   RDLENGTH                    |
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
|                                               |
/                     RDATA                     /
/                                               /
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
```

The current RIPE Atlas response contains four Answer
Resource Records.

---

# 6.1 Answer Count

The RIPE Atlas result contains

```json
{
    "ANCOUNT": 4
}
```

This indicates that the DNS response contains four
Resource Records in the Answer Section.

dnspython stores these records as

```python
message.answer
```

The parser converts them into

```json
{
    "answer_count": 4
}
```

---

## Why Keep answer_count?

The number of returned records provides useful operational
information.

Examples include:

- Single-server responses
- Load-balanced services
- CDN deployments
- Geo-distributed services

Future Telemetry may generate

- Average Answer Count
- Multi-answer Response Ratio
- Resolver Consistency

---

# 6.2 Resource Records

Each Answer RR contains one IPv6 address.

The parser converts every Resource Record into a canonical
record object.

Decoded Result

| RR | TYPE | Address |
|----|------|-------------------------------------------|
| 1 | AAAA | 2a12:bec4:1da0:003e:: |
| 2 | AAAA | 2a10:0288:0110:f600:: |
| 3 | AAAA | 2606:4700:00f1:: |
| 4 | AAAA | 2601:41d0:0423:9800:c300::0123 |

The parser stores

```json
{
    "answers": [

        {
            "type":"AAAA",
            "address":"2a12:bec4:1da0:003e::"
        },

        {
            "type":"AAAA",
            "address":"2a10:0288:0110:f600::"
        },

        {
            "type":"AAAA",
            "address":"2606:4700:00f1::"
        },

        {
            "type":"AAAA",
            "address":"2601:41d0:0423:9800:c300::0123"
        }

    ]
}
```

---

## Why Keep answers?

The Answer records represent the final DNS resolution
result.

They are the most valuable protocol-level data extracted
from the packet.

Future applications include

- Resolver Validation
- CDN Analysis
- Geo-distributed Resolution
- IPv6 Deployment Analysis
- Address Change Detection

Unlike raw packets, these values can be directly consumed
by higher platform layers.

---

# 6.3 TTL

Each Resource Record contains a Time To Live (TTL).

RFC1035 defines TTL as the maximum amount of time that the
record may be cached.

Example

```
TTL

↓

130 seconds
```

The parser currently stores

```json
{
    "ttl":130
}
```

When multiple Resource Records are returned, the parser
retains the minimum TTL.

This guarantees that cache lifetime never exceeds the
earliest expiration among all returned records.

---

## Why Keep TTL?

TTL is one of the most useful operational fields in DNS.

It reflects caching behaviour rather than network latency.

Future Telemetry can produce

- Average TTL
- TTL Distribution
- Cache Lifetime Analysis
- Resolver Policy Comparison

---

# 6.4 Answer Section Mapping

The complete mapping for the current RIPE Atlas packet is
summarized below.

| RFC1035 | RIPE Atlas | dnspython | Canonical DNS Protocol |
|----------|------------|-----------|------------------------|
| ANCOUNT | 4 | len(message.answer) | answer_count |
| TYPE | AAAA | rrset.rdtype | answers[].type |
| TTL | 130 | rrset.ttl | ttl |
| RDATA | IPv6 Address | record.address | answers[].address |

At this point the entire Answer Section has been converted
from RFC1035 Resource Records into the Canonical DNS
Protocol representation.

The resulting fields are now independent of the original
DNS packet format and can be directly consumed by the
Observation Framework and future Telemetry Builder.

# 7. RFC1035 Authority Section

The Authority Section contains Resource Records that identify
the authoritative name servers responsible for the queried
domain.

According to RFC1035, this section has the same Resource
Record (RR) structure as the Answer Section.

```
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
|                     NAME                      |
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
|                     TYPE                      |
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
|                     CLASS                     |
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
|                      TTL                      |
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
|                   RDLENGTH                    |
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
|                     RDATA                     |
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
```

---

## Current RIPE Atlas Example

```json
{
    "NSCOUNT": 0
}
```

The current DNS response contains no Authority Records.

dnspython therefore creates

```python
message.authority

↓

[]
```

The parser converts this into

```json
{
    "authority_count": 0,

    "authority": []
}
```

---

## Why Keep authority?

Although many recursive DNS responses contain no Authority
records, the field is retained because it is part of the DNS
protocol defined by RFC1035.

Future parser versions may extract

- NS Records
- SOA Records
- Delegation Information

Future telemetry examples include

- Authoritative DNS Analysis
- Delegation Validation
- Zone Transfer Investigation

---

# 8. RFC1035 Additional Section

The Additional Section contains supplementary Resource
Records.

Most modern DNS responses include an EDNS OPT record
defined by RFC6891.

The current RIPE Atlas packet contains

```json
{
    "ARCOUNT": 1
}
```

dnspython parses

```python
message.additional
```

which contains one OPT Resource Record.

Current parser implementation stores

```json
{
    "additional_count": 1,

    "additional": []
}
```

The OPT record is currently counted but not decoded.

---

## Why Keep additional?

The Additional Section is important because future protocol
extensions are almost always carried here.

Examples include

- EDNS
- DNS Cookies
- Client Subnet (ECS)
- Padding
- DNSSEC Options

Future parser versions may decode these records without
changing the Observation Framework.

---

# 9. dnspython Message Object

After the Base64 packet has been decoded, dnspython converts
the binary packet into a structured Message object.

The current RIPE Atlas packet produces the following logical
structure.

```
message

├── id
│      22409
│
├── opcode
│      QUERY
│
├── rcode
│      NOERROR
│
├── question
│      └──
│           name
│                2.pool.ntp.org.
│
│           type
│                AAAA
│
│           class
│                IN
│
├── answer
│      ├── AAAA
│      ├── AAAA
│      ├── AAAA
│      └── AAAA
│
├── authority
│      []
│
└── additional
       └── OPT
```

The DNS Packet Parser never accesses the raw binary packet
again.

All protocol information is extracted from this Message
object.

---

# 10. Mapping to the Canonical DNS Protocol

The Packet Parser converts the dnspython Message object into
a structured DNS Packet Model.

The DNS Decoder then converts that packet model into the
Canonical DNS Protocol object.

```
RFC1035

↓

Binary DNS Packet

↓

dnspython Message

↓

Packet Parser

↓

DNS Packet Model

↓

DNS Decoder

↓

Canonical DNS Protocol
```

The Canonical DNS Protocol generated from the current packet
is

```json
{
    "transaction_id": 22409,

    "opcode": "QUERY",

    "rcode": "NOERROR",

    "query_name": "2.pool.ntp.org",

    "query_type": "AAAA",

    "query_class": "IN",

    "answer_count": 4,

    "answers": [

        {
            "type": "AAAA",
            "address": "2a12:bec4:1da0:003e::"
        },

        {
            "type": "AAAA",
            "address": "2a10:0288:0110:f600::"
        },

        {
            "type": "AAAA",
            "address": "2606:4700:00f1::"
        },

        {
            "type": "AAAA",
            "address": "2601:41d0:0423:9800:c300::0123"
        }

    ],

    "ttl": 130,

    "authority_count": 0,

    "additional_count": 1
}
```

At this stage the protocol has become completely independent
from RIPE Atlas, Base64 encoding, RFC1035 wire format and
dnspython implementation.

The Observation Framework interacts only with the Canonical
DNS Protocol object.
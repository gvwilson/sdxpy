---
template: slides
title: "Transferring Files"
---

## The Problem

-   We want to make information available to others

    -   Which includes programs as well as people

-   Understanding how a web server works will help us do this

---

## TCP/IP

-   Most networked computers use [%g internet_protocol "Internet Protocol (IP)" %]

-   Defines multiple layers on top of each other

-   [%g tcp "Transmission Control Protocol (TCP/IP)" %]
    makes communication between computers look like
    reading and writing files

---

## Sockets

-   A [%g socket "sockets" %] is one end of a point-to-point communication channel

-   [%g ip_address "IP address" %] identifies machine

    -   Typically written as four 8-bit numbers like `93.184.216.34`

-   [%g port "port" %] identifies a specific connection on that machine

    -   A number in the range 0–65535

    -   Some numbers reserved for well-known applications

    -   E.g., port 80 is usually a web server

---

<!--# class="aside" -->

## Naming Things

-   IP addresses are hard to remember

    -   And might actually identify a set of machines

-   [%g dns "Domain Name System (DNS)" %] translates names like `third-bit.com`
    into numerical identifiers

---

## Clients and Servers

-   A [%g client "client" %] sends requests and processes responses
    (e.g., web browser)

-   A [%g server "server" %] waits for requests and replies to them
    (e.g., a web server)

---

## Socket Client

[%inc client_all.py %]

---

## Socket Server

[%inc server_raw.py omit=main %]

---

## Interactions

[% figure
   slug="ftp-interaction"
   img="interaction.svg"
   alt="Client/server interaction"
   caption="Steps and messages in client/server interaction."
%]

---

## Using the Library

[%inc server_lib.py %]

---

## Chunking

-   Server uses `self.request.recv(CHUNK_SIZE)`

-   What if client sends more data than that?

-   Allocating a larger [%g buffer_memory "buffer" %] just delays the problem

-   Better solution: keep reading until there is no more data

---

## Reading Chunks

[%inc server_chunk.py mark=class %]

---

## Writing Chunks

[%inc client_chunk.py mark=send %]

-   Try to send all remaining data

-   Advance marker by amount actually sent and re-try

---

## Output

-   Client

[%inc client_chunk.out %]

- Server

[%inc server_chunk.out %]

---

## Testing

-   Manual testing:
    -   Start the server
    -   Wait for it to be ready
    -   Run the client
    -   Shut down the server

-   Better: use a [%g mock_object "mock object" %]
    instead of a real network connection

---

## Refactor the Logging

[%inc logging_handler.py mark=class omit=debug %]

[%inc logging_handler.py mark=debug %]

---

## Creating a Testable Server

[%inc test_server.py mark=handler %]

-   *Don't* upcall constructor of `LoggingHandler`

-   Don't want to trigger all of the library's socket machinery

---

## Mocking the Request Object

1.  A constructor that records
    the data we're going to pretend to have received over a socket
    and does other setup

2.  A `recv` method with the same signature as the real object's

3.  A `sendall` method whose signature matches the real thing's

---

## Mocking the Request Object

[%inc test_server.py mark=request %]

---

## Our First Test

[%inc test_server.py mark=test %]

-   Trade [%g test_fidelity "fidelity" %] for ease of use

---

<!--# class="summary" -->

## Summary	       

[% figure
   slug="ftp-concept-map"
   img="concept_map.svg"
   alt="Concept map of web server"
   caption="Concept map."
%]

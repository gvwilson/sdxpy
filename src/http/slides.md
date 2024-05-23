---
template: slides
title: "Serving Web Pages"
---

## The Problem

-   Uploading and downloading files ([%x ftp %]) is useful,
    but we want to do more

-   Don't want to create a new [%g protocol "protocol" %] for every interaction

-   Use a standard protocol in a variety of ways

---

## HTTP

-   [%g http "Hypertext Transfer Protocol (HTTP)" %] specifies
    what kinds of messages clients and servers can exchange
    and how those messages are formatted

-   Client sends a [%g http_request "request" %] as text over a socket connection

-   Server replies with a [%g http_response "response" %] (also text)

-   Requests and responses may carry (non-textual) data with them

-   *Server can respond to requests however it wants*

---

## HTTP Requests

-   A [%g http_method "method" %] such as `GET` or `POST`

-   A [%g url "URL" %]

-   A [%g http_protocol_version "protocol version" %]

[%inc minimal_http_request.txt %]

---

## Headers

-   Requests may also have [%g http_header "headers" %]

[%inc http_request_headers.txt %]

-   A key can appear any number of times

---

## HTTP Response

-   Protocol and version

-   A [%g http_status_code "status code" %] and phrase

-   Headers, possibly including `Content-Length` (in bytes)

-   Blank line followed by content

[%inc http_response.txt %]

---

## Requests

[%inc requests_example.py %]
[%inc requests_example.out %]

---

## HTTP Lifecycle

[% figure
   slug="http-lifecycle"
   img="http_lifecycle.svg"
   alt="HTTP request/response lifecycle"
   caption="Lifecycle of an HTTP request and response."
%]

---

## Basic HTTP Server

[%inc basic_server.py %]

---

## Running the Server

[%inc basic_server.sh %]

-   Displays nothing until we go to `http://localhost:8080` in our browser

-   Browser shows page

-   Shell shows log messages

[%inc basic_server.out %]

---

## Serving Files

[%inc file_server.py mark=do_get %]

---

## Read and Reply

-   Translate path in URL into path to local file

-   [%g path_resolution "Resolve" %] paths relative to server's directory

[%inc file_server.py mark=handle_file %]

---

## Handling Errors

[%inc file_server.py mark=error_page %]
[%inc file_server.py mark=handle_error %]

-   Use `try`/`except` to handle errors in called methods

-   [%g throw_low_catch_high "Throw low, catch high" %]

---

## Problems

-   Client can escape from our [%g sandbox "sandbox" %]
    by asking for `http://localhost:8080/../../passwords.txt`

-   `send_content` always says it is returning HTML with `Content-Type`

    -   Should use things like `image/png` for images

-   But we got [%g character_encoding "character encoding" %] right

---

## Test Case

-   Want to write this

[%inc test_testable_server.py mark=example %]

---

## Combining Code

-   Use [%g multiple_inheritance "multiple inheritance" %]

[% figure
   slug="http-inheritance"
   img="inheritance.svg"
   alt="Testing class hierarchy"
   caption="Class hierarchy for a testable server."
%]

---

## Mock Request Handler

[%inc mock_handler.py %]

---

## Application Code

[%inc testable_server.py mark=handler omit=skip %]

---

## Two Servers

[%inc testable_server.py mark=main %]

[%inc test_testable_server.py mark=combined %]

---

## Summary

[% figure
   slug="http-concept-map"
   img="concept_map.svg"
   alt="HTTP concept map"
   caption="HTTP concept map."
%]

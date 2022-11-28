---
title: "A Web Server"
syllabus:
-   Every computer on a network has a unique IP address.
-   The Domain Name System (DNS) translates human-readable names into IP addresses.
-   The programs on each computer send and receive messages through numbered sockets.
-   The program that receives a message must interpret the bytes in the message.
-   The HyperText Transfer Protocol (HTTP) specifies one way to interact via messages over sockets.
-   A minimal HTTP request has a method, a URL, and a protocol version.
-   A complete HTTP request may also have headers and a body.
-   An HTTP response has a status code, a status phrase, and optionally some headers and a body.
-   "HTTP is a stateless protocol: the application is responsible for remembering things between requests."
---

The Internet is simpler than most people realize
(as well as being more complex than anyone could possibly comprehend).
Most systems still follow the rules they did thirty years ago;
in particular,
most web servers still handle the same kinds of messages in the same way.

## Using TCP/IP {: #server-tcpip}

Pretty much every program on the web
runs on a family of communication standards called
[%i "Internet Protocol (IP)" "IP (Internet Protocol)" %][%g internet_protocol "Internet Protocol (IP)" %][%/i%].
The one that concerns us is the
[%i "Transmission Control Protocol (TCP/IP)" "TCP/IP (Transmission Control Protocol)" %][%g tcp "Transmission Control Protocol (TCP/IP)" %][%/i%],
which makes communication between computers look like reading and writing files.

Programs using IP communicate through [%i "socket" %][%g socket "sockets" %][%/i%]
([%f server-sockets %]).
Each socket is one end of a point-to-point communication channel,
just like a phone is one end of a phone call.
A socket consists of an [%i "IP address" %][%g ip_address "IP address" %][%/i%] that identifies a particular machine
and a [%i "port" %][%g port "port" %][%/i%] on that machine
The IP address consists of four 8-bit numbers,
which are usually written as `93.184.216.34`;
the [%i "Domain Name System (DNS)" "DNS (Domain Name System)" %][%g dns "Domain Name System (DNS)" %][%/i%]
matches these numbers to symbolic names like `example.com`
that are easier for human beings to remember.

A port is a number in the range 0-65535
that uniquely identifies the socket on the host machine.
(If an IP address is like a company's phone number,
then a port number is like an extension.)
Ports 0-1023 are reserved for the operating system's use;
anyone else can use the remaining ports.

[% figure
   slug="server-sockets"
   img="server_sockets.svg"
   alt="Sockets, IP addresses, and DNS"
   caption="How sockets, IP addresses, and DNS work together."
%]

Most web applications consists of [%i "client (web application)" %][%g client "clients" %][%/i%]
and [%i "server (web application)" %][%g server "servers" %][%/i%].
A client program initiates communication by sending a message and waiting for a response;
a server,
on the other hand,
waits for requests and the replies to them.
There are typically many more clients than servers:
for example,
there may be hundreds or thousands of browsers fetching pages from this book's website right now,
but there is only one server handling those requests.

Here's a simple socket client:

[% inc file="socket_client.py" %]

From top to bottom, this code:

1.  Imports some modules and defines some constants.
    The most interesting of these is `SERVER_ADDRESS` consisting of a host identifier and a port.
    The empty string `""` for the host means "the current machine";
    we could also use the string `"localhost"`.
2.  We use `socket.socket` to create a new socket.
    The values `AF_INET` and `SOCK_STREAM` specify the protocols we're using;
    we'll always use those in our examples,
    so we won't go into details about them.
3.  We connect to the server…
4.  …send our message as a bunch of bytes with `sock.sendall`…
5.  …and print a message saying the data's been sent.
6.  We then read up to a kilobyte from the socket with `sock.recv`.
    If we were expecting longer messages,
    we'd keep reading from the socket until there was no more data.
7.  Finally, we print another message.

The corresponding server is only a little more complicated:

[% inc file="socket_server.py" %]

Python's `socketserver` library provides two things:
a class called `TCPServer` that listens for incoming connections
and then manages them for us,
and another class called `BaseRequestHandler`
that does everything *except* process the incoming data.
In order to do that,
we derive a class of our own from `BaseRequestHandler` that provides a `handle` method.
Every time `TCPServer` gets a new connection
it creates a new object of our class
and calls that object's `handle` method.
This method is the inverse of the code that sends request.
It:

1.  Reads up to a kilobyte from `self.request`
    (which is set up automatically for us in the base class `BaseRequestHandler`).
2.  Prints a diagnostic message.
3.  Use `self.request` again to send data back to whoever we received the message from.

The easiest way to test this is to open two terminal windows side by side.
[%t server-transcript %] shows the sequence of commands and their output:

<div class="table" id="server-transcript" caption="Sequence of operations in socket client/server interaction" markdown="1">
| Server                           | Client                                                      |
| -------------------------------- | ----------------------------------------------------------- |
| `$ python socket_server.py`      |                                                             |
|                                  | `$ python socket_client.py`                                 |
|                                  | `client sent 12 bytes`                                      |
| `got request from 127.0.0.1: 12` |                                                             |
|                                  | `client received 30 bytes: 'got request from 127.0.0.1: 12` |
</div>

<div class="callout" markdown="1">

### Testing Multiprocess Applications

Testing single-process command-line applications is straightforward:
we just run a single command (either directly or via [%i "Make" %][Make][gnu_make][%/i%]).
To test a client-server application,
on the other hand,
we have to start the server,
wait for it to be ready,
then run the client,
and then shut down the server.
It's easy to do this interactively,
but automating it is difficult,
since there's no way to tell how long to wait before trying to talk to the server,
and no easy way to shut the server down.
We will explore some possible approaches once we have a larger application to test.

</div>

## HTTP {: #server-http}

The [%i "Hypertext Transfer Protocol (HTTP)" "HTTP (Hypertext Transfer Protocol)" %][%g http "Hypertext Transfer Protocol (HTTP)" %][%/i%]
specifies one way programs can exchange data over IP.
HTTP is deliberately simple:
the client sends a [%i "HTTP request" %][%g http_request "request" %][%/i%]
specifying what it wants over a socket connection,
and the server sends a [%i "HTTP response" %][%g http_response "response" %][%/i%] containing some data.
That data may be copied from a file on disk,
generated dynamically by a program,
or some mix of the two.

The most important thing about an HTTP request is that it's just text:
any program that wants to can create one or parse one.
An absolutely minimal HTTP request has just
a [%g http_method "method" %],
a [%g url "URL" %],
and a [%g http_protocol_version "protocol version" %]
on a single line separated by spaces:

```
GET /index.html HTTP/1.1
```

The HTTP method is almost always either `GET` (to fetch information)
or `POST` (to submit form data or upload files).
The URL specifies what the client wants:
it is often a path to a file on disk,
such as `/index.html`,
but (and this is the crucial part)
it's completely up to the server to decide what to do with it.
The HTTP version is usually "HTTP/1.0" or "HTTP/1.1";
the differences between the two don't matter to us.

Most real requests have a few extra lines called
[%i "HTTP header" "header (HTTP)" %][%g http_header "headers" %][%/i%],
which are key value pairs like the three shown below:

```
GET /index.html HTTP/1.1
Accept: text/html
Accept-Language: en, fr
If-Modified-Since: 16-May-2022
```

Unlike the keys in hash tables,
keys may appear any number of times in HTTP headers,
so that (for example)
a request can specify that it's willing to accept several types of content.

Finally,
the [%g http_body "body" %] of the request is any extra data associated with it,
such as form data or uploaded files.
There must be a blank line between the last header and the start of the body
to signal the end of the headers,
and if there is a body,
the request must have a header called `Content-Length`
that tells the server how many bytes to read.

An HTTP response is formatted like an HTTP request.
Its first line has the protocol,
a [%i "HTTP status code" "status code (HTTP)" %][%g http_status_code "status code" %][%/i%]
like 200 for "OK" or 404 for "Not Found",
and a status phrase (e.g., the word "OK").
There are then some headers,
a blank line,
and the body of the response:

```
HTTP/1.1 200 OK
Date: Thu, 16 June 2022 12:28:53 GMT
Server: minserve/2.2.14 (Linux)
Last-Modified: Wed, 15 Jun 2022 19:15:56 GMT
Content-Type: text/html
Content-Length: 53

<html>
<body>
<h1>Hello, World!</h1>
</body>
</html>
```

Constructing HTTP requests is tedious,
so most people use libraries to do most of the work.
The most popular such library in Python is called [requests][requests].

[% inc pat="requests_example.*" fill="py out" %]

`request.get` sends an HTTP GET request to a server
and returns an object containing the response ([%f server-http-lifecycle %]).
That object's `status_code` member is the response's status code;
its `content_length` member  is the number of bytes in the response data,
and `text` is the actual data—in this case, an HTML page
that we can analyze or render.

[% figure
   slug="server-http-lifecycle"
   img="server_http_lifecycle.svg"
   alt="HTTP request/response lifecycle"
   caption="Lifecycle of an HTTP request and response."
%]

## Hello, Web {: #server-static}

We're now ready to write a simple HTTP server that will:

1.  wait for someone to connect and send an HTTP request;
2.  parse that request;
3.  figure out what it's asking for;
4.  send back an HTML page.

Steps 1, 2, and 4 are the same from one application to another,
so the Python standard library has a module called `http.server`
that contains tools to do that for us.
Here's the entire server:

[% inc file="basic_http_server.py" %]

Let's start at the bottom and work our way up.

1.  Again, `SERVER_ADDRESS` specifies the server's host and port.
2.  The `HTTPServer` class takes care of parsing requests and sending back responses.
    When we construct it,
    we give it the server address and the name of the class we've written
    that handles requests the way we want—in this case, `RequestHandler`.
3.  Finally, we call the server's `serve_forever` method,
    which runs until it crashes or we stop it with Ctrl-C.

So what does `RequestHandler` do?

1.  When the server receives a `GET` request,
    it looks in the request handler for a method called `do_GET`.
    (If it gets a `POST`, it looks for `do_POST` and so on.)
2.  `do_GET` converts the text of the page we want to send back
    from characters to bytes—we'll talk about this below.
3.  It then sends a response code (200),
    a couple of headers to say what the content type is
    and how many bytes the receiver should expect,
    and a blank line (produced by the `end_headers` method).
4.  Finally, `do_GET` sends the content of the response
    by calling `self.wfile.write`.
    `self.wfile` is something that looks and acts like a write-only file,
    but is actually sending bytes to the socket connection.

If we run this program from the command line,
it doesn't display anything:

[% inc file="basic_http_server.sh" %]

If we then go to `http://localhost:8080` with our browser,
though,
we get this in our browser:

```
Hello, web!
```

and this in our shell:

```
127.0.0.1 - - [16/Sep/2022 06:34:59] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [16/Sep/2022 06:35:00] "GET /favicon.ico HTTP/1.1" 200 -
```

The first line is straightforward:
since we didn't ask for a particular file,
our browser has asked for '/' (the root directory of whatever the server is serving).
The second line appears because
our browser automatically sends a second request
for an image file called `/favicon.ico`,
which it will display as an icon in the address bar if it exists.

## Serving Files {: #server-files}

Serving the same page for every request isn't particularly useful,
so let's rewrite our simple server to return files.
The basic logic looks like this:

[% inc file="file_server.py" keep="do_get" %]

We first turn the path in the URL into a local file path.
(We assume that all paths are [%g path_resolution "resolved" %]
relative to the directory that the server is running in.)
If that path corresponds to a file, we send it back to the client.
If nothing is there,
or if what's there is not a file,
we send an error message.
{: .continue}

It might seem simpler to rewrite `do_GET` to use `if`/`else` instead of `try`/`except`,
but the latter has an advantage:
we can handle errors that occur inside methods we're calling (like `handle_file`)
in the same place and in the same way as we handle errors that occur here.
This approach is sometimes called "throw low, catch high",
which means that errors should be flagged in many places
but handled in a few places high up in the code.
The method that handles files is an example of this:

[% inc file="file_server.py" keep="handle_file" %]

If there's an error at any point in the processing cycle
we send a page with an error message
*and* an error status code:

[% inc file="file_server.py" keep="handle_error" %]

The error page is just HTML with some placeholders for the path and message:

[% inc file="file_server.py" keep="error_page" %]

The code that actually sends the response is similar to what we've seen before:
{: .continue}

[% inc file="file_server.py" keep="send_content" %]

This server works, but only for a very forgiving definition of "works".
We are careful not to show clients the actual paths to files on the server
in our error messages,
but if someone asked for `http://localhost:8080/../../passwords.txt`,
this server will happily look two levels up from the directory where it's running
and try to return that file.
The server machine's passwords probably aren't stored there,
but with enough `..`'s and some patience,
an attacker could poke around large parts of our filesystem.
We will tackle this security hole in the exercises.

Another problem is that `send_content` always tells clients that
it is returning an HTML file with the `Content-Type` header.
It should instead look at the extension on the file's name
and set the content type appropriately,
e.g.,
return `image/png` for a PNG-formatted image.

One thing the server is doing right is character encoding.
The `send_content` method expects `content` to be a `bytes` object,
not a string,
because the HTTP protocol requires the content length to be the number of bytes.
The server reads files in binary mode
by using `"rb"` instead of just `"r"` when it opens files in `handle_file`,
converts the internally-generated error page from characters to bytes
using the [%g utf_8 "UTF-8" %] encoding,
and specifies `charset=utf-8` as part of the content type.

## Testing  {: #server-testing}

At this point we really need to figure out how to test the servers we're building.
The key to our approach is the notion of [%i "fidelity (in testing)" %][%g test_fidelity "fidelity" %][%/i%]:
how close is what we test to what we use in production?
In an ideal world they are exactly the same,
but in cases like this it makes sense to sacrifice a little fidelity for testability's sake.

Let's work backward from a test we want to be able to write.
We would like to create a file,
simulate an HTTP GET request,
and check that the status, headers, and content are correct.
In the code below,
the `CombinedHandler` class does double duty:
it handles the simulated request,
and also stores the values that the client would receive.

[% inc file="test_testable_server.py" keep="example" %]

The class we are testing is called `CombinedHandler`
because it is derived from two things:
a class that implements our application's `do_GET`
and another class that provides replacements for
the `BaseHTTPRequestHandler` properties and methods
that our application actually uses.
The latter is just a few lines long,
though it would be larger if our application used
more of `BaseHTTPRequestHandler`'s functionality:

[% inc file="mock_handler.py" %]

The application-specific class contains the code we've already seen:

[% inc file="testable_server.py" keep="handler" omit="skip" %]

However,
`ApplicationRequestHandler` *doesn't* inherit from `BaseHTTPRequestHandler`.
Instead,
we create a class that combines the two when we need it:
{: .continue}

[% inc file="testable_server.py" keep="main" %]

and create another class for testing that combines
the application-specific class with `MockHandler`.
This class is the `CombinedClass` that our test uses:
{: .continue}

[% inc file="test_testable_server.py" keep="combined" %]

[%f server-inheritance %] shows the final inheritance hierarchy.
It's a lot of work to test a GET request for one file,
but we can re-use `MockRequestHandler` to test
the application-specific code for other servers.
Most libraries don't provide helper classes like this to support testing,
but programmers appreciate those that do.

[% figure
   slug="server-inheritance"
   img="server_inheritance.svg"
   alt="Testing class hierarchy"
   caption="Class hierarchy for a testable server."
%]

## Summary {: #server-summary}

[% figure
   slug="server-concept-map"
   img="server_concept_map.svg"
   alt="HTTP server concept map"
   caption="HTTP server concept map."
%]

## Exercises {: #server-exercises}

### Reading and writing chunks {: .exercise}

Modify the socket client and socket server so that:

1.  the client reads any amount of data from standard input
    (including none at all)
    and sends it to the server in kilobyte-sized chunks;
    and

2.  the server reads any amount of data from the socket
    in chunks of four kilobytes
    and sends a message with a byte count back to the client.

### Parsing HTTP requests {: .exercise}

Write a function that takes a list of lines of text as input
and parses them as if they were an HTTP request.
The result should be a dictionary with the request's method,
URL,
protocol version,
and headers.

### Query parameters {: .exercise}

A URL can contain [%i "query parameter" %][%g query_parameter "query parameters" %][%/i%].
Read the documentation for the [urlparse][py_urlparse] module
and then modify the file server example so that
a URL containing a query parameter `bytes=N`
(for a positive integer N)
returns the first N bytes of the requested file.

### Better path resolution {: .exercise}

Modify the file server so that:

1.  it must be given the absolute path to a directory
    as a command-line argument
    when started; and

2.  it only serves files in or below that directory
    (so that paths containing `..` and other tricks
    can't be used to retrieve arbitrary files).

### Better content types {: .exercise}

Read the documentation for the [mimetypes][py_mimetypes] module
and then modify the file server to return the correct content type
for files that aren't HTML (such as images).

### Uploading files {: .exercise}

Modify the file server to handle POST requests.

1.  The URL must specify the name of the file being uploaded.

2.  The body of the request must be the bytes of the file.

3.  All uploaded files are saved in a single directory,
    i.e.,
    upload paths cannot contain directory components.

### Checking content length {: .exercise}

Modify the file server so that:

1.  if the client sends more content than indicated in the `Content-Length` header,
    the extra bytes are read but ignored; and

2.  if the client sends less content,
    the server doesn't wait indefinitely for the missing bytes.

What status code should the server return to the client in each case?

### Directory listing {: .exercise}

1.  Modify the file server so that
    if the path portion of the URL identifies a directory,
    the server returns a plain text list of the directory's contents.

2.  Write tests for this using the [pyfakefs][pyfakefs] module.

### Dynamic results {: .exercise}

Modify the file server so that if the client requests the "file" `/time`,
the server returns an HTML page that reports the current time on the server's machine.

### Templated results {: .exercise}

Modify the file server to:

1.  turn the query parameter's in the URL into a dictionary;

2.  use that dictionary to fill in a template page ([%x templating %]); and

3.  return the resulting HTML page to the client.

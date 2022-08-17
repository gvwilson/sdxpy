---
title: "A Web Server"
syllabus:
- Every computer on a network has a unique IP address.
- The Domain Name System (DNS) translates human-readable names into IP addresses.
- The programs on each computer send and receive messages through numbered sockets.
- The program that receives a message must interpret the bytes in the message.
- The HyperText Transfer Protocol (HTTP) specifies one way to interact via messages over sockets.
- A minimal HTTP request has a method, a URL, and a protocol version.
- A complete HTTP request may also have headers and a body.
- An HTTP response has a status code, a status phrase, and optionally some headers and a body.
- "HTTP is a stateless protocol: the application is responsible for remembering things between requests."
---

The Internet is simpler than most people realize
(as well as being more complex than anyone could possibly have imagined).
Most systems still follow the rules they did thirty years ago;
in particular,
most web servers still handle the same kinds of messages in the same way.

## Sockets {: #server-sockets}

Pretty much every program on the web
runs on a family of communication standards called Internet Protocol (IP).
The member of that family which concerns us is the Transmission Control Protocol (TCP/IP),
which makes communication between computers look like reading and writing files.

Programs using IP communicate through sockets.
Each socket is one end of a point-to-point communication channel,
just like a phone is one end of a phone call.
A socket consists of an IP address that identifies a particular machine
and a port number on that machine.
The IP address consists of four 8-bit numbers,
such as `174.136.14.108`;
the Domain Name System (DNS) matches these numbers to symbolic names like `example.com`
that are easier for human beings to remember.

A port number is a number in the range 0-65535
that uniquely identifies the socket on the host machine.
(If an IP address is like a company's phone number,
then a port number is like an extension.)
Ports 0-1023 are reserved for the operating system's use;
anyone else can use the remaining ports.

Here's a simple socket client:

[% excerpt f="socket_client.py" %]

From top to bottom, it:

1.  Imports some modules and defines some constants.
    The most interesting of these is `SERVER_ADDRESS`
    The empty string `""` for the host means "the current machine";
    we could also use the string `"localhost"`.
2.  We use `socket.socket` to create a new socket.
    The values `AF_INET` and `SOCK_STREAM` specify the protocols we're using;
    we'll always use those in our examples,
    so we won't go into details about them.
3.  We connect to the server...
4.  ...send our message as a bunch of bytes with `sock.sendall`...
5.  ...and print a message saying the data's been sent.
6.  We then read up to a kilobyte from the socket with `sock.recv`.
    If we were expecting longer messages,
    we'd keep reading from the socket until there was no more data,
    but we're trying to keep this example simple.
7.  Finally, we print another diagnostic message.

The receiving end is only a little more complicated:

[% excerpt f="socket_server.py" %]

Python's `socketserver` library provides two things:
a class called `TCPServer` that listens for incoming connections
and then manages them for us,
and another class called `BaseRequestHandler`
that does everything *except* process the incoming data.
In order to do that,
we derive a class of our own from `BaseRequestHandler` that provides a `handle` method.
Every time `TCPServer` gets a new connection
it creates a new instance of our class
and calls its `handle` method.

Our `handle` method is the inverse of the code that sends request:

1.  Read up to a kilobyte from `self.request`
    (which is set up automatically for us in the base class `BaseRequestHandler`).
2.  Construct and print a diagnostic message.
3.  Use `self.request` again to send data back to whoever we received the message from.

The easiest way to test this is to open two terminal windows side by side.
[%t server-transcript %] shows the sequence of operations side by side:

<div class="table" id="server-transcript" caption="Sequence of operations in socket client/server interaction" markdown="1">
| Server                           | Client                                                      |
| -------------------------------- | ----------------------------------------------------------- |
| `$ python socket_server.py`      |                                                             |
|                                  | `$ python socket_client.py "a test message"`                |
|                                  | `client sent 14 bytes`                                      |
| `got request from 127.0.0.1: 14` |                                                             |
|                                  | `client received 30 bytes: 'got request from 127.0.0.1: 14` |
</div>

## HTTP {: #server-http}

The Hypertext Transfer Protocol (HTTP) describes one way that
programs can exchange data over IP.
HTTP is deliberately simple:
the client sends a request specifying what it wants over a socket connection,
and the server sends some data in response.
The data may be copied from a file on disk,
generated dynamically by a program,
or some mix of the two.

The most important thing about an HTTP request is that it's just text:
any program that wants to can create one or parse one.
An absolutely minimal HTTP request has just a *method*,
a *URL*,
and a *protocol version*
on a single line separated by spaces:

```
GET /index.html HTTP/1.1
```

The HTTP method is almost always either "GET" (to fetch information)
or "POST" (to submit form data or upload files).
The URL specifies what the client wants;
it is often a path to a file on disk,
such as `/index.html`,
but (and this is the crucial part)
it's completely up to the server to decide what to do with it.
The HTTP version is usually "HTTP/1.0" or "HTTP/1.1";
the differences between the two don't matter to us.

Most real requests have a few extra lines called *headers*,
which are key value pairs like the three shown below:

```
GET /index.html HTTP/1.1
Accept: text/html
Accept-Language: en, fr
If-Modified-Since: 16-May-2022
```

Unlike the keys in hash tables,
keys may appear any number of times in HTTP headers.
This allows a request to do things like
specify that it's willing to accept several types of content.

Finally,
the *body* of the request is any extra data associated with the request.
This is used when submitting data via web forms,
when uploading files,
and so on.
There must be a blank line between the last header and the start of the body
to signal the end of the headers.
If there is a body,
the request must have a header called `Content-Length`
that tells the server how many bytes to read in the body of the request.

An HTTP response is formatted like an HTTP request.
Its first line has the protocol,
a *status code* (like 200 for "OK" or 404 for "Not Found")
and a status phrase (like "OK").
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

[% excerpt pat="requests_example.*" fill="py out" %]

`request.get` sends an HTTP GET request to a server
and returns an object containing the response.
That object's `status_code` member is the response's status code;
its `content_length` member  is the number of bytes in the response data,
and `text` is the actual data
(in this case, an HTML page).

## Hello, Web {: #server-static}

We're now ready to write our first simple HTTP server.
The basic idea is simple:

1.  Wait for someone to connect to our server and send an HTTP request;
2.  parse that request;
3.  figure out what it's asking for;
4.  fetch that data (or generate it dynamically);
5.  format the data as HTML; and
6.  send it back.

Steps 1, 2, and 6 are the same from one application to another,
so the Python standard library has a module called `http.server`
that contains tools to do that for us
so that we just have to take care of steps 3-5.
Here's our first working web server:

[% excerpt f="basic_http_server.py" %]

Let's start at the bottom and work our way up.

1.  Again, `SERVER_ADDRESS` that specifies the host the server is running on
    and the port it's listening on.
2.  The `HTTPServer` class takes care of parsing requests and sending back responses.
    When we construct it,
    we give it the server address and the name of the class we've written
    that handles requests the way we want---in this case, `RequestHandler`.
3.  Finally, we call the server's `serve_forever` method.
    It will then run until it crashes or we stop it with Ctrl-C.

So what does `RequestHandler` do?

1.  When the server receives a `GET` request,
    it looks in the request handler for a method called `do_GET`.
    (If it gets a `POST`, it looks for `do_POST` and so on.)
2.  `do_GET` converts the text of the page we want to send back
    from characters to bytes---we'll talk about this below.
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

```bash
$ python serve_static_content.py
```

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

## Exercises {: #server-exercises}

FIXME

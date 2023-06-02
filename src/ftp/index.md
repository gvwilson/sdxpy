---
syllabus:
-   Every computer on a network has a unique IP address.
-   The Domain Name System (DNS) translates human-readable names into IP addresses.
-   The programs on each computer send and receive messages through numbered sockets.
-   The program that receives a message must interpret the bytes in the message.
---

The Internet is simpler than most people realize
(as well as being more complex than anyone could possibly comprehend).
Most systems still follow the rules they did thirty years ago;
in particular,
most web servers still handle the same kinds of messages in the same way.

## Using TCP/IP {: #ftp-tcpip}

Pretty much every program on the web
runs on a family of communication standards called
[%i "Internet Protocol (IP)" "IP (Internet Protocol)" %][%g internet_protocol "Internet Protocol (IP)" %][%/i%].
The one that concerns us is the
[%i "Transmission Control Protocol (TCP/IP)" "TCP/IP (Transmission Control Protocol)" %][%g tcp "Transmission Control Protocol (TCP/IP)" %][%/i%],
which makes communication between computers look like reading and writing files.

Programs using IP communicate through [%i "socket" %][%g socket "sockets" %][%/i%]
([%f ftp-sockets %]).
Each socket is one end of a point-to-point communication channel,
just like a phone is one end of a phone call.
A socket consists of an [%i "IP address" %][%g ip_address "IP address" %][%/i%] that identifies a particular machine
and a [%i "port" %][%g port "port" %][%/i%] on that machine.

[% figure
   slug="ftp-sockets"
   img="sockets.svg"
   alt="Sockets, IP addresses, and DNS"
   caption="How sockets, IP addresses, and DNS work together."
%]

The IP address consists of four 8-bit numbers,
which are usually written as `93.184.216.34`;
the [%i "Domain Name System (DNS)" "DNS (Domain Name System)" %][%g dns "Domain Name System (DNS)" %][%/i%]
matches these numbers to symbolic names like `example.com`
that are easier for human beings to remember.

A port is a number in the range 0-65535
that uniquely identifies the socket on the host machine.
(If an IP address is like a company's phone number,
then a port number is like an extension.)
Ports 0-1023 are reserved for well-known TCP/IP applications like web servers;
custom applications should use the remaining ports
(and should allow users to decide *which* port,
since there's always the chance that two different people will pick 1234 or 6789).

Most web applications consists of [%i "client (web application)" %][%g client "clients" %][%/i%]
and [%i "server (web application)" %][%g server "servers" %][%/i%].
A client program initiates communication by sending a message and waiting for a response;
a server,
on the other hand,
waits for requests and the replies to them.
There are typically many more clients than servers:
for example,
there may be hundreds or thousands of browsers
fetching pages from this book's website right now,
but there is only one server handling those requests.

Here's a basic socket client:

[% inc file="client.py" %]

We call it "basic" rather than "simple" because there's a lot going on here.
From top to bottom, this code:
{: .continue}

1.  Imports some modules and defines some constants.
    The most interesting of these is `SERVER_ADDRESS`
    consisting of a host identifier and a port.
    The string `"localhost"` means "the current machine".
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

The corresponding server has just as much low-level detail:

[% inc file="raw_server.py" omit="main" %]

This code claims a socket,
listens until it receives a connection request,
reads up to a kilobyte of data,
prints a message,
and replies to the client.
[%f ftp-interaction %] shows the order of operations and messages
when we run the client and server in separate terminal windows.
{: .continue}

[% figure
   slug="ftp-interaction"
   img="interaction.svg"
   alt="Client/server interaction"
   caption="Steps and messages in client/server interaction."
%]

<div class="callout" markdown="1">

### Testing Multiprocess Applications

Testing single-process command-line applications is hard enough;
to test a client-server application,
we have to start the server,
wait for it to be ready,
then run the client,
and then shut down the server if it hasn't shut down by itself.
It's easy to do this interactively,
but automating it is difficult because
there's no way to tell how long to wait before trying to talk to the server
and no easy way to shut the server down.
We will explore some approaches once we have a larger application to test.

</div>

There's a *lot* going on here,
so most people who have to program at this level
use Python's `socketserver` library,
which provides two things:
a class called `TCPServer` that manages incoming connections
and another class called `BaseRequestHandler`
that does everything *except* process the incoming data.
In order to do that,
we derive a class of our own from `BaseRequestHandler` that provides a `handle` method.
Every time `TCPServer` gets a new connection
it creates a new object of our class
and calls that object's `handle` method.
Using these,
our server is:

[% inc file="lib_server.py" %]

These two library classes use a different design than what we've seen before.
Instead of creating one class for programmers to extend,
the `socketserver` library puts the low-level details in `TCPServer`,
which can be used as-is,
and asks users to create a plug-in class from `BaseRequestHandler`
for the server to use.
This approach isn't intrinsically better or worse than
the "derive and override" approach we've seen before;
they're just two more tools in a software designer's toolbox.
{: .continue}

## Summary {: #ftp-summary}

[% figure
   slug="ftp-concept-map"
   img="concept_map.svg"
   alt="File transfer concept map"
   caption="File transfer concept map."
%]

## Exercises {: #ftp-exercises}

[% fixme exercises %]

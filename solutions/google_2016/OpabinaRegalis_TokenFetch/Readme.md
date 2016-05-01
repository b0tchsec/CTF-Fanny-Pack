# Google CTF 2016 : Opabina Regalis - Token Fetch

**Category:** Web
**Points:** 50
**Solves:** 79
**Description:**


>
>There are a variety of client side machines that have access to certain websites we'd like to access. We have a system in place, called "Opabina Regalis" where we can intercept and modify HTTP requests on the fly. Can you implement some attacks to gain access to those websites?
>
>Opabina Regalis makes use of [Protocol Buffers](https://developers.google.com/protocol-buffers/) to send a short snippet of the HTTP request for modification.
>
>Here's the protocol buffer definition used:
>
>
>     package main;
>
>     message Exchange {
>
>        enum VerbType {
>                GET = 0;
>                POST = 1;
>        }
>
>        message Header {
>                required string key = 1;
>                required string value = 2;
>        }
>
>        message Request {
>                required VerbType ver = 1; // GET
>                required string uri = 2; // /blah
>                repeated Header headers = 3; // Accept-Encoding: blah
>                optional bytes body = 4;
>        }
>
>        message Reply {
>                required int32 status = 1; // 200 or 302
>                repeated Header headers = 2;
>                optional bytes body = 3;
>        }
>
>        oneof type {
>                Request request = 1;
>                Reply reply = 2;
>        }
>     }
>

>The network protocol uses a 32-bit little endian integer representing the length of the marshalled protocol buffer, followed by the marshalled protocol buffer.
>
>Listening on port 1876 on ssl-added-and-removed-here.ctfcompetition.com
>


## Write-up

In order to solve this problem, I had to learn a little bit about Protocol buffer.  I started by reading the documentation that was linked in the challenge description.  It looks like Google supports a few different languages, so I decided to go with Python.  But first I had to install the protocol buffer compiler (protoc).


Download the protocl buffer project
```
$ git clone https://github.com/google/protobuf.git
```


Compile and install (from [Google's Git Documentaion](https://github.com/google/protobuf/tree/master/src))
```
$ cd ./protobuf/
$ ./autogen.sh
$ ./configure
$ make
$ make check
$ sudo make install
$ sudo ldconfig # refresh shared library cache.
```

Google has provided the contents of our message file in the challenge description, simply save it as main.proto.

Now that the protocol buffer compiler has been installed and we have our main.proto file created, it is time to run the compiler.
```
$ protoc -I=./ --python_out=./ main.proto
```

Wow, I am finally ready to start writing code.  I can create an empty Exchange message protocol buffer with the following snippet:
```python
import main_pb2
msg = main_pb2.Exchange()
```

Once I verified that I could import main_pb2, I setup the TCP/SSL socket as such:
```python
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
ws = ssl.wrap_socket(s, ssl_version=ssl.PROTOCOL_SSLv23)
```

This is the code I wrote for reading from the socket, careful to obey the requirement for 32bit little-endian integers.
```python
def rx_msg(sock):
  data = sock.recv(4)
  
  #Unpack the message length
  msg_len = struct.unpack('<I', data)[0]
  data = sock.recv(msg_len)
  
  #Read the protocol buffer message
  msg = main_pb2.Exchange()
  msg.ParseFromString(data)
```

And the code for writing to the socket.
```python
def tx_msg(sock, msg):
  p = pack_msg(msg.SerializeToString())
  sock.send(p)
```

And add some simple code to print the request so that I can easily see what is happening.
```python
def print_req(req):
  print('VerbType: ' + repr(req.ver))
  print('URI: ' + repr(req.uri))
  print('Headers:')
  for i in req.headers:
  	print(repr(i))
  print('Body: ' + repr(req.body))
```

I should be all set, let's connect to the socket and see if I get a request.
```
VerbType: 0
URI: u'/not-token'
Headers:
key: "User-Agent"
value: "opabina-regalis.go"
```

Hmm...  Looks like someone is trying to connect to '/not-token'.  What if I create a new request for '/token'
```python
new_dat = main_pb2.Exchange()
new_dat.request.ver = main_pb2.Exchange.GET
new_dat.request.uri = u'/token'
new_dat.request.body = ''
tx_msg(ws, new_dat)
```

Now let's see what the whole script output looks like.
```
VerbType: 0
URI: u'/not-token'
Headers:
key: "User-Agent"
value: "opabina-regalis.go"

Body: ''
Status: 200
Headers:
key: "Server"
value: "opabina-regalis.go"

Body: 'CTF{WhyDidTheTomatoBlush...ItSawTheSaladDressing}'
```

[Click here for entire Python implementation](https://github.com/b0tchsec/CTF-Fanny-Pack/blob/master/solutions/google_2016/OpabinaRegalis_TokenFetch/client.py)

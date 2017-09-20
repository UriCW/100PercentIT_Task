# Solution to task by 100 percent IT

Calculates an estimate of bytes sent or recieved by each project.

## Setup
Ensure all data is stored in database named pmacct, you also need to modify the login details in tests.py
```python
    def setUp(self):
        engine = create_engine('mysql://<user>:<password>@localhost/pmacct', echo=False)
```
and change \<user\>\:\<password\> accordingly.

## Run
To view the results run
```bash
    $python tests.py
```

the query takes a while to process, but you should start seeing results come out as they come

### Notes
I joined both the snat and fip audit tables as I am not sure what's the difference
This provides an estimate, this is due to corrolating based on IP address usage in a 5 minutes time window. if a customer switches project within the 5 minutes window, some of the bytes consumed might show as consumed by both projects. 

# Solution to task by 100 percent IT

Calculates an estimate of bytes consumed per each project.
This correlates an IP address and a time stamp, if a customer switches projects in a 5 minutes time window, some of the bytes consumed will show up in both projects.
## Setup
Ensure all data is stored in database named pmacct, you also need to modify the login details in tests.py
```python
    def setUp(self):
        engine = create_engine('mysql://<user>:<password>@localhost/pmacct', echo=False)
    change <user>:<password> accordingly.
```
## Run
To view the results run
```bash
    $python tests.py
```

the query takes a while to process, but you should start seeing results come out as they come

### Notes
Note that the task did not specify if the total bytes were uploaded or downloaded, so i summed both
also note that I joined both the snat and fip audit tables as I am not sure what's the difference
This provides an estimate, this is due to corrolating based on IP address usage in a 5 minutes time window.

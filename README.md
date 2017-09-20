Calculates an estimate of bytes consumed per each project.
This corrolates an IP address and a time stamp, if a customer switches projects in a 5 minutes time window, some of the bytes consumed will show up in both projects.

Ensure all data is stored in database named pmacct, you also need to modify the login details in tests.py
    def setUp(self):
        engine = create_engine('mysql://<user>:<password>@localhost/pmacct', echo=False)
    change <user>:<password> accordingly.

To view the results run
$python tests.py

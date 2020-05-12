# ms-sender.py 

#### ms-sender.cfg

```bash
[default]
webhook_url = web hook url (required)
log_level = ERROR (required, can be overridden by --log_level)
sender = My tiny Webserver (optional, can be overridden by --sender, hostname is used as a fallback)
fact.Env = Staging (optional)
fact.Project = Project Name (optional)
logs = D:\mst-sender\logs (ms-sender.py log directory; optional, the current script directory used as a fallback)
```

#### ms-sender.py command line arguments:
* `--profile` - profile used in `ms-sender.cfg`
* `--sender`  - notification sender 
* `--message` - a message which is posted to MS Teams
* `--title`   - a card message title 


# nxlog 
#### Windows 

* Download and install nxlog-ce (or Enterprise edition) [download](https://nxlog.co/products/nxlog-community-edition/download)
* Have a Python installed (v2.7)
* Clone this repo or download `mst-sender.py` along with `mst-sender.cfg.sample` which are used to push notification to MS Teams
* Rename `mst-sender.cfg.sample` to `mst-sender.cfg` and paste your MS Teams Web Hook Url in it
* Edit your nxlog configuration file found in `C:\Program Files (x86)\nxlog\conf` (or `C:\Program Files\nxlog\conf`) and add the following code:


```bash
<Extension _exec>
    Module  xm_exec
</Extension>

<Input in>
    Module  im_file
    File    "D:\\mst-sender\\sample\\test.log"
        <Exec>
        if $raw_event =~ /(\S+)\ (.+) \[ERROR (.+)/
        {
            exec_async("C:\\Python27\\python.exe", "D:\\mst-sender\\mst-sender.py", "--log_level", "ERROR", "--message", $raw_event);
        }
        if $raw_event =~ /(\S+)\ (.+) \[WARNING (.+)/
        {
            exec_async("C:\\Python27\\python.exe", "D:\\mst-sender\\mst-sender.py", "--log_level", "WARNING", "--message", $raw_event);
        }
        </Exec>
</Input>

<Output out1>
    Module  om_null
</Output>

<Route 1>
    Path    in => out1
</Route>
```
where:
```
* C:\\Python27\\python.exe - path to your python installation
* D:\\mst-sender\\test\\test.log - log file being monitored by nxlog
* D:\\mst-sender\\mst-sender.py - path to `sender.py`
```

* Restart `nxlog` service
* Verify if it works; add a couple of ERROR, WARNING lines in `test.log`. You should get notifications in MS Teams

#### Linux (Ubuntu)
* Install python requests `sudo apt-get install -y python-requests.`
* Download nxlog (download)[https://nxlog.co/products/nxlog-community-edition/download]
* Transfer the file to the target server scp or a similar secure method 
* Install nxlog packadges ie. `sudo dpkg -i nxlog-ce_2.10.2150_ubuntu_xenial_amd64.deb` [nxlog installation manual](https://nxlog.co/documentation/nxlog-user-guide/deploy_debian.html)
* Verify the installation works `nxlog -v`
* Pull `sender.py` onto the server `wget https://raw.githubusercontent.com/cloudradar-monitoring/mst-sender/master/mst-sender.py -O /usr/local/bin/mst-sender && chmod +x /usr/local/bin/mst-sender`
* Pull the configuration file onto the server `mkdir /etc/mst-sender/` and then `wget https://raw.githubusercontent.com/cloudradar-monitoring/mst-sender/master/mst-sender.cfg.sample -O /etc/mst-sender/mst-sender.cfg`
* Paste your MS Teams Web Hook Url into `/mst-sender.cfg`
* Pull the test log file onto the server `wget https://raw.githubusercontent.com/cloudradar-monitoring/mst-sender/master/sample/test.log -O /etc/mst-sender/test.log`
* Edit `nxlog.conf` in `/etc/nxlog`

```bash
<Extension _exec>
    Module  xm_exec
</Extension>

<Input in>
    Module  im_file
    File    "/etc/mst-sender/test.log"
        <Exec>
        if $raw_event =~ /(\S+)\ (.+) \[ERROR (.+)/
        {
            exec_async("/usr/bin/python", "/usr/local/bin/mst-sender", "--log_level", "ERROR", "--message", $raw_event);
        }
        if $raw_event =~ /(\S+)\ (.+) \[WARNING (.+)/
        {
            exec_async("/usr/bin/python", "/usr/local/bin/mst-sender", "--log_level", "WARNING", "--message", $raw_event);
        }
        </Exec>
</Input>

<Output out1>
    Module  om_null
</Output>

<Route 1>
    Path    in => out1
</Route>
```

* restart nxlog `sudo systemctl restart nxlog`
* Verify if it works; add a couple of ERROR, WARNING lines in `test.log`. You should get notifications in MS Teams

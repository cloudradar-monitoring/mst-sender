# Windows 

* Download and install nxlog-ce (or Enterprise edition) [download](https://nxlog.co/products/nxlog-community-edition/download)
* Have a Python installed
* Clone this repo or download `sender.py` which is used to push notification to MS Teams
* Rename `mst-sender.conf.sample` to `mst-sender.conf` and paste your MS Teams Web Hook Url in it
* Edit your nxlog configuration file found in `C:\Program Files (x86)\nxlog\conf` (or `C:\Program Files\nxlog\conf`) and add the following code:


```bash
<Extension _exec>
    Module  xm_exec
</Extension>

<Input in>
    Module  im_file
    File    "D:\\mst-sender\\log\\test.log"
        <Exec>
        if $raw_event =~ /(\S+)\ (.+) \[ERROR (.+)/
        {
            exec_async("C:\\Python36\\python.exe", "D:\\mst-sender\\sender.py", "--log_level", "ERROR", "--message", $raw_event);
        }
        if $raw_event =~ /(\S+)\ (.+) \[WARNING (.+)/
        {
            exec_async("C:\\Python36\\python.exe", "D:\\mst-sender\\sender.py", "--log_level", "WARNING", "--message", $raw_event);
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
* C:\\Python36\\python.exe is your  path to your python installation
* D:\\mst-sender\\test\\test.log is your log file being monitored by nxlog
* D:\\mst-sender\\sender.py is the path to `sender.py`
```

* Restart `nxlog` service

# Linux (Ubuntu)
* Install python requests `sudo apt-get install -y python-requests.`
* Download nxlog (download)[https://nxlog.co/products/nxlog-community-edition/download]
* Transfer the file to the target server scp or a similar secure method 
* Install nxlog packadges ie. `sudo dpkg -i nxlog-ce_2.10.2150_ubuntu_xenial_amd64.deb` [Installation](https://nxlog.co/documentation/nxlog-user-guide/deploy_debian.html)
* Verify the installation works `nxlog -v`
* Pull `sender.py` onto the server `wget https://raw.githubusercontent.com/cloudradar-monitoring/mst-sender/master/sender.py -O /usr/local/bin/mst-sender && chmod +x /usr/local/bin/mst-sender`
* Pull the configuration file `mkdir /etc/mst-sender/` and `wget https://raw.githubusercontent.com/cloudradar-monitoring/mst-sender/master/mst-sender.conf.sample -O /etc/mst-sender/mst-sender.conf`
* Edit `nxlog.conf` in `/etc/nxlog`

```bash
<Extension _exec>
    Module  xm_exec
</Extension>

<Input in>
    Module  im_file
    File    "/etc/nxlog/test.log"
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

#### nxlog config file 


```bash
define ACTION_ERROR { log_info("error found:"); log_info($raw_event); drop();}
define ACTION_WARNING { log_info("warning found:"); log_info($raw_event); drop();}

<Extension _exec>
    Module  xm_exec
</Extension>

<Input in>
    Module  im_file
    File    "D:\\mst-sender\\test.log"
        <Exec>
        if $raw_event =~ /(\S+)\ (.+) \[ERROR (.+)/
        {
				exec_async("C:\\Python36\\python.exe", "D:\\mst-sender\\sender.py", "--log_level", "ERROR", "--message", $raw_event);
				%ACTION_ERROR%
        }
        if $raw_event =~ /(\S+)\ (.+) \[WARNING (.+)/
		{
				exec_async("C:\\Python36\\python.exe", "D:\\mst-sender\\sender.py", "--log_level", "WARNING", "--message", $raw_event);
				%ACTION_WARNING%
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

The command which calls the python script
```bash
exec_async("C:\\Python36\\python.exe", "D:\\mst-sender\\sender.py", "--log_level", "ERROR", "--message", $raw_event);
```

where:
* `$raw_event` is the actual log line which matches the regex
* `log_level` WARNING or ERROR 

Note: `ACTION_ERROR` and `ACTION_WARNING` are defined and used only for debugging purposes. 


### `sender_basic.py` 
We could at any time switch over to a basic sender but the Python Wrapper Library to send requests to Microsoft Teams Webhooks called pymsteams would need to be used
<br>

#### Install 
```bash
pip install -r requirements.txt
```


##### Useful links:
* [send-message-cards-with-microsoft-teams/](https://www.lee-ford.co.uk/send-message-cards-with-microsoft-teams/)
* [pymsteams](https://pypi.org/project/pymsteams/)
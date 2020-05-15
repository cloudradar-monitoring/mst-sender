# mst-sender.py 

#### What it is for 

The script sends a notification message in form of a MS Teams Message Card.
<br>
It could be also easily integrated with [nxlog](https://nxlog.co/). 
<br>

It works with Python 2.7 `mst-sender.py` and Python 3.x `mst-sender3.py`.

Notification example received in MS Teams with the `INFO` severity:

![card-sample](https://raw.githubusercontent.com/cloudradar-monitoring/mst-sender/master/sample/card.png)

#### How to create a Webhook url in MS Teams
[Follow this instruction](https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/connectors-using#setting-up-a-custom-incoming-webhook)

#### How to install
##### Windows
* Have a Python installed with python [requests](https://requests.readthedocs.io/en/master/)
* Download `mst-sender` python script along with `mst-sender.cfg.sample`
* Rename `mst-sender.cfg.sample` to `mst-sender.cfg` and paste your MS Teams Web Hook Url into it: `webhook_url = `
* Send a test message 

```
# Python 2.7
python mst-sender.py --severity ERROR --message "Test from Windows" --profile production
# Python 3.x
python3 mst-sender3.py --severity ERROR --message "Test from Windows" --profile production
```

##### Linux
* Have a Python installed
* Install python [requests]([requests](https://requests.readthedocs.io/en/master/)) `sudo apt-get install -y python-requests`.
* Pull ms-sender script onto the server 
```
# Python 2.7
wget https://raw.githubusercontent.com/cloudradar-monitoring/mst-sender/master/mst-sender.py -O /usr/local/bin/mst-sender && chmod +x /usr/local/bin/mst-sender
# Python 3.x
wget https://raw.githubusercontent.com/cloudradar-monitoring/mst-sender/master/mst-sender3.py -O /usr/local/bin/mst-sender && chmod +x /usr/local/bin/mst-sender
```
* Pull the configuration file onto the server `mkdir /etc/mst-sender`/ and then `wget https://raw.githubusercontent.com/cloudradar-monitoring/mst-sender/master/mst-sender.cfg.sample -O /etc/mst-sender/mst-sender.cfg`
* Enter your MS Teams Web Hook Url in `mst-sender.cfg` as `webhook_url = ` in the `[production]` profile. 
* Send a test message

```
# Python 2.7
python /usr/local/bin/mst-sender --message "Test from Linux" --profile production --config /etc/mst-sender
# Python 3.x
python3 /usr/local/bin/mst-sender3 --message "Test from Linux" --profile production --config /etc/mst-sender
```

#### General usage

#### Configuration - mst-sender.cfg

```bash
[default]
# Enter your web hook url created on MS Teams
webhook_url = https://outlook.office.com/webhook/<YOUR_TOKEN>

# Specify a severity, can be overridden by '--severity'
# The severity determines the color of the message.
# ERROR, WARNING or INFO
severity = ERROR

# Optionally specify who should appear as sender.
# If not given, the local hostname is used.
# Can be overridden by --sender
sender = My server

# You can append any facts to the message. Optional.
# Format fact.FACT_NAME ie. fact.Project Name = Your Project Name fact becomes 'Project Name: Your Project Name'
fact.Env = Staging
fact.Project Name = Your Project Name
```

#### Command line options:
* `--profile` - the profile you plan to use in `mst-sender.cfg` ie `--profile production`
* `--sender`  - a notification sender, to determine who should appear as a sender 
* `--message` - a message which is posted to MS Teams
* `--title`   - a card message title 
* `--severity` - the notification severity (INFO, ERROR, WARNING)
* `--config` - a directory where `mst-sender.cfg` sits (a current working directory of the script used as a fallback)

Examples:

```
# Send a test message with a severity of ERROR using [production] profile from mst-sender.cfg
python /usr/local/bin/mst-sender --severity ERROR --message "Test from ubuntu" --profile production --config /etc/mst-sender

# Send a test message with a severity of INFO using [default] profile from mst-sender.cfg
python /usr/local/bin/mst-sender --severity INFO --message "Test from ubunt" --config /etc/mst-sender

# Send a test message with a severity of WARNING using [default] profile from mst-sender.cfg
# as a message sender Developer is used; the card title reads I AM A NEW TITLE
python3 C:\\mst-sender\\mst-sender3.py --severity WARNING --message "Test from Windows - Python3" --config C:\\mst-sender --sender Developer --title "I AM A NEW TITLE"
```

# Integrate mst-sender with NX Log
 
#### Windows 

* Install and configure `mst-sender` (see above for instruction)
* Download and install nxlog-ce (or Enterprise edition) [download](https://nxlog.co/products/nxlog-community-edition/download)
* Edit your nxlog configuration file found in `C:\Program Files (x86)\nxlog\conf` (or `C:\Program Files\nxlog\conf`) and add the following code (assuming `--profile` is `[default]`):

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
            exec_async("C:\\Python27\\python.exe", "D:\\mst-sender\\mst-sender.py", "--severity", "ERROR", "--message", $raw_event);
        }
        if $raw_event =~ /(\S+)\ (.+) \[WARNING (.+)/
        {
            exec_async("C:\\Python27\\python.exe", "D:\\mst-sender\\mst-sender.py", "--severity", "WARNING", "--message", $raw_event);
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
C:\\Python27\\python.exe (C:\\Python36\\python.exe) - path to your python installation
D:\\mst-sender\\test\\test.log - log file being monitored by nxlog
D:\\mst-sender\\mst-sender.py - path to mst-sender.py or mst-sender3.py
```

* Restart `nxlog` service
* Verify if it works; add a couple of ERROR, WARNING lines in `test.log`. You should get notifications in MS Teams

#### Linux (Ubuntu)
* Install and configure `mst-sender` (see above for instruction)
* Download nxlog [download](https://nxlog.co/products/nxlog-community-edition/download)
* Transfer the file to the target server scp or a similar secure method 
* Install nxlog packadges ie. `sudo dpkg -i nxlog-ce_2.10.2150_ubuntu_xenial_amd64.deb` [nxlog installation manual](https://nxlog.co/documentation/nxlog-user-guide/deploy_debian.html)
* Verify the installation works `nxlog -v`
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
            exec_async("/usr/bin/python", "/usr/local/bin/mst-sender", "--severity", "ERROR", "--message", $raw_event, "--config", "/etc/mst-sender/", "--profile", "production");
        }
        if $raw_event =~ /(\S+)\ (.+) \[WARNING (.+)/
        {
            exec_async("/usr/bin/python", "/usr/local/bin/mst-sender", "--severity", "WARNING", "--message", $raw_event, "--config", "/etc/mst-sender/", "--profile", "production");
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
* Verify if it works; append a couple of ERROR, WARNING lines in `test.log`. You should get notifications in MS Teams ie.
```
echo "01/May/2020:20:55:33 +0000 [WARNING 0 /hub.cloudradar.php] PHP message: PHP Notice:  Indirect 2 modification of overloaded element of Silex\Application has no effect in /var/www/hub/src/app.php on line 96" >> test.log
echo "01/May/2020:20:55:33 +0000 [ERROR 0 /hub.cloudradar.php] PHP message: PHP Notice:  Indirect 2 modification of overloaded element of Silex\Application has no effect in /var/www/hub/src/app.php on line 96" >> test.log
```


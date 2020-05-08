# mst-sender `sender.py`

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
# mst-sender
We use the Python Wrapper Library to send requests to Microsoft Teams Webhooks called pymsteams
<br>
[pymsteams](https://pypi.org/project/pymsteams/)

#### Install 
```bash
pip install -r requirements.txt
```

#### Config file 


```bash
define ACTION { log_info("event found:"); log_info($raw_event); drop();}

<Extension _exec>
    Module  xm_exec
</Extension>

<Input in>
    Module  im_file
    File    "D:\\mst-sender\\test.log"
        <Exec>
        if $raw_event =~ /(\S+)\ (.+) \[ERROR (.+)/
        {
				exec_async("C:\\Python36\\python.exe", "D:\\mst-sender\\sender.py", $raw_event, "Error in raw_event found");
				%ACTION%
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
exec_async("C:\\Python36\\python.exe", "D:\\mst-sender\\sender.py", $raw_event, "Error in raw_event found");
```

where:
* `$raw_event` is the actual log line which matches the regex
* `Error in raw_event found` is the title of the message card




# sshkeyupdate
Insert or Remove SSH Keys from Remote Servers

## IP Range
Simply run the script with an IP range

```
python updatekeys.py 192.168.1.50 192.168.2.120
```

This will run the script within the IP range, inclusively.
If you want to run (or test?) only on a single IP, simply write the IP address twice.

```
python updatekeys.py 192.168.1.50 192.168.1.50
```

## Config File

All of the settings are read from the **config** file. First copy the example file and edit it.

```
cp config.example config
```

This file has three sections.

### [connect]

The **connect** section specifies simple connection settings. Here choose the Private Key path to use, and the password it is encrypted with. Probably all other options are default.
The **authfile** and **authfile2** values are the path of the **authorized keys** files in the remote server to look for. It is usually the root user we want to change it is set like that.

### [insert] and [delete]

The **insert** and **delete** sections are where you specify what keys to insert or delete. The field name is for ease of use, you need to specify one, but it is not relevant. The value is used in the "sed" line at the remote server, to use the full line for the insert lines. Yet you do not have to specify the full key in the delete section, only part of the key will be enough. Just make sure that part is not a common one.

Please note that for ease of explanation, my public key is in the insert section by default, delete that line before proceeding.

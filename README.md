# sshkeyupdate
Insert or Remove SSH Keys from Remote Servers

## Usage
Simply run the script with an IP range

```
python updatekeys.py 192.168.1.100 192.168.1.100
```

This will run the script within the IP range, inclusively.
All of the settings are read from the **config** file. This file has three sections.

The **connect** section specified simple connection settings. Here choose the Private Key path to use, and the password it is encrypted with. Probably all other options are default.

The **insert** and **delete sections are where you specify what keys to insert or delete. The field name is for ease of use, you need to specify one, but it is not relevant. The value is used in the "sed" line at the remote server, to use the full line for the insert lines. Yet you do not have to specify the full key in the delete section, only part of the key will be enough. Just make sure that part is not a common one.

Please note that for ease of explanation, my public key is in the insert section by default, delete that line before proceeding.

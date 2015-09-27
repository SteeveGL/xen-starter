# xen-starter

1.
Add a tag named "Auto start" to a VM to auto start the VM.

If you wish, you could named it diferantly. Just don't forget to change the variable in the xen-starter.py file:
<code>
tagAutostart = "Auto start"
</code>

2.
On the VM host, edit the crontab with <code>crontab -e</code> and add this line: <code>@reboot /root/xs_autostart.py</code>

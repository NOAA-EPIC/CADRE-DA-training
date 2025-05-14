# da-training

## Connecting to an HPC Environment via SSH

A Secure SHell (SSH) tunnel creates an encrypted connection between two computer systems. This secure connection allows users to access and use a remote system via the command line on their local machine. SSH connections can also be used to transfer data securely between two systems. Many HPC platforms, including NOAA systems and commercial cloud systems (e.g., AWS, Azure), are accessed via SSH from a user’s computer.

### Instructions for Mac Users

#### Create a Public/Private Key Pair

Open the MacOS terminal application





Generate a public/private key pair on your local laptop by issuing the following command in your terminal window: 

```
ssh-keygen -t ed25519 -f /Users/<username>/.ssh/id_ed25519_student{1-30} 
```

where `{1-30}` is replaced with your assigned number. 

When prompted for a passphrase, press return/enter twice and leave blank

This should generate a public/private key pair in the user’s home `.ssh` directory

Use a text editor of your choice to view the public key file (e.g., vim).

For example:
```
vim /Users/<username>/.ssh/id_ed25519_student(n).pub
```
(when using vim, press `:q` to quit the editor)

Copy and paste the contents of the public key to the workshop administrator via the Slack workspace channel `#publickeys` and inform them of which student number you were assigned (i.e., student 5).  

NOTE: There will be 2 keys generated, a public and a private key. DO NOT SEND THE PRIVATE KEY! A public key (the correct one) will look like this: 

```
ssh-ed25519 AAAA3N
```

And a private key will look like this…

```
-----BEGIN OPENSSH PRIVATE KEY-----
AAAAAAAAABAAAA
11111111==
-----END OPENSSH PRIVATE KEY-----
```

The workshop administrators will add the public key to the authorization file on the bastion host, which will allow you to login.









#### Connecting to HPC Environment via MacOS 

Next, add the newly generated key to your laptop’s identity by issuing the command: 

```
ssh-add /User/<username>/.ssh/id_ed25519_student(n)
```

where `(n)` is replaced by your assigned student number. 

If successful, you should see a message similar to the following:

```
Identity added: /Users/<username>/.ssh/id_ed25519_student5 (username@MacBook-Pro.local)
```

Now you may access the HPC environment through the bastion host proxy by issuing the command below in the terminal (again replacing `(n)` with your assigned student number): 

```
ssh student(n)@137.75.93.46
```

You should be automatically redirected through the bastion proxy to the controller node of your HPC environment. If you run the `ls` command, you will see the Land DA container (.img) file, the inputs data directory, and a rocoto directory.  






### Instructions for Windows Users


# da-training


## Connecting to an HPC Environment via SSH

A Secure SHell (SSH) tunnel creates an encrypted connection between two computer systems. This secure connection allows users to access and use a remote system via the command line on their local machine. SSH connections can also be used to transfer data securely between two systems. Many HPC platforms, including NOAA systems and commercial cloud systems (e.g., AWS, Azure), are accessed via SSH from a user’s computer.

### Instructions for Mac Users

Open the MacOS terminal application and type the following commands to generate a public/private key pair on your local system: 

```
ssh-keygen -t ed25519 -f /Users/<username>/.ssh/id_ed25519_student{1-30} 
```

where `username` is replaced with your actual username, and `{1-30}` is replaced with your assigned number. 

The output from the command should look like the following lines except that username is replaced with your username:

```
Generating public/private ed25519 key pair.
Enter passphrase for "/Users/gpetro/.ssh/id_ed25519_student3" (empty for no passphrase): 
Enter same passphrase again:
```

When prompted for a passphrase, press return/enter twice and leave blank. 
This should generate a public/private key pair in the user's home `.ssh` directory.

```
Your identification has been saved in /Users/gpetro/.ssh/id_ed25519_student3
Your public key has been saved in /Users/gpetro/.ssh/id_ed25519_student3.pub
The key fingerprint is:
SHA256:GhEIm283dy9n5vAzdkaPfQ3g7z5C6wLOIRFzF8wYYjo gpetro@gpetro-MacBook-Pro
The key's randomart image is:
+--[ED25519 256]--+
|      o....o...  |
|      o=. +..o   |
|      += . .E    |
|      .o     . . |
|      ..S o = = +|
|      .+0. +.o = |
|      .+ o ...O .|
|        o .ooo.* |
|         ..+=+o..|
+----[SHA256]-----+
```


Use a text editor of your choice to view the public key file in the user's home `.ssh` directory (e.g., vim).

For example:
```
vim /Users/<username>/.ssh/id_ed25519_student(n).pub
```
(when using vim, press `:q` to quit the editor)

Copy and paste the contents of the public key to the workshop administrator via the Slack workspace channel `#publickeys` and inform them of which student number you were assigned (i.e., student 5).  

NOTE: There will be 2 keys generated, a public and a private key. DO NOT SEND THE PRIVATE KEY! A public key (the correct one) will end in `.pub` and will start like this: 

```
ssh-ed25519 AAAA3N
```

A private key will look like this:

```
-----BEGIN OPENSSH PRIVATE KEY-----
AAAAAAAAABAAAA
11111111==
-----END OPENSSH PRIVATE KEY-----
```

The workshop administrators will add the **public** key to the authorization file on the bastion host, which will allow you to log in.

Next, add the newly generated key to your laptop’s identity by issuing the command: 

```
ssh-add /User/<username>/.ssh/id_ed25519_student(n)
```

where `username` is replaced with your actual username, and `(n)` is replaced by your assigned student number. 

If successful, you should see a message similar to the following:

```
Identity added: /Users/<username>/.ssh/id_ed25519_student5 (username@MacBook-Pro.local)
```

Now you may access the HPC environment through the bastion host proxy by issuing the command below in the terminal (again replacing `(n)` with your assigned student number): 

```
ssh student(n)@137.75.93.46
```

You should be automatically redirected through the bastion proxy to the controller node of your HPC environment. If you run the `ls` command, you will see the Land DA container (`.img`) file, the `inputs` data directory, and a `rocoto` directory.  


### Instructions for Windows Users

Open the PowerShell or Command Prompt application and run the following command in a PowerShell or Command Prompt window:
```
ssh-keygen -t ecdsa
```

The output from the command should look like the following lines except that username is replaced with your username:
```
Generating public/private ecdsa key pair.
Enter file in which to save the key (C:\Users\username/.ssh/id_ecdsa):
To accept the default file path, select Enter ; otherwise, specify a path or file name for your generated keys.
```

Next, you will be prompted to use a passphrase to encrypt your private key files. Leave the passphrase empty by pressing `Enter` twice:
```
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in C:\Users\username/.ssh/id_ecdsa.
Your public key has been saved in C:\Users\username/.ssh/id_ecdsa.pub.
```

This should generate a public/private key pair in the directory you selected (default or other).
```
The key fingerprint is:
SHA256:OIzc1yE7joL2Bzy8!gS0j8eGK7bYaH1FmF3sDuMeSj8 username@LOCAL-HOSTNAME

The key's randomart image is:
+--[ECDSA 256]--+
|        .        |
|         o       |
|    . + + .      |
|   o B * = .     |
|   o= S B .      |
|   .=B O o       |
|  + =+% o        |
| *oo.O.E         |
|+.o+=o. .        |
+----[SHA256]-----+ 
```
Now you have a public/private ECDSA key pair in the specified location. The `.pub` file is the public key, and the file without an extension is the private key.
Use a text editor of your choice to view the public key file or view it in the command line:
```
type /Users/<username>/.ssh/id_ed25519_student(n).pub
```

Copy-paste the public key contents to the workshop administrator via the Slack workspace channel `#publickeys` and inform them of your student number (i.e., student 5).
NOTE: Two (2) keys are generated: a public and a private key. DO NOT SEND THE PRIVATE KEY! 
A public key will end in `.pub` and will start something like this: 
```
ecdsa-sha2-nistp256 AAAAA
```

And a private key will look like this: 
```
-----BEGIN OPENSSH PRIVATE KEY-----
AAAAAAAAABAAAA
11111111==
-----END OPENSSH PRIVATE KEY-----
```

Workshop administrators will add the public key to the authorization file on the bastion host, which will allow you to log in.

Ensure that the Windows SSH client (OpenSSH) is installed and configured. Information on how to perform this task can be found here: 
https://learn.microsoft.com/en-us/windows/terminal/tutorials/ssh

Access the HPC environment using Windows Powershell or Command Prompt through the bastion host proxy by issuing the command below: 
```
ssh -i C:\Users\<User>/.ssh/id_ecdsa student(n)@137.75.93.46
```
where `C:\Users\<User>/.ssh/` is replaced with the path to the `id_ecdsa` file on the user’s system.

NOTE: This will only work during the training when the HPC system is active for the training! 

The user may see a message asking whether the user wants to continue connecting. 
Verify that you are connecting to the correct system and enter `yes` to continue.

This should automatically redirect users through the bastion proxy to the controller node of their HPC environment. 
If you run the `ls` command, you will see the Land DA container (`.img`) file, the `inputs` data directory, and a `rocoto` directory: 

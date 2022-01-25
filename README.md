# Flask-User-Blogging-Website
Flask Multi User Blogging Website. Multiple Users can log in, add posts, delete posts, view others profile, add pictures, etc

You can check out the website here: 
https://multiuserblogapp.herokuapp.com/

The hosted version has certain limitations such as blocking of email server, resetting of database files on server to originally committed files, etc.

In order to view the website's complete range and functionality, you can host this website on your local computer in the following manner:

--> First open your bash/cmd/shell

--> To clone use:
```
git clone -b master https://github.com/Vashesh08/Flask-User-Blogging-Website.git
```

--> To run the app,go into the cloned repository 
```
cd Flask-User-Blogging-Website
```

--> Now run the following commands:

--> To activate virtual environment, run the commands on your shell:
```
cd Scripts
activate
cd ..
```

--> The dependencies and modules required for this website are mentioned in the requirements.txt file
--> To install all the dependencies, run the command on your shell:
```
pip3 install -r requirements.txt
```

--> To run the file 
```
python3 app.py
```

The app will now run on your local host. 
http://127.0.0.1:5000/

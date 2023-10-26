# pennycas

--------------

To run this application locally using the Flask test HTTP server:

Issue these commands:

# Create an APP_SECRET_KEY environment variable
export APP_SECRET_KEY=<somesecretkey>

# Run the test server
python runserver.py <someport>

On a Mac or Linux computer it would be common to place the export
command in the .bashrc file.

---------------

To run this application on Render:

(1) Deploy the application to Render as usual.

(2) Configure the application such that it has an environment variable
whose name is APP_SECRET_KEY and whose value is some secret key.


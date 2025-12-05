# apollo_superday_2025

*******REQUIRED INSTALLATIONS*******

This implementation requires SQLAlchemy and FastAPI. They can be downloaded with:

pip install SQLAlchemy

pip install "fastapi[standard]"

*******FILE INFORMATION*******

There are 4 python files in this implementation: main.py, model.py, and session.py,
tests.py.

main.py contains code for the app created by FastAPI, including functions for: 
- get all
- get by id
- post (add to database)
- update by id
- delete by id
- input error checking and handling

model.py contains the Vehicles model used in the database, created with SQLAlchemy

session.py contains code for starting a SQLAlchemy session, since this implementation
uses SQLAlchemy ORM. 

tests.py contains unit tests for the functions in main.py. NOTE: unit tests
are not complete. Additional unit test should be added to check edge cases
and all functionalities

The file vehicles.db contains the vehicle database.

*******RUNNING THE APP*******

The app can be started by running:

fastapi dev main.py

at the command line. The output will give hostname for both the server and the
documentation. Queries can by either adding the appropriate URI to the end of
the server hostname, or using the interactive API found at the documentation
hostname.
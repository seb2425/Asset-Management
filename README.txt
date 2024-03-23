****SETUP for WINDOWS*****
PYTHON ENVIRONMENT/PACKAGES
1.We may choose to run the app in a virtual environment(venv).To do so write py -3 -m venv <name> and this will create
a new virtual environment for our app.We also to to specify the python.exe in \envname\Scripts\python.exe as the Interpreter,
In vscode we can do it from command palette.
2.We also have to make our terminal use this virtual env. to do so we just have to run the activate.bat file in Scripts folder.
to do so write \venvname\Scripts\activate.bat in the terminal and run it. 

3.Then we have to install all the dependencies mentioned in requirements.txt. These are packages written by other people which is used in the project. We can do 
pip install fatapi[all] in the terminal, this will install most of the required dependencies and then manually do pip install for anything left.

MONGODB
1.We need 3 things mongod,mongosh(mongo shell) and Compass(UI). Earlier the shell used to come preinstalled with mongod but now we have to install
them seperately.We can install them from https://www.mongodb.com/try/download
we must add them to the system path variables if not added already. In windows we can go to System properties >> Advanced >> Edit environment variables
Then select path and add the location of the installed software to the path.

Also the .exe for python also has to be added to path

we can see if everything is installed and working by checking mongod --version, mongosh --version


**USING THE BACKEND****
To start the app fo the folder where main.py is in the terminal and enter uvicorn main:app --reload.this will start the webapp and the 
localhost address will be given. We can go the address and  add a "/docs" at the end. the url will be "http://127.0.0.1:8000/docs". This will open swaggerUI which will act as a frontend
for making requests. WE can also use POSTMAN but that has to be installed seperately. swaggerUI is easier and also provides example schemas for requests


**AUTHORIZATION****
i have used jwt for authorization.
Currently authorization is added only for making posts. we can add authorization to any other request just by adding "dependencies=[Depends(jwtBearer())]"
to the route parameters. With authorization i can do the request only when i am authorized.
How to authorize?
1.First we need to signup with name,email and a password.
2.Then we login with valid id and pass. This will return a hashed token value based on the algorithm and secret in the .env file.
To autorize we can click on the authorize button in swaggerUI and enter token value that we get after signing up or loggin in.
We are now authorized(the lock icon in swaggerUI is closed) and can make post.


**CODE HIGH LEVEL EXPLANATION****
We use three databases. database1 is for asset details, database2 is for users and database3 is for asset performance. The main.py works with these 
3 databases and does CRUD operations as required. All the databse schema are in model.py. For authorization we have a jwthandler.py and 
jwt_bearer.py. The jwt_handler has 3 functions to encode,decode and return signed JWTs. The jwt_beearer.py file authenticates and authorizes 
any requests made to the web application.


**ENDPOINT DOCUMENTATION*********
ASSET SECTION
1.GET
/asset
Read
Used to get all the assets in the database. The request body is empty. just send the request .

2.POST
/asset
Casset
Used to post a new asset in the database. Follows the Asset schema in model.py.This endpoint is a secured endpoint so authorize properly before executing this request(Authorization steps are in authorization section)
.Enter values in the request according to the schema and then execute.


3.GET
/asset/{id}
Get One Asset
Used to fetch only one single asset from the database. In the request url enter the id at the end and then execute.Request body is empty

4.PUT
/asset/{id}
Upd
Update one single asset in the database, updates the databse with specified id in the route path. Request body has two parameters attribute
and new_value .changes the attribute of the asset to new_value

DELETE
/asset/{id}
Del Asset
5.Used to delete an asset by it's id.In the request url enter the id at the end and then execute.Request body is empty

/******************************************************************************************************/
USER SECTION
1.POST
/user/signup
Singup
Creates a new user following the Signup schema, stores the new user into database. go to the url and in the request body fill the request body with a valid Signup schema
and then execute

2.POST
/user/login
LoginTo be used for login by registered users, returns the hashed token value on succesful login. Uses the login schema in model.to make a request fill the request body with a 
valid login schema and execute.

/******************************************************************************************************/
ASSET PERFORMANCE SECTION
1.GET
/asset/perform/all
Get Perm
Used to fetch performance of all assets. has empty request body. go to the url and execute

2.GET
/asset/perform/{id}
Get One Perm
Used to fetch performance of one asset. has empty request body.Add the id of the asset to be fetched at the end of url and execute ,has empty request body

2.POST
/asset/perform/
Create Perm
Used to post a asset performance. follows the AssetPerformance schema in model.py . to make a post request go to the url and fill the body with a valid 
AssetPerformance schema and execute.

3.PUT
/asset/performance/{id}
Update Perm
Used to update a asset performance with the id.has empty request body.

4.DELETE
/asset/performance/{id}
Del Perm
Used to delete an asset performance with the id.has empty request body.

/********************************************************************************************************************************************************/
ASSET PERFORMANCE FUNCTIONS
this section has some functions that are directly accessible from the front-end.The functions are for getting average downtime of assets,fetching total maintainence cost of assets
and to find out high failure rate assets. requests made to these endpoints will return appropriate data.

1.GET
/asset/downtime/avg
Get Avg D
Used to find the average downtime of all assets currently present in the database. has empty request body

2.GET
/asset/maintainence/total
Total Maintainence Cost
Used to find the total maintencne cost of all assets currently present in the database. has empty request body

3.GET
/asset/failure/highest
Highest Failure
Used to find the asset with highest failure rate.has empty request body.


4.GET
/asset/failure/high/{threshold}
High Fail Rates
This is another failure rate function that returns all assets with a failure rate abve a certain threshold. pass the threshold number in the request url and execute 
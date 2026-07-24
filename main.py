from fastapi import FastAPI , Depends , HTTPException

from sqlalchemy.orm import Session

from database import engine, SessionLocal, get_db
# update code


from models import Base, HospitalStaff
# update code, as Employee contains the complete table structure defined in
# FastAPI will get to know which tables to create

from schemas import HospitalStaff as HospitalStaffSchema
#update code
# here we have used aliases, as Hospitalstaff already exists

from schemas import LoginSchema

from jose import jwt

SECRET_KEY = "mysecretkey"
# secret key is used to create and verify JWT tokens
# "mysecretkey" is the secret password  used to sign and verify JWT tokens.

ALGORITHM = "HS256"
# a method used to encrypt/ sign the token

from passlib.context import CryptContext


app = FastAPI()

Base.metadata.create_all(bind = engine)
# Base contains the tables, metadata stores table information, create_all creates the tables,
# and bind = engine connects them with the database


# write a function to create a JWT token
def create_token(data: dict):
    # data: dict means input data should be in dictionary format

    token = jwt.encode(
    # encode the data into a JWT token

        data,
        # payload data to be stored inside the token

        SECRET_KEY,
        # secret key used to sign and verify the token

        algorithm= ALGORITHM
        # alogorithm used for encrytion/signing (e.g., HS256)
    )

    return token
# return the generated JWT token
# this function converts user data into a secure JWT token using a secret key and encryption alogorithm



# here, we are using bcrypt algorithm
pwd_context = CryptContext(
    schemes= ["bcrypt"],
    # use bcrypt algorithm for hashing passwords

    deprecated = "auto"
    # automatically mark older password hashing methods as outdated and upgrade them when needed
)
# CryptContext is configured to hash and verify passwords secirely using the bcrypt algorithm

# create a function named hash_password that accepts a password as input 
def hash_password(password):

    return pwd_context.hash(password)
# use pwd_context to hash the password

# verify password function
def verify_password(plain_password, hashed_password):

# as per users enters, password as abc123, but in the db we have its hashed from $2b$12$XkPz
# here, we can not do, plain_password == hashed_password, as abc123 != $2b$12$XkPz
    return pwd_context.verify(plain_password, hashed_password)


@app.get("/")
def home():

    return{"message": "Database Connected Successfully"}

# create databse session
session = SessionLocal()



# insert data using POST
@app.post("/hospitalstaff/{id}/{username}/{password}/{role}/{department}")
# placeholder means a temporary space reserved for dynamic values, coming from Postman / Swagger
def add_hospitalstaff(id: int, username: str, password: str, role: str, department: str):
    # the data coming from the API route should follow these datatypes
    
    hospitalstaff = HospitalStaff(id = id, username = username, password = password, role = role, department = department)
    # creates hospitalstaff record, left side is the table columns name, right side is the values coming from API endpoint
    
    session.add(hospitalstaff)
    # adds data temporarily

    session.commit()
    # saves data permanently into PostgreSQL

    return {"message": "Hospitalstaff Added Successfully"}
# confirmation message

# fetch data using GET
@app.get("/hospitalstaff")
def get_hospitalstaff():

    hospitalstaff = session.query(HospitalStaff).all()
    #fetch data from Hospitalstaff table, where all means fetch all rows

    return hospitalstaff


# APIs using pydantic model
# Pydantic Model for Login and register 

@app.post("/register_staff")

def add_hospitalstaff(stf: HospitalStaffSchema):
    # staff must follow the structure defined in HospitalStaffSchema
    # i.e. it accepts JSON data and validate it using Pydantic model

    hospitalstaff = HospitalStaff(id = stf.id, username = stf.username, password = stf.password, role = stf.role, department = stf.department)   
     # access Hospitalstaff table, find hospitalstaff whose ID matches, and return first matching row

    session.add(hospitalstaff)

    session.commit()

    return{"message": " Hospitalstaff Registered Successfully Using Pydentic Model"}

# get api

@app.get("/hospitalstaff")

def get_hospitalstaff():
   
    hospitalstaff = session.query(HospitalStaff).all()
    
    return hospitalstaff


# Create a login endpoint
@app.post("/login")

# function to register a new user
def login_user(user: LoginSchema, db = Depends(get_db)):
    # to check existing user

   existing_user =  db.query(HospitalStaff).filter(HospitalStaff.username == user.username).first()

    # verify user
   if existing_user is None:
    #use exception handling
        raise HTTPException(status_code=404, detail="User not found")

# if user exists, then verify password
   if existing_user.password != user.password :
        raise HTTPException(
            status_code=401,
            detail="Incorrect Password"
        )

   return {"message": "Login Successful"}
# return response

# create login endpoint -- jwt token implementation
@app.post("/login_jwt")

# function to register a new user
def login_user(user: LoginSchema, db= Depends(get_db)):
    # to check existing user
    existing_user = db.query(HospitalStaff).filter(HospitalStaff.username == user.username).first()

    # verify user
    if existing_user is None:
        # use exception handling
        raise HTTPException(status_code= 404, detail = "User not found")

    # if user exists, then verify password
    if existing_user.password != user.password:
        # use exception handling
        raise HTTPException(status_code=401, detail = "Incorrect Password")

    token = create_token({"username":user.username})

# create a JWT token and store the username inside the token payload
# the username is stored in the token so that user does not need to login for every request

    return {"access_token": token}            
# return the generated token to the user after successful login

 # modify registeration API
@app.post("/register_hashed")

# function to register a new user 
def register_user(user: HospitalStaffSchema, db: Session = Depends(get_db)):
    #to check for existing user
    existing_user = db.query(HospitalStaff).filter(HospitalStaff.username == user.username).first()

    if existing_user:
        # use exception handling
        raise HTTPException( status_code= 400, detail = "Username already exists")
    
    # if user does not exist, then create user object
    new_user = HospitalStaff(id = user.id, username = user.username, password = hash_password(user.password), role = user.role, department = user.department)

    # save user
    db.add(new_user)

    db.commit()

    # return response
    return {"message": "Staff Registered Successfully"}

# modify login API to verify hashed password
@app.post("/login_hashed")

# function to authenticate a user during login
def login_user(user: LoginSchema, db = Depends(get_db)):

    # tocheck existing user
    existing_user = db.query(HospitalStaff).filter(HospitalStaff.username == user.username).first()

    # verify user
    if existing_user is None:
        # use exception handling
        raise HTTPException(status_code= 404, detail = "User not found")
    
    # If user existd, then verify password
    if not verify_password(user.password, existing_user.password):
        # does this password generate the same hash, if yes then password id correct
        # user exception handling, if it is not correct
        raise HTTPException(status_code = 401, detail = "Incorrect Password")
    
    token = create_token({"username": user.username})
    # create a JWT token and store the username inside thr token inside the token payload
    # the username is stored in the token so the user does not need to log in for every request

    return{"access_token":token}

# Pagination
# GET with Pagination
@app.get("/hospitalstaff_pagination")

def get_hospitalstaff(skip: int = 0, limit: int = 5, db = Depends(get_db)):
    # do not skip any records and return 5 records, and here we are setting it as default

    # is acceptable, but we will write it in a better way as follows using line continuation character \
    
    hospitalstaff = db.query(HospitalStaff)\
                  .order_by(HospitalStaff.id)\
                  .offset(skip)\
                  .limit(limit)\
                  .all()

    return hospitalstaff


# Search by username
@app.get("/hospitalstaff_s/search")

def search_hospitalstaff(username: str, db = Depends(get_db)):
    # name: str, is our query parameter received from URL

    hospitalstaff = db.query(HospitalStaff).filter(HospitalStaff.username == username).all()
    # HospitalStaff.name == name, search employee whose name matches input

    return hospitalstaff

# Filter by Department, and its explanation will remain same as earlier
@app.get("/hospitalstaff_f/filter")

def filter_hospitalstaff(department: str, db = Depends(get_db)):

    hospitalstaff = db.query(HospitalStaff).filter(HospitalStaff.department == department).all()

    return hospitalstaff


# create a higher function
def check_role(username: str, db = Depends(get_db)):
    # function to retrieve the role of a user from the database

    role = db.query(HospitalStaff).filter(HospitalStaff.username == username).first()
    # search the Role table for the given username
    # return the first matching record

    return role
# return the user's role information

# create an endpoint and a route to delete roles from the database based on role
# suppose only: Admin can delete roles

@app.delete("/delete_role_rb/{id}")

# function to delete a role
def delete_role(id: int, username: str, db = Depends(get_db)):
# function to delete a role after verifing the user's role
# for now: we manually pass username to identify who is making the request
# later JWT will do this automatically

# get user role
    user_role = check_role(username, db)

    # verify role
    if user_role.role != "Director":
        # deny access if the user is not an admin

        raise HTTPException(status_code = 403, detail = "Access Denied")
    
    # if user is admin then proceed, and search for the role record to be delete
    existing_role = db.query(HospitalStaff).filter(HospitalStaff.id == id).first()

    if existing_role is None:
# check if the role does not exist
        raise HTTPException(status_code = 404, detail = "Role Not Found")
    
    # if exists then delete
    db.delete(existing_role)

    # save changes
    db.commit()

    return{"message": "Role Deleted Successfully"}



# create an endpoint and route to assign roles
# and, suppose only admins can assign roles
@app.post("/assign_role_rb")

def assign_role(role_data: HospitalStaffSchema, username: str, db = Depends(get_db)):
# function to assign role after verifying the user's role
# for now: we manually pass username to identify who is making the request:
# later JWT will do this automatically

# get user role
    user_role = check_role(username, db)

# verify role
    if user_role.role != "Director":
    # deny access of the user is not an admin
        raise HTTPException(status_code= 403, detail="Access Denied")

# if user is admin than proceed and create a new role record
    new_role = HospitalStaff(id = role_data.id, username = role_data.username, password = role_data.password, role = role_data.role, department = role_data.department)

    db.add(new_role)
# add role to database session

    db.commit()
# save changes

    return{"message": "Role assigned Successfully"}


@app.put("/update_role_rb/{id}")

# function to update a role, note here we did not used any UpdateSchema, we are using RoleSchema
def update_role(id: int, role_data: HospitalStaffSchema, username: str, db = Depends(get_db)):
    # function to update a role after verifying the user's role
    # for now: we manually pass username to identify who is making the request
    # later JWT will do this automatically


    # get role
    user_role = check_role(username, db)

    # verify role
    if user_role.role != "Director":
    # deny access of the user is not an admin
        raise HTTPException(status_code= 403, detail="Access Denied")

# if user is admin than proceed and search for the role record to be  updated
    existing_role = db.query(HospitalStaff).filter(HospitalStaff.id == id).first()
    # exception handling
    if existing_role is None:
# check if role does not exist
        raise HTTPException(status_code = 404, detail = "Role Not Found")
    
    # if exists then update
    existing_role.username = role_data.username
    existing_role.role = role_data.role

    # save changes
    db.commit()

    # return response
    return {"message": "Role Updated Successfully"}
# returning message

# fastapi_run_python_script_from_path_url
Fastapi app to run python script sent by path url
Smart file inclusion implementation

Overview of Request Flow
1.	Check for rate limit
2.	Authenticate
3.	Sanitize
4.	Slugify
5.	Search for file
6.	Execute file, if present. If not, raise an exception.
7.	Return result of file as response.

Create virtual env  and activate:
python -m venv venv
venv\scripts\activate
Install requirements:
pip install -r req.txt

Build and run redis container
docker-compose up -d --build

 
Run main app:
python main.py













Test with postman:
GET http://localhost:8000/authenticated_sanitized_magic/first
 

http://localhost:8000/authenticated_sanitized_magic/second

 




Basic flow of the code:
1.	Each request will be checked for rate limiting. If client send passes limit an exception with http status code 429 will be send back.
 
2.	Each request will be required to authenticate. If client did not provided a valid Bearer Token, an errod with http status code 403 will returned
 

3.	If token is provided, token will be verified. If token is invalid 401 will be returned.
 if not token.credentials == "123456789":        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
            headers={"WWW-Authenticate": token.scheme},
        )

 


4.	If request authenticated. File name will be extracted from the URL as string with file_name variable name.
/authenticated_sanitized_magic/{file_name}
5.	file_name variable will be sanitized
6.	file_name will be slugified (  like “FILE name > “file_name”)
7.	current folder will be searched for “{file_name}.py” file.
8.	If file is found in the current folder, file will be executed and its result will be returned to client
 

9.	If file cannot found. An error message will be send back
 








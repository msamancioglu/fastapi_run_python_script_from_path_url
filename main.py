
from fastapi import FastAPI, Depends, HTTPException, status, Path
from fastapi.security import HTTPBearer
from slugify import slugify
import html
from os.path import isfile
import sys
import subprocess
import aioredis
import uvicorn

from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter


token_auth_scheme = HTTPBearer() 

app = FastAPI()

def authenticated_sanitizer(token: str = Depends(token_auth_scheme), 
                            function_name: str= Path(..., title="Please define filename to include")):
    #check for credentials first
    if not token.credentials == "123456789":        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
            headers={"WWW-Authenticate": token.scheme},
        )
    sanitized_fname = html.escape(function_name)
    slugified_filename = slugify(sanitized_fname, to_lower=True, separator="_")
    slugified_fullname =  f"{slugified_filename}.py"
    
    
    if isfile(slugified_fullname):
        return slugified_fullname     
    else:
        raise HTTPException(status_code=404, 
                            detail= f"{slugified_fullname} not found")
    

@app.get("/authenticated_sanitized_magic/{function_name}/", dependencies=[Depends(RateLimiter(times=2, seconds=5))])
async def public(function_name: str = Depends(authenticated_sanitizer)):    
    result = subprocess.check_output([sys.executable, function_name, "34"])        
    return {
        "file_name": f"{function_name}.py",
        "result":result
    }


@app.on_event("startup")
async def startup():
    redis = await aioredis.from_url("redis://localhost", encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(redis)



if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
        
    
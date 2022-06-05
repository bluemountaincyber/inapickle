from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import sqlite3
from pydantic import BaseModel
import pickle
from starlette.responses import FileResponse

# Initialize Database, if necessary
con = sqlite3.connect('database.sqlite')
cur = con.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS contacts (
               contact_id INTEGER PRIMARY KEY AUTOINCREMENT,
               first_name TEXT NOT NULL,
               last_name TEXT NOT NULL,
               email TEXT NOT NULL UNIQUE,
               phone TEXT NOT NULL UNIQUE
               );""")
con.commit()
con.close()

class CreateItem(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str

class LookupItem(BaseModel):
    first_name: str
    last_name: str

class RestoreItem(BaseModel):
    first_name: str
    last_name: str

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", description="Home page for contacts", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "title": "SEC542 Contacts"})

@app.post("/create-contact", description="Creates a new contact. See POST request body schema for required fields.")
async def create(item: CreateItem):
    con = sqlite3.connect('database.sqlite')
    cur = con.cursor()
    query = "INSERT INTO contacts (first_name, last_name, email, phone) " + "VALUES('" + item.first_name + "', '" + item.last_name + "', '" + item.email + "', '" + item.phone + "');"
    try:
        cur.execute(query)
        con.commit()
    except:
        return "Something went wrong!"
    con.close()
    return "Success"

@app.post("/read-contact", description="Displays a single contact. See POST request body schema for required fields.")
async def read(item: LookupItem):
    con = sqlite3.connect('database.sqlite')
    cur = con.cursor()
    result = cur.execute("SELECT * FROM contacts WHERE first_name = '" + item.first_name + 
        "' AND last_name = '" + item.last_name + "';").fetchall()
    return result

@app.get("/read-all-contacts", description="Displays all contacts.")
async def readall():
    results = []
    con = sqlite3.connect('database.sqlite')
    cur = con.cursor()
    for row in cur.execute("SELECT * FROM contacts;"):
        results.append(row)
    con.close()
    return results

@app.post("/delete-sqlite", description="Deletes entire contact database. USE WITH CAUTION!")
async def delete(item: LookupItem):
    con = sqlite3.connect('database.sqlite')
    cur = con.cursor()
    cur.execute("DELETE FROM contacts WHERE first_name = '" + item.first_name + 
        "' AND last_name = '" + item.last_name + "';").fetchall()
    con.commit()
    con.close()
    return "Success!"

@app.get("/backup-sqlite", description="Creates database backup file to download to system. Note that the file is stored as pickled data and cannot be read.")
async def backup():
    sqlfile = open('database.sqlite', mode = 'rb').read()
    content = pickle.dumps(sqlfile, protocol=0)
    tmpFile = open('/tmp/pickle.pkl', 'wb')
    tmpFile.write(content)
    return FileResponse('/tmp/pickle.pkl', media_type='application/octet-stream',filename='db_backup.pkl')

@app.post("/restore-sqlite", description="Restores database. Requires uploading pickled data previously created using /backup-db.")
async def restore(file: UploadFile = File()):
    contents = await file.read()
    unpickled = pickle.loads(contents)
    if isinstance(unpickled, (bytes, bytearray)):
        sqlfile = open('database.sqlite', mode = 'wb')
        sqlfile.write(unpickled)
        return "Restore successful!"
    else:
        return "Invalid data"

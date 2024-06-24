import grpc
import file_transfer_pb2
import file_transfer_pb2_grpc
from fastapi import FastAPI, UploadFile
from fastapi.responses import HTMLResponse, FileResponse

app = FastAPI()
channel = grpc.insecure_channel("localhost:50051")
stub = file_transfer_pb2_grpc.FileTransferStub(channel)


def upload_file(file_path, filename):
    def file_chunks():
        with open(file_path, "rb") as f:
            while chunk := f.read(1024):
                yield file_transfer_pb2.FileChunk(content=chunk, filename=filename)

    response = stub.Upload(file_chunks())
    print(f"Upload response: {response.message}")

def upload_file_new(f, filename):
    def file_chunks():
        while chunk := f.read(1024):
            yield file_transfer_pb2.FileChunk(content=chunk, filename=filename)

    response = stub.Upload(file_chunks())
    print(f"Upload response: {response.message}")

def list_files(folder):
    request = file_transfer_pb2.ListRequest(folder=folder)
    response = stub.ListFiles(request)
    return response.listOfFiles


def download_file(filename, download_path):
    request = file_transfer_pb2.FileRequest(filename=filename)
    response = stub.Download(request)
    with open(download_path, "wb") as f:
        for chunk in response:
            f.write(chunk.content)
    print(f"File downloaded successfully to {download_path}")



@app.get("/", response_class=HTMLResponse)
async def index():
    with open("index.html") as f:
        return f.read()


@app.get("/styles/{path}")
async def style_file(path):
    return FileResponse(f"styles/{path}")


@app.get("/scripts/{path}")
async def script_file(path):
    return FileResponse(f"scripts/{path}")


@app.get("/list-files")
async def list_files_api():
    response = list_files("")
    return {"list_files": response}


@app.post("/upload")
async def upload_api(file: UploadFile):
    upload_file_new(file, file.filename)
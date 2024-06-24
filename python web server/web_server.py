import grpc
import file_transfer_pb2
import file_transfer_pb2_grpc
from fastapi import FastAPI, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
import json

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
            print("entra")

    print("before")
    response = stub.Upload(file_chunks())
    print("Passou")
    print(f"Upload response: {response.message}")


def list_files(folder):
    request = file_transfer_pb2.ListRequest(folder=folder)
    response = stub.ListFiles(request)
    return list(response.listOfFiles)


def download_file(filename, download_path):
    request = file_transfer_pb2.FileRequest(filename=filename)
    response = stub.Download(request)
    with open(download_path, "wb") as f:
        for chunk in response:
            f.write(chunk.content)
    print(f"File downloaded successfully to {download_path}")


@app.get("/list-files")
async def list_files_api():
    response = list_files("")
    return response


@app.post("/upload")
async def upload_api_new(file: UploadFile):
    upload_file_new(file.file, file.filename)
    # with open(f'uploads/{file.filename}', 'wb') as f:
    #     f.write(file.file.read())
    return "Success"


app.mount("/", StaticFiles(directory="../website", html=True), name="website")

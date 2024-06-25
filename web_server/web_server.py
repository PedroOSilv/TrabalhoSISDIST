import grpc
import file_transfer_pb2
import file_transfer_pb2_grpc
from fastapi import FastAPI, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os

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

    response = stub.Upload(file_chunks())
    print(f"Upload response: {response.message}")


def list_files(folder):
    request = file_transfer_pb2.ListRequest(folder=folder)
    response = stub.ListFiles(request)
    return list(response.listOfFiles)


def download_file(filename):
    request = file_transfer_pb2.FileRequest(filename=filename)
    response = stub.Download(request)
    for file_chunk in response:
        file_path = os.path.join("downloads", file_chunk.filename)
        with open(file_path, "ab") as f:
            f.write(file_chunk.content)
    print(f"{filename} file downloaded successfully to downloads")


def delete_file(filename):
    request = file_transfer_pb2.FileRequest(filename=filename)
    response = stub.Delete(request)
    print(f"Delete response: {response.success}")


class FileRequest(BaseModel):
    filename: str


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


@app.post("/download")
async def download_api(fileRequest: FileRequest):
    print(f"Downloading file: {fileRequest.filename}")
    download_file(fileRequest.filename)
    return FileResponse(f"downloads/{fileRequest.filename}")


@app.post("/delete")
async def delete_file_api(fileRequest: FileRequest):
    delete_file(fileRequest.filename)
    return "Success"


app.mount("/", StaticFiles(directory="../website", html=True), name="website")

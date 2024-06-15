import grpc
import filetransfer_pb2
import filetransfer_pb2_grpc

def upload_file(stub, file_path):
    def file_chunks(file_path):
        with open(file_path, 'rb') as f:
            while True:
                chunk = f.read(1024)
                if not chunk:
                    break
                yield filetransfer_pb2.FileChunk(content=chunk, filename=file_path)

    response = stub.UploadFile(file_chunks(file_path))
    print("Upload response:", response.message)

def download_file(stub, filename, download_path):
    file_request = filetransfer_pb2.FileRequest(filename=filename)
    response_iterator = stub.DownloadFile(file_request)
    with open(download_path, 'wb') as f:
        for chunk in response_iterator:
            f.write(chunk.content)
    print(f"Downloaded {filename} to {download_path}")

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = filetransfer_pb2_grpc.FileServiceStub(channel)
        # Upload a file
        upload_file(stub, 'path/to/your/upload_file')
        # Download a file
        download_file(stub, 'uploaded_file', 'path/to/your/download_file')

if __name__ == '__main__':
    run()

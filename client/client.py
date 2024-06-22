import grpc
import file_transfer_pb2
import file_transfer_pb2_grpc

def upload_file(stub, file_path, filename):
    def file_chunks():
        with open(file_path, 'rb') as f:
            while chunk := f.read(1024):
                yield file_transfer_pb2.FileChunk(content=chunk, filename=filename)

    response = stub.Upload(file_chunks())
    print(f"Upload response: {response.message}")

def download_file(stub, filename, download_path):
    request = file_transfer_pb2.FileRequest(filename=filename)
    response = stub.Download(request)
    with open(download_path, 'wb') as f:
        for chunk in response:
            f.write(chunk.content)
    print(f"File downloaded successfully to {download_path}")

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = file_transfer_pb2_grpc.FileTransferStub(channel)
        upload_file(stub, 'textoSample.txt', 'uploaded_file.txt')
        download_file(stub, 'uploaded_file.txt', 'downloaded_file.txt')

if __name__ == '__main__':
    run()

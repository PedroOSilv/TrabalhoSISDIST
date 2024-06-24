import grpc
import argparse
import file_transfer_pb2
import file_transfer_pb2_grpc

def upload_file(stub, file_path, filename):
    def file_chunks():
        with open(file_path, 'rb') as f:
            while chunk := f.read(1024):
                yield file_transfer_pb2.FileChunk(content=chunk, filename=filename)

    response = stub.Upload(file_chunks())
    print(f"Upload response: {response.message}")


def run(file_path, filename): 
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = file_transfer_pb2_grpc.FileTransferStub(channel)
        upload_file(stub, file_path, filename)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Client for uploading and downloading files via gRPC.')
    parser.add_argument('file_path', type=str, help='The path to the file to be uploaded.')
    parser.add_argument('filename', type=str, help='The name of the file to be uploaded.')

    args = parser.parse_args()
    run(args.file_path, args.filename)
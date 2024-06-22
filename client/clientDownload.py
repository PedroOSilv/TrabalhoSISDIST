import grpc
import argparse
import file_transfer_pb2
import file_transfer_pb2_grpc   


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
        download_file(stub, 'uploaded_file.txt', 'downloaded_file.txt')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Client for uploading and downloading files via gRPC.')
    parser.add_argument('file_path', type=str, help='The path to the file to be uploaded.')
    parser.add_argument('filename', type=str, help='The name of the file to be uploaded.')

    args = parser.parse_args()
    run(args.file_path, args.filename, args.servers)
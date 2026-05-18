import os
import json
import time
import shutil

# --- Local Storage (On-Premise Analogy) ---
# This class simulates storing data on a local server's file system.
# It requires managing directories and physical disk space.
class LocalStorage:
    def __init__(self, base_path="local_data"):
        self.base_path = base_path
        os.makedirs(self.base_path, exist_ok=True)
        print(f"LocalStorage initialized at: {os.path.abspath(self.base_path)}")

    def upload(self, filename, content):
        file_path = os.path.join(self.base_path, filename)
        with open(file_path, 'w') as f:
            f.write(content)
        print(f"  [Local] Uploaded '{filename}' to {file_path}")

    def download(self, filename):
        file_path = os.path.join(self.base_path, filename)
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                content = f.read()
            print(f"  [Local] Downloaded '{filename}'")
            return content
        print(f"  [Local] File '{filename}' not found.")
        return None

    def list_files(self):
        files = os.listdir(self.base_path)
        print(f"  [Local] Files: {files}")
        return files

# --- Cloud Storage Simulator (AWS S3 Analogy) ---
# This class simulates a cloud storage service like AWS S3.
# It abstracts away the underlying infrastructure, offering storage as a service.
class CloudStorageSimulator:
    _storage = {} # Simulates a global, remote storage service accessible by all instances

    def __init__(self, bucket_name="my-cloud-bucket"):
        self.bucket_name = bucket_name
        if bucket_name not in CloudStorageSimulator._storage:
            CloudStorageSimulator._storage[bucket_name] = {}
        print(f"CloudStorageSimulator (Bucket: '{self.bucket_name}') initialized.")
        # This simulates "renting" a storage service (a bucket) without managing underlying hardware.

    def upload(self, filename, content):
        # Simulate network latency for a remote service
        time.sleep(0.05)
        CloudStorageSimulator._storage[self.bucket_name][filename] = content
        print(f"  [Cloud] Uploaded '{filename}' to bucket '{self.bucket_name}'")

    def download(self, filename):
        # Simulate network latency
        time.sleep(0.05)
        if filename in CloudStorageSimulator._storage[self.bucket_name]:
            content = CloudStorageSimulator._storage[self.bucket_name][filename]
            print(f"  [Cloud] Downloaded '{filename}' from bucket '{self.bucket_name}'")
            return content
        print(f"  [Cloud] File '{filename}' not found in bucket '{self.bucket_name}'.")
        return None

    def list_files(self):
        # Simulate network latency
        time.sleep(0.02)
        files = list(CloudStorageSimulator._storage[self.bucket_name].keys())
        print(f"  [Cloud] Files in bucket '{self.bucket_name}': {files}")
        return files

# --- Main Demonstration ---
if __name__ == "__main__":
    print("--- Demonstrating Local Storage (On-Premise Analogy) ---")
    local_store = LocalStorage() # Requires managing local disk resources
    local_store.upload("report.txt", "This is a confidential report from local server.")
    local_store.upload("image.jpg", "Binary data for an image...") # Content is string for simplicity
    local_store.list_files()
    downloaded_local_report = local_store.download("report.txt")
    print(f"  Content of report.txt (local): {downloaded_local_report[:50]}...")
    print("\n" + "="*60 + "\n")

    print("--- Demonstrating Cloud Storage (AWS S3 Analogy) ---")
    # Here, we "rent" a storage service (a bucket) without managing servers or disks.
    cloud_store = CloudStorageSimulator("my-company-data")
    cloud_store.upload("presentation.pptx", "Content for a cloud presentation.")
    cloud_store.upload("user_logs.json", json.dumps({"user": "alice", "action": "login", "timestamp": time.time()}))
    cloud_store.list_files()
    downloaded_cloud_logs = cloud_store.download("user_logs.json")
    print(f"  Content of user_logs.json (cloud): {downloaded_cloud_logs[:50]}...")

    # Demonstrate another "instance" of cloud storage (another bucket) easily provisioned
    print("\n--- Demonstrating another Cloud Storage 'Bucket' ---")
    dev_cloud_store = CloudStorageSimulator("dev-environment-files")
    dev_cloud_store.upload("test_data.csv", "col1,col2\n1,a\n2,b")
    dev_cloud_store.list_files()
    cloud_store.list_files() # Original bucket is unaffected and separate

    print("\n--- Key Cloud Concepts Illustrated ---")
    print("1. Abstraction: We interact with 'upload/download' methods, not raw disk management.")
    print("2. On-Demand: 'CloudStorageSimulator()' instantly gives us a new storage unit (bucket) without hardware setup.")
    print("3. Scalability (Simulated): No need to worry about underlying disk space or hardware capacity.")
    print("4. Managed Service: We don't manage the 'server' where data lives; the provider does.")

    # Cleanup local_data directory created by LocalStorage
    if os.path.exists(local_store.base_path):
        print(f"\nCleaning up local data directory: {local_store.base_path}")
        shutil.rmtree(local_store.base_path)

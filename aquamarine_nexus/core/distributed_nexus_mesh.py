import socket
import json
import threading
import time
from typing import Dict, Any, List

class DistributedNexusMeshCore:
    BUFFER_SIZE = 65536
    DEFAULT_PORT = 9876

    @staticmethod
    def start_worker_node(host: str = "0.0.0.0", port: int = DEFAULT_PORT):
        """Runs a sovereign background worker server on a secondary mobile/PC."""
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((host, port))
        server.listen(5)
        print(f"[NEXUS MESH WORKER] Active on {host}:{port}. Waiting for cluster tasks...")

        while True:
            conn, addr = server.accept()
            try:
                raw_data = b""
                while True:
                    chunk = conn.recv(DistributedNexusMeshCore.BUFFER_SIZE)
                    if not chunk:
                        break
                    raw_data += chunk
                    if b"__END_TASK__" in raw_data:
                        break

                if not raw_data:
                    conn.close()
                    continue

                task_payload = json.loads(raw_data.replace(b"__END_TASK__", b"").decode('utf-8'))
                
                # Execute computation shard
                chunk_data = task_payload.get("data_slice", [])
                task_type = task_payload.get("task_type", "vector_norm_sum")

                if task_type == "vector_norm_sum":
                    # Sharded partial reduction: sum(x^2 for x in data)
                    partial_result = sum(x * x for x in chunk_data)
                else:
                    partial_result = sum(chunk_data)

                response = {
                    "worker_ip": addr[0],
                    "processed_elements": len(chunk_data),
                    "partial_result": partial_result,
                    "status": "TASK_SUCCESS"
                }

                conn.sendall(json.dumps(response).encode('utf-8'))
            except Exception as e:
                err_resp = {"error": str(e), "status": "TASK_FAILED"}
                conn.sendall(json.dumps(err_resp).encode('utf-8'))
            finally:
                conn.close()

    @staticmethod
    def dispatch_mesh_cluster_job(worker_ips: List[str], dataset: List[float], port: int = DEFAULT_PORT) -> Dict[str, Any]:
        """
        Shards dataset evenly across all reachable worker IPs,
        transmits via raw sockets, and aggregates the cluster reduction.
        """
        if not worker_ips:
            raise ValueError("Worker IPs list cannot be empty.")

        n_workers = len(worker_ips)
        chunk_size = len(dataset) // n_workers
        results = []
        threads = []

        def worker_client_thread(w_ip: str, data_shard: List[float], index: int):
            try:
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.settimeout(5.0)
                client.connect((w_ip, port))
                
                payload = json.dumps({
                    "task_id": f"shard_{index}",
                    "task_type": "vector_norm_sum",
                    "data_slice": data_shard
                }) + "__END_TASK__"
                
                client.sendall(payload.encode('utf-8'))
                
                resp_data = b""
                while True:
                    chunk = client.recv(DistributedNexusMeshCore.BUFFER_SIZE)
                    if not chunk:
                        break
                    resp_data += chunk

                res_json = json.loads(resp_data.decode('utf-8'))
                results.append(res_json)
                client.close()
            except Exception as e:
                results.append({"worker_ip": w_ip, "error": str(e), "status": "WORKER_TIMEOUT_OR_UNREACHABLE"})

        t0 = time.perf_counter()
        for idx, ip in enumerate(worker_ips):
            start_i = idx * chunk_size
            end_i = start_i + chunk_size if idx < n_workers - 1 else len(dataset)
            shard = dataset[start_i:end_i]

            t = threading.Thread(target=worker_client_thread, args=(ip, shard, idx))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        total_time = time.perf_counter() - t0

        # Master Reduction
        valid_shards = [r["partial_result"] for r in results if r.get("status") == "TASK_SUCCESS"]
        cluster_sum = sum(valid_shards)

        return {
            "cluster_master_nodes_queried": n_workers,
            "total_elements_distributed": len(dataset),
            "cluster_execution_time_sec": round(total_time, 4),
            "aggregated_cluster_sum": cluster_sum,
            "node_responses": results,
            "mesh_status": "CLUSTER_JOB_COMPLETE" if len(valid_shards) == n_workers else "PARTIAL_DEGRADED"
        }

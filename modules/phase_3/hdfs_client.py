"""
Orbitalytics Phase 3: Data Ingestion and HDFS Data Lake
HDFS Client Wrapper for Live Docker Hadoop Ecosystem
"""

import os
import subprocess
import tempfile
import hashlib
from pathlib import Path
from typing import List, Dict, Any, Optional

class HDFSClient:
    """Production-grade client interfacing with live Apache Hadoop HDFS in Docker."""

    def __init__(self, container_name: str = "hadoop-namenode"):
        self.container = container_name

    def _exec(self, cmd: str, timeout: int = 45) -> subprocess.CompletedProcess:
        """Executes a command inside the NameNode container."""
        full_cmd = ["docker", "exec", self.container, "bash", "-c", cmd]
        res = subprocess.run(full_cmd, capture_output=True, text=True, timeout=timeout)
        if res.returncode != 0:
            err_msg = res.stderr.strip() or res.stdout.strip()
            raise RuntimeError(f"HDFS command failed ({res.returncode}): {cmd}\nOutput: {err_msg}")
        return res

    def mkdir(self, hdfs_path: str) -> bool:
        """Creates HDFS directory hierarchy recursively."""
        self._exec(f"hdfs dfs -mkdir -p {hdfs_path}")
        return True

    def exists(self, hdfs_path: str) -> bool:
        """Checks if a path exists in HDFS."""
        try:
            full_cmd = ["docker", "exec", self.container, "hdfs", "dfs", "-test", "-e", hdfs_path]
            res = subprocess.run(full_cmd, capture_output=True, text=True, timeout=15)
            return res.returncode == 0
        except Exception:
            return False

    def put_file(self, local_path: str, hdfs_path: str, overwrite: bool = True) -> bool:
        """Uploads a local file to HDFS via Docker container staging."""
        local = Path(local_path)
        if not local.exists():
            raise FileNotFoundError(f"Local file does not exist: {local_path}")

        temp_name = f"/tmp/{local.name}_{os.getpid()}"
        
        # 1. Docker cp local -> container /tmp/
        cp_cmd = ["docker", "cp", str(local), f"{self.container}:{temp_name}"]
        cp_res = subprocess.run(cp_cmd, capture_output=True, text=True, timeout=30)
        if cp_res.returncode != 0:
            raise RuntimeError(f"Failed to copy file to container: {cp_res.stderr}")

        # 2. hdfs dfs -put -f /tmp/ -> hdfs_path
        flag = "-f" if overwrite else ""
        try:
            self._exec(f"hdfs dfs -put {flag} {temp_name} {hdfs_path}")
        finally:
            # 3. Clean up container /tmp/
            self._exec(f"rm -f {temp_name}")

        return True

    def put_bytes(self, data_bytes: bytes, remote_filename: str, hdfs_dir: str, overwrite: bool = True) -> str:
        """Uploads in-memory bytes directly to HDFS."""
        with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{remote_filename}") as tmp:
            tmp.write(data_bytes)
            tmp_path = tmp.name

        try:
            target_hdfs_path = f"{hdfs_dir.rstrip('/')}/{remote_filename}"
            self.put_file(tmp_path, target_hdfs_path, overwrite=overwrite)
            return target_hdfs_path
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

    def get_file(self, hdfs_path: str, local_path: str) -> bool:
        """Downloads a file from HDFS to local path."""
        target_dir = Path(local_path).parent
        target_dir.mkdir(parents=True, exist_ok=True)
        
        filename = Path(hdfs_path).name
        temp_name = f"/tmp/dl_{filename}_{os.getpid()}"

        try:
            self._exec(f"hdfs dfs -get -f {hdfs_path} {temp_name}")
            cp_cmd = ["docker", "cp", f"{self.container}:{temp_name}", str(local_path)]
            cp_res = subprocess.run(cp_cmd, capture_output=True, text=True, timeout=30)
            if cp_res.returncode != 0:
                raise RuntimeError(f"Failed to copy file from container: {cp_res.stderr}")
            return True
        finally:
            self._exec(f"rm -f {temp_name}")

    def ls(self, hdfs_path: str, recursive: bool = False) -> List[Dict[str, Any]]:
        """Lists files and directories in HDFS."""
        flag = "-R" if recursive else ""
        res = self._exec(f"hdfs dfs -ls {flag} {hdfs_path}")
        lines = [line.strip() for line in res.stdout.strip().split("\n") if line.strip() and not line.startswith("Found")]
        
        items = []
        for line in lines:
            parts = line.split(maxsplit=7)
            if len(parts) >= 8:
                items.append({
                    "permissions": parts[0],
                    "replication": int(parts[1]) if parts[1] != "-" else 0,
                    "owner": parts[2],
                    "group": parts[3],
                    "size": int(parts[4]),
                    "date": f"{parts[5]} {parts[6]}",
                    "path": parts[7],
                    "is_dir": parts[0].startswith("d")
                })
        return items

    def cat(self, hdfs_path: str, lines: Optional[int] = None) -> str:
        """Reads file contents from HDFS."""
        pipe = f"| head -n {lines}" if lines else ""
        res = self._exec(f"hdfs dfs -cat {hdfs_path} {pipe}")
        return res.stdout

    def du(self, hdfs_path: str) -> int:
        """Returns size in bytes of HDFS path."""
        res = self._exec(f"hdfs dfs -du -s {hdfs_path}")
        # Output format: <size> <replicated_size> <path>
        line = res.stdout.strip().split("\n")[0]
        size_bytes = int(line.split()[0])
        return size_bytes

    def mv(self, src_path: str, dst_path: str) -> bool:
        """Moves/renames a file in HDFS."""
        self._exec(f"hdfs dfs -mv {src_path} {dst_path}")
        return True

    def rm(self, hdfs_path: str, recursive: bool = False) -> bool:
        """Deletes file or directory from HDFS."""
        flag = "-r -skipTrash" if recursive else "-skipTrash"
        self._exec(f"hdfs dfs -rm {flag} {hdfs_path}")
        return True

    def checksum(self, hdfs_path: str) -> str:
        """Calculates MD5 hash of a file stored in HDFS by streaming it."""
        res = self._exec(f"hdfs dfs -cat {hdfs_path} | md5sum")
        md5 = res.stdout.strip().split()[0]
        return md5


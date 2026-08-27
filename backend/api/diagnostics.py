import subprocess
import socket
import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/diagnostics", tags=["Diagnostics"])

class DiagnosticRequest(BaseModel):
    target: str

class TerminalRequest(BaseModel):
    command: str
    run_as_root: bool = False

class ToolLaunchRequest(BaseModel):
    tool_name: str # "wireshark" or "burpsuite"

@router.post("/ping")
def run_ping(req: DiagnosticRequest):
    target = req.target.strip()
    # Simple shell injection sanitization
    if not target or any(char in target for char in [";", "&", "|", "`", "$"]):
        raise HTTPException(status_code=400, detail="Invalid target character sequence detected")
        
    try:
        # Run standard 3-count ping command
        res = subprocess.run(
            ["ping", "-c", "3", "-W", "2", target],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=10
        )
        return {
            "stdout": res.stdout,
            "stderr": res.stderr,
            "exit_code": res.returncode
        }
    except subprocess.TimeoutExpired:
        return {"stdout": "", "stderr": "Error: Command timed out", "exit_code": -1}
    except Exception as e:
        return {"stdout": "", "stderr": f"Error executing command: {e}", "exit_code": -1}

@router.post("/traceroute")
def run_traceroute(req: DiagnosticRequest):
    target = req.target.strip()
    if not target or any(char in target for char in [";", "&", "|", "`", "$"]):
        raise HTTPException(status_code=400, detail="Invalid target character sequence detected")
        
    try:
        # Check if traceroute is installed, fallback to ping-based lookup
        res = subprocess.run(
            ["traceroute", "-w", "2", "-m", "15", target],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=25
        )
        return {
            "stdout": res.stdout,
            "stderr": res.stderr,
            "exit_code": res.returncode
        }
    except subprocess.TimeoutExpired:
        return {"stdout": "", "stderr": "Error: Command timed out", "exit_code": -1}
    except Exception as e:
        return {"stdout": "", "stderr": f"Error executing command: {e}", "exit_code": -1}

@router.post("/dns")
def run_dns_lookup(req: DiagnosticRequest):
    target = req.target.strip()
    if not target or any(char in target for char in [";", "&", "|", "`", "$"]):
        raise HTTPException(status_code=400, detail="Invalid target character sequence")
        
    results = {}
    record_types = ["A", "AAAA", "MX", "TXT", "NS"]
    
    # Try resolving via host command (standard Kali command)
    try:
        output_lines = []
        for r_type in record_types:
            res = subprocess.run(
                ["host", "-t", r_type, target],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=5
            )
            if res.returncode == 0:
                output_lines.append(res.stdout.strip())
        
        return {
            "stdout": "\n".join(output_lines) if output_lines else "No records resolved.",
            "stderr": "",
            "exit_code": 0
        }
    except Exception as e:
        return {"stdout": "", "stderr": f"DNS Lookup failed: {e}", "exit_code": -1}

@router.post("/terminal")
def run_terminal_command(req: TerminalRequest):
    command = req.command.strip()
    if not command:
        raise HTTPException(status_code=400, detail="Command cannot be empty")
        
    # Command safety check (allow standard network/system diagnostics commands, reject destructive ones)
    blocked_keywords = ["rm ", "dd ", "mkfs", "reboot", "shutdown", "> /dev", "chmod -r", "chown -r"]
    if any(keyword in command for keyword in blocked_keywords):
        raise HTTPException(status_code=400, detail="Action prohibited: command contains destructive keyword pattern")
        
    try:
        # Prepend sudo if run_as_root is requested
        # -n flag to run non-interactively (fails if password is required and not cached)
        cmd_args = ["bash", "-c", command]
        if req.run_as_root:
            cmd_args = ["sudo", "-n", "bash", "-c", command]
            
        res = subprocess.run(
            cmd_args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=15
        )
        
        stdout_out = res.stdout
        stderr_out = res.stderr
        
        if req.run_as_root and "sudo: a password is required" in stderr_out:
            stderr_out += "\n[!] Sudo require contraseña. Ejecute 'sudo setcap' o configure sudo sin contraseña para comandos no interactivos."
            
        return {
            "stdout": stdout_out,
            "stderr": stderr_out,
            "exit_code": res.returncode
        }
    except subprocess.TimeoutExpired:
        return {"stdout": "", "stderr": "Error: Command execution timed out", "exit_code": -1}
    except Exception as e:
        return {"stdout": "", "stderr": f"Command execution failed: {e}", "exit_code": -1}

@router.post("/launch_tool")
def launch_gui_tool(req: ToolLaunchRequest):
    tool = req.tool_name.strip().lower()
    
    if tool not in ["wireshark", "burpsuite"]:
        raise HTTPException(status_code=400, detail="Invalid tool request. Only wireshark or burpsuite allowed.")
        
    try:
        # Run tool as a detached background GUI process
        # We redirect stdout/stderr to devnull so uvicorn doesn't wait
        devnull = open(os.devnull, 'wb')
        
        # Wireshark needs root to capture packets natively (often launched with gksudo or sudo)
        if tool == "wireshark":
            # Attempt to launch wireshark (users often configure wireshark group so no sudo is needed)
            subprocess.Popen(["wireshark"], stdout=devnull, stderr=devnull, start_new_session=True)
        else:
            # Launch burpsuite
            subprocess.Popen(["burpsuite"], stdout=devnull, stderr=devnull, start_new_session=True)
            
        return {"status": "success", "message": f"Successfully launched {tool} on desktop background."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to launch tool {tool}: {e}")

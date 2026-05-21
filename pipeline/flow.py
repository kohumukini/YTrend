import subprocesses
import sys

from pathlib import Path
from prefect import flow, task

def run_script(path): 
    base_path = Path(__file__).parent.parent
    script_path = base_path / path

    return subprocesses.run(
        [sys.executable, str(script_path)], 
        check = True, 
        cwd = str(base_path)
    )

@task
def pull_raw(): 
    run_script("pipeline/etl/")
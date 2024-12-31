import subprocess
from typing import Tuple
import logSetup

logger = logSetup.log("CommandsHandler", "log.txt")


class CommandsHandler:
    """
    A Class to handle command execution...
    """
    
    @staticmethod
    def execute_command(command: str) -> Tuple[int, str, str]:
        """
        Executes a shell command and returns the output.

        Args:
            command (str): The shell command to execute.

        Returns:
            Tuple[int, str, str]: A tuple containing the return code, standard output, and standard error.
        """
        try:
            result = subprocess.run(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
            return result.returncode, result.stdout, result.stderr
        except subprocess.CalledProcessError as e:
            logger.error(f"Command failed: {e.cmd}, Return code: {e.returncode}")
            return e.returncode, e.output, e.stderr

    @staticmethod
    def check_command_success(return_code: int) -> bool:
        """
            checks if the command was successful based on return code

            Returns:
                bool : True if command was successful, False otherwise
        """

        if return_code == 0 :
            return True
        else:
            logger.warning(f"Command failed with return code: {return_code}")
            return False
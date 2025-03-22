from cat.mad_hatter.decorators import hook
import subprocess

@hook(priority=50)  # High priority to intercept before other hooks
def cat_recall_query(message, cat):
    # Check if the message starts with ":install:"
    if message.startswith(":install:"):
        package = message.split(":install:")[1].strip()
        
        try:
            # Run apt-get update without sudo
            update_result = subprocess.run(
                ['apt-get', 'update'],
                capture_output=True,
                text=True,
                check=True
            )
            
            # Install the package without sudo
            install_result = subprocess.run(
                ['apt-get', 'install', '-y', package],
                capture_output=True,
                text=True,
                check=True
            )
            
            # Build the response message
            response = (
                f"✅ Package '{package}' successfully installed.\n"
                f"--- Output of apt-get update ---\n{update_result.stdout}\n"
                f"--- Output of apt-get install ---\n{install_result.stdout}"
            )
        except subprocess.CalledProcessError as e:
            # Handle any errors that occur during installation
            response = (
                f"❌ Error while installing '{package}':\n"
                f"{e.stderr}"
            )
        
        # Send the response message to the user
        cat.send_chat_message(response)

        # Return the original message (unchanged)
        return response
    
    # If the message is not an installation command, return it unchanged
    return message

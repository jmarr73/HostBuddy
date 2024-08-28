# HostBuddy

HostBuddy is a user-friendly tool for managing your `/etc/hosts` file with a simple graphical user interface (GUI). It allows you to add, update, remove host entries, create backups, and preview the current state of your hosts file, all within a streamlined interface.

## Features

- **Add/Update Host Entries**: Easily add new entries or update existing ones in your `/etc/hosts` file.
- **Remove Host Entries**: Remove unwanted entries with a single click.
- **Backup Creation**: Automatically create backups of your `/etc/hosts` file before making any changes.
- **Preview Hosts File**: View the current contents of your hosts file in a scrollable popup window.
- **Clear Input Fields**: Quickly clear the IP and hostname fields with a dedicated button.
- **File Selection**: Choose a different hosts file to manage, if needed.

## Requirements

- Python 3.x
- Tkinter (included with Python on most systems)

## Installation

1. Clone the repository to your local machine:

    ```bash
    git clone https://github.com/jmarr73/HostBuddy.git
    ```

2. Navigate to the project directory:

    ```bash
    cd HostBuddy
    ```

3. (Optional) Make the file executable:

   ```bash
   chmod +x ./HostBuddy
   ```

4. Run the application:
   1. If you made the file executable:

    ```bash
    sudo ./hostbuddy.py
    ```

   2. If you did not make it executable:

   ```bash
   sudo python3 hostbuddy.py
   ```

## Usage

1. Enter the IP address and hostname you want to manage.
2. Click "Add/Update Entry" to add or update an entry in the hosts file.
3. Use the "Remove Entry" button to delete an entry from the hosts file.
4. Click "Preview Hosts File" to view the current contents of the hosts file in a popup window.
5. Use the "Restore from Backup" button to revert to the last saved backup.
6. The "Clear" button clears the input fields for new entries.

## Contribution

Contributions are welcome! Please fork this repository, make your changes, and submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- The inspiration for this project came from the need to efficiently manage hosts file entries during my OffSec, TryHackMe, and HackTheBox training sessions.

import sqlite3

connection = sqlite3.connect(':memory:')
cursor = connection.cursor()


def create_database(database_name):
    # Connect to the SQLite database
    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()

    # Create a table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            pages INTEGER NOT NULL,
            coverType TEXT NOT NULL,
            category TEXT NOT NULL
        )
    ''')
    connection.commit()

    return connection, cursor


def execute_sql_command(cursor, command):
    try:
        cursor.execute(command)
        return cursor.fetchall()
    except sqlite3.Error as e:
        return f"Error executing command: {e}"


def main():
    # my database name
    database_name = 'Library.db'
    connection, cursor = create_database(database_name)
    command_counter = 0

    try:
        while True:
            # Take user input from the console
            command = input("Enter a SQL command (or 'exit' to quit): ")
            # Exit the loop if the user enters 'exit
            if command.lower() == 'exit':
                break
            try:
                cursor.execute(command)
                connection.commit()
                # Execute the command
                result = execute_sql_command(cursor, command)
                # Print the result and write to a file
                if isinstance(result, list):
                    with open('output.txt', 'a') as file1:
                        file1.write(command + '\n')
                    # Write each row to a file
                    for row in result:
                        print(row)
                        with open('output.txt', 'a') as file1:
                            file1.write(str(row) + '\n')
                print("Command executed successfully.")
            except sqlite3.Error as e:
                print("Error executing query: ", e)
            # Write the SELECT statement to a file
            with open("Command_history.txt", "a") as file:
                file.write(str(command_counter) + " command" + "\n")
                file.write(command + '\n')
                command_counter += 1

    finally:

        print("done")


if __name__ == "__main__":
    main()

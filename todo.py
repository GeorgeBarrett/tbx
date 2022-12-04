import argparse
import settings

# I imported this module for enhancement 1
from datetime import datetime   


class Handler:
    def __init__(self):
        self.todo_file = settings.TODO_FILE
        self.done_file = settings.DONE_FILE

    def handle(self):
        """Interpret the first command line argument, and redirect."""
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "action",
            choices=["add", "list", "delete", "do", "done"],
            help="The action to take",
        )
        parser.add_argument("other", nargs="?")
        args = parser.parse_args()

        action = getattr(self, args.action)
        action()
    
    def list(self):
        """Show all items in the todo file."""
        parser = argparse.ArgumentParser()
        parser.add_argument("action", choices=["list"])
        # attempting enhancement 5
        parser.add_argument("filter", type=str)
        args = parser.parse_args()

        with open(self.todo_file) as f:
            items = f.readlines()
            
        # enhancement 2
        # this line ensures the todo list starts at 1 not 0
        for i, line in enumerate(items, start=1):
            # enhancement 3
            # 6d fixes the indentation problem
            print(f"{i:6d} {line.strip()}")
        print(f"---\n{len(items)} item(s)")

    def done(self):
        """Show all items in the done file."""
        with open(self.done_file) as f:
            items = f.readlines()
        # this line ensures the done list starts at 1 not 0
        for i, line in enumerate(items, start=1):
            # enhancement 3
            # 6d fixes the indentation problem
            print(f"{i:6d} {line.strip()}")
        print(f"---\n{len(items)} item(s) done")

    def add(self):
        """Add a new item to the todo file."""
        parser = argparse.ArgumentParser()
        parser.add_argument("action", choices=["add"])
        parser.add_argument("item", type=str)
        args = parser.parse_args()

        with open(self.todo_file, "a") as f:
            # bug 1
            # this line ensures that an inputted new line character will be replaced by a space  
            f.write(args.item.replace("\n", " ") + "\n")

    # enhancement 4
    def delete(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("action", choices=["delete"])
        parser.add_argument("line_number", type=int)
        args = parser.parse_args()

        # Read in all the todo items
        with open(self.todo_file, "r") as f:
            items = f.readlines()
        
        # this variable means the user can start deleting items starting from 1 not 0
        list_index = args.line_number - 1

        # bug 2
        # make sure todo number is valid
        if len(items) > list_index:
            
            # Write out all but the done items
            with open(self.todo_file, "w") as f:
                new_todos = "".join(
                    items[: list_index] + items[list_index + 1 :] 
                )
                f.write(new_todos)
            print(f"Deleted: {items[list_index].strip()}")
        
        else:
            # This line ensures that the print message matches the print message suggested by Torchbox
            print(f"There is no item {args.line_number}. Please choose a number from 1 to {len(items)}")


    def do(self):
        """Move an item from the todo file to the done file."""
        parser = argparse.ArgumentParser()
        parser.add_argument("action", choices=["do"])
        parser.add_argument("line_number", type=int)
        args = parser.parse_args()

        # Read in all the todo items
        with open(self.todo_file, "r") as f:
            items = f.readlines()
        
        # enhancement 2
        # get the list index from the user's input (offset by 1)
        list_index = args.line_number - 1

        # bug 2
        # make sure todo number is valid
        if len(items) > list_index:
            # Append the done item to the done file
            with open(self.done_file, "a") as f:
                # enhancement 1
                # adding a date to when items get moved into the done.txt
                f.write(f"{items[list_index][:-1]} ({datetime.today().strftime('%Y-%m-%d')})\n")
                # other options
                # f.write(f"{items[list_index].replace("\n", "")} ({datetime.today().strftime('%Y-%m-%d')})\n")
                # f.write(items[list_index].replace("\n", "") + ' (' + datetime.today().strftime('%Y-%m-%d') + ')\n')
                # or "".join like they did below


            # Write out all but the done items
            with open(self.todo_file, "w") as f:
                new_todos = "".join(
                    items[: list_index] + items[list_index + 1 :] 
                )
                f.write(new_todos)
            print(f"Done: {items[args.line_number].strip()}")
        
        else:
            # This line ensures that the print message matches the print message suggested by Torchbox
            print(f"There is no item {args.line_number}. Please choose a number from 1 to {len(items)}")

if __name__ == "__main__":
    handler = Handler()
    handler.handle()
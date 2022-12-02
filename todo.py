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
        with open(self.todo_file) as f:
            items = f.readlines()
        for i, line in enumerate(items):
            print(f"{i} {line.strip()}")
        print(f"---\n{len(items)} item(s)")

    def done(self):
        """Show all items in the done file."""
        with open(self.done_file) as f:
            items = f.readlines()
        for i, line in enumerate(items):
            print(f"{i} {line.strip()}")
        print(f"---\n{len(items)} item(s) done")

    def add(self):
        """Add a new item to the todo file."""
        parser = argparse.ArgumentParser()
        parser.add_argument("action", choices=["add"])
        parser.add_argument("item", type=str)
        args = parser.parse_args()

        with open(self.todo_file, "a") as f:
            # bug 1
            # If the input has any new line characters then they will be replaced by a space  
            f.write(args.item.replace("\n", " ") + "\n")

        
    
    # enhancement 4
    # def delete(self):
    #     parser = argparse.ArgumentParser()
    #     parser.add_argument("action", choices=["delete"])
    #     parser.add_argument("item", type=str)
    #     args = parser.parse_args()

    def do(self):
        """Move an item from the todo file to the done file."""
        parser = argparse.ArgumentParser()
        parser.add_argument("action", choices=["do"])
        parser.add_argument("line_number", type=int)
        args = parser.parse_args()

        # Read in all the todo items
        with open(self.todo_file, "r") as f:
            items = f.readlines()
        print(items[args.line_number])
        # bug 2
        # make sure todo number is valid
        if len(items) > args.line_number:
            # Append the done item to the done file
            with open(self.done_file, "a") as f:
                # enhancement 1
                # adding a date to when items get moved into the done.txt
                f.write(items[args.line_number].replace("\n", "") + ' (' + datetime.today().strftime('%Y-%m-%d') + ')\n')
                # could do f-string:
                # f.write(f"{items[args.line_number].replace("\n", "")} ({datetime.today().strftime('%Y-%m-%d')})\n")
                # or
                # f.write(f"{items[args.line_number][:-1]} ({datetime.today().strftime('%Y-%m-%d')})\n")
                # or "".join like they did below


            # Write out all but the done items
            with open(self.todo_file, "w") as f:
                new_todos = "".join(
                    items[: args.line_number] + items[args.line_number + 1 :] 
                )
                f.write(new_todos)
            print(f"Done: {items[args.line_number].strip()}")
        
        else:
            print("There is no item 6. Please choose a number from 0 to 3")


if __name__ == "__main__":
    handler = Handler()
    handler.handle()
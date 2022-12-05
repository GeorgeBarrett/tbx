import argparse
import settings
import itertools

# I imported this module for enhancement 1
from datetime import datetime   

def get_today_time():
    return datetime.today().strftime('%Y-%m-%d')


class GetMaxLineNo:
    """ store whole file in memory"""
    def __init__(self, filename):
        self.filename = filename

    def get(self):
        with open(self.filename) as f:
            items = f.readlines()
        return len(items)

class BetterGetMaxLineNumber:
    """ read line by line as we do not need to store it in memmory"""
    def __init__(self, filename):
        self.filename = filename

    def get(self):
        with open(self.filename) as f:
            for counter in itertools.count():
                line = f.readline()
                if not line:
                    break
        return counter


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
        parser.add_argument("filter", type=str, nargs="*")
        args = parser.parse_args()
        # print(f"xxxxxxxxxxxx/def add {args.filter}")

        max_line_getter = BetterGetMaxLineNumber(self.todo_file)
        max_line_no = max_line_getter.get()

        num_of_digits = len(str(max_line_no))

        with open(self.todo_file) as f:
            items = f.readlines()
        
        printed_items = 0
        # enhancement 2
        # this line ensures the todo list starts at 1 not 0
        for i, line in enumerate(items, start=1):

            if line.strip() == args.filter[0]:
               printed_items += 1
               # enhancement 3
               print(f"{i:>{num_of_digits}} {line.strip()}")
        print(f"---\n{printed_items} item(s)")

    def done(self):
        """Show all items in the done file."""
        max_line_getter = BetterGetMaxLineNumber(self.done_file)
        max_line_no = max_line_getter.get()
        
        with open(self.done_file) as f:
            items = f.readlines()

        num_of_digits = len(str(max_line_no))
        
            # this line ensures the done list starts at 1 not 0
        for i, line in enumerate(items, start=1):
            # enhancement 3
            # 6d fixes the indentation problem
            print(f"{i:>{num_of_digits}} {line.strip()}")
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
        if not len(items) > list_index:
            # This line ensures that the print message matches the print message suggested by Torchbox
            print(f"There is no item {args.line_number}. Please choose a number from 1 to {len(items)}")
            return
            
        # Write out all but the done items
        with open(self.todo_file, "w") as f:
            new_todos = "".join(
                items[: list_index] + items[list_index + 1 :] 
            )
            f.write(new_todos)

        print(f"Deleted: {items[list_index].strip()}")


    def do(self):
        """Move an item from the todo file to the done file."""
        parser = argparse.ArgumentParser()
        parser.add_argument("action", choices=["do"])
        parser.add_argument("line_number", type=int)
        args = parser.parse_args()
        
        # enhancement 2
        # get the list index from the user's input (offset by 1)
        list_index = args.line_number - 1

        if list_index < 0:
            print('Must start from 1')

        # Read in all the todo items
        with open(self.todo_file, "r") as f:
            items = f.readlines()
        
        if not len(items) > list_index:
            # This line ensures that the print message matches the print message suggested by Torchbox
            print(f"There is no item {args.line_number}. Please choose a number from 1 to {len(items)}")
            return

        to_remove =  items[list_index]
        # bug 2
        # make sure todo number is valid
        # Append the done item to the done file
        with open(self.done_file, "a") as f:
            # enhancement 1
            # adding a date to when items get moved into the done.txt
            today_time = get_today_time()
            f.write(f"{items[list_index].strip()} ({today_time})\n")

        del items[list_index]

        # Write out all but the done items
        with open(self.todo_file, "w") as f:
            f.write(''.join(items))

        print(f"Done: {to_remove.strip()}")
        

if __name__ == "__main__":
    handler = Handler()
    handler.handle()

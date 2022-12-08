import argparse
import settings
import itertools    

# I imported this module for enhancement 1
from datetime import datetime   

def get_today_time():
    return datetime.today().strftime('%Y-%m-%d')


class GetMaxLineNumber:
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
            choices=["add", "list", "delete", "do", "done", "pri"],
            help="The action to take",
        )
        # by changing the ? to the * I can now take as many arguments as I like
        parser.add_argument("other", nargs="*")
        args = parser.parse_args()

        action = getattr(self, args.action)
        action()

    def list(self):
        """Show all items in the todo file."""
        parser = argparse.ArgumentParser()
        parser.add_argument("action", choices=["list"])
        parser.add_argument("filter", type=str, nargs="*")
        args = parser.parse_args()

        max_line_getter = GetMaxLineNumber(self.todo_file)
        max_line_num = max_line_getter.get()
        num_of_digits = len(str(max_line_num))
        printed_items = 0
        
        with open(self.todo_file) as f:
            items = f.readlines()

        # check if to-do list is empty
            if len(items) == 0:
                return
       
        # enhancement 2 in the '+1' inside the sorted
        # enhancement 6 in the multiple sorted statements
        sorted_items     = sorted((items, index+1) for index, items in enumerate(items))
        index_unranked   = next(index for index, item in enumerate(sorted_items) if item[0][0]  != '(')
        ranked_items     = sorted_items[0:index_unranked]
        unranked_items   = sorted(sorted_items[index_unranked::], key = lambda x: x[1])
        items            = ranked_items + unranked_items

       
        for item in items:
            if len(args.filter) == 0:
                    print(f"{item[1]:>{num_of_digits}} {item[0]}")
            else:
                    if args.filter[0] in item[0]:
                        printed_items += 1
                        # enhancement 3
                        print(f"{item[1]:>{num_of_digits}} {item[0]}")
        print(f"---\n{printed_items} item(s)")     
    
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

        to_remove = items[list_index]
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

    def pri(self):
        # own enhancemnt TODO
        # currently possible to have two items assigned to (A) 
        parser = argparse.ArgumentParser()
        parser.add_argument("action", choices=["pri"])
        parser.add_argument("inputs", type=str, nargs="*")
        args = parser.parse_args()

        # Extract the inputs
        list_inputs = args.inputs
        if not len(list_inputs) == 2:
            # Check there's exactly 2 inputs
            print(f"2 input arguments required: line number, priority. {len(list_inputs)} arguments were input.")
            return
        line_number = list_inputs[0]
        prio = list_inputs[1]

        # Check the line number is an integer
        try:
            line_number = int(line_number)
        except:
            print(f"First input must be an integer. {line_number} is not acceptable.")
            return

        list_index = line_number - 1

        if list_index < 0:
            print('Must start from 1')
            return

        # Read in all the todo items
        with open(self.todo_file, "r") as f:
            items = f.readlines()
        
        if not len(items) > list_index:
            print(f"There is no item {line_number}. Please choose a number from 1 to {len(items)}")
            return
        
        if not len(prio) == 1:
            # Check the prio is length 1
            print(f"Priority must be a single alphabetical character (from A, most important to Z, least important). {prio} is not acceptable.")
            return

        if not prio.isalpha():
            # Check the prio is an alphabetical character
            print(f"Priority must be a single alphabetical character (from A, most important to Z, least important). {prio} is not acceptable.")
            return

        # Set the prio to upper case
        prio = prio.upper()
        
        # Extract the relevant line
        line_before = items[list_index]

        # Check if there is already a prio assigned (think about edge cases for this... what if the item has parentheses?)
        if line_before[0]=="(" and line_before[2]==")":
            line_before = line_before[3:]

        # Format the item with the prio letter
        line_before = line_before.lstrip()
        line_after = "({}) {}".format(prio, line_before)
        items[list_index] = line_after
        
        # Write out
        with open(self.todo_file, "w") as f:
            out = "".join(items)
            f.write(out)

    
if __name__ == "__main__":
    handler = Handler()
    handler.handle()

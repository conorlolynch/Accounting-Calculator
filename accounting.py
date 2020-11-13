
# create ledger "nl-name"                             -- Create a Ledger
# create account "acc-name" dr                        -- Create an account and decide which side increases the account
#
# add "nl-name" "acc-name"                            -- Add an account to a named ledger
#
# insert "acc-name" *side *name *amount               -- Insert an entry to an existing account
#
# set "acc-name" dr/cr                                -- Sets an account to be increased on debit or credit side
#
# balance ledger "nl-name"                            -- Balance all the accounts in the ledger called "nl-name"
# balance account "acc-name"                          -- Balance an account called "acc-name"
#
# show "ledger or account name"                       -- Display the ledger or specific account
# quit                                                -- Exit the calculator


ledger_list = dict()           # ledger_list = {ledger_name: [a1, a2, a3 ...], ...}
account_list = dict()          # account_list = {acc_name: [side, [dr_entries], [cr_entries]], ...}


def createFunction(args):

    # Check if second argument is "ledger" or "account"
    if (args[1] == 'ledger'):

        # Do a quick check so that not too many arguments for ledger were given
        if (len(args) <= 3):

            # Do a check to make sure a ledger of the same name doesnt exist
            if (args[2] not in ledger_list):
                ledger_list[args[2]] = []
                return True, ""
            else:
                return False, "Ledger with name {} already exists.".format(args[2])

        else:
            return False, "Too many arguments for create ledger given."


    elif (args[1] == 'account'):

        # Do a check to make sure not too many arguments were given for create account
        if (len(args) <= 4):

            # Do a check to make sure an account of the same name doest exist
            if (args[2] not in account_list):

                tmp = []
                if (len(args) < 4):
                    tmp = [None, [], []]
                else:
                    tmp = [args[3], [], []]

                account_list[args[2]] = tmp
                return True, ""

            else:
                return False, "Account with name {} already exists.".format(args[2])

        else:
            return False, "Too many arguments for create account given."

    else:
        return False, "Invalid syntax for create statement."



def addFunction(args):
    if (len(args) == 3):
        # Need to see if the ledger exists
        if (args[1] in ledger_list):

            # Need to see if the account exists
            if (args[2] in account_list):
                ledger_list[args[1]].append(args[2])
                return True, ""

            else:
                return False, "Account {} does not exist".format(args[2])

        else:
            return False, "Ledger {} does not exist".format(args[1])


    elif (len(args) < 3):
        return False, "Not enough parameters given."
    else:
        return False, "Too many parameters given."



def insertFunction(args):
    # args[1] = account name
    # args[2] = string "side"
    # args[3] = string "name"
    # args[4] = int    "amount"

    # Check number of arguments passed
    if (len(args) == 5):

        # Check to see if args[1] is an existing account
        if (args[1] in account_list):

            # Check to see if side paramter is valid
            if (args[2] == 'dr' or args[2] == 'cr'):

                # Last check is to see if args[4] is an int
                if (args[4].isnumeric()):

                    # Insert array of ["acc-name", amount]
                    tmp = [args[3], args[4]]

                    if (args[2] == 'dr'):
                        account_list[args[1]][1].append(tmp)
                    else:
                        account_list[args[1]][2].append(tmp)

                    #print(account_list[args[1]])

                    return True, ""
                else:
                    return False, "Amount parameter invalid as it is not a number."

            else:
                return False, "Invalid account column: {}. Must be either dr or cr.".format(args[2])

        else:
            return False, "Could not insert into account: {} as it does not exist.".format(args[1])


    elif (len(args) > 5):
        return False, "Too many arguments passed for inserting entry."
    else:
        return False, "Too few arguments passed for inserting entry."



def balanceFunction(args):
    return False, "Not implemented"


def help():
    print("""
     create ledger "nl-name"                             -- Create a Ledger
     create account "acc-name" dr                        -- Create an account and decide which side increases the account

     add "nl-name" "acc-name"                            -- Add an account to a named ledger

     insert "acc-name" *side *name *amount               -- Insert an entry to an existing account

     set "acc-name" dr/cr                                -- Sets an account to be increased on debit or credit side

     balance ledger "nl-name"                            -- Balance all the accounts in the ledger called "nl-name"
     balance account "acc-name"                          -- Balance an account called "acc-name"

     show "ledger or account name"                       -- Display the ledger or specific account
     quit                                                -- Exit the calculator
    """)


def autoexec():
    commands = [
    "create account cash dr",
    "insert cash dr sales 500"
    ]

    return commands


def main():
    running = True
    run_autoexec = False
    commands = autoexec()

    while running:
        bool_successful = True
        error = None

        if (run_autoexec):
            # Check to see if commands isnt null
            if (len(commands) > 0):
                com = commands.pop(0)
                print("> "+str(com))
                input_args = com.split()
            else:
                run_autoexec = False

        if (not run_autoexec):
            input_args = input("> ").split()

        if (len(input_args) > 0):

            if (input_args[0] == 'create'):
                bool_successful, error = createFunction(input_args)

            elif (input_args[0] == 'add'):
                bool_successful, error = addFunction(input_args)

            elif (input_args[0] == 'insert'):
                bool_successful, error = insertFunction(input_args)

            elif (input_args[0] == 'balance'):
                bool_successful, error = balanceFunction(input_args)

            elif (input_args[0] == 'quit'):
                running = False

            elif (input_args[0] == 'help'):
                help()

            elif (input_args[0] == 'autoexec'):
                run_autoexec = True

            else:
                print("Invalid Input.")


            if (not bool_successful):
                print(error)

main()

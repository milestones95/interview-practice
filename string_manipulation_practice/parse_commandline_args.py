"""
Practice Problem: Parse Command-Line-Style Arguments

You're given a single string representing arguments typed after a command, like:

python
args = "--name John --verbose --retries=3 --path=/usr/local/bin --tag=beta --tag=prod"

Rules:

Arguments start with --
Some are flags with no value: --verbose
Some use = to attach a value directly: --retries=3
Some take their value as the next space-separated token instead of using =: --name John
A key can appear more than once (see --tag twice) — last one wins
You don't know in advance which style (= vs next-token vs flag) a given argument will use — you have to figure it out per-token as you go
"""

# took 21 mins to finish
test_args = "--name John --verbose --retries=3 --path=/usr/local/bin --tag=beta --tag=prod"



def parse_command_args(args):

    result = args.split("--")

    print("result: ", result)

    arg_dict = {}

    for arg in result:
        arg = arg.strip()



        if "=" in arg:
            left, right = arg.split("=",1)

        elif " " in arg:
            left, right = arg.split(None,1)

        else:

            if not arg == '' :
                left = arg
                right = True

            else:
                continue

        print("left: ", left, " right: ", right)

        if left == '':
            continue
            
        arg_dict[left] = right


    print("dict: ", arg_dict)
        

parse_command_args(test_args)
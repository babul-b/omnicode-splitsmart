# Part 2 test script — used to prove your OpenCode setup works.
# Prompt OpenCode with:
#   "Fix the bug in this file and add a function that returns the
#    factorial of a number, then call it for 5."

def greet_user(name):
    # Intentional bug: missing the 'f' prefix, so {name} won't be substituted.
    print("Hello, {name}! Your AI coding stack is working.")


if __name__ == "__main__":
    greet_user("Developer")

import time


def delay_decorator(function):
    print("hey")

    def wrapper_fun():
        time.sleep(2)
        function()

    return wrapper_fun


@delay_decorator
def call_deco():
    print("hey man")


# deco = delay_decorator(call_deco)
# deco()


call_deco()

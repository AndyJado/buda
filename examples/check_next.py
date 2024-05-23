from ansa import guitk
import os

def main():
    os.system('clear')
    window = guitk.BCWindowCreate("Action", guitk.constants.BCOnExitDestroy)

    action = guitk.BCActionCreate(window, "Action", onAction, ['M'])

    action_salve = guitk.BCActionCreate(window,"duh",onAction,['a'])

    next_lhs = guitk.BCPushButtonCreate(window, "NEXT MASTER", None, None)

    next_rhs = guitk.BCPushButtonCreate(window, "NEXT SLAVE", None, None)


    # this line make button trigger action
    guitk.BCActionAddWidget(action, next_lhs)
    guitk.BCActionAddWidget(action_salve,next_rhs)

    guitk.BCShow(window)


def onAction(action, data):
    print(data) # this print ['M']
    return 0


if __name__ == "__main__":
    main()
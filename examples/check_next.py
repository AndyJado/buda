from ansa import guitk

def main():
    window = guitk.BCWindowCreate("Action", guitk.constants.BCOnExitDestroy)
    action = guitk.BCActionCreate(window, "Action", onAction, ['M'])
    pBtn = guitk.BCPushButtonCreate(window, "Trigger Action", None, None)

    # Widget under control of action
    guitk.BCActionSetCheckable(action, True)
    guitk.BCActionTrigger(action)
    guitk.BCActionSetChecked(action, False)

    if guitk.BCActionIsCheckable(action):
        print("Action is Checkable")

    # this line make button trigger action
    widget = guitk.BCActionAddWidget(action, pBtn)

    if widget:
        print("Widget was added successfully to action")
    else:
        print("Widget was not added successfully to action")

    guitk.BCShow(window)


def onAction(action, data):
    print("Action Happened")
    print(data) # this print ['M']
    state = "Off"
    if guitk.BCActionIsChecked(action):
        state = "On"
    print("Current state of Action is: " + state)
    return 0


if __name__ == "__main__":
    main()
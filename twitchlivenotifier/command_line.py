import twitchlivenotifier


def main():
    twitchlivenotifier.config()
    twitchlivenotifier.get_lock()
    twitchlivenotifier.main()

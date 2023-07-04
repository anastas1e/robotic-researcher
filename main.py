import random

from const import BASE_WIKI_URL, SCIENTISTS, TOPICS
from robotics import Robot

robot = Robot("Quandrinaut")


def main():
    robot.introduce()
    robot.open_browser(BASE_WIKI_URL)
    for person in SCIENTISTS:
        birth, death, person_age, brief_info = robot.generate_info(person)
        msg = f"Let's talk about {person}.\n"
        msg += f"This person was born on the {birth}.\n"
        if death:
            msg += f"The date of death is {death}.\n"
        msg += f"Age of the person: {person_age}.\n"
        msg += f"Please find a brief information about {person} below:\n"
        msg += brief_info + "\n"
        print(msg)
    robot.close_browser()


def extended_main():
    """
    This function represents a possible extension of robot functionality. The main idea is to scrap data not only
    about scientists but about others as well (e.g. Actors). The simplest way to represent this idea is to use
    random.choice()
    """
    topic = random.choice(list(TOPICS.keys()))
    robot.introduce(topic)
    robot.open_browser(BASE_WIKI_URL)
    for person in TOPICS[topic]:
        birth, death, person_age, brief_info = robot.generate_info(person)
        msg = f"Let's talk about {person}.\n"
        msg += f"This person was born on the {birth}.\n"
        if death:
            msg += f"The date of death is {death}.\n"
        msg += f"Age of the person: {person_age}.\n"
        msg += f"Please find a brief information about {person} below:\n"
        msg += brief_info
        print(msg)
    robot.close_browser()


if __name__ == "__main__":
    main()

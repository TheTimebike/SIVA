# SIVA

SIVA, or the Strategic Integration Via Activities service, is an application that integrates your Destiny 2 experience with Discords rich presence features. When running, your Discord server-mates will be able to see what activity you are in and how many people there are in your fireteam for any activity.

SIVA comes with a custom built GUI that makes it especially easy to use, and saves your options into a config file that loads up on the next reload, meaning you dont have to type in your information constantly.

The majority of SIVA's settings are server-side, and not included in the actual program itself. This makes it easy for me to expand the activities that SIVA can manage, in big content drops like Shadowkeep, without needing an update to the program. Infact, it wont even need to restart.

## How To Install?

[SIVA does not need to install itself, as it runs from a single-file application which can be downloaded here.](https://github.com/TheTimebike/SIVA/releases/)

## What Do I Need To Run It?

SIVA is built to be lightweight, and should be compatible with most Windows systems. Linux and MacOS versions are unavalible at this time.

[SIVA also requires an API token, which can be gotten by creating an application here.](https://www.bungie.net/en/Application)
Copy the API key into SIVA, include your platform and username, and SIVA should be ready to run.

If you are on PC using BattleNet, ensure to include your battle-tag. For example: TheTimebike#2349

## Interface

![Interface](https://raw.githubusercontent.com/TheTimebike/SIVA/master/images/interface.png)

As of SIVA version v0.2, you can enable a dark mode version.

![Dark Interface](https://raw.githubusercontent.com/TheTimebike/SIVA/master/images/interface_dark.png)

After entering all of the details, press the start button to launch the SIVA service.

## How Does It Work?

Periodically, SIVA checks the Bungie.net API for the activity that you are taking part in. SIVA then connects with your Discord account through its rich presence system and updates your Discord account with this new information.

SIVA also checks against its servers to collect information about activities, meaning I can update these remotely without even needing you to reboot the program.

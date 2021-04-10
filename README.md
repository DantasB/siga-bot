# Siga-Bot

![demonstration](https://cdn.discordapp.com/attachments/539836343094870016/830289568300662824/unknown.png)

## Tabela de conteúdos

<!--ts-->
   * [About](#about)
   * [Requirements](#requirements)
   * [How to use](#how-to-use)
      * [Bot creation](#bot-creation)
      * [Setting up Program](#program-setup)
      * [Commands](#commands)
   * [To get introduced](#to-get-introduced)
   * [Technologies](#technologies)
<!--te-->

## About

A simple Discord bot constructed using Python3 and some other libraries made by Bruno Dantas.

Siga Bot is an original Discord bot written in Python3, using the discord.py library. The objective is to access the UFRJ Siga and download some documents.

## Requirements

To run this repository by yourself you will need to install python3 in your machine and them install all the requirements inside the [requirements](requirements.txt) file

## How to use

### Bot Creation

Before configuring the bot, you will need to access the https://discordapp.com/developers/applications/ to create your own bot and get the credentials.

### Program Setup

```bash
# Clone this repository
$ git clone <https://github.com/DantasB/Siga-Bot>

# Access the project page on your terminal
$ cd Siga-Bot

# Install all the requirements
$ pip install -r requirements.txt

# Create a .env file
$ touch .env  

# Create the following parameters
 TOKEN #Your discord bot token
 PREFIX #Your bot prefix if you want any differente from "!"

# Execute the main program
$ python siga_bot.py

# Them it's just wait for the code run
```
![demonstration](https://cdn.discordapp.com/attachments/539836343094870016/830289349781618738/unknown.png)

### Commands

- !document <Login> <Password> <Type Of Document> => downloads the required document and sends it to your discord;


## To Get Introduced

Using a bot in discord is a good thing and will help you to manage or have fun in your server. According to this, there are some files that will help you to improve the bot or construct a bot from the drawing board:
1. https://discordapp.com/developers/docs/intro
2. https://discordpy.readthedocs.io/en/rewrite/
3. https://sourcecode.glitch.me/
4. https://leovoel.github.io/embed-visualizer/

## Technologies

* Python3
* beautifulsoup4
* aiohttp
* PyPDF2
* validate_docbr
* discord.py


If you still need help, fell free to contact me on discord: BDantas#3692
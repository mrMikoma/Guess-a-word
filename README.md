# Distributed Systems
Course project for LUT's Distributed Systems -course.

## Project Introduction
The idea of this project was to create a word-guessing CLI game, where players could try to explain and guess randomized Finnish words.

## Project Architecture

This system consists of two main components: server services and client applications.

Server side is divided into three main services: 

1. Master database 
2. Master node 
3. Worker node

## How to use?

1. **Setup Master Database:**
 
 Please refer to README in `./master/database/`

2. **Setup Master Node:**

 Please refer to README in `./master/`

3. **Setup Worker Node:**

 Please refer to README in `./worker/`

4. **Use Client:**

 Run the client using Python3:
 ```bash
 cd ./client
 python3 ./main.py
 ```

## References:

**Wordlist used in the game if from Kotus:**

 Nykysuomen sanalista. Kotimaisten kielten keskus. Päivitetty 20.4.2023 [viitattu 25.4.2024]. Saatavissa https://kaino.kotus.fi/lataa/nykysuomensanalista2022.csv
